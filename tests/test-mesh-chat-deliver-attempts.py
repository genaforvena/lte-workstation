#!/usr/bin/env python3
"""Regression for per-message terminal evidence, including grouped failures."""
import importlib.machinery
import importlib.util
import json
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader("deliver", str(ROOT / "scripts/mesh-chat-deliver"))
spec = importlib.util.spec_from_loader("deliver", loader)
deliver = importlib.util.module_from_spec(spec)
loader.exec_module(deliver)

with tempfile.TemporaryDirectory() as td:
    base = Path(td)
    deliver.LEDGER = base / "ledger.json"
    deliver.DLOG = base / "delivery.log"
    deliver.MAX_ATTEMPTS = 3
    deliver.MAX_AGE = 10
    now = time.time()
    rows = []
    states = {}
    expected = {}
    for attempts in range(4):
        raw = f"2026-09-08T15:00:0{attempts}Z  sender@test  ::  [@witness] fact {attempts}"
        rec = {"id": deliver.message_id(raw), "when": "2026-09-08T15:00:00Z",
               "sender": "sender", "target": "witness", "body": f"fact {attempts}"}
        rows.append(rec)
        states[rec["id"]] = {"target": "witness", "sender": "sender",
                              "first_seen": "2026-09-08T15:00:00Z", "attempts": attempts,
                              "status": "awaiting-ack"}
        expected[rec["id"]] = attempts

    # The zero-attempt row is old enough to expire; the other rows exercise the
    # one-, two-, and three-attempt terminal arms in one grouped failure.
    deliver.LEDGER.write_text(json.dumps({"version": 1, "messages": states}))
    deliver.records = lambda: (rows, {})
    deliver.targets = lambda: ["witness"]
    deliver.mind_idle = lambda _target: False
    calls = []
    deliver.run = lambda args, **kwargs: calls.append(args) or type("R", (), {"returncode": 0})()
    deliver.one_pass(["witness"])

    message = calls[0][-1]
    assert "attempts:" in message and "reason:" in message, message
    for rec in rows:
        assert f"{rec['id']}={expected[rec['id']]}" in message, message
    assert f"{rows[0]['id']}=age-expiry" in message, message
    for rec in rows[1:3]:
        assert f"{rec['id']}=age-expiry" in message, message
    assert f"{rows[3]['id']}=attempt-limit" in message, message
    ledger = json.loads(deliver.LEDGER.read_text())["messages"]
    assert [ledger[r["id"]]["attempts"] for r in rows] == [0, 1, 2, 3]
    assert ledger[rows[0]["id"]]["terminal_reason"] == "age-expiry"
    print("test-mesh-chat-deliver-attempts: PASS (grouped 0/1/2/3 mapping; age expiry distinct)")
