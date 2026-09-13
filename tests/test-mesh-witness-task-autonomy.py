#!/usr/bin/env python3
"""Fixture-test the scheduled witness task recovery and self-pick checks."""
from __future__ import annotations

import importlib.util
from importlib.machinery import SourceFileLoader
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCH = ROOT / "scripts" / "mesh-witness-task-autonomy"
WRAPPER = ROOT / "scripts" / "mesh-task-unblock-sweep"
SPEC = importlib.util.spec_from_loader("mesh_witness_task_autonomy", SourceFileLoader("mesh_witness_task_autonomy", str(WATCH)))
watch = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(watch)


def run() -> None:
    with tempfile.TemporaryDirectory(prefix="mesh-witness-task-autonomy-") as raw:
        base = Path(raw)
        watch.JOURNAL = base / "tasks.journal"
        watch.TAPE = base / "tape.log"
        watch.STATE = base / "state.json"
        watch.ALERT_SECONDS = 1800
        calls: list[list[str]] = []
        alerts: list[str] = []
        omit_bob_unowned = False
        audit = (
            "OPEN_UNOWNED\talice\towned/work\tdispatch=sent\n"
            "OPEN_UNOWNED\t-\tpool/work\tdispatch=sent\n"
            "BLOCKED\thaunt\tchain/wait\tdependency\tretry=prerequisite\n"
        )
        global_queue = "alice\towned/work\t0\tdescription\n-\tpool/work\t0\tdescription\n"

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
            elif argv == [watch.MIND_STATE, "--stats"]:
                out = "WINDOW\tSTATE\nalice\tIDLE\nbob\tIDLE\nwitness\tWORKING\n"
            elif argv[0] == watch.CHAT:
                alerts.append(" ".join(argv[1:]))
            else:
                rc = 64
            return subprocess.CompletedProcess(argv, rc, out, "")

        watch.command = fake_command
        if watch.run_once() != 0:
            raise AssertionError("healthy ownerless queue fixture failed")
        tape = watch.TAPE.read_text(encoding="utf-8")
        for field in ("health=PASS", "source=PASS", "unfinished=3", "blocked=1",
                      "idle_minds=2", "dispatchable=2", "ownerless=1", "ownerless_visible=2"):
            if field not in tape:
                raise AssertionError(f"tape missing {field}: {tape}")
        for mind in ("alice", "bob"):
            if [watch.TASK, "queue", "--dispatch", "--owner", mind] not in calls:
                raise AssertionError(f"ownerless work was not checked in {mind}'s queue")
            if [watch.TASK, "check", "dispatch", "pool/work", mind] not in calls:
                raise AssertionError(f"ownerless work was not eligibility-checked by {mind}")

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
    print("witness-task-autonomy: PASS (journal, audit, exact checks, idle self-pick, failure, wiring)")


if __name__ == "__main__":
    run()
