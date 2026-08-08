# Validation Report

## Scope

Validation covers deterministic behavior, project structure, SDK object construction, deliverable presence, secret hygiene, and a live Gemini provider run.

## Automated Checks

- `pytest`: four tests covering score range, high-risk classification, the structured offline report, and rejection of OAuth tokens passed as Gemini API keys.
- `customer_success.validate`: six specialists, eight tools, six handoffs, six manager agent-tools, sample data, knowledge base, and score bounds.
- Offline demo: JSON and Markdown reports generated for `ACME-001`.
- Live provider demo: the decentralized OpenAI Agents SDK handoff completed with `gemini/gemini-3.6-flash` and returned a structured health report for `ACME-001` (health score 34, critical risk, six recommended actions).
- Presentation QA: all 12 slides rendered and the final PPTX passed the overflow test.
- Demo video QA: 5 minutes 16 seconds, 1280x720 H.264 video with AAC narration, inspected with `ffprobe`.
- Package QA: archive contents and SHA-256 checksums generated.

## Live Provider Notes

The successful live validation used `customer-success-agents --account ACME-001 --handoff-demo`. The Gemini key was stored outside the submission in macOS Keychain and was not present in the project or archive. The full manager path can exceed Gemini 3.6 Flash's five-request-per-minute free-tier limit; the handoff demo stays within that limit while exercising live SDK routing, tool use, and structured output.

On 8 August 2026, the saved Keychain item was rechecked and found to contain an OAuth-style `AQ...` token rather than a Google AI Studio API key. Live mode now rejects that credential immediately with a clear configuration error. Unit tests, architecture validation, and the offline SDK-compatible demonstration all pass; a new `AIza...` Gemini API key is required for another live provider call.
