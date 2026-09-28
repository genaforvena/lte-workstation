#!/usr/bin/env python3
"""A shared Tiny Fleet run root must have at most one live matrix writer."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts/mesh-study-duplicate-check"
RUNNER = "/fleet/scripts/run_study_matrix.py"


class DuplicateCheckTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.proc = Path(self.temp.name)

    def worker(self, pid, run_root, runner=RUNNER):
        entry = self.proc / str(pid)
        entry.mkdir()
        argv = ["/fleet/.venv/bin/python", runner, "--registration", "/fleet/registration.json",
                "--run-root", run_root]
        (entry / "cmdline").write_bytes(b"\0".join(x.encode() for x in argv) + b"\0")

    def check(self):
        return subprocess.run([str(CHECK)], capture_output=True, text=True,
                              env={**os.environ, "MESH_STUDY_DUP_PROC_ROOT": str(self.proc),
                                   "MESH_STUDY_DUP_RUNNER": RUNNER})

    def test_same_run_root_is_failure(self):
        self.worker(101, "/fleet/runs/study")
        self.worker(102, "/fleet/runs/study")
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("count=2", result.stdout)
        self.assertIn("/fleet/runs/study", result.stdout)

    def test_distinct_roots_are_not_duplicates(self):
        self.worker(101, "/fleet/runs/study-a")
        self.worker(102, "/fleet/runs/study-b")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unrelated_runner_is_not_counted(self):
        self.worker(101, "/fleet/runs/study")
        self.worker(102, "/fleet/runs/study", "/other/scripts/run_study_matrix.py")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_long_unrelated_command_is_not_unknown(self):
        self.worker(101, "/fleet/runs/study")
        entry = self.proc / "102"
        entry.mkdir()
        (entry / "cmdline").write_bytes(b"python3\0-c\0" + b"x" * 9000 + b"\0")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_oversized_process_command_is_unknown(self):
        entry = self.proc / "101"
        entry.mkdir()
        (entry / "cmdline").write_bytes(b"x" * 8193)
        result = self.check()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("UNKNOWN", result.stdout)


if __name__ == "__main__":
    unittest.main()
