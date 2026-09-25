#!/usr/bin/env python3
"""Isolated real-witness cutover and one-shot sink boundaries (never live state)."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))


class WitnessBoundary(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / "core"
        self.home.mkdir()
        self.calls = self.root / "calls"
        self.mind = self.root / "mind"
        self.mind.write_text("#!/usr/bin/env python3\nimport hashlib,json,os,sys\nfrom pathlib import Path\n"
                             "a=sys.argv; event=Path(a[a.index('--event-file')+1]); e=json.loads(event.read_text()); "
                             "p=Path(os.environ['MESH_DIR'])/'mishe-mind'/e['channel']/(e['request_id']+'.json'); "
                             "p.parent.mkdir(parents=True,exist_ok=True); "
                             "Path(os.environ['CALLS']).open('a').write(e['request_id']+'\\n'); "
                             "p.write_text(json.dumps({'channel':e['channel'],'request_id':e['request_id'], "
                             "'generation':e['generation'],'event_sha256':hashlib.sha256(event.read_bytes()).hexdigest(), "
                             "'status':os.environ.get('MIND_RESULT','settled'),'disposition':'non-actionable','task_id':None}))\n")
        self.mind.chmod(0o755)
        self.env = {**os.environ, "MESH_DIR": str(self.root / "mesh"), "MESH_MISHE_HOME": str(self.home),
                    "MESH_MISHE_CORE": str(CORE), "MESH_MISHE_REAL_ALLOWLIST": "witness",
                    "MESH_MISHE_WITNESS_MODEL": "openai-codex/gpt-6-luna",
                    "MESH_MISHE_SINK": str(ROOT / "scripts/mesh-mishe-mind-sink"),
                    "MESH_MISHE_MIND_CMD": str(self.mind), "CALLS": str(self.calls)}
        seed = self.feed("observation/witness", "STATE: RED\nOBSERVATION: source=top-pane/witness freshness=stale value-coverage=unknown")
        self.pass_s1(seed)
        self.feed("mishe-tauftauf", f"entry {seed} for top-pain witness: wake")
        self.admission_tail = self.feed("mishe-tauftauf", f"wake requested top-pain witness for entry {seed}")

    def call(self, script, *args, env=None):
        return subprocess.run([str(ROOT / "scripts" / script), *args], env=env or self.env,
                              text=True, capture_output=True, timeout=30)

    def feed(self, source, body):
        result = subprocess.run(["python3", "-c", "from mishe_tauftauf.feed import Feed; import sys; "
                                 "print(Feed(sys.argv[1]).append_runtime(sys.argv[2],sys.argv[3]).sequence)",
                                 str(self.home), source, body],
                                env={**self.env, "PYTHONPATH": str(CORE / "src")},
                                text=True, capture_output=True, check=True)
        return int(result.stdout)

    def activate(self):
        result = self.call("mesh-mishe-authority", "switch", "witness", "--to", "mishe",
                           "--expect-generation", "0", "--feed-seq", str(self.admission_tail))
        self.assertEqual(result.returncode, 0, result.stderr)

    def pass_s1(self, sequence):
        self.feed("mishe-tauftauf", f"judged relevance for top-pain witness on entry {sequence}: yes probability=0.8 question-version=1 policy-version=1")
        self.feed("mishe-tauftauf", f"judged desired-state-met for top-pain witness on entry {sequence}: no probability=0.1 question-version=1 policy-version=1")

    def request(self):
        seq = self.feed("observation/witness", "STATE: RED\nOBSERVATION: source=top-pane/witness freshness=fresh journal=stale signal=0123456789abcdef")
        self.last_stimulus = seq
        self.pass_s1(seq)
        self.feed("mishe-tauftauf", f"entry {seq} for top-pain witness: wake")
        return self.feed("mishe-tauftauf", f"wake requested top-pain witness for entry {seq}")

    def test_preflight_reports_hold_and_sequence_without_changing_authority(self):
        (self.home / ".fleet-shadow-hold").write_text("held\n")
        probe = self.call("mesh-mishe-authority", "preflight", "witness", "--expect-generation", "0",
                          "--feed-seq", str(self.admission_tail))
        self.assertEqual(probe.returncode, 2)
        self.assertFalse(json.loads(probe.stdout)["gates"]["hold_released"])
        self.assertEqual(self.call("mesh-mishe-authority", "read", "witness").returncode, 0)
        self.assertEqual(json.loads(self.call("mesh-mishe-authority", "read", "witness").stdout)["authority"], "legacy")
        self.assertNotEqual(self.call("mesh-mishe-authority", "switch", "witness", "--to", "mishe",
                                      "--expect-generation", "0", "--feed-seq", str(self.admission_tail)).returncode, 0)
        (self.home / ".fleet-shadow-hold").unlink()
        ready = self.call("mesh-mishe-authority", "preflight", "witness", "--expect-generation", "0",
                          "--feed-seq", str(self.admission_tail))
        self.assertEqual(ready.returncode, 0, ready.stderr)
        self.assertTrue(json.loads(ready.stdout)["ready"])
        self.activate()
        self.assertNotEqual(self.call("mesh-mishe-authority", "switch", "witness", "--to", "legacy",
                                      "--expect-generation", "0", "--feed-seq", "0").returncode, 0)

    def test_preflight_rejects_unknown_system_one_even_if_core_requested_wake(self):
        self.home = self.root / "unverified"
        self.home.mkdir()
        self.env["MESH_MISHE_HOME"] = str(self.home)
        seq = self.feed("observation/witness", "STATE: RED\nOBSERVATION: source=top-pane/witness freshness=stale value-coverage=unknown")
        for question in ("relevance", "desired-state-met"):
            self.feed("mishe-tauftauf", f"judged {question} for top-pain witness on entry {seq}: unknown probability=unknown question-version=1 policy-version=1")
        self.feed("mishe-tauftauf", f"entry {seq} for top-pain witness: wake")
        tail = self.feed("mishe-tauftauf", f"wake requested top-pain witness for entry {seq}")
        probe = self.call("mesh-mishe-authority", "preflight", "witness",
                          "--expect-generation", "0", "--feed-seq", str(tail))
        self.assertEqual(probe.returncode, 2)
        self.assertFalse(json.loads(probe.stdout)["gates"]["s1_proven"])
        self.assertNotEqual(self.call("mesh-mishe-authority", "switch", "witness", "--to", "mishe",
                                      "--expect-generation", "0", "--feed-seq", str(tail)).returncode, 0)

    def test_double_dispatch_does_not_duplicate_mind_invocation(self):
        self.activate()
        seq = self.request()
        key = f"witness:1:{seq}"
        first = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)["results"], [{"key": key, "status": "delivered"}])
        again = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(self.calls.read_text().splitlines(), [f"witness-g1-r{seq}"])
        repeat_sink = self.call("mesh-mishe-mind-sink", "--idempotency-key", key, "witness", "ignored")
        self.assertEqual(repeat_sink.returncode, 0, repeat_sink.stderr)
        self.assertEqual(self.calls.read_text().splitlines(), [f"witness-g1-r{seq}"])

    def test_repeated_s1_for_same_observation_does_not_launch_second_mind(self):
        self.activate()
        first_seq = self.request()
        duplicate_seq = self.feed("mishe-tauftauf",
                                  f"wake requested top-pain witness for entry {self.last_stimulus}")
        self.assertGreater(duplicate_seq, first_seq)
        result = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([row["status"] for row in json.loads(result.stdout)["results"]], ["delivered", "held"])
        self.assertEqual(self.calls.read_text().splitlines(), [f"witness-g1-r{first_seq}"])

    def test_distinct_s1_admitted_observations_each_get_one_disposable_mind(self):
        self.activate()
        first = self.request()
        delivered = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertEqual(delivered.returncode, 0, delivered.stderr)
        second_source = self.feed(
            "observation/witness",
            "STATE: RED\nOBSERVATION: source=top-pane/witness freshness=fresh "
            "journal=stale signal=fedcba9876543210",
        )
        self.pass_s1(second_source)
        self.feed("mishe-tauftauf", f"entry {second_source} for top-pain witness: wake")
        second = self.feed("mishe-tauftauf",
                           f"wake requested top-pain witness for entry {second_source}")
        self.assertGreater(second, first)
        awakened = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertEqual(awakened.returncode, 0, awakened.stderr)
        self.assertEqual(self.calls.read_text().splitlines(),
                         [f"witness-g1-r{first}", f"witness-g1-r{second}"])
        replay = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertEqual(replay.returncode, 0, replay.stderr)
        self.assertEqual(len(self.calls.read_text().splitlines()), 2)

    def test_unverified_source_and_stale_generation_never_invoke(self):
        self.activate()
        seq = self.feed("mishe-tauftauf", "wake requested top-pain witness for entry 999")
        held = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertEqual(json.loads(held.stdout)["results"][0]["status"], "held")
        self.assertFalse(self.calls.exists())
        valid_seq = self.request()
        forged = self.home / "outbox/witness" / f"2-{valid_seq}.json"
        forged.parent.mkdir(parents=True, exist_ok=True)
        forged.write_text(json.dumps({"channel": "witness", "generation": 2,
                                      "request_id": valid_seq, "key": f"witness:2:{valid_seq}",
                                      "status": "claimed"}))
        stale = self.call("mesh-mishe-mind-sink", "--idempotency-key", f"witness:2:{valid_seq}",
                          "witness", "ignored")
        self.assertEqual(json.loads(stale.stdout)["status"], "unknown")
        self.assertIn("authority generation", stale.stderr)
        self.assertNotEqual(self.call("mesh-mishe-authority", "switch", "witness", "--to", "legacy",
                                      "--expect-generation", "0", "--feed-seq", str(seq)).returncode, 0)
        self.assertFalse(self.calls.exists())

    def test_healthy_or_unknown_observation_cannot_awaken_witness(self):
        self.activate()
        for body in ("STATE: GREEN\nOBSERVATION: source=top-pane/witness freshness=fresh journal=fresh",
                     "STATE: UNKNOWN\nOBSERVATION: source=unavailable/witness freshness=unknown value-coverage=unknown"):
            seq = self.feed("observation/witness", body)
            self.feed("mishe-tauftauf", f"entry {seq} for top-pain witness: wake")
            self.feed("mishe-tauftauf", f"wake requested top-pain witness for entry {seq}")
        refused = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertEqual(refused.returncode, 0, refused.stderr)
        self.assertEqual([r["status"] for r in json.loads(refused.stdout)["results"]], ["held", "held"])
        self.assertFalse(self.calls.exists())

    def test_unknown_system_one_verdict_cannot_awaken_witness(self):
        self.activate()
        seq = self.feed("observation/witness", "STATE: RED\nOBSERVATION: source=top-pane/witness freshness=stale value-coverage=unknown")
        for question in ("relevance", "desired-state-met"):
            self.feed("mishe-tauftauf", f"judged {question} for top-pain witness on entry {seq}: unknown probability=unknown question-version=1 policy-version=1")
        self.feed("mishe-tauftauf", f"entry {seq} for top-pain witness: wake")
        self.feed("mishe-tauftauf", f"wake requested top-pain witness for entry {seq}")
        refused = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertEqual([r["status"] for r in json.loads(refused.stdout)["results"]], ["held"])
        self.assertFalse(self.calls.exists())

    def test_unknown_sink_claim_and_refused_destination_are_not_reinvoked(self):
        self.activate()
        seq = self.request()
        key = f"witness:1:{seq}"
        wrong = self.call("mesh-mishe-mind-sink", "--idempotency-key", key, "cleaner", "ignored")
        self.assertEqual(json.loads(wrong.stdout)["status"], "unknown")
        self.assertFalse(self.calls.exists())
        self.env["MIND_RESULT"] = "running"
        first = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertNotEqual(first.returncode, 0)
        self.assertIn("unknown outcome", first.stderr)
        second = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertEqual(json.loads(second.stdout)["results"][0]["status"], "unknown")
        self.assertEqual(self.calls.read_text().splitlines(), [f"witness-g1-r{seq}"])
        rollback = self.call("mesh-mishe-authority", "switch", "witness", "--to", "legacy",
                             "--expect-generation", "1", "--feed-seq", str(seq))
        self.assertNotEqual(rollback.returncode, 0)

    def test_source_backed_mishe_obligation_wakes_once_after_explicit_s1(self):
        self.activate()
        seq = self.feed("observation/witness",
                        "STATE: RED\nOBSERVATION: source=top-pane/witness freshness=fresh "
                        "journal=fresh signal=0123456789abcdef tasks-total=9 tasks-unfinished=2 "
                        "tasks-unowned=1 mishe-issues=2 issue-digest=0123456789abcdef")
        self.pass_s1(seq)
        self.feed("mishe-tauftauf", f"entry {seq} for top-pain witness: wake")
        request = self.feed("mishe-tauftauf", f"wake requested top-pain witness for entry {seq}")
        result = self.call("mesh-mishe-dispatch", "--once", "witness")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["results"],
                         [{"key": f"witness:1:{request}", "status": "delivered"}])
        self.assertEqual(self.calls.read_text().splitlines(), [f"witness-g1-r{request}"])

    def test_enrolled_shadow_tick_drains_admitted_witness_wake(self):
        self.activate()
        seq = self.request()
        self.env.update(MESH_REPO=str(ROOT), MESH_MISHE_PYTHON=os.environ.get("PYTHON", "python3"),
                        MESH_MISHE_JUDGE="/bin/false", MESH_MISHE_MANUAL_SHADOW="0",
                        MESH_MISHE_SKIP_AUTO_DRAIN="0")
        initialized = self.call("mesh-mishe-run", "init")
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        (self.home / "fleet-channels").write_text("witness\n")
        top_pain = self.home / "top-pains/witness"
        top_pain.write_text("#!/bin/sh\nprintf 'MISHE-STATE: UNKNOWN\\nMISHE-SOURCE: top-pane\\nMISHE-FRESHNESS: STALE\\n'\n")
        top_pain.chmod(0o755)
        projector = self.home / "projectors/witness"
        projector.write_text(f"#!/bin/sh\nexec '{ROOT}/scripts/mesh-mishe-project' --channel witness \"$@\"\n")
        projector.chmod(0o755)
        tick = self.call("mesh-mishe-run", "once", "--channel", "witness")
        self.assertEqual(tick.returncode, 0, tick.stderr)
        self.assertEqual(self.calls.read_text().splitlines(), [f"witness-g1-r{seq}"])



if __name__ == "__main__":
    unittest.main()
