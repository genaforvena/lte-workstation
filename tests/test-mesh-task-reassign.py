#!/usr/bin/env python3
"""Coordinator-only single-chain reassignment sheds queued load to live minds."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"


class TaskReassignTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        fake = root / "bin"
        fake.mkdir()
        for name in ("chat", "handoff"):
            tool = fake / name
            tool.write_text("#!/bin/sh\nexit 0\n")
            tool.chmod(0o755)
        self.env = os.environ | {
            "MESH_DIR": str(root / "mesh"),
            "MESH_TASK_DIR": str(root / "mesh" / "task-chains"),
            "MESH_TASK_CHAT_CMD": str(fake / "chat"),
            "MESH_TASK_HANDOFF_CMD": str(fake / "handoff"),
            "MESH_TASK_ACTOR": "witness",
            "MESH_TASK_COORDINATOR": "witness",
            "MESH_TASK_LIVE_OWNERS": "witness health",
        }
        for chain in ("backlog-a", "backlog-b"):
            plan = root / f"plan-{chain}.tsv"
            plan.write_text(f"witness\treview\treview {chain}\n")
            self.command("create", chain, str(plan))
        self.command("take", "backlog-a", "review")

    def tearDown(self):
        self.tmp.cleanup()

    def command(self, *args, expect=0, actor="witness"):
        env = self.env | {"MESH_TASK_ACTOR": actor}
        got = subprocess.run(["python3", str(TASK), *args], env=env,
                             text=True, capture_output=True)
        self.assertEqual(got.returncode, expect, got.stderr)
        return got

    def test_queued_chain_moves_to_live_mind_and_redispatches(self):
        out = self.command("reassign", "backlog-b", "health", "shed queued load to idle mind")
        self.assertIn("reassigned backlog-b/review owner=witness -> health", out.stdout)
        status = self.command("status", "backlog-b").stdout
        self.assertIn("owner=health", status)
        audit = self.command("audit").stdout
        self.assertIn("QUEUED\thealth\tbacklog-b/review", audit)
        self.assertIn("dispatch=sent", audit)

    def test_active_claim_is_refused(self):
        out = self.command("reassign", "backlog-a", "health", "shed", expect=2)
        self.assertIn("refusing to reassign active task", out.stderr)
        self.assertIn("owner=witness", self.command("status", "backlog-a").stdout)

    def test_non_coordinator_is_refused(self):
        out = self.command("reassign", "backlog-b", "health", "shed", actor="health", expect=2)
        self.assertIn("coordinator required", out.stderr)

    def test_offline_new_owner_is_refused(self):
        out = self.command("reassign", "backlog-b", "steward", "shed", expect=2)
        self.assertIn("staffs no live mind window", out.stderr)
        self.assertIn("owner=witness", self.command("status", "backlog-b").stdout)

    def test_shell_window_is_refused_as_new_owner(self):
        env_owner = self.env | {"MESH_TASK_LIVE_OWNERS": "witness health bash"}
        got = subprocess.run(["python3", str(TASK), "reassign", "backlog-b", "bash", "shed"],
                             env=env_owner, text=True, capture_output=True)
        self.assertEqual(got.returncode, 2)
        self.assertIn("staffs no live mind window", got.stderr)

    def test_same_owner_and_empty_reason_are_refused(self):
        out = self.command("reassign", "backlog-b", "witness", "shed", expect=2)
        self.assertIn("must differ", out.stderr)
        out = self.command("reassign", "backlog-b", "health", "  ", expect=2)
        self.assertIn("reason is required", out.stderr)


if __name__ == "__main__":
    unittest.main()
