#!/usr/bin/env python3
"""Exact one-shot Mind sink status and ambiguous-crash fence."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SINK = ROOT / "scripts/mesh-mishe-mind-sink"
KEY = "synthetic:1:3"


class MindSinkTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / "mishe"
        (self.home / "authority").mkdir(parents=True)
        (self.home / "authority/synthetic.json").write_text(json.dumps({
            "channel": "synthetic", "generation": 1, "authority": "mishe",
            "active_feed_seq": 1, "installed_at": "2026-09-23T00:00:00Z"}))
        mind = self.root / "mind"
        mind.write_text("#!/usr/bin/env python3\nimport hashlib,json,os,pathlib,sys\n"
                        "a=sys.argv; ch=a[a.index('--channel')+1]; key=a[a.index('--request-id')+1]; event=pathlib.Path(a[a.index('--event-file')+1])\n"
                        "count=pathlib.Path(os.environ['CALL_COUNT']); count.write_text(str(int(count.read_text())+1 if count.exists() else 1))\n"
                        "p=pathlib.Path(os.environ['MESH_DIR'])/'mishe-mind'/ch/(key+'.json'); p.parent.mkdir(parents=True,exist_ok=True)\n"
                        "p.write_text(json.dumps({'channel':ch,'request_id':key,'generation':1,'event_sha256':hashlib.sha256(event.read_bytes()).hexdigest(),'status':os.environ.get('MIND_RESULT','running')}))\n")
        mind.chmod(0o755)
        self.count = self.root / "calls"
        self.env = {**os.environ, "MESH_DIR": str(self.root), "MESH_MISHE_HOME": str(self.home),
                    "MESH_MISHE_MIND_CMD": str(mind), "CALL_COUNT": str(self.count)}

    def call(self, *args):
        return subprocess.run([str(SINK), *args], env=self.env, text=True, capture_output=True)

    def test_running_record_is_unknown_and_never_relaunched(self):
        self.assertEqual(self.call("--idempotency-status", KEY).returncode, 3)
        first = self.call("--idempotency-key", KEY, "synthetic", "ignored prompt")
        self.assertEqual(first.returncode, 3)
        self.assertEqual(json.loads(first.stdout)["status"], "unknown")
        self.assertEqual(self.call("--idempotency-key", KEY, "synthetic", "ignored prompt").returncode, 3)
        self.assertEqual(self.count.read_text(), "1")

    def test_only_exact_settled_record_is_delivered(self):
        self.env["MIND_RESULT"] = "settled"
        sent = self.call("--idempotency-key", KEY, "synthetic", "ignored prompt")
        self.assertEqual(sent.returncode, 0, sent.stderr)
        self.assertEqual(json.loads(self.call("--idempotency-status", KEY).stdout)["status"], "delivered")
        self.assertEqual(self.call("--idempotency-key", KEY, "synthetic", "ignored prompt").returncode, 0)
        self.assertEqual(self.count.read_text(), "1")
        record = self.root / "mishe-mind/synthetic/synthetic-g1-r3.json"
        value = json.loads(record.read_text())
        value["generation"] = 2
        record.write_text(json.dumps(value))
        self.assertEqual(self.call("--idempotency-status", KEY).returncode, 3)

    def test_wrong_destination_and_legacy_authority_do_not_launch(self):
        self.assertEqual(self.call("--idempotency-key", KEY, "health", "ignored prompt").returncode, 3)
        authority = self.home / "authority/synthetic.json"
        value = json.loads(authority.read_text())
        value["authority"] = "legacy"
        authority.write_text(json.dumps(value))
        self.assertEqual(self.call("--idempotency-key", KEY, "synthetic", "ignored prompt").returncode, 3)
        self.assertFalse(self.count.exists())


if __name__ == "__main__":
    unittest.main()
