#!/usr/bin/env python3
"""Verify experiment-contract is accepted as a typed task blocker."""
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"


def run(env, *args):
    result = subprocess.run(["python3", str(TASK), *args], env=env,
                            text=True, capture_output=True)
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    bin_dir = root / "bin"
    bin_dir.mkdir()
    chat = bin_dir / "chat"
    chat.write_text("#!/bin/sh\nexit 0\n")
    chat.chmod(0o755)
    handoff = bin_dir / "handoff"
    handoff.write_text("#!/bin/sh\nexit 0\n")
    handoff.chmod(0o755)
    env = os.environ | {
        "MESH_DIR": str(root / "mesh"),
        "MESH_TASK_DIR": str(root / "mesh" / "task-chains"),
        "MESH_TASK_CHAT_CMD": str(chat),
        "MESH_TASK_HANDOFF_CMD": str(handoff),
        "MESH_TASK_ACTOR": "haunt",
        "MESH_TASK_LIVE_OWNERS": "haunt",
    }
    plan = root / "plan.tsv"
    plan.write_text("haunt\tresolve\tresolve experiment contract\n")
    run(env, "create", "experiment-contract-test", str(plan))
    run(env, "take", "experiment-contract-test", "resolve")
    run(env, "block", "experiment-contract-test", "resolve", "experiment-contract",
        "claim exceeds measured scope", "event:claim-narrowed")
    data = json.loads(run(env, "replay", "--json"))
    row = data["experiment-contract-test"]["data"]["steps"][0]
    assert row["status"] == "blocked"
    assert row["blocker_type"] == "experiment-contract"
    assert row["retry"] == "event:claim-narrowed"
