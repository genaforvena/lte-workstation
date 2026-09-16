#!/usr/bin/env python3
"""Artifact paths that moved out of the genome tree still settle.

Receipts, audits, chat-range reviews and plan files became node-local evidence on 2026-09-16
(docs/EVIDENCE-MOVED.md, mesh-evidence-dir). Ledger rows are NOT rewritten, so a row — or a mind
copying a path out of one — keeps the old spelling, naming a file that really exists under the
node's root. Before this change `done` refused it with "artifact does not exist", i.e. a real
artifact read as missing evidence.

Each claim here is driven through the CLI, not the helper: the point is that the three verb sites
(settle/progress/recover) resolve, and that a genuinely absent path is STILL refused — widening the
guard to accept anything would make `done` meaningless.
"""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# MESH_TASK_TEST_BIN lets this suite be driven against a pre-change copy to prove it is red for the
# right reason (the same defect the fix addresses), rather than passing vacuously.
TASK = Path(os.environ.get("MESH_TASK_TEST_BIN", str(ROOT / "scripts" / "mesh-task")))


class NodeLocalArtifactPathTests(unittest.TestCase):
    def setUp(self):
        # NOT under /tmp: reject_ephemeral_artifact_path() refuses a settled artifact under /tmp,
        # /dev/shm or TMPDIR — correctly, since a done receipt must outlive the temp dir that made it.
        # A fixture inside /tmp would be refused for that unrelated reason and prove nothing.
        cache = Path.home() / ".cache"
        cache.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="mesh-task-node-local-", dir=str(cache))
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
        self.mesh = root / "mesh"
        self.evidence = self.mesh / "evidence" / "receipts"
        self.evidence.mkdir(parents=True)
        self.env = os.environ | {
            "MESH_DIR": str(self.mesh),
            # node_local_roots() prefers the explicit roots over MESH_DIR (same
            # precedence as mesh-evidence-dir), so the fixture must pin them too:
            # without this the node's real MESH_EVIDENCE_ROOT leaks in and the
            # legacy spelling resolves outside the fixture.
            "MESH_EVIDENCE_ROOT": str(self.mesh / "evidence"),
            "MESH_PLANS_DIR": str(self.mesh / "plans"),
            "MESH_TASK_DIR": str(self.mesh / "task-chains"),
            "MESH_TASK_CHAT_CMD": str(fake / "chat"),
            "MESH_TASK_HANDOFF_CMD": str(fake / "handoff"),
            "MESH_TASK_ACTOR": "alpha",
            "MESH_TASK_CHAT_EVENTS": str(chat_log),
        }
        plan = root / "plan.tsv"
        plan.write_text("alpha\tinspect\tinspect the durable state\n")
        self.command("create", "node-local", str(plan))
        self.command("take", "node-local", "inspect")

    def tearDown(self):
        self.tmp.cleanup()

    def step_record(self):
        """The chain's first step. The file is the canonical record, whatever wrapper it uses."""
        record = json.loads((self.mesh / "task-chains" / "node-local.json").read_text())
        data = record.get("data") if isinstance(record, dict) else None
        return (data or record)["steps"][0]

    def command(self, *args, expect=0):
        got = subprocess.run(["python3", str(TASK), *args], env=self.env,
                             text=True, capture_output=True)
        self.assertEqual(got.returncode, expect, got.stderr)
        return got

    def test_legacy_receipt_spelling_settles_onto_the_node_local_copy(self):
        real = self.evidence / "legacy-receipt.md"
        real.write_text("verified evidence\n")
        self.command("done", "node-local", "inspect", "docs/task-receipts/legacy-receipt.md")
        step = self.step_record()
        # the row stores where the file IS, so its own digest check stays meaningful
        self.assertEqual(step["artifact"], str(real))
        self.assertTrue(step.get("artifact_sha256"), "settled step must carry a digest")

    def test_progress_with_a_legacy_spelling_renews_instead_of_refusing(self):
        real = self.evidence / "progress-receipt.md"
        real.write_text("progress evidence\n")
        self.command("progress", "node-local", "inspect", "docs/task-receipts/progress-receipt.md",
                     "keep going", "2030-01-01T00:00:00Z")
        self.assertEqual(self.step_record()["progress_artifact"], str(real))

    def test_legacy_artifacts_spelling_settles_onto_the_node_local_copy(self):
        # same class as the receipts arm: the `artifacts/` corpus also left the tree on 2026-09-16,
        # and a row settled before the sweep named the in-repo spelling.
        real = self.mesh / "evidence" / "artifacts" / "legacy-artifact.md"
        real.parent.mkdir(parents=True, exist_ok=True)
        real.write_text("legacy artifact\n")
        self.command("done", "node-local", "inspect", "artifacts/legacy-artifact.md")
        self.assertEqual(self.step_record()["artifact"], str(real))

    def test_a_genuinely_missing_artifact_is_still_refused(self):
        got = self.command("done", "node-local", "inspect", "docs/task-receipts/never-written.md",
                           expect=2)
        self.assertIn("artifact does not exist", got.stderr)
        self.assertNotEqual(self.step_record()["status"], "done",
                            "a refused settle must not mark the step done")


if __name__ == "__main__":
    unittest.main(verbosity=2)
