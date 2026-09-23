#!/usr/bin/env python3
"""Closed-window parity compares IDs, not approximate timestamps or private text."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
START = "2026-09-23T04:00:00Z"
END = "2026-09-23T04:02:00Z"


class ClosedParityTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.legacy = self.base / "legacy.jsonl"
        self.projected = self.base / "projected.jsonl"

    def write(self, legacy, projected):
        for path, rows in ((self.legacy, legacy), (self.projected, projected)):
            path.write_text("".join(json.dumps(row) + "\n" for row in rows))

    def event(self, identity, at, kind="pane", **extra):
        return {"channel": "tg", "event_id": identity * 32, "kind": kind, "at": at, **extra}

    def check(self):
        return subprocess.run([str(ROOT / "scripts/mesh-mishe-parity"), "--channel", "tg",
                               "--closed-window", START + "/" + END,
                               "--legacy-events", str(self.legacy),
                               "--projected-events", str(self.projected)],
                              capture_output=True, text=True)

    def test_matching_ids_and_latency_pass(self):
        self.write([self.event("a", "2026-09-23T04:00:10Z", "task"),
                    self.event("b", "2026-09-23T04:00:20Z")],
                   [self.event("a", "2026-09-23T04:00:30Z", "task", source="task-ledger", feed_seq=1),
                    self.event("b", "2026-09-23T04:00:40Z", source="top-pane", feed_seq=2)])
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS channel=tg sample=2 matched=2 missing=0 late=0 duplicate=0 invalid=0", result.stdout)

    def test_shared_normalizer_identity_closes_window_without_pane_text(self):
        key = self.base / "projection.key"
        key.write_bytes(b"z" * 32)
        key.chmod(0o600)
        secret = "fixture-private-closed-window"
        env = {**os.environ, "MESH_MISHE_HOME": str(self.base)}
        observed = subprocess.run([str(ROOT / "scripts/mesh-pane-consume"), "--pane-identity", "tg"],
                                  input=f"status=UP\n{secret}\n", env=env, capture_output=True, text=True)
        self.assertEqual(observed.returncode, 0, observed.stderr)
        identity = observed.stdout.strip()
        self.write([{"channel": "tg", "event_id": identity, "kind": "pane", "at": "2026-09-23T04:00:10Z"}],
                   [{"channel": "tg", "event_id": identity, "kind": "pane", "at": "2026-09-23T04:00:20Z",
                     "source": "top-pane", "feed_seq": 7}])
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn(secret.encode(), self.legacy.read_bytes() + self.projected.read_bytes() + result.stdout.encode())

    def test_zero_evidence_is_unknown(self):
        self.write([], [])
        result = self.check()
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNKNOWN sample=0", result.stdout)
        self.write([self.event("a", "2026-09-23T04:00:10Z")], [])
        self.assertEqual(self.check().returncode, 2)

    def test_missing_late_duplicate_and_invalid_are_failures(self):
        self.write([self.event("a", "2026-09-23T04:00:10Z"),
                    self.event("b", "2026-09-23T04:00:20Z")],
                   [self.event("a", "2026-09-23T04:00:30Z", source="top-pane", feed_seq=1)])
        self.assertIn("missing=1", self.check().stdout)
        self.write([self.event("a", "2026-09-23T04:00:10Z")],
                   [self.event("a", "2026-09-23T04:04:00Z", source="top-pane", feed_seq=1)])
        self.assertIn("late=1", self.check().stdout)
        item = self.event("a", "2026-09-23T04:00:30Z", source="top-pane", feed_seq=1)
        self.write([self.event("a", "2026-09-23T04:00:10Z")], [item, item])
        self.assertIn("duplicate=1", self.check().stdout)
        self.write([self.event("a", "2026-09-23T04:00:10Z"), self.event("b", "2026-09-23T04:00:20Z")],
                   [item, self.event("b", "2026-09-23T04:00:40Z", source="top-pane", feed_seq=1)])
        self.assertIn("invalid=1", self.check().stdout)
        self.write([self.event("a", "2026-09-23T04:00:10Z")], [dict(item, secret="fixture-private-text")])
        result = self.check()
        self.assertEqual(result.returncode, 2)  # no valid projected sample
        self.assertNotIn("fixture-private-text", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
