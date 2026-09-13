#!/usr/bin/env python3
"""Queue aging prevents starvation and favors blocker resolvers among peers."""
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"


class DispatchFairnessTests(unittest.TestCase):
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
            "MESH_TASK_QUEUE_AGING_SECONDS": "1",
            "MESH_TASK_CHAT_EVENTS": str(root / "chat-events.log"),
        }

    def tearDown(self):
        self.tmp.cleanup()

    def command(self, *args):
        result = subprocess.run(["python3", str(TASK), *args], env=self.env,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def create(self, chain, owner, slug, priority):
        plan = Path(self.tmp.name) / f"{chain.replace('/', '-')}.tsv"
        plan.write_text(f"{owner}\t{slug}\t{priority}\t{chain} {slug}\n")
        self.command("create", chain, str(plan))

    def test_age_beats_new_priority_and_audit_matches_dispatch_order(self):
        self.create("old", "alpha", "work", 0)
        time.sleep(1.1)  # task timestamps have one-second resolution
        self.create("new", "beta", "work", 100)

        rows = self.command("queue", "--dispatch").splitlines()
        ids = [row.split("\t")[1] for row in rows]
        self.assertEqual(ids, ["old/work", "new/work"], rows)
        audit_ids = [row.split("\t")[2] for row in self.command("audit").splitlines()]
        self.assertEqual(audit_ids, ids, "audit should show the dispatch frontier in the same order")

    def test_resolvers_lead_same_age_peers(self):
        self.env["MESH_TASK_QUEUE_AGING_SECONDS"] = "86400"
        self.create("ordinary", "alpha", "work", 0)
        self.create("unblock/gamma/dependency", "gamma", "resolve", 0)

        rows = self.command("queue", "--dispatch").splitlines()
        ids = [row.split("\t")[1] for row in rows]
        self.assertEqual(ids, [
            "unblock/gamma/dependency/resolve",
            "ordinary/work",
        ], rows)

    def test_redelivery_does_not_reset_a_task_queue_age(self):
        self.create("old", "alpha", "work", 0)
        time.sleep(1.1)
        self.create("new", "beta", "work", 0)

        self.env["MESH_TASK_ACTOR"] = "alpha"
        self.command("reschedule", "old")
        self.env["MESH_TASK_ACTOR"] = "witness"
        rows = self.command("queue", "--dispatch").splitlines()
        ids = [row.split("\t")[1] for row in rows]
        self.assertEqual(ids, ["old/work", "new/work"], rows)


if __name__ == "__main__":
    unittest.main()
