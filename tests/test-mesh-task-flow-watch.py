#!/usr/bin/env python3
"""Exercise the task-flow reflex against isolated ledger, git, and command fixtures."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from mesh_task_log import encode_readable


ROOT = Path(__file__).resolve().parents[1]
WATCH = ROOT / "scripts" / "mesh-task-flow-watch"
STALE_TASK = "tg-scripts-layout-migration-20260912/retire-layout-shims"
RECOVERY_TASK = "tg-layout-migration-owner-receipt-20260912/settle-expired-owner-receipt"


def run() -> None:
    with tempfile.TemporaryDirectory(prefix="mesh-task-flow-watch-test-") as tmp:
        base = Path(tmp)
        repo = base / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        (repo / "tracked").write_text("committed\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "tracked"], check=True)
        old = int(time.time()) - 8 * 3600
        env = os.environ.copy()
        env.update({
            "GIT_AUTHOR_DATE": str(old), "GIT_COMMITTER_DATE": str(old),
            "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@example.invalid",
        })
        subprocess.run(["git", "-C", str(repo), "commit", "-qm", "old"], env=env, check=True)
        (repo / "tracked").write_text("dirty\n", encoding="utf-8")

        fakebin = base / "bin"
        fakebin.mkdir()
        fixture = base / "audit.txt"
        fixture.write_text(
            f"OVERDUE\tgenome\t{STALE_TASK}\tlease=2026-09-12T21:34:18Z\n"
            f"OPEN_UNOWNED\tgenome\t{RECOVERY_TASK}\tcurrent={RECOVERY_TASK} dispatch=sent\n",
            encoding="utf-8",
        )
        (fakebin / "mesh-task").write_text(
            "#!/bin/sh\n"
            "case $1 in\n"
            "  audit) cat \"$FLOW_AUDIT\" ;;\n"
            "  queue) exit 0 ;;\n"
            "  reschedule-task) printf '%s\\n' \"$2\" >> \"$FLOW_ACTIONS\" ;;\n"
            "  *) exit 64 ;;\n"
            "esac\n",
            encoding="utf-8",
        )
        (fakebin / "mesh-chat").write_text(
            "#!/bin/sh\nprintf '%s\\n' \"$*\" >> \"$FLOW_CHAT\"\n",
            encoding="utf-8",
        )
        for executable in fakebin.iterdir():
            executable.chmod(0o755)

        chat = base / "chat.log"
        recovery = {
            "version": 2, "chain": "tg-layout-migration-owner-receipt-20260912",
            "created": "2026-09-12T21:46:05Z", "status": "open", "current": 0,
            "dispatch": "sent",
            "steps": [{
                "id": RECOVERY_TASK, "slug": "settle-expired-owner-receipt",
                "owner": "genome", "status": "open",
                "description": f"Settle the overdue owner receipt for {STALE_TASK}",
                "dispatched_at": "2026-09-13T02:20:55Z",
            }],
        }
        event = encode_readable(recovery, 1)
        chat.write_text(f"2026-09-12T21:46:05Z witness@mesh-home :: {event}\n",
                        encoding="utf-8")

        actions = base / "actions.log"
        board = base / "board.log"
        tape = base / "flow.log"
        state = base / "flow-state.json"
        run_env = os.environ.copy()
        run_env.update({
            "PATH": f"{fakebin}:{os.environ['PATH']}",
            "FLOW_AUDIT": str(fixture), "FLOW_ACTIONS": str(actions),
            "FLOW_CHAT": str(board), "MESH_TASK_FLOW_ROOT": str(repo),
            "MESH_TASK_FLOW_CHAT_LOG": str(chat), "MESH_TASK_FLOW_TAPE": str(tape),
            "MESH_TASK_FLOW_STATE": str(state), "MESH_TASK_FLOW_NOW": str(int(time.time())),
            "MESH_TASK_FLOW_COMMIT_AGE": str(7 * 3600),
            "MESH_TASK_FLOW_RENOTIFY_AGE": str(1800),
        })
        result = subprocess.run([sys.executable, str(WATCH), "--once"], env=run_env,
                                text=True, capture_output=True, check=False)
        if result.returncode:
            raise AssertionError(f"watch failed rc={result.returncode}: {result.stderr}\n{result.stdout}")
        output = result.stdout
        for field in ("overdue=1", "dispatchable=0", "commit_age_s=", "dirty=1",
                      "repair=renotified", STALE_TASK, RECOVERY_TASK):
            if field not in output:
                raise AssertionError(f"watch output missing {field!r}: {output}")
        if actions.read_text(encoding="utf-8").splitlines() != [RECOVERY_TASK]:
            raise AssertionError("watch did not re-notify the exact current owner-recovery task")
        if board.exists() and board.stat().st_size:
            raise AssertionError("successful re-notification must not raise a failure alert")
        run_row = tape.read_text(encoding="utf-8")
        for field in ("RUN", "overdue=1", "dispatchable=0", "repair=renotified", "health=DEGRADED"):
            if field not in run_row:
                raise AssertionError(f"per-pass tape missing {field!r}: {run_row}")

        before_tape = tape.read_bytes()
        dry = subprocess.run([sys.executable, str(WATCH), "--test"], env=run_env,
                             text=True, capture_output=True, check=False)
        if dry.returncode or "PASS" not in dry.stdout:
            raise AssertionError(f"--test failed: rc={dry.returncode}\n{dry.stdout}\n{dry.stderr}")
        if tape.read_bytes() != before_tape:
            raise AssertionError("--test wrote the live observability tape")
        print("task-flow-watch fixture: PASS (overdue lock detected, exact recovery re-notified, tape fresh, --test dry)")


if __name__ == "__main__":
    run()
