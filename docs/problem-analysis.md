# Problem Analysis

## Business Context

Subscription software companies depend on renewal and expansion revenue. Customer-success teams must notice falling adoption, unresolved support issues, negative sentiment, inactive licensed seats, and approaching renewals early enough to intervene. Those signals usually live in separate tools, so account reviews become manual, inconsistent, and late.

## Stakeholders

- Customer-success managers need prioritized accounts and practical interventions.
- Account owners need an evidence-backed daily action list.
- Support leaders need visibility into high-severity issues affecting renewal risk.
- Product teams need recurring adoption and usability signals.
- Revenue leaders need reliable health and renewal forecasts.
- Customers need timely, relevant help without automated actions being taken behind their backs.

## Problem Statement

Build a multi-agent customer-success platform that monitors customer activity, predicts churn risk, recommends interventions, answers product questions, schedules approved follow-ups, escalates severe cases, and generates structured account health reports.

## Pain Points

- Health scoring is subjective and varies by account owner.
- Product usage, support load, sentiment, and commercial context are reviewed separately.
- High-risk accounts can remain hidden until the renewal window is too short.
- Generic outreach ignores the account's actual adoption blockers.
- Fully autonomous scheduling or escalation would create operational and reputational risk.

## Objectives

1. Calculate a transparent 0–100 health score from five signal groups.
2. Coordinate at least five specialized agents through manager tools and handoffs.
3. Provide at least five usable data/action tools.
4. Preserve conversation history with local SQLite memory.
5. Return schema-validated health, intervention, and executive report objects.
6. Require a human decision before scheduling or escalation side effects.
7. Produce a reproducible offline demo when a provider key is unavailable.

## Success Criteria

- Every sample account produces a score between 0 and 100.
- The high-risk sample exposes multiple concrete risk drivers.
- Side-effecting tools declare mandatory approval.
- The final output validates against `AccountHealthReport`.
- The repository runs without secrets in offline mode and passes its tests.
