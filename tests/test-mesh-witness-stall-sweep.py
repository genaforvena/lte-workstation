#!/usr/bin/env python3
"""End-to-end stall sweep on a disposable ledger: no live mesh touched.

Builds a temp task ledger with (a) a wait that turns dead when its
prerequisite chain is rejected, and (b) a blocked head whose retry names a
DONE task. Runs the real sweep --run with fakes for chat/tell and asserts the
dead park is cleared, the satisfied retry is nudged to the exact owner, and a
PASS tape row is written. A second run asserts throttle silence (no re-nudge).
"""
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"
SWEEP = ROOT / "scripts" / "mesh-witness-stall-sweep"


class StallSweepTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        fake = root / "bin"
        fake.mkdir()
        self.chat_log = root / "chat-events.log"
        self.told = root / "told.log"
        (fake / "chat").write_text(
            f"#!/bin/sh\nprintf '%s\\n' \"$*\" >> {self.chat_log}\nexit 0\n")
        (fake / "handoff").write_text("#!/bin/sh\nexit 0\n")
        (fake / "tell").write_text(
            f"#!/bin/sh\nprintf '%s\\n' \"$*\" >> {self.told}\nexit 0\n")
        for tool in ("chat", "handoff", "tell"):
            (fake / tool).chmod(0o755)
        mesh = root / "mesh"
        self.env = os.environ | {
            "MESH_DIR": str(mesh),
            "MESH_TASK_DIR": str(mesh / "task-chains"),
            "MESH_TASK_CHAT_CMD": str(fake / "chat"),
            "MESH_TASK_HANDOFF_CMD": str(fake / "handoff"),
            "MESH_TASK_ACTOR": "haunt",
            "MESH_WITNESS_STALL_TASK": str(TASK),
            "MESH_WITNESS_STALL_TELL": str(fake / "tell"),
            "MESH_WITNESS_STALL_CHAT": str(fake / "chat"),
            "MESH_WITNESS_STALL_ACTOR": "witness",
            "MESH_WITNESS_STALL_TAPE": str(mesh / "stall.log"),
            "MESH_WITNESS_STALL_STATE": str(mesh / ".stall.json"),
        }
        self.root = root

    def tearDown(self):
        self.tmp.cleanup()

    def task(self, *args, expect=0, actor=None):
        env = dict(self.env)
        if actor:
            env["MESH_TASK_ACTOR"] = actor
        got = subprocess.run(["python3", str(TASK), *args], env=env,
                             text=True, capture_output=True)
        self.assertEqual(got.returncode, expect, (args, got.stderr))
        return got

    def sweep(self, *args):
        got = subprocess.run(["python3", str(SWEEP), *args], env=self.env,
                             text=True, capture_output=True)
        self.assertEqual(got.returncode, 0, (args, got.stdout, got.stderr))
        return got

    def plan(self, name, rows):
        path = self.root / f"{name}.tsv"
        path.write_text("".join(f"{o}\t{s}\t{d}\n" for o, s, d in rows))
        return str(path)

    def test_dead_park_cleared_and_satisfied_retry_nudged(self):
        # Prerequisite chain: head (current, open) + tail (future).
        self.task("create", "pre", self.plan("pre", [
            ("haunt", "head", "prerequisite head"),
            ("vpn", "tail", "prerequisite tail")]))
        # Waiter parks behind the currently-open head: allowed at park time.
        self.task("create", "waiter", self.plan("waiter", [
            ("haunt", "w", "needs pre head")]))
        self.task("take", "waiter", "w")
        self.task("block", "waiter", "w", "dependency",
                  "needs pre", "after pre/head")
        self.task("wait-for", "waiter", "w", "pre/head")
        # The prerequisite chain is then rejected: head terminal, tail open
        # non-current in a rejected chain. The wait can never resolve.
        self.task("take", "pre", "head")
        self.task("reject", "pre", "head", "superseded by operator decision")
        # Blocked head whose retry names a DONE task.
        self.task("create", "aid", self.plan("aid", [
            ("haunt", "job", "produce evidence")]))
        self.task("take", "aid", "job")
        self.task("done", "aid", "job", str(TASK), "verified")
        self.task("create", "stuck", self.plan("stuck", [
            ("haunt", "s", "stalled work")]))
        self.task("take", "stuck", "s")
        self.task("block", "stuck", "s", "experiment-contract",
                  "needs aid", "retry after aid/job has PASS")

        out = self.sweep("--run").stdout
        self.assertIn("parks=1 cleared=1", out)
        self.assertIn("satisfied=1 nudged=1", out)

        status = self.task("status", "waiter").stdout
        self.assertNotIn("waiting_for", status)
        self.assertIn("waiter [open]", status)

        told = self.told.read_text()
        self.assertIn("haunt", told)
        self.assertIn("stuck/s", told)
        self.assertIn("aid/job", told)
        self.assertIn("mesh-task resume stuck s", told)

        tape = (Path(self.env["MESH_WITNESS_STALL_TAPE"])).read_text()
        self.assertIn("health=PASS", tape)
        # The cleared wait is dispatched again: haunt sees it in its queue.
        queue = self.task("queue", "--dispatch", "--owner", "haunt").stdout
        self.assertIn("waiter/w", queue)

        # Second run: throttle silence — nothing new to clear or nudge.
        out2 = self.sweep("--run").stdout
        self.assertIn("parks=0 cleared=0", out2)
        self.assertIn("satisfied=1 nudged=0", out2)
        state = json.loads(Path(self.env["MESH_WITNESS_STALL_STATE"]).read_text())
        self.assertIn("waiter/w", state.get("cleared", []))
        self.assertIn("stuck/s", state.get("nudged", {}))


if __name__ == "__main__":
    unittest.main()
