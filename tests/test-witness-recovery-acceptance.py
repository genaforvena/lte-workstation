#!/usr/bin/env python3
"""Independent recovery/replay and narrow-pane acceptance using isolated fixtures."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("no_expiry_fixture", ROOT / "tests/test-mesh-task-no-expiry.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class RecoveryAcceptance(fixture.TaskNoExpiryTests):
    def recovery_chain(self):
        self.command("reject", "no-expiry", "inspect", "fixture complete")
        root = Path(self.tmp.name)
        plan = root / "recovery.tsv"
        plan.write_text("alpha\thead\tverify prerequisite\nbeta\twork\tdownstream work\ngamma\tfinal\tindependent acceptance\n")
        self.command("create", "recovery", str(plan))
        self.command("take", "recovery", "head")
        self.command("reject", "recovery", "head", "verification failed")
        artifact = root / "recovery.md"
        artifact.write_text("Prerequisite reviewed; explicit owner disposition.\n")
        return artifact

    def test_recovery_replay_and_exact_owner(self):
        artifact = self.recovery_chain()
        self.command("recover", "recovery", "work", "reactivate", str(artifact), "reviewed", expect=2)
        self.env["MESH_TASK_ACTOR"] = "gamma"
        self.command("recover", "recovery", "final", "reactivate", str(artifact), "reviewed", expect=2)
        self.env["MESH_TASK_ACTOR"] = "beta"
        self.command("recover", "recovery", "work", "reactivate", str(artifact), "reviewed")
        before = self.command("replay", "--json").stdout
        self.command("recover", "recovery", "work", "reactivate", str(artifact), "reviewed")
        self.assertEqual(before, self.command("replay", "--json").stdout)
        records = json.loads(before)
        state = next(v["data"] for v in records.values() if v["data"]["chain"] == "recovery")
        self.assertEqual(state["current"], 1)
        self.assertEqual([s["status"] for s in state["steps"]], ["rejected", "open", "open"])
        self.env["MESH_TASK_ACTOR"] = "gamma"
        self.command("take", "recovery", "work", expect=2)
        self.env["MESH_TASK_ACTOR"] = "beta"
        self.command("take", "recovery", "work")
        self.command("done", "recovery", "work", str(artifact), "finished")
        self.assertIn("recovery/final [open] owner=gamma", self.command("status", "recovery").stdout)

    def test_hold_is_idempotent_and_never_dispatches(self):
        artifact = self.recovery_chain()
        self.env["MESH_TASK_ACTOR"] = "beta"
        self.command("recover", "recovery", "work", "hold", str(artifact), "verification unresolved")
        before = self.command("replay", "--json").stdout
        self.command("recover", "recovery", "work", "hold", str(artifact), "verification unresolved")
        self.assertEqual(before, self.command("replay", "--json").stdout)
        self.assertNotIn("recovery/work", self.command("queue", "--dispatch").stdout)
        self.command("take", "recovery", "work", expect=2)

    def test_narrow_pane_keeps_rejected_hold_visible(self):
        root = Path(self.tmp.name)
        mesh = root / ".mesh"
        mesh.mkdir()
        (mesh / "chat.log").write_text("".join(f"2026-09-09T00:00:00Z fixture :: raw-{i}\n" for i in range(20)))
        (mesh / "tasks.journal").write_text(
            "task_rows=1 unfinished_tasks=1 rejected_tasks=0 done_tasks=0\n"
            "HELD_REJECTED\tbeta\trecovery/work\tpredecessor=recovery/head\n")
        env = os.environ | {"HOME": str(root), "MESH_DIR": str(mesh),
                           "MESH_DASH_FAST": "1", "MESH_DASH_PANE_ROWS": "50",
                           "MESH_DASH_PANE_COLS": "80"}
        got = subprocess.run([str(ROOT / "scripts/mesh-dash"), "--once", "witness"],
                             env=env, text=True, capture_output=True, timeout=20)
        self.assertEqual(got.returncode, 0, got.stderr)
        self.assertIn("HELD_REJECTED\tbeta\trecovery/work", got.stdout)
        self.assertEqual(got.stdout.count("fixture :: raw-"), 20)


if __name__ == "__main__":
    unittest.main()
