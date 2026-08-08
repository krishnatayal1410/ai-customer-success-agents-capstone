from __future__ import annotations

import argparse
import json
from pathlib import Path

from .data_store import get_account, load_product_knowledge
from .models import AccountHealthReport
from .scoring import assess_health, make_intervention


def build_offline_report(account_id: str) -> AccountHealthReport:
    account = get_account(account_id)
    health = assess_health(account)
    intervention = make_intervention(account, health)
    knowledge = load_product_knowledge()
    guidance = [item["summary"] for item in knowledge[:2]]
    support_summary = (
        f"{account.open_tickets} open ticket(s), including {account.high_priority_tickets} high-priority; "
        f"NPS is {account.nps}."
    )
    return AccountHealthReport(
        account_id=account.account_id,
        executive_summary=(
            f"{account.company} has a health score of {health.health_score}/100 and {health.risk_level} churn risk. "
            f"The next decision is to approve a {intervention.due_in_days}-day intervention led by {account.owner}."
        ),
        health=health,
        intervention=intervention,
        product_guidance=guidance,
        support_summary=support_summary,
        follow_up_message=(
            f"Hi {account.company} team, we reviewed adoption and support signals and prepared a focused success plan. "
            "Could we meet this week to confirm priorities and owners?"
        ),
    )


def markdown_report(report: AccountHealthReport) -> str:
    health = report.health
    plan = report.intervention
    return f"""# Account Health Report: {health.company}

**Account:** {report.account_id}  
**Health score:** {health.health_score}/100  
**Risk:** {health.risk_level.upper()}

## Executive Summary

{report.executive_summary}

## Risk Drivers

{chr(10).join(f'- {item}' for item in health.risk_drivers) or '- No material risk drivers'}

## Positive Signals

{chr(10).join(f'- {item}' for item in health.positive_signals) or '- No strong positive signal yet'}

## Approved Intervention Draft

**Objective:** {plan.objective}  
**Owner:** {plan.owner}  
**Due:** {plan.due_in_days} day(s)  
**Human approval required:** {'Yes' if plan.requires_human_approval else 'No'}

{chr(10).join(f'- {item}' for item in plan.actions)}

## Customer Message Draft

{report.follow_up_message}
"""


def write_offline_report(account_id: str, output_dir: str | Path = ".") -> AccountHealthReport:
    """Build and save the deterministic report used by both CLI entry points."""
    report = build_offline_report(account_id)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "demo-output.json").write_text(report.model_dump_json(indent=2), encoding="utf-8")
    (destination / "demo-output.md").write_text(markdown_report(report), encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the deterministic capstone demo without an API key.")
    parser.add_argument("--account", default="ACME-001")
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args(argv)
    report = write_offline_report(args.account, args.output_dir)
    print(report.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
