# Implementation

## Provider Layer

The project uses `openai-agents[litellm]` and `LitellmModel` so the OpenAI Agents SDK can orchestrate Gemini. The provider model is configurable with `GEMINI_MODEL`; the default is `gemini/gemini-3.6-flash`.

## Health Model

The deterministic score combines:

- 25% login recency
- 25% feature adoption
- 20% licensed-seat utilization
- 15% NPS sentiment
- 15% support burden

This model is intentionally transparent. The language model explains and plans from the score; it does not silently fabricate the score.

## Error Handling

- Unknown account IDs raise an explicit `KeyError`.
- Pydantic rejects invalid customer data and output shapes.
- The live CLI fails clearly when no provider key is present and automatically offers offline behavior.
- Approval rejection returns a model-visible explanation and continues safely.
- Runtime secrets and mutable state are excluded through `.gitignore`.

## Logging and Audit Trail

Approved schedule and escalation actions are written to `data/audit-log.jsonl` with UTC timestamps, event type, and structured payload. The file is ignored because it is runtime state.

## Session Persistence

Live runs use `customer-success-memory.sqlite`. The session ID is configurable through `CUSTOMER_SUCCESS_SESSION`, allowing repeated turns to remember prior account context.

## Offline Demonstration

`python -m customer_success.offline_demo` runs the same data and scoring layer without a network or API key. It creates both JSON and Markdown reports. This makes grading reproducible while the live Agents SDK path remains available when `GEMINI_API_KEY` is configured.

## Run Commands

```bash
python -m customer_success.offline_demo --account ACME-001 --output-dir .
python -m pytest
python -m customer_success.validate
customer-success-agents --account ACME-001
customer-success-agents --account ACME-001 --handoff-demo
```
