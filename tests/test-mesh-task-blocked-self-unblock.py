#!/usr/bin/env python3
"""Regression coverage for actionable, exact-owner blocked-task recovery."""
import json
import os
import subprocess
import tempfile
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
        artifact = Path(self.tmp.name) / "old.md"
        artifact.write_text("old resolver did not clear the parent\n")
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
        artifact = Path(self.tmp.name) / "clear.md"
        artifact.write_text("left only\n")
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
        artifact = Path(self.tmp.name) / "terminal.md"
        artifact.write_text("terminal evidence\n")
        self.command("done", "terminal", "inspect", str(artifact), "complete", actor="alpha")
        status = self.command("status", "terminal").stdout
        self.assertIn("terminal [complete]", status)
        self.assertNotIn("blocker=", status)
        self.assertNotIn("retry=", status)


if __name__ == "__main__":
    unittest.main()
