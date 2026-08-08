# AI Customer Success Manager

OpenAI Agents SDK capstone for Summer School'26. The project monitors SaaS customer activity, calculates churn risk, recommends product and support interventions, gates side effects behind human approval, retains conversation memory, and returns a structured account health report.

## Submission Requirement Coverage

- 6 specialized agents: Customer Health, Product Expert, Support Assistant, Escalation Manager, Success Planner, and Analytics.
- 8 tools: customer profile, usage, support history, product knowledge, health scoring, success planning, follow-up scheduling, and escalation.
- Two orchestration patterns: manager-as-tools and decentralized SDK handoffs.
- `SQLiteSession` conversation memory and append-only audit logging.
- Pydantic structured outputs for health, intervention, and final reporting.
- Human approval gates on follow-up scheduling and account escalation.
- Gemini through the OpenAI Agents SDK LiteLLM adapter.
- Deterministic offline demo for evaluators without an API key.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m customer_success.offline_demo --account ACME-001 --output-dir .
python -m pytest
python -m customer_success.validate
```

## Live Gemini Run

1. Copy `.env.example` to `.env.local`.
2. Add a Gemini API key to `GEMINI_API_KEY`.
3. Run:

```bash
source .venv/bin/activate
customer-success-agents --account ACME-001
```

The default model is `gemini/gemini-3.6-flash`. Override it with `GEMINI_MODEL`. Side-effecting tool calls pause for explicit approval. Use `--handoff-demo` to run the decentralized handoff path. Use `--approve` only in a controlled demonstration.

## Project Layout

```text
src/customer_success/   Agents, tools, memory, scoring, CLI, offline demo
data/                   Sample customer accounts and product knowledge
tests/                  Deterministic unit tests
docs/                   Analysis, architecture, implementation, demo script
diagrams/               Editable Graphviz source plus PNG/SVG exports
presentation/           12-slide final deck
demo-video/             Demo MP4 and transcript
```

## Safety

No API key, customer secret, email address, or production credential is included. `.env.local`, SQLite memory, and runtime audit logs are ignored. The sample companies and metrics are synthetic.

## Documentation

- [Problem analysis](docs/problem-analysis.md)
- [Architecture and agent design](docs/architecture.md)
- [Implementation details](docs/implementation.md)
- [Validation report](docs/validation-report.md)
- [Submission checklist](SUBMISSION-CHECKLIST.md)

## GitHub Submission

Public repository: <https://github.com/krishnatayal1410/ai-customer-success-agents-capstone>

## Official References

- OpenAI Agents SDK: <https://openai.github.io/openai-agents-python/>
- Agents and structured outputs: <https://openai.github.io/openai-agents-python/agents/>
- Handoffs: <https://openai.github.io/openai-agents-python/handoffs/>
- Human-in-the-loop: <https://openai.github.io/openai-agents-python/human_in_the_loop/>
- Sessions: <https://openai.github.io/openai-agents-python/sessions/>
- Gemini models: <https://ai.google.dev/gemini-api/docs/models>
