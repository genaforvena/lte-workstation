#!/usr/bin/env python3
"""Synthetic one-shot Mind lease, claim, receipt and crash recovery."""
import json
import contextlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/mesh-mishe-mind"


class OneShot(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "mesh/charter").mkdir(parents=True)
        (self.root / "mesh/handoff").mkdir()
        (self.root / "core/handoffs").mkdir(parents=True)
        (self.root / "mesh/charter/synthetic.md").write_text("Synthetic test channel.\n")
        self.event = self.root / "event.json"
        self.event.write_text(json.dumps({"channel": "synthetic", "request_id": "req1", "kind": "task"}))
        self.auth = self.helper("authority", "print('{\"authority\":\"mishe\",\"generation\":1}')")
        self.dash = self.helper("dash", "print('TOP PANE fresh')")
        self.pred = self.helper("predictions", """
import os, sys
from pathlib import Path
if 'needle=' in sys.argv[2]:
    print('NO' if (Path(os.environ['MESH_DIR'])/'core-receipt-missing').exists() else 'YES')
else:
    print('EXPECTATIONS\\n(none)')
""")
        self.task = self.helper("task", """
import os, sys
from pathlib import Path
p=Path(os.environ['MESH_DIR'])/'task-state'
state=p.read_text() if p.exists() else 'open'
if sys.argv[1]=='status':
    print(f'  1. demo/do [{state}] owner=synthetic' + (' artifact=' + str(Path(os.environ['MESH_DIR'])/'artifact') if state=='done' else ''))
elif sys.argv[1]=='check':
    if state!='open': sys.exit(2)
elif sys.argv[1]=='take':
    if (Path(os.environ['MESH_DIR'])/'take-sleep').exists():
        (Path(os.environ['MESH_DIR'])/'take-entered').write_text('yes')
        import time; time.sleep(60)
    p.write_text('active')
else: sys.exit(2)
""")
        self.omp = self.helper("omp", """
import os, sys, time
from pathlib import Path
root=Path(os.environ['MESH_DIR'])
mode=(root/'omp-mode').read_text() if (root/'omp-mode').exists() else 'settle'
if mode=='sleep':
    (root/'omp-entered').write_text('yes')
    time.sleep(60)
elif mode=='effect-sleep':
    with (root/'external-actions').open('a') as f: f.write('action\\n')
    (root/'omp-entered').write_text('yes')
    time.sleep(60)
elif mode=='no-handoff':
    pass
else:
    if mode=='settle-effect':
        with (root/'external-actions').open('a') as f: f.write('action\\n')
    token=os.environ['MESH_MISHE_INVOCATION']
    (root/'omp-prompt').write_text(sys.argv[-1])
    (Path(os.environ['MESH_MISHE_HOME'])/'handoffs/synthetic.md').write_text('invocation:'+token)
    with (root/'chat.log').open('a') as f: f.write('[fyi] invocation:'+token+'\\n')
    if (root/'task-state').exists():
        (root/'task-state').write_text('done')
        (root/'artifact').write_text('result')
""")
        self.env = dict(os.environ, MESH_DIR=str(self.root / "mesh"), MESH_MISHE_HOME=str(self.root / "core"),
                        MESH_REPO=str(self.root), MESH_MISHE_AUTHORITY_CMD=str(self.auth),
                        MESH_MISHE_TASK_CMD=str(self.task), MESH_MISHE_DASH_CMD=str(self.dash),
                        MESH_MISHE_PYTHON=str(self.pred), MESH_MISHE_OMP_CMD=str(self.omp))
        (self.root / "mesh/chat.log").write_text("")

    def helper(self, name, body):
        p = self.root / name
        p.write_text("#!/usr/bin/env python3\n" + body + "\n")
        p.chmod(0o755)
        return p

    def command(self, task=False):
        args = [sys.executable, str(SCRIPT), "--channel", "synthetic", "--request-id", "req1",
                "--event-file", str(self.event)]
        if task:
            args += ["--task-id", "demo/do"]
        return args

    def call(self, task=False):
        return subprocess.run(self.command(task), env=self.env, capture_output=True, text=True, timeout=20)

    def check(self):
        return subprocess.run([sys.executable, str(SCRIPT), "--check", "synthetic"],
                              env=self.env, capture_output=True, text=True, timeout=5)

    def create_wip_ref(self):
        def git(*args):
            return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                                  capture_output=True, text=True).stdout.strip()
        git("init", "-q")
        git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-qm", "base")
        commit = git("rev-parse", "HEAD")
        git("update-ref", "refs/wip/synthetic", commit)
        return commit

    def test_noop_receipt_and_repeat(self):
        self.assertIn("DISABLED", self.check().stdout)
        first = self.call()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.call().returncode, 0)
        record = json.loads((self.root / "mesh/mishe-mind/synthetic/req1.json").read_text())
        self.assertEqual(record["status"], "settled")
        self.assertIn("input_sha256", record)
        self.assertIn("PASS", self.check().stdout)

    def test_task_claim_and_verified_artifact(self):
        result = self.call(task=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "mesh/task-state").read_text(), "done")


    def test_prompt_excludes_raw_dashboard_handoff_and_predictions(self):
        self.dash = self.helper("private-dash", "print('PRIVATE-dashboard-source')")
        self.env["MESH_MISHE_DASH_CMD"] = str(self.dash)
        self.pred = self.helper("private-predictions", "import sys\nprint('YES' if 'needle=' in sys.argv[2] else 'PRIVATE-predictions-source')")
        self.env["MESH_MISHE_PYTHON"] = str(self.pred)
        (self.root / "core/handoffs/synthetic.md").write_text("PRIVATE-prior-handoff\n")
        result = self.call()
        self.assertEqual(result.returncode, 0, result.stderr)
        prompt = (self.root / "mesh/omp-prompt").read_text()
        for secret in ("PRIVATE-dashboard-source", "PRIVATE-predictions-source",
                       "PRIVATE-prior-handoff"):
            self.assertNotIn(secret, prompt)

    def test_real_owner_is_not_invoked_without_projected_s0_s1_sink(self):
        self.event.write_text(json.dumps({"channel": "cleaner", "request_id": "req1"}))
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--channel", "cleaner", "--request-id", "req1",
             "--event-file", str(self.event)], env=self.env, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 2)
        self.assertIn("projected S0/S1", result.stderr)
        self.assertFalse((self.root / "mesh/omp-prompt").exists())
        self.assertFalse((self.root / "mesh/mishe-mind/cleaner").exists())

    def test_no_handoff_is_incomplete_then_recovered(self):
        (self.root / "mesh/omp-mode").write_text("no-handoff")
        first = self.call()
        self.assertEqual(first.returncode, 2)
        self.assertIn("handoffs/synthetic.md", first.stderr)
        self.assertEqual(json.loads((self.root / "mesh/mishe-mind/synthetic/req1.json").read_text())["status"], "running")
        self.assertEqual(self.check().returncode, 2)
        self.assertIn("orphan invocation", self.check().stdout)
        (self.root / "mesh/omp-mode").write_text("settle")
        self.assertEqual(self.call().returncode, 0)

    def test_missing_board_receipt_keeps_unknown(self):
        (self.root / "mesh/omp-mode").write_text("no-handoff")
        handoff = self.root / "core/handoffs/synthetic.md"
        handoff.write_text("invocation:req1")
        result = self.call()
        self.assertEqual(result.returncode, 2)
        self.assertIn("board receipt absent", result.stderr)

    def test_missing_core_feed_receipt_keeps_unknown(self):
        (self.root / "mesh/core-receipt-missing").write_text("yes")
        result = self.call()
        self.assertEqual(result.returncode, 2)
        self.assertIn("core feed handoff receipt absent", result.stderr)

    def test_kill_before_claim_retries(self):
        (self.root / "mesh/take-sleep").write_text("yes")
        child = subprocess.Popen(self.command(task=True), env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            marker = self.root / "mesh/take-entered"
            for _ in range(100):
                if marker.exists():
                    break
                time.sleep(.05)
            self.assertTrue(marker.exists())
            child.kill()
            child.wait(timeout=5)
            self.assertEqual(self.check().returncode, 2)
            (self.root / "mesh/take-sleep").unlink()
            recovered = self.call(task=True)
            self.assertEqual(recovered.returncode, 0, recovered.stderr)
        finally:
            if child.poll() is None:
                child.kill()
                child.wait()
            with contextlib.suppress(Exception):
                child.stdout.close()
                child.stderr.close()

    def test_kill_after_claim_and_lease_release(self):
        commit = self.create_wip_ref()
        (self.root / "mesh/omp-mode").write_text("sleep")
        child = subprocess.Popen(self.command(task=True), env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            marker = self.root / "mesh/omp-entered"
            for _ in range(100):
                if marker.exists():
                    break
                time.sleep(.05)
            self.assertTrue(marker.exists(), "omp was not entered")
            contender = self.call(task=True)
            self.assertEqual(contender.returncode, 2)
            self.assertIn("lease busy", contender.stderr)
            child.kill()
            child.wait(timeout=5)
            (self.root / "mesh/omp-mode").write_text("settle")
            recovered = self.call(task=True)
            self.assertEqual(recovered.returncode, 0, recovered.stderr)
            self.assertIn("refs/wip/synthetic " + commit, (self.root / "mesh/omp-prompt").read_text())
        finally:
            if child.poll() is None:
                child.kill()
                child.wait()
            with contextlib.suppress(Exception):
                child.stdout.close()
                child.stderr.close()

    def test_model_side_effect_before_handoff_remains_ambiguous(self):
        """A same-ID retry can repeat model actions; dispatch must hold UNKNOWN."""
        (self.root / "mesh/omp-mode").write_text("effect-sleep")
        child = subprocess.Popen(self.command(), env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            marker = self.root / "mesh/omp-entered"
            for _ in range(100):
                if marker.exists():
                    break
                time.sleep(.05)
            self.assertTrue(marker.exists())
            child.kill()
            child.wait(timeout=5)
            self.assertEqual(self.check().returncode, 2)
            self.assertEqual((self.root / "mesh/external-actions").read_text().splitlines(), ["action"])
            (self.root / "mesh/omp-mode").write_text("settle-effect")
            self.assertEqual(self.call().returncode, 0)
            self.assertEqual((self.root / "mesh/external-actions").read_text().splitlines(), ["action", "action"])
        finally:
            if child.poll() is None:
                child.kill()
                child.wait()
            with contextlib.suppress(Exception):
                child.stdout.close()
                child.stderr.close()

    def test_event_identity_mismatch(self):
        self.event.write_text(json.dumps({"channel": "pub", "request_id": "req1"}))
        self.assertEqual(self.call().returncode, 2)
        self.assertFalse((self.root / "mesh/mishe-mind/synthetic/req1.json").exists())

    def test_verified_wip_pointer_reaches_recovery_prompt(self):
        commit = self.create_wip_ref()
        result = self.call()
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads((self.root / "mesh/mishe-mind/synthetic/req1.json").read_text())
        self.assertEqual(record["wip_commit"], commit)
        self.assertIn("refs/wip/synthetic " + commit, (self.root / "mesh/omp-prompt").read_text())

    def test_witness_uses_explicit_luna_and_requires_disposition_receipt(self):
        core = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))
        self.env.update(MESH_MISHE_CORE=str(core), MESH_MISHE_REAL_ALLOWLIST="witness",
                        MESH_MISHE_WITNESS_MODEL="openai-codex/gpt-6-luna",
                        MESH_MISHE_SINK=str(SCRIPT.with_name("mesh-mishe-mind-sink")))
        self.env["MESH_MISHE_DASH_CMD"] = str(self.helper("witness-dash", "print('PRIVATE-witness-chat-tail')"))
        (self.root / "core/handoffs/witness.md").write_text("PRIVATE-prior-handoff\n")
        (self.root / "mesh/charter/witness.md").write_text("Check source-backed signals.\n")
        self.auth = self.helper("authority", "print('{\"authority\":\"mishe\",\"generation\":1,\"active_feed_seq\":0}')")
        self.env["MESH_MISHE_AUTHORITY_CMD"] = str(self.auth)
        feed = subprocess.run([sys.executable, "-c",
                               "from mishe_tauftauf.feed import Feed; import sys; "
                               "f=Feed(sys.argv[1]); s=f.append_runtime('observation/witness','STATE: RED\\nOBSERVATION: source=top-pane/witness freshness=stale value-coverage=unknown'); "
                               "f.append_runtime('mishe-tauftauf',f'judged relevance for top-pain witness on entry {s.sequence}: yes probability=0.8 question-version=1 policy-version=1'); "
                               "f.append_runtime('mishe-tauftauf',f'judged desired-state-met for top-pain witness on entry {s.sequence}: no probability=0.1 question-version=1 policy-version=1'); "
                               "f.append_runtime('mishe-tauftauf',f'entry {s.sequence} for top-pain witness: wake'); "
                               "r=f.append_runtime('mishe-tauftauf',f'wake requested top-pain witness for entry {s.sequence}'); "
                               "print(s.sequence,r.sequence)", str(self.root / "core")],
                              env={**self.env, "PYTHONPATH": str(core / "src")},
                              capture_output=True, text=True, check=True)
        stimulus, request = map(int, feed.stdout.split())
        request_id = f"witness-g1-r{request}"
        self.event.write_text(json.dumps({"channel": "witness", "request_id": request_id,
                                          "source": "observation/witness", "generation": 1,
                                          "outbox_key": f"witness:1:{request}", "stimulus_seq": stimulus}))
        outbox = self.root / "core/outbox/witness" / f"1-{request}.json"
        outbox.parent.mkdir(parents=True)
        outbox.write_text(json.dumps({"channel": "witness", "generation": 1,
                                      "request_id": request, "key": f"witness:1:{request}",
                                      "status": "claimed"}))
        self.omp = self.helper("omp-witness", """
import json,os,sys
from pathlib import Path
root=Path(os.environ['MESH_DIR']); home=Path(os.environ['MESH_MISHE_HOME'])
token=os.environ['MESH_MISHE_INVOCATION']
(root/'omp-args').write_text(json.dumps(sys.argv[1:-1]))
(root/'omp-prompt').write_text(sys.argv[-1])
(root/'omp-calls').open('a').write(token+'\\n')
(home/'handoffs/witness.md').write_text('invocation:'+token)
(root/'chat.log').open('a').write('[fyi] invocation:'+token+' disposition=non-actionable\\n')
if not (root/'omit-receipt').exists():
    evidence=home/'evidence.txt'; evidence.write_text('checked source invocation:'+token)
    p=home/'mind-dispositions/witness'/(token+'.json'); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps({'channel':'witness','request_id':token,'disposition':'non-actionable',
                             'task_id':None,'evidence':str(evidence)}))
""")
        self.env["MESH_MISHE_OMP_CMD"] = str(self.omp)
        command = [sys.executable, str(SCRIPT), "--channel", "witness", "--request-id", request_id,
                   "--event-file", str(self.event)]
        (self.root / "mesh/omit-receipt").write_text("yes")
        first = subprocess.run(command, env=self.env, capture_output=True, text=True)
        self.assertEqual(first.returncode, 2)
        self.assertIn("mind-dispositions", first.stderr)
        (self.root / "mesh/omit-receipt").unlink()
        retry = subprocess.run(command, env=self.env, capture_output=True, text=True)
        self.assertEqual(retry.returncode, 2)
        self.assertIn("prior witness invocation unresolved", retry.stderr)
        self.assertEqual((self.root / "mesh/omp-calls").read_text().splitlines(), [request_id])
        self.assertIn("--model=openai-codex/gpt-6-luna", json.loads((self.root / "mesh/omp-args").read_text()))
        prompt = (self.root / "mesh/omp-prompt").read_text()
        self.assertNotIn("PRIVATE-witness-chat-tail", prompt)
        self.assertNotIn("PRIVATE-prior-handoff", prompt)
        self.assertIn("STATE: RED", prompt)
        evidence = self.root / "core/evidence.txt"
        evidence.write_text("checked source invocation:" + request_id)
        receipt = self.root / "core/mind-dispositions/witness" / f"{request_id}.json"
        receipt.parent.mkdir(parents=True)
        receipt.write_text(json.dumps({"channel": "witness", "request_id": request_id,
                                       "disposition": "non-actionable", "task_id": None,
                                       "evidence": str(evidence)}))
        recovered = subprocess.run(command, env=self.env, capture_output=True, text=True)
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        record = json.loads((self.root / "mesh/mishe-mind/witness" / f"{request_id}.json").read_text())
        self.assertEqual((record["status"], record["disposition"]), ("settled", "non-actionable"))
        self.assertEqual((self.root / "mesh/omp-calls").read_text().splitlines(), [request_id])


if __name__ == "__main__":
    unittest.main()
