#!/usr/bin/env python3
"""Cleaner generated-file action identity and crash reconciliation."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/cleaner/mesh-cleaner-action"


class CleanerAction(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.root = base / "repo"
        self.state = base / "state"
        (self.root / ".firecrawl").mkdir(parents=True)
        self.state.mkdir()
        self.source = self.root / ".firecrawl/old.json"
        self.source.write_text('{"generated":true}\n')
        old = time.time() - 7200
        os.utime(self.source, (old, old))
        st = self.source.stat()
        self.row = {"path": ".firecrawl/old.json", "reasons": ["disposable-generated"],
                    "device_inode": f"{st.st_dev}:{st.st_ino}",
                    "mtime_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(st.st_mtime)),
                    "active_refs": [], "owner_refs": [], "task_refs": []}
        self.manifest = base / "manifest.json"
        self.manifest.write_text(json.dumps({"version": 1, "scan_id": "2026-09-23T13:45:02Z",
                                             "candidates": [self.row]}))
        identity = ["2026-09-23T13:45:02Z", self.row["path"], self.row["device_inode"], self.row["mtime_utc"]]
        self.key = hashlib.sha256(json.dumps(identity, separators=(",", ":")).encode()).hexdigest()

    def call(self, *args, fault=None):
        env = dict(os.environ)
        if fault:
            env["MESH_CLEANER_ACTION_FAULT"] = fault
        return subprocess.run([sys.executable, str(SCRIPT), "--synthetic-root", str(self.root),
                               "--state-dir", str(self.state), *args], env=env,
                              text=True, capture_output=True, timeout=5)

    def apply(self, fault=None):
        return self.call("--quarantine", self.key, "--manifest", str(self.manifest),
                         "--path", self.row["path"], fault=fault)

    def test_receipt_reconciles_after_move_and_repeated_key(self):
        self.assertEqual(self.call("--status", self.key).returncode, 3)
        first = self.apply(fault="after-move")
        self.assertEqual(first.returncode, 3)
        self.assertFalse(self.source.exists())
        status = self.call("--status", self.key)
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertEqual(json.loads(status.stdout)["status"], "delivered")
        repeated = self.apply()
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(len(list((self.state / "quarantine").rglob("old.json"))), 1)

    def test_plan_crash_retries_only_unchanged_source(self):
        self.assertEqual(self.apply(fault="after-plan").returncode, 3)
        status = self.call("--status", self.key)
        self.assertEqual(status.returncode, 3)
        self.assertEqual(json.loads(status.stdout)["status"], "pending")
        self.assertEqual(self.apply().returncode, 0)
        self.assertEqual(self.call("--status", self.key).returncode, 0)

    def test_changed_source_holds(self):
        self.assertEqual(self.apply(fault="after-plan").returncode, 3)
        self.source.write_text("changed")
        self.assertEqual(self.apply().returncode, 3)
        self.assertTrue(self.source.exists())
        self.assertEqual(json.loads(self.call("--status", self.key).stdout)["status"], "unknown")

    def test_two_locations_hold_without_second_move(self):
        self.assertEqual(self.apply(fault="after-plan").returncode, 3)
        dest = self.state / "quarantine" / self.key / ".firecrawl/old.json"
        dest.parent.mkdir(parents=True)
        dest.write_bytes(self.source.read_bytes())
        self.assertEqual(json.loads(self.call("--status", self.key).stdout)["status"], "unknown")
        self.assertEqual(self.apply().returncode, 3)
        self.assertTrue(self.source.exists())
        self.assertTrue(dest.exists())

    def test_scope_and_owner_guards(self):
        self.row["active_refs"] = ["open-by-mind"]
        self.manifest.write_text(json.dumps({"version": 1, "scan_id": "2026-09-23T13:45:02Z",
                                             "candidates": [self.row]}))
        self.assertEqual(self.apply().returncode, 3)
        self.assertTrue(self.source.exists())
        self.row["active_refs"] = []
        self.row["path"] = "scripts/protected.json"
        self.manifest.write_text(json.dumps({"version": 1, "scan_id": "2026-09-23T13:45:02Z",
                                             "candidates": [self.row]}))
        protected_identity = ["2026-09-23T13:45:02Z", self.row["path"], self.row["device_inode"], self.row["mtime_utc"]]
        protected_key = hashlib.sha256(json.dumps(protected_identity, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(self.call("--quarantine", protected_key, "--manifest", str(self.manifest),
                                   "--path", self.row["path"]).returncode, 3)


if __name__ == "__main__":
    unittest.main()
