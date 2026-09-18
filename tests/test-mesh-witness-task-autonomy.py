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
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCH = ROOT / "scripts" / "mesh-witness-task-autonomy"
WRAPPER = ROOT / "scripts" / "mesh-task-unblock-sweep"
sys.path.insert(0, str(ROOT / "scripts"))
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
            "OPEN_UNOWNED\t-\towned/work\tdispatch=sent\n"
            "OPEN_UNOWNED\t-\tfailed/work\tdispatch=failed\n"
            "OPEN_UNOWNED\t-\tpool/work\tdispatch=sent\n"
            "RUNNING\tgenome\tgenome/landing\tlease=2030-01-01T00:00:00Z\n"
            "RUNNING\thealth\thealth-warning/ace9180f/triage\tlease=2030-01-01T00:00:00Z\n"
            "RUNNING\tgenome\tdone/stale-lease\tlease=2030-01-01T00:00:00Z\n"
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
                    {"id": "done/stale-lease", "owner": "genome", "status": "done",
                     "artifact": "/tmp/fixture-artifact", "result": "ok"},
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
        for field in ("health=PASS", "source=PASS", "unfinished=7", "blocked=1",
                      "idle_minds=2", "dispatchable=2", "unroutable=1", "ownerless=1", "ownerless_visible=2",
                      "dispatch_repairs=1"):
            if field not in tape:
                raise AssertionError(f"tape missing {field}: {tape}")
        # carol staffs no live window, so its exact-owner row must leave the
        # dispatchable count without being checked or repaired away.
        if [watch.TASK, "check", "dispatch", "failed/work", "carol"] in calls:
            raise AssertionError("unroutable-owner work was eligibility-checked as dispatchable")
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
        # Triage rows are the detector's own repair queue: an aged
        # health-warning triage must never read as stalled work nor wake triage
        # about itself (ace9180f triaged stalled 92f9dc0c).
        if "active-task-stalled-health-warning/ace9180f/triage-for-" in stalled_tape:
            raise AssertionError(f"stalled triage row was reported as stalled work: {stalled_tape}")
        if any("health-warning/ace9180f/triage" in wake[-1] for wake in recovery_wakes):
            raise AssertionError(f"stalled triage row woke its owner: {recovery_wakes}")
        # A DONE row holding a live lease is journal lag, not a stall: no
        # error and no recovery wake for it, while the live claim still pages.
        if "active-task-stalled-done/stale-lease-for-" in stalled_tape:
            raise AssertionError(f"canonically DONE row was reported as stalled: {stalled_tape}")
        if any("done/stale-lease" in wake[-1] for wake in recovery_wakes):
            raise AssertionError(f"DONE row woke its owner: {recovery_wakes}")
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

    def refusal_case(kind: str) -> tuple[int, str, list[list[str]]]:
        with tempfile.TemporaryDirectory(prefix=f"mesh-witness-dispatch-refusal-{kind}-") as raw:
            base = Path(raw)
            watch.JOURNAL = base / "tasks.journal"
            watch.TAPE = base / "tape.log"
            watch.STATE = base / "state.json"
            watch.FOLLOWTHROUGH = base / "followthrough.tsv"
            calls: list[list[str]] = []
            taken = [kind == "stale"]
            task_id = f"{kind}/work"
            prior_first_seen = int(time.time()) - 1700
            if kind == "stale":
                watch.STATE.write_text(json.dumps({"active_observed": {
                    task_id: {"owner": "health", "lease": "2030-01-01T00:30:01Z",
                              "first_seen": prior_first_seen}
                }}), encoding="utf-8")

            def step(status: str) -> dict[str, str]:
                value = {"id": task_id, "owner": "health", "status": status,
                         "queued_at": "2030-01-01T00:00:00Z"}
                if status in ("active", "claimed"):
                    value.update(started="2030-01-01T00:00:01Z",
                                 lease_until="2030-01-01T00:30:01Z")
                return value

            def record(status: str) -> str:
                steps = [step(status)]
                if kind == "owner-busy" and taken[0]:
                    steps.append({"id": f"{kind}/existing", "owner": "health", "status": "active",
                                  "lease_until": "2030-01-01T00:30:01Z"})
                return json.dumps({kind: {"data": {
                    "chain": kind, "status": "active" if status == "active" else "open",
                    "current": 0, "steps": steps}}})

            def queue_row() -> str:
                return f"health\t{task_id}\t0\tfixture task\n"

            audit_open = f"OPEN_UNOWNED\t-\t{task_id}\tdispatch=sent\n"
            audit_active = f"RUNNING\thealth\t{task_id}\tlease=2030-01-01T00:30:01Z\n"
            audit_owner_busy = (audit_open +
                                f"RUNNING\thealth\t{kind}/existing\tlease=2030-01-01T00:30:01Z\n")
            audit_reads = [0]
            replay_reads = [0]
            queue_reads = [0]

            def refusal_command(argv: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
                calls.append(argv)
                out = ""
                rc = 0
                if argv[0] == watch.JOURNAL_CMD:
                    watch.JOURNAL.write_text(
                        "timestamp=now\ntask_source=PASS\nsource_events=1 source_errors=0\n",
                        encoding="utf-8")
                elif argv[:2] == [watch.TASK, "audit"]:
                    audit_reads[0] += 1
                    if kind == "unreadable" and taken[0] and audit_reads[0] > 1:
                        rc = 1
                    elif kind == "stale" and audit_reads[0] == 1:
                        out = ""  # The first witness audit omitted the pre-existing active row.
                    elif kind == "owner-busy" and taken[0]:
                        out = audit_owner_busy
                    elif taken[0]:
                        out = audit_active
                    else:
                        out = audit_open
                elif argv[:3] == [watch.TASK, "replay", "--json"]:
                    replay_reads[0] += 1
                    if kind == "malformed" and taken[0] and replay_reads[0] > 1:
                        out = "{malformed current task snapshot"
                    elif kind == "stale" and replay_reads[0] == 1:
                        out = json.dumps({"unrelated": {"data": {
                            "chain": "unrelated", "status": "open", "current": 0,
                            "steps": [{"id": "unrelated/step", "owner": "witness", "status": "open"}]}}})
                    else:
                        current_status = "active" if taken[0] and kind != "owner-busy" else "open"
                        out = record(current_status)
                elif argv[:2] == [watch.TASK, "queue"]:
                    queue_reads[0] += 1
                    current = (taken[0] and kind in ("race", "stale", "owner-busy", "malformed")
                               and not (kind == "stale" and queue_reads[0] == 1))
                    current = current or (kind == "eligible-refusal" and queue_reads[0] > 1)
                    if argv[2:] == ["--dispatch"]:
                        out = "" if current else queue_row()
                    elif argv[2:] == ["--dispatch", "--owner", "health"]:
                        out = "" if current else queue_row()
                    else:
                        rc = 64
                elif argv[:3] == [watch.TASK, "check", "dispatch"]:
                    rc = int(kind[-1]) if kind in ("rc1", "rc3") else 2
                    if kind in ("race", "owner-busy", "malformed", "unreadable"):
                        taken[0] = True  # The owner claims the row after the queue snapshot.
                elif argv == [watch.MIND_STATE, "--stats"]:
                    out = "WINDOW\tSTATE\nhealth\tWORKING\nwitness\tWORKING\n"
                elif argv[:2] == [watch.TELL, "--origin"]:
                    pass
                elif argv[0] == watch.CHAT:
                    pass
                else:
                    rc = 64
                return subprocess.CompletedProcess(argv, rc, out, "")

            watch.command = refusal_command
            result = watch.run_once()
            tape = watch.TAPE.read_text(encoding="utf-8").splitlines()[-1]
            if kind == "stale":
                refreshed = json.loads(watch.STATE.read_text(encoding="utf-8"))
                actual_first_seen = refreshed["active_observed"]["stale/work"]["first_seen"]
                if actual_first_seen != prior_first_seen:
                    raise AssertionError("a stale audit reset the prior age of a newly recovered active task")
            return result, tape, calls

    for kind in ("race", "stale", "owner-busy"):
        result, tape, calls = refusal_case(kind)
        if result != 0 or "health=PASS" not in tape or "active=1" not in tape:
            raise AssertionError(f"proven {kind} transition stayed failed or lost its active row: {tape}")
        if "errors=none" not in tape or "check-" in tape:
            raise AssertionError(f"proven {kind} transition retained a refusal error: {tape}")
        if calls.count([watch.TASK, "replay", "--json"]) < 2:
            raise AssertionError(f"{kind} refusal did not re-read canonical task records")

    result, tape, _ = refusal_case("persistent")
    if result != 1 or "health=FAIL" not in tape or "check-persistent/work-for-health-rc-2" not in tape:
        raise AssertionError(f"persistent exact-owner refusal was hidden: {tape}")

    result, tape, _ = refusal_case("eligible-refusal")
    if result != 1 or "health=FAIL" not in tape or "reconcile-check-refusal-still-eligible" not in tape:
        raise AssertionError(f"refusal against a still-eligible ledger row was hidden: {tape}")

    for rc in (1, 3):
        result, tape, calls = refusal_case(f"rc{rc}")
        exact_error = f"check-rc{rc}/work-for-health-rc-{rc}"
        if result != 1 or "health=FAIL" not in tape or exact_error not in tape:
            raise AssertionError(f"check exit {rc} was not kept failed: {tape}")
        if calls.count([watch.TASK, "audit"]) != 1:
            raise AssertionError(f"check exit {rc} incorrectly entered refusal reconciliation")

    result, tape, _ = refusal_case("malformed")
    if result != 1 or "health=FAIL" not in tape or "reconcile-replay-parse" not in tape:
        raise AssertionError(f"malformed post-refusal ledger was not kept loud: {tape}")

    result, tape, _ = refusal_case("unreadable")
    if result != 1 or "health=FAIL" not in tape or "reconcile-audit-rc-1" not in tape:
        raise AssertionError(f"unreadable post-refusal audit was not kept loud: {tape}")

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
