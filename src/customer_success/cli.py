from __future__ import annotations

import argparse
import asyncio
import os

from agents import Runner, SQLiteSession
from dotenv import load_dotenv

from .agents import build_agent_team
from .offline_demo import write_offline_report


async def run_live(account_id: str, handoff_demo: bool, auto_approve: bool) -> None:
    team = build_agent_team()
    agent = team.triage if handoff_demo else team.manager
    session_id = os.getenv("CUSTOMER_SUCCESS_SESSION", "summer-school-demo")
    session = SQLiteSession(session_id, "customer-success-memory.sqlite")
    prompt = (
        f"Create a complete customer success review for account {account_id}. Use every relevant specialist, "
        "explain churn risk, recommend product and support actions, create an intervention plan, and draft a follow-up."
    )
    result = await Runner.run(agent, prompt, session=session)
    while result.interruptions:
        state = result.to_state()
        for interruption in result.interruptions:
            if auto_approve:
                approved = True
            else:
                answer = input(
                    f"Approve {interruption.name or 'tool'} with {interruption.arguments}? [y/N]: "
                ).strip().lower()
                approved = answer in {"y", "yes"}
            if approved:
                state.approve(interruption)
            else:
                state.reject(interruption, rejection_message="A human reviewer rejected this side effect.")
        result = await Runner.run(agent, state, session=session)
    output = result.final_output
    print(output.model_dump_json(indent=2) if hasattr(output, "model_dump_json") else output)


def main() -> None:
    load_dotenv(".env.local")
    parser = argparse.ArgumentParser(description="AI Customer Success Manager")
    parser.add_argument("--account", default="ACME-001")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--handoff-demo", action="store_true")
    parser.add_argument("--approve", action="store_true", help="Auto-approve side effects for a controlled demo.")
    args = parser.parse_args()
    if args.offline or not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        report = write_offline_report(args.account)
        print(report.model_dump_json(indent=2))
        return
    try:
        asyncio.run(run_live(args.account, args.handoff_demo, args.approve))
    except RuntimeError as exc:
        parser.exit(2, f"Live run configuration error: {exc}\n")


if __name__ == "__main__":
    main()
