#!/usr/bin/env python3
"""Fixture-test the scheduled witness task recovery and self-pick checks."""
from __future__ import annotations

import importlib.util
from importlib.machinery import SourceFileLoader
import json
import os
import subprocess
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCH = ROOT / "scripts" / "mesh-witness-task-autonomy"
WRAPPER = ROOT / "scripts" / "mesh-task-unblock-sweep"
SPEC = importlib.util.spec_from_loader("mesh_witness_task_autonomy", SourceFileLoader("mesh_witness_task_autonomy", str(WATCH)))
watch = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(watch)


def run() -> None:
    # Exercise the real subprocess boundary before replacing commands with fixtures.
    with tempfile.TemporaryDirectory(prefix="mesh-autonomy-missing-command-") as raw:
        missing = str(Path(raw) / "absent-command")
        result = subprocess.run(
            [str(WATCH), "--once"], text=True, capture_output=True,
            env={**os.environ, "MESH_DIR": raw,
                 "MESH_WITNESS_AUTONOMY_JOURNAL_CMD": missing,
                 "MESH_WITNESS_AUTONOMY_TASK": missing,
                 "MESH_WITNESS_AUTONOMY_MIND_STATE": missing,
                 "MESH_WITNESS_AUTONOMY_CHAT": missing}, check=False)
        tape_path = Path(raw) / "witness-task-autonomy.log"
        assert result.returncode == 1 and tape_path.exists(), (
            "missing dependency must leave a failed RUN artifact", result.stderr)
        assert "health=FAIL" in tape_path.read_text()
        assert "journal-rc-127" in tape_path.read_text()
        assert "alert=failed-rc-127" in tape_path.read_text()
    timed = watch.command([sys.executable, "-c", "import time; time.sleep(10)"], timeout=0.05)
    assert timed.returncode == 124, "a timed-out probe must become a reportable failure"
    with tempfile.TemporaryDirectory(prefix="mesh-witness-task-autonomy-") as raw:
        base = Path(raw)
        watch.JOURNAL = base / "tasks.journal"
        watch.TAPE = base / "tape.log"
        watch.STATE = base / "state.json"
        watch.FOLLOWTHROUGH = base / "followthrough.tsv"
        watch.ALERT_SECONDS = 1800
        calls: list[list[str]] = []
        alerts: list[str] = []
        recovery_wakes: list[list[str]] = []
        dispatch_repairs: list[list[str]] = []
        omit_bob_unowned = False
        audit = (
            "OPEN_UNOWNED\talice\towned/work\tdispatch=sent\n"
            "OPEN_UNOWNED\tcarol\tfailed/work\tdispatch=failed\n"
            "OPEN_UNOWNED\t-\tpool/work\tdispatch=sent\n"
            "RUNNING\tgenome\tgenome/landing\tlease=2030-01-01T00:00:00Z\n"
            "BLOCKED\thaunt\tchain/wait\tdependency\tretry=prerequisite\n"
        )
        global_queue = ("alice\towned/work\t0\tdescription\n"
                        "carol\tfailed/work\t0\tdescription\n"
                        "-\tpool/work\t0\tdescription\n")

        def fake_command(argv: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
            nonlocal omit_bob_unowned
            calls.append(argv)
            out = ""
            rc = 0
            if argv[0] == watch.JOURNAL_CMD:
                watch.JOURNAL.write_text(
                    "timestamp=now\ntask_source=PASS\nsource_events=3 source_errors=0\n",
                    encoding="utf-8")
            elif argv[:2] == [watch.TASK, "audit"]:
                out = audit
            elif argv[:3] == [watch.TASK, "replay", "--json"]:
                out = json.dumps({"fixture": {"data": {"steps": [
                    {"id": "owned/work", "owner": "alice", "status": "open",
                     "queued_at": "1970-01-01T00:15:00Z"},
                    {"id": "failed/work", "owner": "carol", "status": "open",
                     "queued_at": "1970-01-01T00:15:30Z"},
                    {"id": "pool/work", "owner": None, "status": "open",
                     "queued_at": "1970-01-01T00:16:00Z"},
                    {"id": "genome/landing", "owner": "genome", "status": "active",
                     "last_progress": "1970-01-01T00:15:00Z"},
                    {"id": "chain/wait", "owner": "haunt", "status": "blocked",
                     "blocked": "1970-01-01T00:14:00Z"},
                ]}}})
            elif argv[:2] == [watch.TASK, "queue"] and argv[2:] == ["--dispatch"]:
                out = global_queue
            elif argv[:2] == [watch.TASK, "queue"] and argv[2:4] == ["--dispatch", "--owner"]:
                mind = argv[4]
                if mind == "alice":
                    out = "alice\towned/work\t0\tdescription\n-\tpool/work\t0\tdescription\n"
                elif mind == "bob" and not omit_bob_unowned:
                    out = "-\tpool/work\t0\tdescription\n"
            elif argv[:2] == [watch.TASK, "check"]:
                if argv[3] == "dispatch" and argv[4] == "missing":
                    rc = 2
            elif argv[:2] == [watch.TASK, "reschedule-task"]:
                dispatch_repairs.append(argv)
            elif argv == [watch.MIND_STATE, "--stats"]:
                out = "WINDOW\tSTATE\nalice\tIDLE\nbob\tIDLE\nwitness\tWORKING\n"
            elif argv[0] == watch.TELL:
                recovery_wakes.append(argv)
            elif argv[0] == watch.CHAT:
                alerts.append(" ".join(argv[1:]))
            else:
                rc = 64
            return subprocess.CompletedProcess(argv, rc, out, "")

        watch.command = fake_command
        original_time = watch.time.time
        moment = [1_000]
        watch.time.time = lambda: moment[0]
        if watch.run_once() != 0:
            raise AssertionError("healthy ownerless queue fixture failed")
        tape = watch.TAPE.read_text(encoding="utf-8")
        for field in ("health=PASS", "source=PASS", "unfinished=5", "blocked=1",
                      "idle_minds=2", "dispatchable=3", "ownerless=1", "ownerless_visible=2",
                      "dispatch_repairs=1"):
            if field not in tape:
                raise AssertionError(f"tape missing {field}: {tape}")
        if dispatch_repairs != [[watch.TASK, "reschedule-task", "failed/work"]]:
            raise AssertionError(f"failed exact-owner dispatch was not repaired: {dispatch_repairs}")
        followthrough = watch.FOLLOWTHROUGH.read_text(encoding="utf-8")
        for evidence in (
                "observed_at\tstate\towner\ttask\tage_s\treason\tnext_action",
                "\tBLOCKED\thaunt\tchain/wait\t160\tdependency retry=prerequisite\t",
                "resolve blocker, then resume exact task",
                "\tRUNNING\tgenome\tgenome/landing\t100\tlease=2030-01-01T00:00:00Z\t",
                "record progress, completion, or concrete blocker"):
            if evidence not in followthrough:
                raise AssertionError(f"followthrough ledger missing {evidence!r}: {followthrough}")
        for mind in ("alice", "bob"):
            if [watch.TASK, "queue", "--dispatch", "--owner", mind] not in calls:
                raise AssertionError(f"ownerless work was not checked in {mind}'s queue")
            if [watch.TASK, "check", "dispatch", "pool/work", mind] not in calls:
                raise AssertionError(f"ownerless work was not eligibility-checked by {mind}")

        moment[0] += watch.ACTIVE_STALL_SECONDS + 1
        if watch.run_once() != 1:
            raise AssertionError("unchanged active claim was not reported as stalled")
        stalled_tape = watch.TAPE.read_text(encoding="utf-8").splitlines()[-1]
        if "active-task-stalled-genome/landing-for-" not in stalled_tape:
            raise AssertionError(f"stalled active claim lacked exact task evidence: {stalled_tape}")
        if len(recovery_wakes) != 1 or recovery_wakes[0][2] != "genome" or "genome/landing" not in recovery_wakes[0][-1]:
            raise AssertionError(f"stalled active claim did not wake its exact owner: {recovery_wakes}")
        watch.time.time = original_time
        watch.STATE.write_text("{}\n", encoding="utf-8")

        omit_bob_unowned = True
        if watch.run_once() != 1:
            raise AssertionError("missing ownerless work in an idle queue did not fail")
        failure_tape = watch.TAPE.read_text(encoding="utf-8").splitlines()[-1]
        if "unowned-pool/work-invisible-to-idle-bob" not in failure_tape:
            raise AssertionError(f"failure tape lacks exact owner/task: {failure_tape}")
        if not alerts or "witness-task-autonomy" not in alerts[-1]:
            raise AssertionError("autonomy failure was not surfaced on the board")

    with tempfile.TemporaryDirectory(prefix="mesh-unblock-reflex-wiring-") as raw:
        base = Path(raw)
        home_bin = base / ".local" / "bin"
        home_bin.mkdir(parents=True)
        order = base / "order"
        for name, marker in (("mesh-task", "sweep"), ("mesh-witness-task-autonomy", "witness")):
            path = home_bin / name
            path.write_text(f"#!/bin/sh\nprintf '%s\\n' {marker} >> '{order}'\n", encoding="utf-8")
            path.chmod(0o755)
        env = os.environ.copy()
        env["HOME"] = str(base)
        result = subprocess.run([str(WRAPPER), "--run"], env=env,
                                text=True, capture_output=True, check=False)
        if result.returncode:
            raise AssertionError(f"scheduled reflex failed: {result.stdout}{result.stderr}")
        if order.read_text(encoding="utf-8").splitlines() != ["sweep", "witness"]:
            raise AssertionError("the scheduled recovery sweep did not run before witness verification")
        (home_bin / "mesh-task").write_text("#!/bin/sh\nexit 9\n", encoding="utf-8")
        order.write_text("")
        result = subprocess.run([str(WRAPPER), "--run"], env=env,
                                text=True, capture_output=True, check=False)
        assert result.returncode == 9, "failed sweep status must remain loud"
        assert order.read_text().splitlines() == ["witness"], (
            "failed recovery must still run witness observation")
    print("witness-task-autonomy: PASS (journal, audit, exact checks, idle self-pick, failure, wiring)")


if __name__ == "__main__":
    run()
