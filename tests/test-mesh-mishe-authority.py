#!/usr/bin/env python3
"""Synthetic authority record: atomic generation and activation fence."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))


class AuthorityTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.env = {**os.environ, "MESH_MISHE_HOME": str(self.home), "MESH_MISHE_CORE": str(CORE)}

    def run_cmd(self, *args):
        return subprocess.run([str(ROOT / "scripts/mesh-mishe-authority"), *args],
                              env=self.env, text=True, capture_output=True)

    def feed(self, body):
        subprocess.run(["python3", "-c", "from mishe_tauftauf.feed import Feed; import sys; Feed(sys.argv[1]).append_runtime('mishe-tauftauf',sys.argv[2])", str(self.home), body],
                       env={**self.env, "PYTHONPATH": str(CORE / "src")}, check=True)

    def test_switch_requires_current_generation_and_feed_tail(self):
        self.feed("shadow")
        self.assertEqual(json.loads(self.run_cmd("read", "synthetic").stdout)["authority"], "legacy")
        self.assertNotEqual(self.run_cmd("switch", "synthetic", "--to", "mishe", "--expect-generation", "0", "--feed-seq", "0").returncode, 0)
        first = self.run_cmd("switch", "synthetic", "--to", "mishe", "--expect-generation", "0", "--feed-seq", "1")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)["generation"], 1)
        self.assertNotEqual(self.run_cmd("switch", "synthetic", "--to", "legacy", "--expect-generation", "0", "--feed-seq", "1").returncode, 0)
        second = self.run_cmd("switch", "synthetic", "--to", "legacy", "--expect-generation", "1", "--feed-seq", "1")
        self.assertEqual(json.loads(second.stdout)["generation"], 2)

    def test_corrupt_record_and_live_channel_fail_closed(self):
        self.assertNotEqual(self.run_cmd("switch", "cleaner", "--to", "mishe", "--expect-generation", "0", "--feed-seq", "0").returncode, 0)
        record = self.home / "authority" / "synthetic.json"
        record.parent.mkdir()
        record.write_text("broken")
        self.assertNotEqual(self.run_cmd("read", "synthetic").returncode, 0)

    def test_rollback_requires_outbox_reconciliation(self):
        self.feed("shadow")
        self.assertEqual(self.run_cmd("switch", "synthetic", "--to", "mishe", "--expect-generation", "0", "--feed-seq", "1").returncode, 0)
        outbox = self.home / "outbox/synthetic/1-2.json"
        outbox.parent.mkdir(parents=True)
        outbox.write_text('{"status":"pending"}')
        self.assertNotEqual(self.run_cmd("switch", "synthetic", "--to", "legacy", "--expect-generation", "1", "--feed-seq", "1").returncode, 0)


if __name__ == "__main__":
    unittest.main()
