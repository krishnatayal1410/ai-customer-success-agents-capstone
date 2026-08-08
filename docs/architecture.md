# Multi-Agent Architecture

## Design Choice

The system implements both orchestration patterns described by the Agents SDK:

1. **Manager pattern:** the `AI Customer Success Manager` keeps control and invokes each specialist with `Agent.as_tool()`.
2. **Handoff pattern:** the `Customer Success Triage` agent transfers a focused request to one of six specialists using SDK handoffs.

The manager pattern is used for a complete account review because it must combine several specialist outputs. The handoff path is useful for a single question such as product guidance or a support escalation.

## Agent Roles

| Agent | Responsibility | Main tools |
|---|---|---|
| Customer Health | Calculate health and explain churn drivers | profile, usage, support, health score |
| Product Expert | Recommend adoption and enablement actions | product knowledge, usage |
| Support Assistant | Summarize support severity and sentiment | support history, profile, knowledge |
| Escalation Manager | Prepare severe-risk escalation | health, support, approved escalation |
| Success Planner | Create an intervention and follow-up | success plan, approved scheduling, knowledge |
| Analytics | Synthesize the schema-validated report | profile, health, usage, support, knowledge, plan |

## Agent Interaction Flow

1. A human supplies an `account_id` and review objective.
2. The manager delegates evidence collection and analysis to specialists.
3. Specialists use local tools rather than inventing customer facts.
4. Analytics assembles an `AccountHealthReport`.
5. If scheduling or escalation is requested, the SDK pauses with an interruption.
6. A human approves or rejects the exact tool call.
7. The run resumes and the result is stored in the same SQLite session.

## Tool Integration Overview

- `get_customer_profile`: local CRM profile API simulation.
- `get_usage_metrics`: product analytics API simulation.
- `get_support_history`: support desk API simulation.
- `search_product_knowledge`: local knowledge retrieval.
- `calculate_account_health`: deterministic risk service.
- `create_success_plan`: intervention planning service.
- `schedule_follow_up`: calendar side effect with mandatory approval.
- `escalate_account`: leadership notification side effect with mandatory approval.

## Memory and Context

`SQLiteSession` stores the conversation and generated run items by session ID. This gives multi-turn memory without manually replaying messages. The local append-only JSONL audit log records approved side effects. Secrets are never stored in agent context or sample data.

## Structured Outputs

Pydantic models provide explicit schemas:

- `HealthAssessment`
- `InterventionPlan`
- `AccountHealthReport`

The manager and Analytics agent request `AccountHealthReport`; Health and Success Planner request their own specialist schemas.

## Human Approval

`schedule_follow_up` and `escalate_account` are decorated with `needs_approval=True`. The CLI reads `result.interruptions`, converts the result to `RunState`, records the human choice, and resumes the original run with the same session.
