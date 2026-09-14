#!/usr/bin/env python3
"""wait-for must refuse prerequisites that can never arrive.

Root cause (2026-09-14, tinyfleet stall): a blocked head parked behind its own
future tail reads as QUEUED in audit while queue --dispatch correctly hides it
(waiting_for is not dispatchable) and take() refuses the tail (not current).
Both sides wait on each other forever; the owner sees an empty queue and idles.
The same shape recurs cross-chain when the prerequisite is queued behind
another blocked head. clear-wait repairs parks minted before this guard.
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"


class TaskWaitGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        fake = root / "bin"
        fake.mkdir()
        chat_log = root / "chat-events.log"
        for name in ("chat", "handoff"):
            tool = fake / name
            if name == "chat":
                tool.write_text(f"#!/bin/sh\nprintf '%s\\n' \"$*\" >> {chat_log}\nexit 0\n")
            else:
                tool.write_text("#!/bin/sh\nexit 0\n")
            tool.chmod(0o755)
        self.env = os.environ | {
            "MESH_DIR": str(root / "mesh"),
            "MESH_TASK_DIR": str(root / "mesh" / "task-chains"),
            "MESH_TASK_CHAT_CMD": str(fake / "chat"),
            "MESH_TASK_HANDOFF_CMD": str(fake / "handoff"),
            "MESH_TASK_ACTOR": "haunt",
        }
        self.root = root

    def tearDown(self):
        self.tmp.cleanup()

    def command(self, *args, expect=0):
        got = subprocess.run(["python3", str(TASK), *args], env=self.env,
                             text=True, capture_output=True)
        self.assertEqual(got.returncode, expect, (args, got.stderr))
        return got

    def make_chain(self, name, rows):
        plan = self.root / f"{name}.tsv"
        plan.write_text("".join(f"{o}\t{s}\t{d}\n" for o, s, d in rows))
        self.command("create", name, str(plan))

    def test_self_future_wait_is_refused(self):
        self.make_chain("demo", [("haunt", "head", "blocked head"),
                                 ("h2", "mid", "middle"),
                                 ("vpn", "tail", "verify tail")])
        self.command("take", "demo", "head")
        self.command("block", "demo", "head", "experiment-contract", "needs X", "retry after Y")
        refused = self.command("wait-for", "demo", "head", "demo/tail", expect=2)
        self.assertIn("future step in the same chain", refused.stderr)
        status = self.command("status", "demo").stdout
        self.assertIn("head [blocked]", status)
        self.assertNotIn("waiting_for", status)

    def test_wait_for_step_queued_behind_blocked_head_is_refused(self):
        self.make_chain("demo", [("haunt", "head", "blocked head"),
                                 ("h2", "mid", "middle"),
                                 ("vpn", "tail", "verify tail")])
        self.command("take", "demo", "head")
        self.command("block", "demo", "head", "experiment-contract", "needs X", "retry after Y")
        self.make_chain("other", [("haunt", "w", "other blocked")])
        self.command("take", "other", "w")
        self.command("block", "other", "w", "dependency", "needs Y", "retry later")
        refused = self.command("wait-for", "other", "w", "demo/tail", expect=2)
        self.assertIn("not runnable", refused.stderr)
        self.assertIn("demo", refused.stderr)

    def test_wait_for_parked_waiter_is_refused(self):
        self.make_chain("pre", [("haunt", "job", "do job")])
        self.make_chain("mid", [("haunt", "m", "middle")])
        self.make_chain("outer", [("haunt", "o", "outer")])
        self.command("take", "mid", "m")
        self.command("block", "mid", "m", "dependency", "needs pre", "after pre/job")
        self.command("wait-for", "mid", "m", "pre/job")
        self.command("take", "outer", "o")
        self.command("block", "outer", "o", "dependency", "needs mid", "after mid/m")
        refused = self.command("wait-for", "outer", "o", "mid/m", expect=2)
        self.assertIn("itself parked", refused.stderr)

    def test_wait_for_runnable_and_done_prerequisites_still_allowed(self):
        self.make_chain("pre", [("haunt", "job", "do job")])
        self.make_chain("main", [("haunt", "q", "needs pre")])
        self.command("take", "main", "q")
        self.command("block", "main", "q", "dependency", "needs pre", "after pre/job")
        # Runnable current step of a healthy chain: allowed.
        self.command("wait-for", "main", "q", "pre/job")
        self.assertIn("waiting_for=pre/job", self.command("audit").stdout)
        # DONE prerequisite: allowed and releases immediately.
        self.command("clear-wait", "main", "q", "test re-park")
        self.command("take", "pre", "job")
        self.command("done", "pre", "job", str(TASK), "finished")
        self.make_chain("main2", [("haunt", "q", "needs pre")])
        self.command("take", "main2", "q")
        self.command("block", "main2", "q", "dependency", "needs pre", "after pre/job")
        self.command("wait-for", "main2", "q", "pre/job")
        self.assertNotIn("waiting_for", self.command("status", "main2").stdout)

    def test_independent_successor_must_not_be_parked_as_wait_for_prerequisite(self):
        self.make_chain("demo", [("haunt", "head", "blocked head"),
                                 ("vpn", "tail", "independent prerequisite")])
        self.command("take", "demo", "head")
        self.command("block", "demo", "head", "dependency", "needs tail", "after tail")
        self.env["MESH_TASK_ACTOR"] = "vpn"
        self.command("independent", "demo", "tail", "owner attests independent prerequisite")
        self.command("check", "dispatch", "demo/tail", "vpn")
        self.env["MESH_TASK_ACTOR"] = "haunt"
        refused = self.command("wait-for", "demo", "head", "demo/tail", expect=2)
        self.assertIn("would make this successor non-runnable", refused.stderr)
        status = self.command("status", "demo").stdout
        self.assertIn("demo/head [blocked]", status)
        self.assertNotIn("waiting_for", status)

        self.env["MESH_TASK_ACTOR"] = "vpn"
        self.command("take", "demo", "tail")
        self.command("done", "demo", "tail", str(TASK), "independent prerequisite complete")
        self.env["MESH_TASK_ACTOR"] = "haunt"
        self.command("resume", "demo", "head", "independent prerequisite complete")
        status = self.command("status", "demo").stdout
        self.assertIn("demo/head [active]", status)
        self.assertNotIn("waiting_for", status)

    def test_clear_wait_unparks_and_redispatches(self):
        self.make_chain("pre", [("haunt", "job", "do job")])
        self.make_chain("main", [("haunt", "q", "needs pre")])
        self.command("take", "main", "q")
        self.command("block", "main", "q", "dependency", "needs pre", "after pre/job")
        self.command("wait-for", "main", "q", "pre/job")
        self.command("take", "pre", "job")
        self.command("block", "pre", "job", "dependency", "stalled", "later")
        # Wrong owner cannot clear; coordinator can.
        self.env["MESH_TASK_ACTOR"] = "vpn"
        refused = self.command("clear-wait", "main", "q", "stalled", expect=2)
        self.assertIn("exact owner or coordinator required", refused.stderr)
        self.env["MESH_TASK_ACTOR"] = "witness"
        cleared = self.command("clear-wait", "main", "q", "prerequisite stalled behind blocked head")
        self.assertIn("unparked main/q (was waiting for pre/job)", cleared.stdout)
        self.env["MESH_TASK_ACTOR"] = "haunt"
        self.assertNotIn("waiting_for", self.command("status", "main").stdout)
        self.assertIn("main/q", self.command("queue", "--dispatch", "--owner", "haunt").stdout)

    def test_clear_wait_requires_a_park(self):
        self.make_chain("solo", [("haunt", "s", "plain work")])
        refused = self.command("clear-wait", "solo", "s", "nothing parked", expect=2)
        self.assertIn("not parked", refused.stderr)


if __name__ == "__main__":
    unittest.main()
