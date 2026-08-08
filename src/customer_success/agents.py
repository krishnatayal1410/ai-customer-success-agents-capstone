from __future__ import annotations

import os
from dataclasses import dataclass

from agents import Agent, ModelSettings, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from .models import AccountHealthReport, HealthAssessment, InterventionPlan
from .tools import (
    calculate_account_health,
    create_success_plan,
    escalate_account,
    get_customer_profile,
    get_support_history,
    get_usage_metrics,
    schedule_follow_up,
    search_product_knowledge,
)


DEFAULT_MODEL = "gemini/gemini-3.6-flash"


@dataclass
class AgentTeam:
    manager: Agent
    triage: Agent
    specialists: dict[str, Agent]
    tools: list


def build_agent_team(api_key: str | None = None, model_name: str | None = None) -> AgentTeam:
    """Build the six-specialist customer-success team and two orchestration agents."""
    resolved_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not resolved_key:
        raise RuntimeError("Set GEMINI_API_KEY to run live mode. Offline demo mode needs no key.")
    if not resolved_key.startswith("AIza"):
        raise RuntimeError(
            "GEMINI_API_KEY must be a Google AI Studio API key (normally beginning with 'AIza'), "
            "not an OAuth access token."
        )
    resolved_model = model_name or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    model = LitellmModel(model=resolved_model, api_key=resolved_key)
    settings = ModelSettings(include_usage=True, temperature=0.2)
    set_tracing_disabled(disabled=True)

    health_agent = Agent(
        name="Customer Health Agent",
        handoff_description="Diagnoses account health and churn risk.",
        instructions="Use profile, usage, support, and health tools. Return evidence-based risk drivers and actions.",
        model=model,
        model_settings=settings,
        tools=[get_customer_profile, get_usage_metrics, get_support_history, calculate_account_health],
        output_type=HealthAssessment,
    )
    product_agent = Agent(
        name="Product Expert Agent",
        handoff_description="Answers product questions and recommends features.",
        instructions="Ground every recommendation in the local product knowledge tool.",
        model=model,
        model_settings=settings,
        tools=[search_product_knowledge, get_usage_metrics],
    )
    support_agent = Agent(
        name="Support Assistant Agent",
        handoff_description="Summarizes tickets and suggests support recovery actions.",
        instructions="Analyze support history, severity, and sentiment. Never claim a ticket was resolved unless the data says so.",
        model=model,
        model_settings=settings,
        tools=[get_support_history, get_customer_profile, search_product_knowledge],
    )
    escalation_agent = Agent(
        name="Escalation Manager Agent",
        handoff_description="Prepares and, after approval, executes account escalations.",
        instructions="Explain why escalation is needed. Use the escalation tool only for high or critical risk.",
        model=model,
        model_settings=settings,
        tools=[calculate_account_health, get_support_history, escalate_account],
    )
    planner_agent = Agent(
        name="Success Planner Agent",
        handoff_description="Creates interventions and schedules approved follow-ups.",
        instructions="Build a practical plan with owner and due date. Ask for approval before scheduling follow-ups.",
        model=model,
        model_settings=settings,
        tools=[create_success_plan, schedule_follow_up, search_product_knowledge],
        output_type=InterventionPlan,
    )
    analytics_agent = Agent(
        name="Analytics Agent",
        handoff_description="Synthesizes the final structured account health report.",
        instructions="Combine health, support, product, and plan evidence into one concise executive report.",
        model=model,
        model_settings=settings,
        tools=[
            get_customer_profile,
            calculate_account_health,
            get_usage_metrics,
            get_support_history,
            search_product_knowledge,
            create_success_plan,
        ],
        output_type=AccountHealthReport,
    )
    specialists = {
        "health": health_agent,
        "product": product_agent,
        "support": support_agent,
        "escalation": escalation_agent,
        "planner": planner_agent,
        "analytics": analytics_agent,
    }

    triage = Agent(
        name="Customer Success Triage",
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
Route focused requests to the correct specialist. Keep the account_id in the handoff context.
Use Customer Health for risk, Product Expert for product questions, Support Assistant for tickets,
Escalation Manager for severe risk, Success Planner for interventions, and Analytics for final reports.""",
        model=model,
        model_settings=settings,
        handoffs=list(specialists.values()),
    )

    manager = Agent(
        name="AI Customer Success Manager",
        instructions=(
            "You are the manager. For a complete account review, call the health, product, support, "
            "planner, and analytics specialists as tools. Call escalation only when evidence shows high "
            "or critical risk. Never execute scheduling or escalation without human approval. Produce the "
            "final answer as the requested structured AccountHealthReport."
        ),
        model=model,
        model_settings=settings,
        tools=[
            health_agent.as_tool(tool_name="analyze_customer_health", tool_description="Assess account health and churn risk."),
            product_agent.as_tool(tool_name="recommend_product_actions", tool_description="Recommend product enablement actions."),
            support_agent.as_tool(tool_name="summarize_support_risk", tool_description="Summarize support and sentiment risk."),
            escalation_agent.as_tool(tool_name="manage_escalation", tool_description="Prepare or execute an approved escalation."),
            planner_agent.as_tool(tool_name="build_success_plan", tool_description="Create an intervention and follow-up plan."),
            analytics_agent.as_tool(tool_name="generate_health_report", tool_description="Synthesize the final account report."),
        ],
        output_type=AccountHealthReport,
    )
    return AgentTeam(
        manager=manager,
        triage=triage,
        specialists=specialists,
        tools=[
            get_customer_profile,
            calculate_account_health,
            get_usage_metrics,
            get_support_history,
            search_product_knowledge,
            schedule_follow_up,
            escalate_account,
            create_success_plan,
        ],
    )
