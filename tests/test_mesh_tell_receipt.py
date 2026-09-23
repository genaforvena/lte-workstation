import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


HELPER = Path(__file__).resolve().parents[1] / "scripts/mesh_tell_receipt.py"
TELL = Path(__file__).resolve().parents[1] / "scripts/mesh-tell"


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.env = dict(os.environ, MESH_TELL_RECEIPT_DIR=self.tmp.name)

    def call(self, *args):
        return subprocess.run(["python3", str(HELPER), *args], env=self.env, text=True, capture_output=True)

    def test_claim_replay_and_conflict(self):
        first = self.call("begin", "cleaner:1:req-a", "cleaner", "a" * 64)
        self.assertEqual(first.returncode, 0, first.stderr)
        token = first.stdout.strip()
        self.assertTrue(token)
        duplicate = self.call("begin", "cleaner:1:req-a", "cleaner", "a" * 64)
        self.assertEqual(duplicate.returncode, 3)
        self.assertEqual(json.loads(self.call("status", "cleaner:1:req-a").stdout)["status"], "unknown")
        self.assertEqual(self.call("begin", "cleaner:1:req-a", "cleaner", "b" * 64).returncode, 2)
        self.assertEqual(self.call("finish", "cleaner:1:req-a", "wrong", "delivered").returncode, 2)
        self.assertEqual(self.call("finish", "cleaner:1:req-a", token, "delivered").returncode, 0)
        self.assertEqual(json.loads(self.call("status", "cleaner:1:req-a").stdout)["status"], "delivered")
        self.assertEqual(self.call("finish", "cleaner:1:req-a", token, "refused").returncode, 2)

    def test_missing_and_ambiguous_claim(self):
        self.assertEqual(self.call("status", "cleaner:1:missing").returncode, 3)
        first = self.call("begin", "cleaner:1:req-b", "cleaner", "a" * 64)
        self.assertEqual(first.returncode, 0)
        self.assertEqual(self.call("status", "cleaner:1:req-b").returncode, 3)

    def test_tell_status_and_unsafe_mode_refusal(self):
        status = subprocess.run([str(TELL), "--idempotency-status", "cleaner:1:missing"], env=self.env, text=True, capture_output=True)
        self.assertEqual(status.returncode, 3)
        self.assertEqual(json.loads(status.stdout)["status"], "unknown")
        unsafe = subprocess.run([str(TELL), "--fresh", "--idempotency-key", "cleaner:1:req", "cleaner", "probe"], env=self.env, text=True, capture_output=True)
        self.assertEqual(unsafe.returncode, 2)
        self.assertEqual(list(Path(self.tmp.name).glob("*.json")), [])

    def test_failed_tmux_send_is_unknown_and_never_replayed(self):
        bindir = Path(self.tmp.name) / "bin"
        bindir.mkdir()
        calls = Path(self.tmp.name) / "send-calls"
        tmux = bindir / "tmux"
        tmux.write_text(
            "#!/bin/sh\n"
            "case \"$1\" in\n"
            "  list-panes) printf '0 0\\n'; exit 0 ;;\n"
            f"  send-keys) printf 'send\\n' >> '{calls}'; exit 1 ;;\n"
            "  capture-pane) exit 0 ;;\n"
            "esac\nexit 1\n", encoding="utf-8")
        tmux.chmod(0o755)
        lifecycle = bindir / "mesh-codex-lifecycle"
        lifecycle.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        lifecycle.chmod(0o755)
        env = dict(self.env, PATH=str(bindir) + ":" + os.environ["PATH"], MESH_TELL_ALLOW_SHELL="1",
                   MESH_TELL_WAL=str(Path(self.tmp.name) / "wal"))
        args = [str(TELL), "--idempotency-key", "cleaner:1:req-c", "cleaner", "harmless"]
        first = subprocess.run(args, env=env, text=True, capture_output=True)
        self.assertEqual(first.returncode, 3, first.stderr)
        self.assertEqual(json.loads(self.call("status", "cleaner:1:req-c").stdout)["status"], "unknown")
        before = calls.read_text(encoding="utf-8")
        again = subprocess.run(args, env=env, text=True, capture_output=True)
        self.assertEqual(again.returncode, 3)
        self.assertEqual(calls.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
