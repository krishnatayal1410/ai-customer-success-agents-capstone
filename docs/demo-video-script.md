# Demo Video Script

## Opening

This is an AI Customer Success Manager built for the OpenAI Agents SDK capstone. The business problem is simple: SaaS teams have customer signals spread across product analytics, support, sentiment, commercial data, and account notes. By the time a human notices low adoption or unresolved incidents, the renewal may already be at risk.

The project coordinates six specialized agents. Customer Health diagnoses churn risk. Product Expert recommends feature adoption actions. Support Assistant summarizes ticket severity. Escalation Manager prepares leadership escalation. Success Planner creates the intervention. Analytics produces the final structured account report.

## Architecture

There are two SDK orchestration patterns. The manager pattern exposes each specialist as an agent tool and is used for the complete account review. A second triage agent demonstrates real SDK handoffs for focused questions. Both paths use the same local data tools and Gemini through the LiteLLM adapter.

The tool layer simulates CRM, product analytics, support, knowledge search, a scoring service, planning, calendar scheduling, and escalation. Scheduling and escalation are side effects, so they require explicit human approval before execution.

## Data and Scoring

The demonstration uses synthetic accounts. Acme Retail India has one hundred twenty licensed seats but only forty-three active seats. The last login was nineteen days ago. Feature adoption is thirty-eight percent, NPS is negative eighteen, seven tickets remain open, and two are high priority. Renewal is forty-two days away.

The health service produces a transparent score using login recency, feature adoption, seat utilization, sentiment, and support burden. This separation is important: the language model explains and plans from evidence, while deterministic code owns the score.

## Offline Run

The offline demo works without any provider key. It loads Acme, calculates the score, lists risk drivers and positive signals, creates an intervention plan, recommends product guidance, summarizes support risk, and drafts a customer follow-up.

For Acme, the score is in the high-risk range. Major drivers are login inactivity, low adoption, low seat utilization, negative NPS, high-priority support issues, and a renewal inside sixty days. The intervention recommends a re-engagement call, enablement for unused features, onboarding for inactive seats, escalation of the high-priority issue, and preparation of the renewal plan.

The final artifact is a Pydantic-validated AccountHealthReport. It contains an executive summary, the nested health assessment, the nested intervention plan, product guidance, support summary, and follow-up message.

## Live Agent Flow

When a Gemini key is configured, the same repository runs through the OpenAI Agents SDK. The manager calls specialist agents as tools and Analytics synthesizes the final output. The handoff demo routes a focused request to one specialist using SDK handoffs.

Conversation history persists in SQLite by session ID. If a tool requests scheduling or escalation, the SDK returns an interruption. The CLI displays the tool name and arguments. A human approves or rejects the call. The run then resumes from RunState with the same session, which preserves context and produces an auditable decision.

## Validation

The validation command constructs the full team without making an API call. It checks six specialists, eight tools, six handoffs, manager tool registration, sample data, knowledge entries, and score bounds. Unit tests verify that every score stays between zero and one hundred, that Acme is correctly classified as high or critical risk, and that the offline report includes a human-approved intervention.

## Closing

This capstone meets the requested problem analysis, multi-agent design, minimum agent and tool counts, handoffs, memory, structured outputs, human approval, error handling, logging, documentation, architecture diagram, presentation, and demo video requirements. The system is safe to share because it contains no production credentials or customer data, and it remains reproducible even when a live provider key is unavailable.
