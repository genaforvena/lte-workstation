#!/usr/bin/env python3
"""Append log is the synthetic board/task/handoff status receipt."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/cleaner/mesh-cleaner-effect"


class Effects(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.state = Path(self.temp.name)
        self.key = hashlib.sha256(b"req/board").hexdigest()
        self.payload = self.state / "payload.json"
        self.payload.write_text(json.dumps({"version": 1, "owner": "cleaner", "marker": "fyi", "message": "synthetic receipt"}))

    def call(self, *args, fault=None):
        env = dict(os.environ)
        if fault:
            env["MESH_CLEANER_EFFECT_FAULT"] = fault
        return subprocess.run([sys.executable, str(SCRIPT), "--synthetic-state", str(self.state), *args],
                              text=True, capture_output=True, timeout=5, env=env)

    def append(self, fault=None):
        return self.call("--append", self.key, "--kind", "board", "--payload", str(self.payload), fault=fault)

    def test_sigkill_after_append_recovers_one_row(self):
        self.assertEqual(self.call("--status", self.key).returncode, 3)
        killed = self.append(fault="kill-after-append")
        self.assertEqual(killed.returncode, -9)
        self.assertEqual(json.loads(self.call("--status", self.key).stdout)["status"], "delivered")
        self.assertEqual(self.append().returncode, 0)
        self.assertEqual(len((self.state / "effects.log").read_text().splitlines()), 1)

    def test_conflicting_payload_and_partial_tail_hold(self):
        self.assertEqual(self.append().returncode, 0)
        self.payload.write_text(json.dumps({"version": 1, "owner": "cleaner", "marker": "fyi", "message": "different"}))
        self.assertEqual(self.append().returncode, 3)
        with (self.state / "effects.log").open("ab") as stream:
            stream.write(b"partial")
        self.assertEqual(self.call("--status", self.key).returncode, 3)
        self.assertEqual(self.append().returncode, 3)

    def test_exact_owner_task_and_handoff_grammar(self):
        task = {"version": 1, "owner": "cleaner", "task_id": "cleaner/req1", "status": "done",
                "artifact_sha256": "a" * 64}
        self.payload.write_text(json.dumps(task))
        self.assertEqual(self.call("--append", self.key, "--kind", "task", "--payload", str(self.payload)).returncode, 0)
        handoff_key = hashlib.sha256(b"req/handoff").hexdigest()
        self.payload.write_text(json.dumps({"version": 1, "owner": "cleaner", "invocation": "req1",
                                            "summary": "invocation:req1 synthetic done"}))
        self.assertEqual(self.call("--append", handoff_key, "--kind", "handoff", "--payload", str(self.payload)).returncode, 0)
        self.assertEqual(len((self.state / "effects.log").read_text().splitlines()), 2)


if __name__ == "__main__":
    unittest.main()
