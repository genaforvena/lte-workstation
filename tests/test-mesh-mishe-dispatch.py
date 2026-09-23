#!/usr/bin/env python3
"""Synthetic outbox and claimed-send recovery."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))


class DispatchTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.sink = self.home / "sink"
        self.sink.write_text("#!/usr/bin/env python3\nimport json,os,sys\nfrom pathlib import Path\n"
                             "p=Path(os.environ['SINK_LEDGER']); a=sys.argv[1:]; d=json.loads(p.read_text()) if p.exists() else {}\n"
                             "if a[0]=='--idempotency-status':\n s=d.get(a[1],'unknown'); print(json.dumps({'status':s})); sys.exit(3 if s=='unknown' else 0)\n"
                             "if a[0]=='--idempotency-key':\n"
                             " if os.environ.get('MESH_TELL_AUTOMATIC')=='1': sys.exit(2)\n"
                             " d[a[1]]='delivered'; p.write_text(json.dumps(d)); sys.exit(0)\n"
                             "sys.exit(2)\n")
        self.sink.chmod(0o755)
        self.env = {**os.environ, "MESH_MISHE_HOME": str(self.home), "MESH_MISHE_CORE": str(CORE),
                    "MESH_MISHE_SINK": str(self.sink), "SINK_LEDGER": str(self.home / "sink-ledger.json")}

    def run_cmd(self, name, *args):
        return subprocess.run([str(ROOT / "scripts" / name), *args], env=self.env, text=True, capture_output=True)

    def feed(self, body):
        result = subprocess.run(["python3", "-c", "from mishe_tauftauf.feed import Feed; import sys; print(Feed(sys.argv[1]).append_runtime('mishe-tauftauf',sys.argv[2]).sequence)", str(self.home), body],
                                env={**self.env, "PYTHONPATH": str(CORE / "src")}, text=True, capture_output=True, check=True)
        return int(result.stdout)

    def activate(self):
        self.feed("wake requested top-pain synthetic for entry 1")
        result = self.run_cmd("mesh-mishe-authority", "switch", "synthetic", "--to", "mishe", "--expect-generation", "0", "--feed-seq", "1")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_shadow_request_excluded_and_delivery_idempotent(self):
        self.activate()
        self.feed("wake requested top-pain synthetic for entry 2")
        self.env["MESH_TELL_AUTOMATIC"] = "1"  # supervisor context must not turn a keyed send into a legacy send
        self.assertEqual(self.run_cmd("mesh-mishe-dispatch", "--check", "synthetic").returncode, 2)
        first = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.run_cmd("mesh-mishe-dispatch", "--check", "synthetic").returncode, 0)
        ledger = json.loads((self.home / "sink-ledger.json").read_text())
        self.assertEqual(list(ledger), ["synthetic:1:2"])
        self.assertEqual(self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic").returncode, 0)
        self.assertEqual(json.loads((self.home / "sink-ledger.json").read_text()), ledger)

    def test_claimed_send_without_sink_confirmation_stays_unknown(self):
        self.activate()
        self.feed("wake requested top-pain synthetic for entry 2")
        env = {**self.env, "MESH_MISHE_FAULT": "after-claim"}
        failed = subprocess.run([str(ROOT / "scripts/mesh-mishe-dispatch"), "--once", "synthetic"], env=env, capture_output=True)
        self.assertNotEqual(failed.returncode, 0)
        retry = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertNotEqual(retry.returncode, 0)
        self.assertFalse((self.home / "sink-ledger.json").exists())
        self.assertIn("unknown", retry.stdout.lower())
        rollback = self.run_cmd("mesh-mishe-authority", "switch", "synthetic", "--to", "legacy", "--expect-generation", "1", "--feed-seq", "2")
        self.assertNotEqual(rollback.returncode, 0)
        self.assertEqual(self.run_cmd("mesh-mishe-dispatch", "--check", "synthetic").returncode, 2)

    def test_all_crash_edges_replay_without_duplicate_sink_key(self):
        for fault in ("before-claim", "after-tell", "after-receipt"):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as tmp:
                self.home = Path(tmp)
                self.env["MESH_MISHE_HOME"] = str(self.home)
                self.env["SINK_LEDGER"] = str(self.home / "sink-ledger.json")
                self.activate()
                self.feed("wake requested top-pain synthetic for entry 2")
                failed = subprocess.run([str(ROOT / "scripts/mesh-mishe-dispatch"), "--once", "synthetic"],
                                        env={**self.env, "MESH_MISHE_FAULT": fault}, text=True, capture_output=True)
                self.assertNotEqual(failed.returncode, 0)
                recovered = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
                self.assertEqual(recovered.returncode, 0, recovered.stderr)
                self.assertEqual(json.loads(recovered.stdout)["results"][0]["status"], "delivered")
                self.assertEqual(len(json.loads((self.home / "sink-ledger.json").read_text())), 1)

    def test_missing_sink_capability_and_corrupt_outbox_fail_closed(self):
        self.activate()
        self.feed("wake requested top-pain synthetic for entry 2")
        absent = subprocess.run([str(ROOT / "scripts/mesh-mishe-dispatch"), "--once", "synthetic"],
                                env={**self.env, "MESH_MISHE_SINK": ""}, text=True, capture_output=True)
        self.assertNotEqual(absent.returncode, 0)
        self.assertFalse((self.home / "sink-ledger.json").exists())
        outbox = self.home / "outbox/synthetic/1-2.json"
        outbox.parent.mkdir(parents=True)
        outbox.write_text("broken")
        self.assertNotEqual(self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic").returncode, 0)
        self.assertFalse((self.home / "sink-ledger.json").exists())


if __name__ == "__main__":
    unittest.main()
