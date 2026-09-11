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
            "MESH_TASK_ACTOR": "alpha",
            "MESH_TASK_CHAT_EVENTS": str(chat_log),
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

    def test_expired_health_warning_dispatch_is_held_but_genuine_open_is_preserved(self):
        root = Path(self.tmp.name)
        health_plan = root / "health-warning.tsv"
        health_plan.write_text("health\ttriage\thistorical bounded health warning\n")
        genuine_plan = root / "genuine.tsv"
        genuine_plan.write_text("alpha\tinspect\tgenuine open work\n")
        self.env["MESH_TASK_LEASE_SECONDS"] = "-1"
        self.command("create", "health-warning/expired", str(health_plan))
        self.command("create", "genuine-open", str(genuine_plan))
        self.env.pop("MESH_TASK_LEASE_SECONDS")
        audit = self.command("audit").stdout
        self.assertIn("HELD_EXPIRED\thealth\thealth-warning/expired/triage\tretry=next fresh health warning", audit)
        self.assertIn("OPEN_UNOWNED\talpha\tgenuine-open/inspect", audit)

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

    def test_blocked_task_is_visible_but_absent_from_dispatch_queue(self):
        self.command("block", "no-expiry", "inspect", "dependency", "missing input", "after input")
        audit = self.command("audit").stdout
        self.assertIn("BLOCKED\talpha\tno-expiry/inspect\tdependency\tafter input", audit)
        queue = self.command("queue", "--dispatch").stdout
        self.assertFalse(any(line.split("\t", 2)[1] == "no-expiry/inspect"
                             for line in queue.splitlines()))

    def test_block_materializes_one_deduplicated_owner_unblock_task(self):
        self.command("block", "no-expiry", "inspect", "dependency", "missing input", "after input")
        other_plan = Path(self.tmp.name) / "other.tsv"
        other_plan.write_text("alpha\tinspect\tinspect the same missing input\n")
        self.command("create", "other", str(other_plan))
        self.command("take", "other", "inspect")
        self.command("block", "other", "inspect", "dependency", "missing input", "after input")

        records = __import__("json").loads(self.command("replay", "--json").stdout)
        unblock = [record["data"] for record in records.values()
                   if record["data"].get("unblock_for") == "alpha|dependency|missing input|after input"]
        self.assertEqual(len(unblock), 1, records)
        self.assertEqual(unblock[0]["steps"][0]["owner"], "alpha")
        self.assertEqual(unblock[0]["steps"][0]["status"], "open")
        self.assertIn("no-expiry/inspect", unblock[0]["steps"][0]["description"])

    def test_unblock_sweep_is_idempotent_for_existing_auto_task(self):
        self.command("block", "no-expiry", "inspect", "dependency", "missing input", "after input")
        sweep = self.command("unblock-sweep", "alpha")
        self.assertIn("unblock-sweep owner=alpha created=0", sweep.stdout)

    def test_completed_resolver_resumes_parent_only_when_owner_marks_blocker_cleared(self):
        self.command("block", "no-expiry", "inspect", "dependency", "missing input", "after input")
        records = __import__("json").loads(self.command("replay", "--json").stdout)
        resolver = next(record["data"] for record in records.values()
                        if record["data"].get("unblock_for") ==
                        "alpha|dependency|missing input|after input")
        resolver_chain = resolver["chain"]
        self.command("take", resolver_chain, "resolve")
        artifact = Path(self.tmp.name) / "cleared.md"
        artifact.write_text("missing input is now available\n")
        settled = self.command("done", resolver_chain, "resolve", str(artifact),
                               "unblock=cleared event=dependency-arrived")
        self.assertIn("complete " + resolver_chain, settled.stdout)
        parent = self.command("status", "no-expiry").stdout
        self.assertIn("no-expiry [active]", parent)
        self.assertIn('"resume_event": "dependency-arrived"', self.command("replay", "--json").stdout)

    def test_completed_resolver_without_cleared_marker_leaves_parent_blocked(self):
        self.command("block", "no-expiry", "inspect", "dependency", "missing input", "after input")
        records = __import__("json").loads(self.command("replay", "--json").stdout)
        resolver = next(record["data"] for record in records.values()
                        if record["data"].get("unblock_for") ==
                        "alpha|dependency|missing input|after input")
        resolver_chain = resolver["chain"]
        self.command("take", resolver_chain, "resolve")
        artifact = Path(self.tmp.name) / "still-blocked.md"
        artifact.write_text("the dependency is still absent\n")
        self.command("done", resolver_chain, "resolve", str(artifact),
                     "unblock=blocked reason=dependency-still-absent")
        parent = self.command("status", "no-expiry").stdout
        self.assertIn("no-expiry [blocked]", parent)

    def test_operator_input_stays_parked_without_owner_resolver(self):
        self.command("block", "no-expiry", "inspect", "operator-input", "csv-path", "event:csv-arrives")
        records = __import__("json").loads(self.command("replay", "--json").stdout)
        self.assertFalse(any(record["data"].get("unblock_for") for record in records.values()), records)
        events = Path(self.env["MESH_TASK_CHAT_EVENTS"]).read_text()
        self.assertIn("event:csv-arrives", events)
        self.assertIn("parked", events)

    def test_external_event_stays_parked_without_owner_resolver(self):
        self.command("block", "no-expiry", "inspect", "external-event", "upstream webhook", "event:webhook")
        records = __import__("json").loads(self.command("replay", "--json").stdout)
        self.assertFalse(any(record["data"].get("unblock_for") for record in records.values()), records)
        events = Path(self.env["MESH_TASK_CHAT_EVENTS"]).read_text()
        self.assertIn("event:webhook", events)
        self.assertIn("parked", events)

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
