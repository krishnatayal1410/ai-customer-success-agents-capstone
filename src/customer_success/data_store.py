from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .models import CustomerAccount


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
ACCOUNTS_PATH = DATA_DIR / "accounts.json"
KNOWLEDGE_PATH = DATA_DIR / "product-knowledge.json"
AUDIT_PATH = DATA_DIR / "audit-log.jsonl"


def load_accounts() -> list[CustomerAccount]:
    payload = json.loads(ACCOUNTS_PATH.read_text(encoding="utf-8"))
    return [CustomerAccount.model_validate(item) for item in payload]


def get_account(account_id: str) -> CustomerAccount:
    for account in load_accounts():
        if account.account_id == account_id:
            return account
    raise KeyError(f"Unknown account_id: {account_id}")


def load_product_knowledge() -> list[dict[str, Any]]:
    return json.loads(KNOWLEDGE_PATH.read_text(encoding="utf-8"))


def append_audit_event(event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event_type": event_type,
        "payload": payload,
    }
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record
