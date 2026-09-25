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
                             " Path(os.environ['SINK_CALLS']).open('a').write(a[1]+'\\n')\n"
                             " d[a[1]]='refused' if os.environ.get('SINK_REFUSE')=='1' else 'delivered'; p.write_text(json.dumps(d)); sys.exit(0)\n"
                             "sys.exit(2)\n")
        self.sink.chmod(0o755)
        self.env = {**os.environ, "MESH_MISHE_HOME": str(self.home), "MESH_MISHE_CORE": str(CORE),
                    "MESH_MISHE_SINK": str(self.sink), "SINK_LEDGER": str(self.home / "sink-ledger.json"),
                    "SINK_CALLS": str(self.home / "sink-calls"),
                    "MESH_MISHE_RETRY_BASE": "0", "MESH_DIR": str(self.home / "mesh")}

    def run_cmd(self, name, *args):
        return subprocess.run([str(ROOT / "scripts" / name), *args], env=self.env, text=True, capture_output=True)

    def feed(self, body):
        result = subprocess.run(["python3", "-c", "from mishe_tauftauf.feed import Feed; import sys; print(Feed(sys.argv[1]).append_runtime('mishe-tauftauf',sys.argv[2]).sequence)", str(self.home), body],
                                env={**self.env, "PYTHONPATH": str(CORE / "src")}, text=True, capture_output=True, check=True)
        return int(result.stdout)

    def request(self):
        stimulus = subprocess.run(["python3", "-c", "from mishe_tauftauf.feed import Feed; import sys; print(Feed(sys.argv[1]).append_runtime('observation/synthetic','STATE: RED').sequence)", str(self.home)],
                                  env={**self.env, "PYTHONPATH": str(CORE / "src")}, text=True, capture_output=True, check=True)
        self.feed(f"wake requested top-pain synthetic for entry {int(stimulus.stdout)}")

    def activate(self):
        self.feed("wake requested top-pain synthetic for entry 1")
        result = self.run_cmd("mesh-mishe-authority", "switch", "synthetic", "--to", "mishe", "--expect-generation", "0", "--feed-seq", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        policy = self.home / "dispatch-policy/synthetic.json"
        policy.parent.mkdir(parents=True)
        policy.write_text(json.dumps({"version": 1, "channel": "synthetic", "domain": "synthetic",
                                      "private": False, "protected": False, "mind_state": "idle",
                                      "refractory_until": 0, "pace_allowed": True, "task_owner": None}))

    def test_shadow_request_excluded_and_delivery_idempotent(self):
        self.activate()
        self.request()
        self.env["MESH_TELL_AUTOMATIC"] = "1"  # supervisor context must not turn a keyed send into a legacy send
        self.assertEqual(self.run_cmd("mesh-mishe-dispatch", "--check", "synthetic").returncode, 2)
        first = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.run_cmd("mesh-mishe-dispatch", "--check", "synthetic").returncode, 0)
        ledger = json.loads((self.home / "sink-ledger.json").read_text())
        self.assertEqual(list(ledger), ["synthetic:1:3"])
        self.assertEqual(self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic").returncode, 0)
        self.assertEqual(json.loads((self.home / "sink-ledger.json").read_text()), ledger)

    def test_refused_sink_receipt_is_terminal(self):
        self.activate()
        self.request()
        self.env["SINK_REFUSE"] = "1"
        first = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(json.loads(first.stdout)["results"][0]["status"], "refused")
        self.env["SINK_REFUSE"] = "0"
        again = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(json.loads(again.stdout)["results"][0]["status"], "refused")
        self.assertEqual((self.home / "sink-calls").read_text().splitlines(), ["synthetic:1:3"])

    def test_claimed_send_without_sink_confirmation_stays_unknown(self):
        self.activate()
        self.request()
        env = {**self.env, "MESH_MISHE_FAULT": "after-claim"}
        failed = subprocess.run([str(ROOT / "scripts/mesh-mishe-dispatch"), "--once", "synthetic"], env=env, capture_output=True)
        self.assertNotEqual(failed.returncode, 0)
        retry = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertNotEqual(retry.returncode, 0)
        self.assertFalse((self.home / "sink-ledger.json").exists())
        self.assertIn("unknown", retry.stdout.lower())
        rollback = self.run_cmd("mesh-mishe-authority", "switch", "synthetic", "--to", "legacy", "--expect-generation", "1", "--feed-seq", "3")
        self.assertNotEqual(rollback.returncode, 0)
        self.assertEqual(self.run_cmd("mesh-mishe-dispatch", "--check", "synthetic").returncode, 2)

    def test_all_crash_edges_replay_without_duplicate_sink_key(self):
        for fault in ("before-claim", "after-tell", "after-receipt"):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as tmp:
                self.home = Path(tmp)
                self.env["MESH_MISHE_HOME"] = str(self.home)
                self.env["SINK_LEDGER"] = str(self.home / "sink-ledger.json")
                self.activate()
                self.request()
                failed = subprocess.run([str(ROOT / "scripts/mesh-mishe-dispatch"), "--once", "synthetic"],
                                        env={**self.env, "MESH_MISHE_FAULT": fault}, text=True, capture_output=True)
                self.assertNotEqual(failed.returncode, 0)
                recovered = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
                self.assertEqual(recovered.returncode, 0, recovered.stderr)
                self.assertEqual(json.loads(recovered.stdout)["results"][0]["status"], "delivered")
                self.assertEqual(len(json.loads((self.home / "sink-ledger.json").read_text())), 1)

    def test_missing_sink_capability_and_corrupt_outbox_fail_closed(self):
        self.activate()
        self.request()
        absent = subprocess.run([str(ROOT / "scripts/mesh-mishe-dispatch"), "--once", "synthetic"],
                                env={**self.env, "MESH_MISHE_SINK": ""}, text=True, capture_output=True)
        self.assertNotEqual(absent.returncode, 0)
        self.assertFalse((self.home / "sink-ledger.json").exists())
        outbox = self.home / "outbox/synthetic/1-3.json"
        outbox.parent.mkdir(parents=True)
        outbox.write_text("broken")
        self.assertNotEqual(self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic").returncode, 0)
        self.assertFalse((self.home / "sink-ledger.json").exists())

    def test_ungrounded_request_is_held_without_sink_call(self):
        self.activate()
        self.feed("wake requested top-pain synthetic for entry 999")
        result = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["results"][0]["status"], "held")
        self.assertFalse((self.home / "sink-ledger.json").exists())

    def test_busy_and_private_policy_block_sink(self):
        self.activate()
        self.request()
        path = self.home / "dispatch-policy/synthetic.json"
        policy = json.loads(path.read_text())
        policy["mind_state"] = "busy"
        path.write_text(json.dumps(policy))
        busy = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(json.loads(busy.stdout)["results"][0]["status"], "held")
        self.assertFalse((self.home / "sink-ledger.json").exists())
        policy["mind_state"] = "idle"
        policy["private"] = True
        path.write_text(json.dumps(policy))
        private = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(json.loads(private.stdout)["results"][0]["status"], "refused")
        self.assertFalse((self.home / "sink-ledger.json").exists())
        policy["private"] = False
        path.write_text(json.dumps(policy))
        replay = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(json.loads(replay.stdout)["results"][0]["status"], "refused")
        self.assertFalse((self.home / "sink-ledger.json").exists())

    def test_transient_policy_holds_retry_when_evidence_clears(self):
        self.activate()
        self.request()
        path = self.home / "dispatch-policy/synthetic.json"
        policy = json.loads(path.read_text())
        for change, reason in (({"pace_allowed": False}, "pace"),
                               ({"pace_allowed": True, "refractory_until": 9999999999}, "refractory"),
                               ({"refractory_until": 0, "task_owner": "synthetic"}, "canonical-task-eligibility-unverified")):
            policy.update(change)
            path.write_text(json.dumps(policy))
            result = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["results"][0]["reason"], reason)
            self.assertFalse((self.home / "sink-ledger.json").exists())
        policy["task_owner"] = None
        path.write_text(json.dumps(policy))
        delivered = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(json.loads(delivered.stdout)["results"][0]["status"], "delivered")

    def test_held_retry_is_bounded_and_never_sends_before_due(self):
        self.activate()
        self.request()
        self.env["MESH_MISHE_RETRY_BASE"] = "2"
        self.env["MESH_MISHE_NOW"] = "1000"
        path = self.home / "dispatch-policy/synthetic.json"
        policy = json.loads(path.read_text())
        policy["mind_state"] = "busy"
        path.write_text(json.dumps(policy))
        first = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(json.loads(first.stdout)["results"][0]["retry_after"], 1002)
        policy["mind_state"] = "idle"
        path.write_text(json.dumps(policy))
        before_due = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(json.loads(before_due.stdout)["results"][0]["status"], "held")
        self.assertFalse((self.home / "sink-ledger.json").exists())
        self.env["MESH_MISHE_NOW"] = "1002"
        due = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(json.loads(due.stdout)["results"][0]["status"], "delivered")
        self.assertEqual(len(json.loads((self.home / "sink-ledger.json").read_text())), 1)

    def test_live_eligibility_adapter_controls_synthetic_sink(self):
        self.activate()
        self.request()
        path = self.home / "dispatch-policy/synthetic.json"
        policy = json.loads(path.read_text())
        policy.update({"evidence_mode": "live", "kind": "telemetry"})
        path.write_text(json.dumps(policy))
        adapter = self.home / "adapter"
        adapter.write_text("#!/usr/bin/env python3\nimport json,os,sys\n"
                           "status=os.environ.get('ADMIT_STATUS','held')\n"
                           "print(json.dumps({'channel':sys.argv[1], 'status':status, 'reason':'live-probe'}))\n"
                           "sys.exit({'eligible':0,'held':1,'refused':1,'unknown':2}[status])\n")
        adapter.chmod(0o755)
        self.env["MESH_MISHE_ELIGIBILITY_BIN"] = str(adapter)
        held = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(json.loads(held.stdout)["results"][0]["status"], "held")
        self.assertFalse((self.home / "sink-ledger.json").exists())
        self.env["ADMIT_STATUS"] = "eligible"
        delivered = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(json.loads(delivered.stdout)["results"][0]["status"], "delivered")

    def test_ambiguous_claim_reconciles_receipt_without_new_eligibility_or_send(self):
        self.activate()
        self.request()
        failed = subprocess.run([str(ROOT / "scripts/mesh-mishe-dispatch"), "--once", "synthetic"],
                                env={**self.env, "MESH_MISHE_FAULT": "after-claim"}, capture_output=True)
        self.assertNotEqual(failed.returncode, 0)
        key = "synthetic:1:3"
        (self.home / "sink-ledger.json").write_text(json.dumps({key: "delivered"}))
        path = self.home / "dispatch-policy/synthetic.json"
        policy = json.loads(path.read_text())
        policy["mind_state"] = "busy"
        path.write_text(json.dumps(policy))
        reconciled = self.run_cmd("mesh-mishe-dispatch", "--once", "synthetic")
        self.assertEqual(reconciled.returncode, 0, reconciled.stderr)
        self.assertEqual(json.loads(reconciled.stdout)["results"][0]["status"], "delivered")
        self.assertEqual(json.loads((self.home / "sink-ledger.json").read_text()), {key: "delivered"})


if __name__ == "__main__":
    unittest.main()
