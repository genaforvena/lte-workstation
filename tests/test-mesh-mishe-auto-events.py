#!/usr/bin/env python3
"""Content-free durable automatic wake intents and explicit feed import."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))


class AutomaticEventTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.env = {**os.environ, "MESH_MISHE_HOME": str(self.home), "MESH_MISHE_CORE": str(CORE)}

    def call(self, *args):
        return subprocess.run([str(ROOT / "scripts/mesh-mishe-auto-events"), *args],
                              env=self.env, text=True, capture_output=True)

    def test_intent_is_durable_content_free_and_imported_once(self):
        secret = "fixture-private-operator-text"
        digest = hashlib.sha256(secret.encode()).hexdigest()
        begin = self.call("begin", "synthetic", "mesh-feed", digest)
        self.assertEqual(begin.returncode, 0, begin.stderr)
        key = begin.stdout.strip()
        records = list((self.home / "automatic-events/events").glob("*.json"))
        self.assertEqual(len(records), 1)
        self.assertNotIn(secret, records[0].read_text())
        record = json.loads(records[0].read_text())
        self.assertEqual(record["source"], "mesh-feed")
        self.assertEqual(record["status"], "pending")
        self.assertEqual(self.call("import", "synthetic").returncode, 0)
        before = (self.home / "feed").read_text()
        self.assertIn("status=unknown", before)
        self.assertEqual(self.call("import", "synthetic").returncode, 0)
        self.assertEqual((self.home / "feed").read_text(), before)
        self.assertEqual(self.call("finish", key, "delivered").returncode, 0)
        self.assertEqual(self.call("import", "synthetic").returncode, 0)
        self.assertIn("status=delivered", (self.home / "feed").read_text())

    def test_malformed_and_real_channel_import_fail_closed(self):
        self.assertNotEqual(self.call("begin", "synthetic", "mesh-feed", "raw-secret").returncode, 0)
        self.assertNotEqual(self.call("import", "health").returncode, 0)
        digest = "a" * 64
        self.assertEqual(self.call("begin", "synthetic", "mesh-feed", digest).returncode, 0)
        event = next((self.home / "automatic-events/events").glob("*.json"))
        event.write_text("broken")
        self.assertNotEqual(self.call("import", "synthetic").returncode, 0)

    def test_live_shadow_drain_is_bounded_and_restart_safe(self):
        digest = "a" * 64
        first = self.call("begin", "cleaner", "mesh-feed", digest)
        second = self.call("begin", "health", "mesh-dispatch", digest)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        one = self.call("drain", "--limit", "1")
        self.assertEqual(one.returncode, 0, one.stderr)
        self.assertEqual(json.loads(one.stdout)["imported"], 1)
        self.assertEqual((self.home / "feed").read_text().count("automatic channel="), 1)
        two = self.call("drain", "--limit", "1")
        self.assertEqual(two.returncode, 0, two.stderr)
        self.assertEqual(json.loads(two.stdout)["imported"], 1)
        self.assertEqual((self.home / "feed").read_text().count("automatic channel="), 2)
        self.assertEqual(json.loads(self.call("drain").stdout)["imported"], 0)
        self.assertEqual(self.call("finish", first.stdout.strip(), "delivered").returncode, 0)
        self.assertEqual(json.loads(self.call("drain").stdout)["imported"], 1)
        feed = (self.home / "feed").read_text()
        self.assertIn("status=delivered", feed)
        self.assertEqual(feed.count("automatic channel="), 3)
        self.assertEqual(json.loads(self.call("drain").stdout)["imported"], 0)

    def test_drain_rejects_corruption_before_import(self):
        self.assertEqual(self.call("begin", "cleaner", "mesh-feed", "b" * 64).returncode, 0)
        event = next((self.home / "automatic-events/events").glob("*.json"))
        event.write_text("broken")
        bad = self.call("drain")
        self.assertEqual(bad.returncode, 2)
        self.assertFalse((self.home / "feed").exists())
        target = self.home / "outside.json"
        target.write_text(json.dumps({"secret": "outside"}))
        event.unlink()
        event.symlink_to(target)
        self.assertEqual(self.call("drain").returncode, 2)

    def test_read_only_check_renders_backlog_and_unknown(self):
        self.assertIn('scripts/mesh-mishe-auto-events" check',
                      (ROOT / "scripts/mesh-doctor").read_text())
        empty = self.call("check")
        self.assertEqual(empty.returncode, 0)
        self.assertEqual(json.loads(empty.stdout)["status"], "DISABLED")
        self.assertFalse((self.home / "automatic-events").exists())
        key = self.call("begin", "cleaner", "mesh-feed", "a" * 64).stdout.strip()
        pending = self.call("check")
        self.assertEqual(pending.returncode, 2)
        self.assertEqual(json.loads(pending.stdout)["backlog"], 1)
        self.assertEqual(self.call("drain").returncode, 0)
        imported_pending = self.call("check")
        self.assertEqual(imported_pending.returncode, 2)
        self.assertEqual(json.loads(imported_pending.stdout)["uncertain"], 1)
        self.assertEqual(self.call("finish", key, "delivered").returncode, 0)
        self.assertEqual(self.call("drain").returncode, 0)
        settled = self.call("check")
        self.assertEqual(settled.returncode, 0)
        self.assertEqual(json.loads(settled.stdout)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
