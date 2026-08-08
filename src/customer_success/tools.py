from __future__ import annotations

import json

from agents.decorators import tool

from .data_store import append_audit_event, get_account, load_product_knowledge
from .scoring import assess_health, make_intervention


@tool
def get_customer_profile(account_id: str) -> str:
    """Return the complete SaaS customer profile for an account ID."""
    return get_account(account_id).model_dump_json(indent=2)


@tool
def calculate_account_health(account_id: str) -> str:
    """Calculate a deterministic 0-100 account health score and risk drivers."""
    return assess_health(get_account(account_id)).model_dump_json(indent=2)


@tool
def get_usage_metrics(account_id: str) -> str:
    """Return login recency, seat utilization, adoption, ARR, and renewal metrics."""
    account = get_account(account_id)
    payload = {
        "account_id": account.account_id,
        "days_since_login": account.days_since_login,
        "seat_utilization": round(account.active_seats / account.licensed_seats, 3),
        "feature_adoption": account.feature_adoption,
        "renewal_days": account.renewal_days,
        "arr_usd": account.arr_usd,
    }
    return json.dumps(payload, indent=2)


@tool
def get_support_history(account_id: str) -> str:
    """Return the current support load and severity indicators."""
    account = get_account(account_id)
    return json.dumps(
        {
            "account_id": account.account_id,
            "open_tickets": account.open_tickets,
            "high_priority_tickets": account.high_priority_tickets,
            "nps": account.nps,
        },
        indent=2,
    )


@tool
def search_product_knowledge(query: str) -> str:
    """Search the local product knowledge base for enablement recommendations."""
    terms = {term.lower() for term in query.split() if len(term) > 2}
    ranked = []
    for item in load_product_knowledge():
        haystack = f"{item['title']} {item['summary']} {' '.join(item['tags'])}".lower()
        score = sum(term in haystack for term in terms)
        if score:
            ranked.append((score, item))
    matches = [item for _, item in sorted(ranked, key=lambda pair: pair[0], reverse=True)[:3]]
    return json.dumps(matches, indent=2)


@tool(needs_approval=True)
def schedule_follow_up(account_id: str, purpose: str, days_from_now: int) -> str:
    """Schedule a customer follow-up. This side effect always requires human approval."""
    account = get_account(account_id)
    event = append_audit_event(
        "follow_up_scheduled",
        {
            "account_id": account_id,
            "company": account.company,
            "purpose": purpose,
            "days_from_now": days_from_now,
            "owner": account.owner,
        },
    )
    return json.dumps(event, indent=2)


@tool(needs_approval=True)
def escalate_account(account_id: str, reason: str, severity: str) -> str:
    """Escalate an at-risk account to leadership. Human approval is mandatory."""
    event = append_audit_event(
        "account_escalated",
        {"account_id": account_id, "reason": reason, "severity": severity},
    )
    return json.dumps(event, indent=2)


@tool
def create_success_plan(account_id: str) -> str:
    """Create a structured intervention plan from account health signals."""
    account = get_account(account_id)
    health = assess_health(account)
    return make_intervention(account, health).model_dump_json(indent=2)
