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


if __name__ == "__main__":
    unittest.main()
