#!/usr/bin/env python3
"""Automatic tells obey authority; deliberate manual tells remain possible."""
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))


class AutomaticTellTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.bin = self.home / "bin"
        self.bin.mkdir()
        self.calls = self.home / "calls"
        tmux = self.bin / "tmux"
        tmux.write_text("#!/bin/sh\n"
                        "case \"$1\" in\n"
                        "  list-panes) printf '0 0\\n'; exit 0 ;;\n"
                        f"  send-keys) printf 'send\\n' >> '{self.calls}'; exit 1 ;;\n"
                        "  capture-pane) exit 0 ;;\n"
                        "esac\nexit 1\n")
        tmux.chmod(0o755)
        self.env = {**os.environ, "PATH": str(self.bin) + ":" + os.environ["PATH"],
                    "MESH_MISHE_HOME": str(self.home / "mishe"), "MESH_MISHE_CORE": str(CORE),
                    "MESH_TELL_ALLOW_SHELL": "1", "MESH_TELL_WAL": str(self.home / "wal")}
        subprocess.run(["python3", "-c", "from mishe_tauftauf.feed import Feed; import sys; Feed(sys.argv[1]).append_runtime('mishe-tauftauf','shadow')", str(self.home / "mishe")],
                       env={**self.env, "PYTHONPATH": str(CORE / "src")}, check=True)
        switched = subprocess.run([str(ROOT / "scripts/mesh-mishe-authority"), "switch", "synthetic",
                                   "--to", "mishe", "--expect-generation", "0", "--feed-seq", "1"],
                                  env=self.env, capture_output=True)
        self.assertEqual(switched.returncode, 0, switched.stderr)

    def tell(self, *args):
        return subprocess.run([str(ROOT / "scripts/mesh-tell"), *args], env=self.env,
                              text=True, capture_output=True, timeout=20)

    def test_automatic_fenced_and_manual_send_kept_distinct(self):
        clear_calls = self.home / "clear-calls"
        clear = self.bin / "mesh-clear"
        clear.write_text(f"#!/bin/sh\nprintf 'clear\\n' >> '{clear_calls}'\n")
        clear.chmod(0o755)
        automatic = self.tell("--automatic", "synthetic", "fixture")
        self.assertNotEqual(automatic.returncode, 0)
        self.assertFalse(self.calls.exists())
        self.assertNotEqual(self.tell("--automatic", "--fresh", "synthetic", "fixture").returncode, 0)
        self.assertFalse(clear_calls.exists(), "fenced automatic tell cleared the destination")
        manual = self.tell("synthetic", "fixture")
        self.assertTrue(self.calls.exists(), manual.stderr)

    def test_switch_waits_for_automatic_send_lock(self):
        rollback = subprocess.run([str(ROOT / "scripts/mesh-mishe-authority"), "switch", "synthetic",
                                   "--to", "legacy", "--expect-generation", "1", "--feed-seq", "1"],
                                  env=self.env, capture_output=True)
        self.assertEqual(rollback.returncode, 0, rollback.stderr)
        entered = self.home / "lifecycle-entered"
        release = self.home / "lifecycle-release"
        lifecycle = self.bin / "mesh-codex-lifecycle"
        lifecycle.write_text(f"#!/bin/sh\ntouch '{entered}'\n"
                             f"while [ ! -f '{release}' ]; do sleep 0.05; done\nexit 0\n")
        lifecycle.chmod(0o755)
        private_prompt = "fixture-private-operator-text"
        tell = subprocess.Popen([str(ROOT / "scripts/mesh-tell"), "--automatic", "synthetic", private_prompt],
                                env=self.env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            for _ in range(100):
                if entered.exists():
                    break
                time.sleep(0.02)
            self.assertTrue(entered.exists(), "automatic tell never acquired fence")
            change = subprocess.Popen([str(ROOT / "scripts/mesh-mishe-authority"), "switch", "synthetic",
                                       "--to", "mishe", "--expect-generation", "2", "--feed-seq", "1"],
                                      env=self.env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                time.sleep(0.2)
                self.assertIsNone(change.poll(), "authority switched while legacy send held lock")
                release.touch()
                tell.communicate(timeout=15)
                _, error = change.communicate(timeout=15)
                self.assertEqual(change.returncode, 0, error)
                self.assertTrue(self.calls.exists(), "legacy send was lost before switch")
                records = list((self.home / "mishe/automatic-events/events").glob("*.json"))
                self.assertEqual(len(records), 1)
                self.assertNotIn(private_prompt, records[0].read_text())
                imported = subprocess.run([str(ROOT / "scripts/mesh-mishe-auto-events"), "import", "synthetic"],
                                          env=self.env, text=True, capture_output=True)
                self.assertEqual(imported.returncode, 0, imported.stderr)
                self.assertNotIn(private_prompt, (self.home / "mishe/feed").read_text())
            finally:
                if change.poll() is None:
                    change.kill()
                    change.communicate()
        finally:
            release.touch()
            if tell.poll() is None:
                tell.kill()
                tell.communicate()


if __name__ == "__main__":
    unittest.main()
