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
        (self.root / "mesh/charter/cleaner.md").write_text("Clean safely.\n")
        self.event = self.root / "event.json"
        self.event.write_text(json.dumps({"channel": "cleaner", "request_id": "req1", "kind": "task"}))
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
    print(f'  1. demo/do [{state}] owner=cleaner' + (' artifact=' + str(Path(os.environ['MESH_DIR'])/'artifact') if state=='done' else ''))
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
    (Path(os.environ['MESH_MISHE_HOME'])/'handoffs/cleaner.md').write_text('invocation:'+token)
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
        args = [sys.executable, str(SCRIPT), "--channel", "cleaner", "--request-id", "req1",
                "--event-file", str(self.event)]
        if task:
            args += ["--task-id", "demo/do"]
        return args

    def call(self, task=False):
        return subprocess.run(self.command(task), env=self.env, capture_output=True, text=True, timeout=20)

    def check(self):
        return subprocess.run([sys.executable, str(SCRIPT), "--check", "cleaner"],
                              env=self.env, capture_output=True, text=True, timeout=5)

    def create_wip_ref(self):
        def git(*args):
            return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                                  capture_output=True, text=True).stdout.strip()
        git("init", "-q")
        git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-qm", "base")
        commit = git("rev-parse", "HEAD")
        git("update-ref", "refs/wip/cleaner", commit)
        return commit

    def test_noop_receipt_and_repeat(self):
        self.assertIn("DISABLED", self.check().stdout)
        first = self.call()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.call().returncode, 0)
        record = json.loads((self.root / "mesh/mishe-mind/cleaner/req1.json").read_text())
        self.assertEqual(record["status"], "settled")
        self.assertIn("input_sha256", record)
        self.assertIn("PASS", self.check().stdout)

    def test_task_claim_and_verified_artifact(self):
        result = self.call(task=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "mesh/task-state").read_text(), "done")

    def test_no_handoff_is_incomplete_then_recovered(self):
        (self.root / "mesh/omp-mode").write_text("no-handoff")
        first = self.call()
        self.assertEqual(first.returncode, 2)
        self.assertIn("handoffs/cleaner.md", first.stderr)
        self.assertEqual(json.loads((self.root / "mesh/mishe-mind/cleaner/req1.json").read_text())["status"], "running")
        self.assertEqual(self.check().returncode, 2)
        self.assertIn("orphan invocation", self.check().stdout)
        (self.root / "mesh/omp-mode").write_text("settle")
        self.assertEqual(self.call().returncode, 0)

    def test_missing_board_receipt_keeps_unknown(self):
        (self.root / "mesh/omp-mode").write_text("no-handoff")
        handoff = self.root / "core/handoffs/cleaner.md"
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
            self.assertIn("refs/wip/cleaner " + commit, (self.root / "mesh/omp-prompt").read_text())
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
        self.assertFalse((self.root / "mesh/mishe-mind/cleaner/req1.json").exists())

    def test_verified_wip_pointer_reaches_recovery_prompt(self):
        commit = self.create_wip_ref()
        result = self.call()
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads((self.root / "mesh/mishe-mind/cleaner/req1.json").read_text())
        self.assertEqual(record["wip_commit"], commit)
        self.assertIn("refs/wip/cleaner " + commit, (self.root / "mesh/omp-prompt").read_text())


if __name__ == "__main__":
    unittest.main()
