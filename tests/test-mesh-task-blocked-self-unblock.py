#!/usr/bin/env python3
"""Regression coverage for actionable, exact-owner blocked-task recovery."""
import json
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"


class BlockedSelfUnblockTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        fake = root / "bin"
        fake.mkdir()
        self.events = root / "chat-events.log"
        chat = fake / "chat"
        chat.write_text(f"#!/bin/sh\nprintf '%s\\n' \"$*\" >> {self.events}\n")
        chat.chmod(0o755)
        handoff = fake / "handoff"
        handoff.write_text("#!/bin/sh\nexit 0\n")
        handoff.chmod(0o755)
        self.env = os.environ | {
            "MESH_DIR": str(root / "mesh"),
            "MESH_TASK_DIR": str(root / "mesh" / "task-chains"),
            "MESH_TASK_CHAT_CMD": str(chat),
            "MESH_TASK_HANDOFF_CMD": str(handoff),
            "MESH_TASK_ACTOR": "alpha",
            "MESH_TASK_LIVE_OWNERS": "alpha beta",
        }

    def tearDown(self):
        self.tmp.cleanup()

    def command(self, *args, actor=None, expect=0):
        env = self.env | ({"MESH_TASK_ACTOR": actor} if actor else {})
        got = subprocess.run(["python3", str(TASK), *args], env=env,
                             text=True, capture_output=True)
        self.assertEqual(got.returncode, expect, got.stderr)
        return got

    def make_active(self, chain, owner="alpha", ref="inspect"):
        plan = Path(self.tmp.name) / f"{chain.replace('/', '-')}.tsv"
        plan.write_text(f"{owner}\t{ref}\t{chain} work\n")
        self.command("create", chain, str(plan), actor=owner)
        self.command("take", chain, ref, actor=owner)

    def test_created_tasks_require_prerequisite_recovery_before_rejection(self):
        plan = Path(self.tmp.name) / "autonomous.tsv"
        plan.write_text("alpha\tinspect\tDo the work\n")
        self.command("create", "autonomous", str(plan), actor="alpha")
        description = self.records()["autonomous"]["data"]["steps"][0]["description"]
        self.assertIn("missing-prerequisite recovery:", description)
        self.assertIn("reuse an exact active prerequisite task or create and link one", description)
        self.assertIn("Reject only invalid, duplicate, out-of-scope, or unsafe work", description)

    def records(self):
        return json.loads(self.command("replay", "--json").stdout)

    def seed_ledger(self, *states):
        sys.path.insert(0, str(ROOT / "scripts"))
        from mesh_task_log import encode
        log = Path(self.env["MESH_DIR"]) / "chat.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        lines = []
        for state in states:
            lines.append("2026-09-11T00:00:00Z  fixture  ::  " + encode(state, 1))
        log.write_text("\n".join(lines) + "\n")

    def resolvers(self):
        return [r["data"] for r in self.records().values()
                if r["data"].get("chain", "").startswith("unblock/")]

    def test_every_blocker_class_materializes_one_owner_resolver(self):
        for kind in ("operator-input", "external-event"):
            chain = f"parked-{kind}"
            self.make_active(chain)
            self.command("block", chain, "inspect", kind, "the-input", "event:ready", actor="alpha")
        resolvers = self.resolvers()
        self.assertEqual(len(resolvers), 2)
        self.assertEqual({r["steps"][0]["owner"] for r in resolvers}, {"alpha"})
        self.assertTrue(all("narrowest safe in-scope" in r["steps"][0]["description"]
                            for r in resolvers))

    def test_operator_input_assumes_consent_and_derives_exact_action_packet(self):
        self.make_active("operator-input-policy")
        self.command("block", "operator-input-policy", "inspect", "operator-input",
                     "the-input", "event:ready", actor="alpha")
        resolver = self.resolvers()[0]["steps"][0]["description"]
        self.assertIn("Operator agreement is assumed", resolver)
        self.assertIn("do not ask for permission", resolver)
        self.assertIn("operator-action packet", resolver)
        self.assertIn("never on approval", resolver)

    def test_operator_directed_external_event_also_assumes_consent(self):
        self.make_active("operator-event-policy")
        self.command("block", "operator-event-policy", "inspect", "external-event",
                     "operator decision and supported recovery path", "operator decision", actor="alpha")
        resolver = self.resolvers()[0]["steps"][0]["description"]
        self.assertIn("Operator agreement is assumed", resolver)
        self.assertIn("operator-action packet", resolver)

    def test_same_text_on_two_parents_has_two_epochs(self):
        for chain in ("first", "second"):
            self.make_active(chain)
            self.command("block", chain, "inspect", "dependency", "same", "event:ready", actor="alpha")
        resolvers = self.resolvers()
        self.assertEqual(len(resolvers), 2)
        self.assertEqual(len({r["unblock_for"] for r in resolvers}), 2)

    def test_legacy_terminal_resolver_does_not_strand_new_block_epoch(self):
        self.make_active("epoch")
        self.command("block", "epoch", "inspect", "dependency", "same", "event:ready", actor="alpha")
        old = self.resolvers()[0]["chain"]
        self.command("take", old, "resolve", actor="alpha")
        artifact = TASK
        self.command("done", old, "resolve", str(artifact), "unblock=blocked reason=still absent", actor="alpha")
        self.command("resume", "epoch", "inspect", "retry:manual", actor="alpha")
        self.command("block", "epoch", "inspect", "dependency", "same", "event:ready", actor="alpha")
        self.assertEqual(len(self.resolvers()), 2)

    def test_sweep_without_owner_discovers_all_blocked_owners_and_is_idempotent(self):
        for chain, owner in (("alpha-chain", "alpha"), ("beta-chain", "beta")):
            self.make_active(chain, owner=owner)
            self.command("block", chain, "inspect", "dependency", "input", "event:ready", actor=owner)
        self.command("unblock-sweep", actor="witness")
        before = len(self.resolvers())
        self.command("unblock-sweep", actor="witness")
        self.assertEqual(len(self.resolvers()), before)

    def test_exact_owner_can_take_unblock_resolver_while_other_work_is_active(self):
        self.make_active("blocked")
        self.command("block", "blocked", "inspect", "dependency", "input", "event:ready", actor="alpha")
        self.make_active("busy")
        resolver = self.resolvers()[0]["chain"]
        self.command("take", resolver, "resolve", actor="alpha")
        self.assertIn("resolve [active]", self.command("status", resolver).stdout)

    def test_blocked_resolver_gets_cross_mind_recovery_and_exact_resume(self):
        self.make_active("blocked")
        self.command("block", "blocked", "inspect", "dependency", "input", "event:ready", actor="alpha")
        resolver = self.resolvers()[0]["chain"]
        self.command("take", resolver, "resolve", actor="alpha")
        self.command("block", resolver, "resolve", "dependency", "backend", "event:backend-ready", actor="alpha")

        nested = [r for r in self.resolvers() if r["chain"] != resolver]
        self.assertEqual(len(nested), 1)
        self.assertEqual(nested[0]["steps"][0]["owner"], "beta")
        self.assertEqual(nested[0]["unblock_parent"], resolver)

        nested_chain = nested[0]["chain"]
        self.command("take", nested_chain, "resolve", actor="beta")
        artifact = TASK
        self.command("done", nested_chain, "resolve", str(artifact),
                     "unblock=cleared event=backend-ready", actor="beta")
        self.assertIn("resolve [active]", self.command("status", resolver).stdout)
        self.assertIn("blocked [blocked]", self.command("status", "blocked").stdout)

    def test_sweep_backfills_recovery_for_legacy_blocked_resolver(self):
        resolver = "unblock/alpha/legacy-resolver"
        self.seed_ledger({
            "version": 2, "chain": resolver, "ask": None,
            "created": "2026-09-11T00:00:00Z", "status": "blocked", "current": 0,
            "unblock_for": "alpha|dependency|backend|event:backend-ready",
            "unblock_parent": "blocked-parent",
            "unblock_step": "blocked-parent/work",
            "steps": [{"id": f"{resolver}/resolve", "owner": "alpha", "slug": "resolve",
                        "description": "legacy resolver", "priority": 90, "status": "blocked",
                        "blocked": "2026-09-11T00:00:01Z", "block_epoch": 1,
                        "blocker_type": "dependency", "needs": "backend",
                        "retry": "event:backend-ready"}]
        })
        self.command("unblock-sweep", actor="witness")
        self.assertEqual(len([r for r in self.resolvers() if r.get("unblock_parent") == resolver]), 1)

    def test_sweep_retries_after_resolver_reports_unresolved_blocker(self):
        self.make_active("blocked")
        self.command("block", "blocked", "inspect", "dependency", "input", "event:ready", actor="alpha")
        resolver = self.resolvers()[0]["chain"]
        self.command("take", resolver, "resolve", actor="alpha")
        self.command("block", resolver, "resolve", "dependency", "backend", "event:backend-ready", actor="alpha")
        nested = next(r for r in self.resolvers() if r["chain"] != resolver)
        self.command("take", nested["chain"], "resolve", actor="beta")
        artifact = TASK
        self.command("done", nested["chain"], "resolve", str(artifact),
                     "unblock=blocked reason=full backend still absent", actor="beta")

        self.command("unblock-sweep", actor="witness")
        retries = [r for r in self.resolvers() if r.get("unblock_parent") == resolver]
        self.assertEqual(len(retries), 2)
        self.assertEqual(sum(r["status"] == "open" for r in retries), 1)
        self.assertEqual(max(r.get("unblock_attempt", 1) for r in retries), 2)

    def test_sweep_backoffs_repeated_unresolved_retry_without_new_evidence(self):
        self.make_active("blocked")
        self.command("block", "blocked", "inspect", "dependency", "input", "event:ready", actor="alpha")
        resolver = self.resolvers()[0]["chain"]
        self.command("take", resolver, "resolve", actor="alpha")
        self.command("block", resolver, "resolve", "dependency", "backend", "event:backend-ready", actor="alpha")
        nested = next(r for r in self.resolvers() if r["chain"] != resolver)
        self.command("take", nested["chain"], "resolve", actor="beta")
        artifact = TASK
        self.command("done", nested["chain"], "resolve", str(artifact),
                     "unblock=blocked reason=backend still absent", actor="beta")
        self.command("unblock-sweep", actor="witness")
        retry = next(r for r in self.resolvers()
                     if r.get("unblock_parent") == resolver and r["chain"] != nested["chain"])
        self.command("take", retry["chain"], "resolve", actor="beta")
        self.command("done", retry["chain"], "resolve", str(artifact),
                     "unblock=blocked reason=backend still absent", actor="beta")
        self.command("unblock-sweep", actor="witness")
        retries = [r for r in self.resolvers() if r.get("unblock_parent") == resolver]
        self.assertEqual(len(retries), 2)

    def test_sweep_migrates_legacy_blocked_parent_with_terminal_old_resolver(self):
        parent = {"version": 2, "chain": "legacy", "ask": None,
                  "created": "2026-09-11T00:00:00Z", "status": "blocked", "current": 0,
                  "steps": [{"id": "legacy/inspect", "owner": "alpha", "slug": "inspect",
                             "description": "legacy", "priority": 0, "status": "blocked",
                             "blocked": "2026-09-11T00:00:01Z", "blocker_type": "dependency",
                             "needs": "same", "retry": "event:ready"}]}
        old = {"version": 2, "chain": "unblock/alpha/legacyold", "ask": None,
               "created": "2026-09-11T00:00:02Z", "status": "complete", "current": 0,
               "unblock_for": "alpha|dependency|same|event:ready",
               "steps": [{"id": "unblock/alpha/legacyold/resolve", "owner": "alpha",
                          "slug": "resolve", "description": "old", "priority": 90,
                          "status": "done", "artifact": "/tmp/old", "artifact_sha256": "x",
                          "result": "unblock=blocked"}]}
        self.seed_ledger(parent, old)
        self.command("unblock-sweep", actor="witness")
        fresh = [r for r in self.resolvers() if r["chain"] != old["chain"]]
        self.assertEqual(len(fresh), 1)

    def test_recent_missing_prerequisite_rejection_gets_one_owner_recovery_task(self):
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parent = {"version": 2, "chain": "haunt-analysis", "ask": None,
                  "created": stamp, "status": "rejected", "current": 0,
                  "steps": [{"id": "haunt-analysis/compare", "owner": "alpha", "slug": "compare",
                             "description": "Run comparison", "priority": 0, "status": "rejected",
                             "rejected": stamp,
                             "rejected_reason": "Rejected as premature: behavioral preflight missing; registration not approved"}]}
        self.seed_ledger(parent)
        self.command("unblock-sweep", actor="witness")
        recovery = self.resolvers()
        self.assertEqual(len(recovery), 1)
        step = recovery[0]["steps"][0]
        self.assertEqual(step["owner"], "alpha")
        self.assertIn("rejected", step["description"].lower())
        self.assertIn("find exact active work or create", step["description"].lower())
        self.assertIn("implement", step["description"].lower())
        self.assertIn("create a fresh exact-owner task", step["description"].lower())
        self.assertIn("do not use mesh-task recover on the rejected step", step["description"].lower())
        self.command("unblock-sweep", actor="witness")
        self.assertEqual(len(self.resolvers()), 1)

    def test_old_or_non_prerequisite_rejection_does_not_spawn_recovery(self):
        old = {"version": 2, "chain": "old-rejection", "ask": None,
               "created": "2026-09-01T00:00:00Z", "status": "rejected", "current": 0,
               "steps": [{"id": "old-rejection/step", "owner": "alpha", "slug": "step",
                          "description": "Run", "priority": 0, "status": "rejected",
                          "rejected": "2026-09-01T00:00:00Z", "rejected_reason": "duplicate"}]}
        self.seed_ledger(old)
        self.command("unblock-sweep", actor="witness")
        self.assertEqual(self.resolvers(), [])

    def test_legacy_terminal_row_does_not_render_stale_blocker_metadata(self):
        terminal = {"version": 2, "chain": "legacy-terminal", "ask": None,
                    "created": "2026-09-11T00:00:00Z", "status": "complete", "current": 0,
                    "steps": [{"id": "legacy-terminal/inspect", "owner": "alpha", "slug": "inspect",
                               "description": "legacy", "priority": 0, "status": "done",
                               "blocked": "2026-09-11T00:00:01Z", "blocker_type": "external-event",
                               "needs": "webhook", "retry": "event:ready", "artifact": "/tmp/x",
                               "artifact_sha256": "x", "result": "complete"}]}
        self.seed_ledger(terminal)
        status = self.command("status", "legacy-terminal").stdout
        self.assertNotIn("blocker=", status)
        self.assertNotIn("retry=", status)

    def test_cleared_resolver_resumes_only_its_exact_parent(self):
        for chain in ("left", "right"):
            self.make_active(chain)
            self.command("block", chain, "inspect", "dependency", "same", "event:ready", actor="alpha")
        left = next(r for r in self.resolvers() if "left/inspect" in r["steps"][0]["description"])
        self.command("take", left["chain"], "resolve", actor="alpha")
        artifact = TASK
        self.command("done", left["chain"], "resolve", str(artifact),
                     "unblock=cleared event=left-ready", actor="alpha")
        self.assertIn("left [active]", self.command("status", "left").stdout)
        self.assertIn("right [blocked]", self.command("status", "right").stdout)

    def test_resume_clears_blocker_metadata_from_active_row(self):
        self.make_active("metadata")
        self.command("block", "metadata", "inspect", "external-event", "webhook", "event:ready", actor="alpha")
        self.command("resume", "metadata", "inspect", "ready", actor="alpha")
        status = self.command("status", "metadata").stdout
        self.assertIn("metadata [active]", status)
        self.assertNotIn("blocker=", status)
        self.assertNotIn("retry=", status)

    def test_terminal_row_does_not_render_historical_blocker_metadata(self):
        self.make_active("terminal")
        self.command("block", "terminal", "inspect", "external-event", "webhook", "event:ready", actor="alpha")
        self.command("resume", "terminal", "inspect", "ready", actor="alpha")
        artifact = TASK
        self.command("done", "terminal", "inspect", str(artifact), "complete", actor="alpha")
        status = self.command("status", "terminal").stdout
        self.assertIn("terminal [complete]", status)
        self.assertNotIn("blocker=", status)
        self.assertNotIn("retry=", status)


if __name__ == "__main__":
    unittest.main()
