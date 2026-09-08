#!/usr/bin/env python3
"""Tasks remain in chat.log until done or explicitly reasoned-rejected."""
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
        self.assertIn("explicitly reject or complete", rejected.stderr)
        self.assertIn("no-expiry [active]", self.command("status", "no-expiry").stdout)

    def test_reject_requires_a_reason_and_is_the_only_non_done_terminal_path(self):
        rejected = self.command("reject", "no-expiry", "inspect", expect=2)
        self.assertIn("reject reason", rejected.stderr)
        self.command("reject", "no-expiry", "inspect", "superseded by operator decision")
        audit = self.command("audit").stdout
        self.assertIn("REJECTED\talpha\tno-expiry/inspect\treason=superseded by operator decision", audit)
        self.assertIn("no-expiry [rejected]", self.command("status", "no-expiry").stdout)

    def test_blocked_task_can_be_rejected_with_reason(self):
        self.command("block", "no-expiry", "inspect", "dependency", "missing input", "never")
        self.command("reject", "no-expiry", "inspect", "dependency will not be supplied")
        audit = self.command("audit").stdout
        self.assertIn("REJECTED\talpha\tno-expiry/inspect\treason=dependency will not be supplied", audit)

    def test_blocked_task_waits_in_queue_for_exact_prerequisite_then_redispatches(self):
        root = Path(self.tmp.name)
        prerequisite_plan = root / "prerequisite.tsv"
        prerequisite_plan.write_text("alpha\tunblock\tproduce the missing input\n")
        self.command("create", "prerequisite", str(prerequisite_plan))
        self.command("block", "no-expiry", "inspect", "dependency", "missing input", "after prerequisite/unblock")
        self.command("wait-for", "no-expiry", "inspect", "prerequisite/unblock")
        self.command("take", "prerequisite", "unblock")
        audit = self.command("audit").stdout
        self.assertIn("QUEUED\talpha\tno-expiry/inspect\twaiting_for=prerequisite/unblock", audit)
        artifact = root / "prerequisite.md"
        artifact.write_text("missing input produced\n")
        self.command("done", "prerequisite", "unblock", str(artifact))
        status = self.command("status", "no-expiry").stdout
        self.assertIn("no-expiry [open]", status)
        self.assertNotIn("waiting_for=", status)
        audit = self.command("audit").stdout
        self.assertIn("QUEUED\talpha\tno-expiry/inspect", audit)

    def test_audit_orders_dispatchable_incident_before_older_normal_task(self):
        root = Path(self.tmp.name)
        plan = root / "incident.tsv"
        plan.write_text("beta\tincident\turgent repair priority:incident\n")
        self.command("create", "newer-incident", str(plan))
        unfinished = [line for line in self.command("audit").stdout.splitlines()
                      if line.startswith(("QUEUED\t", "OPEN_UNOWNED\t", "RUNNING\t", "OVERDUE\t"))]
        self.assertTrue(unfinished[0].startswith("QUEUED\tbeta\tnewer-incident/incident"), unfinished)
        queue = self.command("queue", "--dispatch").stdout.splitlines()
        self.assertTrue(queue[0].startswith("beta\tnewer-incident/incident\t0\t"), queue)

    def test_numeric_priority_is_stored_and_queue_can_sort_explicitly(self):
        root = Path(self.tmp.name)
        plan = root / "priority.tsv"
        plan.write_text("beta\tlow\t10\tolder low\n")
        high = root / "high.tsv"
        high.write_text("alpha\thigh\t90\tyounger high\n")
        self.command("create", "prioritized", str(plan))
        self.command("create", "prioritized-high", str(high))
        state = self.command("replay", "--json").stdout
        self.assertIn('"priority": 90', state)
        queue = self.command("queue", "--sort", "priority").stdout.splitlines()
        self.assertTrue(queue[0].startswith("alpha\tprioritized-high/high\t90\t"), queue)
        self.assertTrue(queue[1].startswith("beta\tprioritized/low\t10\t"), queue)

    def test_default_dispatch_queue_uses_same_priority_order(self):
        root = Path(self.tmp.name)
        plan = root / "priority.tsv"
        plan.write_text("beta\tlow\t10\tolder low\n")
        high = root / "high.tsv"
        high.write_text("alpha\thigh\t90\tyounger high\n")
        self.command("create", "prioritized-default", str(plan))
        self.command("create", "prioritized-default-high", str(high))
        queue = self.command("queue", "--dispatch").stdout.splitlines()
        self.assertTrue(queue[0].startswith("alpha\tprioritized-default-high/high\t90\t"), queue)


if __name__ == "__main__":
    unittest.main()
