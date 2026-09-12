#!/usr/bin/env python3
"""Isolated end-to-end acceptance for a synthetic TG ask; never touches live intake."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="tg-intake-acceptance-") as td:
        root = Path(td)
        mesh = root / "mesh"
        chains = mesh / "task-chains"
        plan = root / "plan.tsv"
        board = root / "board.log"
        event_writer = root / "mesh-chat-event"
        chain = "synthetic-tg-acceptance"
        step = "accept"
        ask = "ask:20991231T235959Z"

        event_writer.write_text(
            "#!/bin/sh\nprintf '%s\\n' \"$1\" >>\"$TEST_BOARD\"\n",
            encoding="utf-8",
        )
        event_writer.chmod(0o700)
        plan.write_text(
            "genome\taccept\taccept isolated synthetic TG ask\n",
            encoding="utf-8",
        )
        env = dict(os.environ)
        env.update({
            "MESH_DIR": str(mesh),
            "MESH_TASK_DIR": str(chains),
            "MESH_CHAT_LOG": str(mesh / "chat.log"),
            "MESH_TASK_CHAT_CMD": str(event_writer),
            "MESH_TASK_HANDOFF_CMD": "/bin/true",
            "MESH_TASK_ACTOR": "genome",
            "TEST_BOARD": str(board),
        })

        def run(*args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
            result = subprocess.run(
                [sys.executable, str(TASK), *args],
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            assert result.returncode == expected, (
                f"{args!r}: expected rc={expected}, got {result.returncode}\n"
                f"stdout={result.stdout}\nstderr={result.stderr}"
            )
            return result

        run("create", chain, str(plan), ask)
        task_key = f"{chain}/{step}"
        queue = run("queue", "--dispatch", "--owner", "genome").stdout.splitlines()
        owned = [line for line in queue if len(line.split("\t")) > 1 and line.split("\t")[1] == task_key]
        assert len(owned) == 1, f"synthetic ask was not dispatched exactly once to genome: {queue!r}"
        assert run("check", "dispatch", task_key, "genome").returncode == 0

        initial_posts = [
            line for line in board.read_text(encoding="utf-8").splitlines()
            if line.startswith("[task] ") and f"task:{task_key}" in line
        ]
        assert len(initial_posts) == 1, f"expected one owner dispatch, got {initial_posts!r}"
        assert "owner: genome" in initial_posts[0] and f"ask:{ask[4:]}" in initial_posts[0]

        run("take", chain, step)
        missing = run("done", chain, step, str(root / "missing.md"), expected=2)
        assert "artifact does not exist" in missing.stderr
        state_path = chains / f"{chain}.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["status"] == "active" and state["ask"] == ask[4:]
        assert not any(
            line.startswith("[done] ") and f"task:{task_key}" in line
            for line in board.read_text(encoding="utf-8").splitlines()
        ), "missing-artifact attempt emitted a completion receipt"

        artifact = root / "acceptance.md"
        artifact.write_text("isolated synthetic acceptance evidence\n", encoding="utf-8")
        run("done", chain, step, str(artifact), "accepted with artifact")
        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["status"] == "complete" and state["ask"] == ask[4:]
        assert state["steps"][0]["artifact_sha256"] == hashlib.sha256(artifact.read_bytes()).hexdigest()

        log_lines = (mesh / "chat.log").read_text(encoding="utf-8").splitlines()
        revisions = [line for line in log_lines if "[task-ledger]" in line and f"/chain=s:{chain}" in line]
        assert len(revisions) >= 3, f"expected create, take, and close ledger revisions; got {len(revisions)}"
        assert all(f"/ask=s:{ask[4:]}" in line for line in revisions), "ask key changed across ledger revisions"
        print("PASS: isolated TG ask kept one owner/key and refused artifact-free closure")


if __name__ == "__main__":
    main()
