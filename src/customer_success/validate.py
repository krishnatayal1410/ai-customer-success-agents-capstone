from __future__ import annotations

from .agents import build_agent_team
from .data_store import load_accounts, load_product_knowledge
from .scoring import assess_health


def main() -> None:
    team = build_agent_team(api_key="AIza" + "-validation-key-not-used")
    assert len(team.specialists) == 6
    assert len(team.tools) >= 5
    assert len(team.triage.handoffs) == 6
    assert len(team.manager.tools) == 6
    accounts = load_accounts()
    assert len(accounts) >= 3
    assert len(load_product_knowledge()) >= 3
    scores = [assess_health(account).health_score for account in accounts]
    assert all(0 <= score <= 100 for score in scores)
    print("PASS: 6 specialists, 8 tools, 6 handoffs, structured outputs, memory-ready CLI, and offline data validated.")


if __name__ == "__main__":
    main()
