from __future__ import annotations

from .models import CustomerAccount, HealthAssessment, InterventionPlan


def _clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def assess_health(account: CustomerAccount) -> HealthAssessment:
    activity = _clamp(100 - account.days_since_login * 4)
    adoption = account.feature_adoption * 100
    seat_utilization = _clamp(account.active_seats / account.licensed_seats * 100)
    sentiment = (account.nps + 100) / 2
    support = _clamp(100 - account.open_tickets * 5 - account.high_priority_tickets * 15)

    score = round(
        activity * 0.25
        + adoption * 0.25
        + seat_utilization * 0.20
        + sentiment * 0.15
        + support * 0.15
    )
    if score < 40:
        risk_level = "critical"
    elif score < 60:
        risk_level = "high"
    elif score < 75:
        risk_level = "medium"
    else:
        risk_level = "low"

    drivers: list[str] = []
    positives: list[str] = []
    actions: list[str] = []

    if account.days_since_login > 14:
        drivers.append(f"No login for {account.days_since_login} days")
        actions.append("Schedule a re-engagement call within three business days")
    else:
        positives.append("Recent product activity")
    if account.feature_adoption < 0.5:
        drivers.append(f"Feature adoption is {account.feature_adoption:.0%}")
        actions.append("Run a targeted enablement session for two unused core features")
    else:
        positives.append(f"Feature adoption is {account.feature_adoption:.0%}")
    if seat_utilization < 60:
        drivers.append(f"Only {seat_utilization:.0f}% of licensed seats are active")
        actions.append("Launch a team onboarding campaign for inactive seats")
    else:
        positives.append(f"Seat utilization is {seat_utilization:.0f}%")
    if account.high_priority_tickets:
        drivers.append(f"{account.high_priority_tickets} high-priority support ticket(s)")
        actions.append("Escalate the high-priority support issue with an executive owner")
    if account.nps >= 30:
        positives.append(f"Positive NPS signal ({account.nps})")
    elif account.nps < 0:
        drivers.append(f"Negative NPS signal ({account.nps})")
        actions.append("Request a root-cause interview and recovery plan")
    if account.renewal_days <= 60:
        actions.append(f"Prepare the renewal plan; renewal is in {account.renewal_days} days")
    if not actions:
        actions.append("Maintain monthly value reviews and identify an expansion use case")

    return HealthAssessment(
        account_id=account.account_id,
        company=account.company,
        health_score=score,
        risk_level=risk_level,
        risk_drivers=drivers,
        positive_signals=positives,
        recommended_actions=actions,
    )


def make_intervention(account: CustomerAccount, health: HealthAssessment) -> InterventionPlan:
    due = 2 if health.risk_level in {"critical", "high"} else 7
    objective = (
        "Prevent churn and restore measurable product value"
        if health.risk_level in {"critical", "high"}
        else "Increase adoption and protect the upcoming renewal"
    )
    return InterventionPlan(
        account_id=account.account_id,
        objective=objective,
        actions=health.recommended_actions[:4],
        owner=account.owner,
        due_in_days=due,
        requires_human_approval=True,
    )
