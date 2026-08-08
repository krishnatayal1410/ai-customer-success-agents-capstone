import pytest

from customer_success.agents import build_agent_team
from customer_success.data_store import get_account, load_accounts
from customer_success.offline_demo import build_offline_report
from customer_success.scoring import assess_health


def test_scores_stay_in_range():
    for account in load_accounts():
        score = assess_health(account).health_score
        assert 0 <= score <= 100


def test_acme_is_high_or_critical_risk():
    health = assess_health(get_account("ACME-001"))
    assert health.risk_level in {"high", "critical"}
    assert health.risk_drivers


def test_offline_report_is_structured():
    report = build_offline_report("ACME-001")
    assert report.account_id == "ACME-001"
    assert report.intervention.requires_human_approval is True
    assert report.follow_up_message


def test_oauth_token_is_rejected_as_gemini_api_key():
    with pytest.raises(RuntimeError, match="Google AI Studio API key"):
        build_agent_team(api_key="AQ.oauth-token-placeholder")
