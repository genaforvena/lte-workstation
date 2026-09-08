#!/usr/bin/env python3
"""Tasks remain in chat.log until done or explicitly reasoned-ignored."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"


class TaskNoExpiryTests(unittest.TestCase):
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
            "MESH_TASK_ACTOR": "alpha",
        }
        plan = root / "plan.tsv"
        plan.write_text("alpha\tinspect\tinspect the durable state\n")
        self.command("create", "no-expiry", str(plan))
        self.env["MESH_TASK_LEASE_SECONDS"] = "-1"
        self.command("take", "no-expiry", "inspect")
        self.env.pop("MESH_TASK_LEASE_SECONDS")

    def tearDown(self):
        self.tmp.cleanup()

    def command(self, *args, expect=0):
        got = subprocess.run(["python3", str(TASK), *args], env=self.env,
                             text=True, capture_output=True)
        self.assertEqual(got.returncode, expect, got.stderr)
        return got

    def test_expired_lease_is_overdue_not_a_reassignment_or_closure(self):
        audit = self.command("audit").stdout
        self.assertIn("OVERDUE\talpha\tno-expiry/inspect", audit)
        self.assertNotIn("EXPIRED\t", audit)
        rejected = self.command("reschedule", "no-expiry", expect=2)
        self.assertIn("explicitly block, ignore, or complete", rejected.stderr)
        self.assertIn("no-expiry [active]", self.command("status", "no-expiry").stdout)

    def test_ignore_requires_a_reason_and_is_the_only_non_done_terminal_path(self):
        rejected = self.command("ignore", "no-expiry", "inspect", expect=2)
        self.assertIn("ignore reason", rejected.stderr)
        self.command("ignore", "no-expiry", "inspect", "superseded by operator decision")
        audit = self.command("audit").stdout
        self.assertIn("IGNORED\talpha\tno-expiry/inspect\treason=superseded by operator decision", audit)
        self.assertIn("no-expiry [ignored]", self.command("status", "no-expiry").stdout)


if __name__ == "__main__":
    unittest.main()
