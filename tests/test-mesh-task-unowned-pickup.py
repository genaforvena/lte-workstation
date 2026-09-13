#!/usr/bin/env python3
"""Any idle mind can see and claim open unowned work; first take wins."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"


class UnownedPickupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        fake = root / "bin"
        fake.mkdir()
        for name in ("chat", "handoff"):
            path = fake / name
            path.write_text("#!/bin/sh\nexit 0\n")
            path.chmod(0o755)
        self.env = os.environ | {
            "MESH_DIR": str(root / "mesh"),
            "MESH_TASK_DIR": str(root / "mesh" / "task-chains"),
            "MESH_TASK_CHAT_CMD": str(fake / "chat"),
            "MESH_TASK_HANDOFF_CMD": str(fake / "handoff"),
            "MESH_TASK_ACTOR": "witness",
        }
        self.plan = root / "plan.tsv"
        self.plan.write_text("-\twork\tunowned work anyone may claim\n")

    def tearDown(self):
        self.tmp.cleanup()

    def run_task(self, *args, actor=None, code=0):
        env = dict(self.env)
        if actor is not None:
            env["MESH_TASK_ACTOR"] = actor
        result = subprocess.run(["python3", str(TASK), *args], env=env,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout

    def test_owner_queues_expose_unowned_tasks_until_first_claim(self):
        self.run_task("create", "pool", str(self.plan))

        alice_queue = self.run_task("queue", "--dispatch", "--owner", "alice")
        bob_queue = self.run_task("queue", "--dispatch", "--owner", "bob")
        self.assertIn("pool/work", alice_queue)
        self.assertIn("pool/work", bob_queue)
        self.run_task("check", "dispatch", "pool/work", "alice")
        self.run_task("check", "dispatch", "pool/work", "bob")

        self.run_task("take", "pool", "work", actor="alice")
        audit = self.run_task("audit")
        self.assertIn("RUNNING\talice\tpool/work", audit)
        self.assertNotIn("pool/work", self.run_task("queue", "--dispatch", "--owner", "bob"))
        self.run_task("check", "dispatch", "pool/work", "bob", code=2)


if __name__ == "__main__":
    unittest.main()
