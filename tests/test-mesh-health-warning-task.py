#!/usr/bin/env python3
"""Health warnings in chat.log become durable health-owned task chains."""

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "mesh-health-warning-task"


def run_watcher(mesh: Path, task_cmd: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ,
               MESH_DIR=str(mesh),
               MESH_CHAT_LOG=str(mesh / "chat.log"),
               MESH_HEALTH_WARNING_TASK_STATE=str(mesh / "warning-tasks.state"),
               MESH_HEALTH_WARNING_TASK_CMD=str(task_cmd))
    return subprocess.run(["python3", str(SCRIPT)], env=env, text=True,
                          capture_output=True, check=False)


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        td = Path(raw)
        mesh = td / "mesh"
        bindir = td / "bin"
        mesh.mkdir()
        bindir.mkdir()
        task_cmd = bindir / "mesh-task"
        task_cmd.write_text(
            "#!/bin/sh\n"
            "if [ \"$1\" = replay ] && [ \"$2\" = --json ]; then\n"
            "  if [ -n \"$REPLAY_FILE\" ] && [ -f \"$REPLAY_FILE\" ]; then\n"
            "    cat \"$REPLAY_FILE\"\n"
            "  elif [ -n \"$EXISTING_CHAIN\" ]; then\n"
            "    printf '%s' \"$EXISTING_CHAIN_JSON\"\n"
            "  else\n"
            "    printf '{}\\n'\n"
            "  fi\n"
            "  exit 0\n"
            "fi\n"
            "printf '%s\\n' \"$@\" >> \"$TASK_CALLS\"\n"
            "if [ \"$1\" = create ] && [ -n \"$PARTIAL_CREATE\" ] && [ ! -f \"$REPLAY_FILE\" ]; then\n"
            "  printf '{\"%s\":{\"data\":{\"chain\":\"%s\",\"status\":\"open\",\"current\":0,\"dispatch\":\"failed\",\"steps\":[{\"status\":\"open\"}]}}}\\n' \"$2\" \"$2\" > \"$REPLAY_FILE\"\n"
            "  echo 'mesh-task: dispatch failed after durable create' >&2\n"
            "  exit 1\n"
            "fi\n"
            "if [ \"$1\" = dispatch ] && [ -n \"$DISPATCH_SUCCESS_JSON\" ]; then\n"
            "  cp \"$DISPATCH_SUCCESS_JSON\" \"$REPLAY_FILE\"\n"
            "  exit 0\n"
            "fi\n"
            "if [ \"$1\" = create ] && [ -n \"$EXISTING_CHAIN\" ]; then\n"
            "  echo \"mesh-task: chain already exists; refusing to overwrite\" >&2\n"
            "  exit 2\n"
            "fi\n"
            "plan=\"\"\n"
            "while [ $# -gt 0 ]; do\n"
            "  if [ \"$1\" = create ]; then shift 2; plan=\"$1\"; fi\n"
            "  shift\n"
            "done\n"
            "cat \"$plan\" >> \"$TASK_PLANS\"\n"
        )
        task_cmd.chmod(0o755)
        os.environ["TASK_CALLS"] = str(td / "calls")
        os.environ["TASK_PLANS"] = str(td / "plans")
        chat = mesh / "chat.log"
        chat.write_text(
            "2026-09-08T10:00:00Z  mesh-home/mesh-room-sense-loss@mesh-home  ::  "
            "[fyi] room sense STILL lost: its EYES DEAD for 21d — held\n"
            "2026-09-08T10:00:01Z  random@mesh-home  ::  [fyi] ordinary update\n"
        )

        first = run_watcher(mesh, task_cmd)
        assert first.returncode == 0, first.stderr
        plans = (td / "plans").read_text()
        assert "health\ttriage\t" in plans, plans
        assert plans.startswith("health\ttriage\t"), plans
        assert (td / "calls").read_text().count("create") == 1

        second = run_watcher(mesh, task_cmd)
        assert second.returncode == 0, second.stderr
        assert (td / "calls").read_text().count("create") == 1

        with chat.open("a") as handle:
            handle.write("2026-09-08T10:04:00Z health  ::  [task] health-warning/fixture/triage "
                         "[health-warning] quoted source; task:fixture\n")
            handle.write("2026-09-08T10:05:00Z health@mesh-home :: [health-warning] "
                         "mesh-egress-health UNKNOWN after probe timeout\n")
        third = run_watcher(mesh, task_cmd)
        assert third.returncode == 0, third.stderr
        assert (td / "calls").read_text().count("create") == 2, (td / "calls").read_text()

        # An already durable blocked chain is a recognized disposition. The
        # watcher must not retry create, but must advance past the source line.
        body = "[health-warning] mesh-egress-health UNKNOWN after probe timeout (blocked retry)"
        key = "tagged:" + body.lower()
        chain = "health-warning/" + hashlib.sha256(key.encode()).hexdigest()[:20]
        blocked = {"data": {"chain": chain, "status": "blocked", "current": 0, "steps": [
            {"status": "blocked", "blocker_type": "dependency"}]}}
        os.environ["EXISTING_CHAIN"] = "1"
        os.environ["EXISTING_CHAIN_JSON"] = json.dumps({chain: blocked})
        probe = subprocess.run([str(task_cmd), "replay", "--json"], text=True,
                               capture_output=True, check=False)
        assert json.loads(probe.stdout)[chain]["data"]["status"] == "blocked", probe.stdout
        with chat.open("a") as handle:
            handle.write("2026-09-08T10:06:00Z health@mesh-home :: " + body + "\n")
        fourth = run_watcher(mesh, task_cmd)
        assert fourth.returncode == 0, fourth.stderr
        assert (td / "calls").read_text().count("create") == 2, (td / "calls").read_text()
        state = json.loads((mesh / "warning-tasks.state").read_text())
        assert state["created"][key]["chain"] == chain

        # A completed deterministic chain is also a durable disposition. The
        # live warning currently exercises this state, and must not retry create.
        complete_body = "[health-warning] mesh-egress-health UNKNOWN after probe timeout (complete retry)"
        complete_key = "tagged:" + complete_body.lower()
        complete_chain = "health-warning/" + hashlib.sha256(complete_key.encode()).hexdigest()[:20]
        complete = {"data": {"chain": complete_chain, "status": "complete", "current": 0, "steps": [
            {"status": "done"}]}}
        os.environ["EXISTING_CHAIN_JSON"] = json.dumps({complete_chain: complete})
        with chat.open("a") as handle:
            handle.write("2026-09-08T10:07:00Z health@mesh-home :: " + complete_body + "\n")
        fifth = run_watcher(mesh, task_cmd)
        assert fifth.returncode == 0, fifth.stderr
        assert (td / "calls").read_text().count("create") == 2, (td / "calls").read_text()
        state = json.loads((mesh / "warning-tasks.state").read_text())
        assert state["created"][complete_key]["chain"] == complete_chain

        # mesh-task create persists an open chain before its dispatch side
        # effect. A retry must dispatch that exact chain, never invoke create
        # again, and only then advance the source cursor.
        partial_body = "[health-warning] mesh-egress-health UNKNOWN after probe timeout (partial create)"
        partial_key = "tagged:" + partial_body.lower()
        partial_chain = "health-warning/" + hashlib.sha256(partial_key.encode()).hexdigest()[:20]
        os.environ.pop("EXISTING_CHAIN", None)
        os.environ.pop("EXISTING_CHAIN_JSON", None)
        os.environ["PARTIAL_CREATE"] = "1"
        replay_file = td / "partial-replay.json"
        success_file = td / "partial-success.json"
        os.environ["REPLAY_FILE"] = str(replay_file)
        os.environ["DISPATCH_SUCCESS_JSON"] = str(success_file)
        success_file.write_text(json.dumps({partial_chain: {"data": {
            "chain": partial_chain, "status": "open", "current": 0,
            "dispatch": "sent", "steps": [{"status": "open"}]}}}))
        with chat.open("a") as handle:
            handle.write("2026-09-08T10:08:00Z health@mesh-home :: " + partial_body + "\n")
        failed_create = run_watcher(mesh, task_cmd)
        assert failed_create.returncode != 0, failed_create.stderr
        assert json.loads((mesh / "warning-tasks.state").read_text())["offset"] < chat.stat().st_size
        calls_before_retry = (td / "calls").read_text().splitlines()
        assert calls_before_retry[-3:-1] == ["create", partial_chain], calls_before_retry
        assert "dispatch" not in calls_before_retry[-3:], calls_before_retry

        retried = run_watcher(mesh, task_cmd)
        assert retried.returncode == 0, retried.stderr
        calls_after_retry = (td / "calls").read_text().splitlines()
        assert calls_after_retry[-2:] == ["dispatch", partial_chain], calls_after_retry
        assert calls_after_retry.count("create") == 3, calls_after_retry
        state = json.loads((mesh / "warning-tasks.state").read_text())
        assert state["created"][partial_key]["chain"] == partial_chain

    # A recovered cursor must not replay an unbounded burst while Health has
    # one running triage and one sent/open queued triage already occupying the
    # admission bound.  The exact first source event remains unread until a
    # slot frees, then only that event is admitted.
    with tempfile.TemporaryDirectory() as raw:
        td = Path(raw)
        mesh = td / "mesh"
        bindir = td / "bin"
        mesh.mkdir()
        bindir.mkdir()
        task_cmd = bindir / "mesh-task"
        task_cmd.write_text(
            "#!/bin/sh\n"
            "if [ \"$1\" = replay ] && [ \"$2\" = --json ]; then cat \"$REPLAY_FILE\"; exit 0; fi\n"
            "printf '%s\\n' \"$@\" >> \"$TASK_CALLS\"\n"
            "if [ \"$1\" = create ]; then\n"
            "  chain=\"$2\"; shift 2; plan=\"$1\"; cat \"$plan\" >> \"$TASK_PLANS\"\n"
            "  if [ \"$(grep -c '^create$' \"$TASK_CALLS\")\" -eq 1 ]; then\n"
            "    printf '{\"%s\":{\"data\":{\"chain\":\"%s\",\"status\":\"open\",\"current\":0,\"dispatch\":\"sent\",\"steps\":[{\"status\":\"open\",\"owner\":\"health\"}]}}}\\n' \"$chain\" \"$chain\" > \"$REPLAY_FILE\"\n"
            "  fi\n"
            "fi\n"
        )
        task_cmd.chmod(0o755)
        calls = td / "calls"
        plans = td / "plans"
        replay = td / "replay.json"
        os.environ["TASK_CALLS"] = str(calls)
        os.environ["TASK_PLANS"] = str(plans)
        os.environ["REPLAY_FILE"] = str(replay)
        os.environ.pop("EXISTING_CHAIN", None)
        os.environ.pop("EXISTING_CHAIN_JSON", None)
        os.environ.pop("PARTIAL_CREATE", None)
        os.environ.pop("DISPATCH_SUCCESS_JSON", None)
        chat = mesh / "chat.log"
        warnings = [
            f"2026-09-08T11:00:0{i}Z health@mesh-home :: [health-warning] replay warning {i} UNKNOWN\n"
            for i in range(3)
        ]
        chat.write_text("".join(warnings))

        def chain_for(index: int) -> str:
            body = f"[health-warning] replay warning {index} UNKNOWN"
            key = "tagged:" + body.lower()
            return "health-warning/" + hashlib.sha256(key.encode()).hexdigest()[:20]

        occupied = {
            "health-warning/running": {"data": {
                "chain": "health-warning/running", "status": "open", "current": 0,
                "dispatch": "sent", "steps": [{"status": "active", "owner": "health"}]},
            },
            "health-warning/queued": {"data": {
                "chain": "health-warning/queued", "status": "open", "current": 0,
                "dispatch": "sent", "steps": [{"status": "open", "owner": "health"}]},
            },
        }
        replay.write_text(json.dumps(occupied))
        blocked = run_watcher(mesh, task_cmd)
        assert blocked.returncode == 0, blocked.stderr
        assert not calls.exists() or calls.read_text() == "", calls.read_text() if calls.exists() else ""
        state = json.loads((mesh / "warning-tasks.state").read_text())
        assert state["offset"] == 0, state

        replay.write_text("{}")
        admitted = run_watcher(mesh, task_cmd)
        assert admitted.returncode == 0, admitted.stderr
        call_lines = calls.read_text().splitlines()
        assert call_lines[:2] == ["create", chain_for(0)], call_lines
        assert call_lines.count("create") == 1, call_lines
        assert "replay warning 0" in plans.read_text()
        state = json.loads((mesh / "warning-tasks.state").read_text())
        assert state["offset"] == len(warnings[0].encode()), state


if __name__ == "__main__":
    main()
