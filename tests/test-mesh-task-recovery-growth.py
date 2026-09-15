#!/usr/bin/env python3
"""Recovery automation must not grow task chains without bound."""
import json
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"


class RecoveryGrowthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        fake = root / "bin"
        fake.mkdir()
        events = root / "chat-events.log"
        chat = fake / "chat"
        chat.write_text(f"#!/bin/sh\nprintf '%s\\n' \"$*\" >> {events}\n")
        chat.chmod(0o755)
        handoff = fake / "handoff"
        handoff.write_text("#!/bin/sh\nexit 0\n")
        handoff.chmod(0o755)
        self.root = root
        self.env = os.environ | {
            "MESH_DIR": str(root / "mesh"),
            "MESH_TASK_DIR": str(root / "mesh" / "task-chains"),
            "MESH_TASK_CHAT_CMD": str(chat),
            "MESH_TASK_HANDOFF_CMD": str(handoff),
            "MESH_TASK_ACTOR": "alpha",
            "MESH_TASK_LIVE_OWNERS": "alpha beta gamma",
        }

    def tearDown(self):
        self.tmp.cleanup()

    def command(self, *args, actor=None, expect=0):
        env = self.env | ({"MESH_TASK_ACTOR": actor} if actor else {})
        got = subprocess.run(["python3", str(TASK), *args], env=env,
                             text=True, capture_output=True)
        self.assertEqual(got.returncode, expect, got.stderr)
        return got

    def make_active(self, chain, actor="alpha"):
        plan = self.root / f"{chain.replace('/', '-')}.tsv"
        plan.write_text(f"{actor}\twork\tresolve the real prerequisite\n")
        self.command("create", chain, str(plan), actor=actor)
        self.command("take", chain, "work", actor=actor)

    def resolvers(self):
        records = json.loads(self.command("replay", "--json").stdout)
        return [row["data"] for row in records.values()
                if row["data"].get("chain", "").startswith("unblock/")]

    def seed_blocked_parent_with_attempts(self, attempt_statuses):
        sys.path.insert(0, str(ROOT / "scripts"))
        from mesh_task_log import encode
        blocked_at = "2026-09-11T00:00:00Z"
        identity = hashlib.sha256(
            "alpha|parent|parent/work|1|2026-09-11T00:00:00Z|dependency|input|event:ready".encode()
        ).hexdigest()[:32]
        parent = {
            "version": 2, "chain": "parent", "ask": None, "created": blocked_at,
            "status": "blocked", "current": 0,
            "steps": [{"id": "parent/work", "owner": "alpha", "slug": "work",
                       "description": "resolve prerequisite", "priority": 0, "status": "blocked",
                       "blocked": blocked_at, "block_epoch": 1, "parent_chain": "parent",
                       "blocker_type": "dependency", "needs": "input", "retry": "event:ready"}],
        }
        states = [parent]
        for attempt, state_status in enumerate(attempt_statuses, 1):
            chain = f"unblock/alpha/attempt{attempt}"
            finished = f"2026-09-11T00:0{attempt}:00Z"
            step = {"id": f"{chain}/resolve", "owner": "alpha", "slug": "resolve",
                    "description": "previous unresolved attempt", "priority": 90,
                    "status": "done" if state_status == "complete" else state_status}
            if state_status == "complete":
                step.update(finished=finished, artifact="/tmp/evidence.md",
                            result="unblock=blocked reason=dependency-still-absent")
            states.append({
                "version": 2, "chain": chain, "ask": None, "created": finished,
                "status": state_status, "current": 0, "dispatch": "sent",
                "unblock_for": identity, "unblock_parent": "parent", "unblock_step": "parent/work",
                "unblock_attempt": attempt, "steps": [step],
            })
        mesh = Path(self.env["MESH_DIR"])
        mesh.mkdir(parents=True, exist_ok=True)
        (mesh / "chat.log").write_text("\n".join(
            f"2026-09-11T00:00:00Z  fixture  ::  {encode(state, 1)}" for state in states
        ) + "\n")

    def test_recovery_depth_is_bounded_after_one_cross_mind_hop(self):
        self.make_active("parent")
        self.command("block", "parent", "work", "dependency", "input", "event:ready")
        first = self.resolvers()[0]
        self.command("take", first["chain"], "resolve", actor="alpha")
        self.command("block", first["chain"], "resolve", "dependency", "backend", "event:backend")
        second = next(r for r in self.resolvers() if r["chain"] != first["chain"])
        self.assertEqual(second["steps"][0]["owner"], "beta")

        self.command("take", second["chain"], "resolve", actor="beta")
        self.command("block", second["chain"], "resolve", "dependency", "runner", "event:runner",
                     actor="beta")
        self.command("unblock-sweep", actor="witness")
        resolvers = self.resolvers()
        self.assertEqual(len(resolvers), 2, resolvers)
        self.assertIn(f"{second['chain']} [blocked]", self.command("status", second["chain"]).stdout)
        self.assertIn("recovery-depth-cap=2", (self.root / "chat-events.log").read_text())

    def test_sweep_does_not_duplicate_while_a_resolver_is_open(self):
        self.seed_blocked_parent_with_attempts(["complete", "open", "open"])
        swept = self.command("unblock-sweep", actor="witness")
        self.assertIn("unblock-sweep owner=all created=0", swept.stdout)
        resolvers = self.resolvers()
        self.assertEqual(max(int(r.get("unblock_attempt", 1)) for r in resolvers), 3)
        self.assertEqual(len(resolvers), 3, resolvers)
        self.assertIn("parent [blocked]", self.command("status", "parent").stdout)

    def test_automatic_attempts_stop_after_three_unresolved_results(self):
        self.seed_blocked_parent_with_attempts(["complete", "complete", "complete"])
        swept = self.command("unblock-sweep", actor="witness")
        self.assertIn("unblock-sweep owner=all created=0", swept.stdout)
        self.assertIn("automatic resolver attempts exhausted at 3",
                      (self.root / "chat-events.log").read_text())
        self.assertEqual(len(self.resolvers()), 3)
        self.assertIn("parent [blocked]", self.command("status", "parent").stdout)


if __name__ == "__main__":
    unittest.main()
