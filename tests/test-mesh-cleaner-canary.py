#!/usr/bin/env python3
"""Tool-free cleaner proposal can only reach the keyed synthetic gateway."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/cleaner/mesh-cleaner-canary"


class Canary(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.root, self.state = base / "repo", base / "state"
        (self.root / ".firecrawl").mkdir(parents=True)
        self.state.mkdir()
        self.source = self.root / ".firecrawl/old.json"
        self.source.write_text('{"generated":true}\n')
        stamp = time.time() - 7200
        os.utime(self.source, (stamp, stamp))
        st = self.source.stat()
        row = {"path": ".firecrawl/old.json", "reasons": ["disposable-generated"],
               "device_inode": f"{st.st_dev}:{st.st_ino}",
               "mtime_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(st.st_mtime)),
               "active_refs": [], "owner_refs": [], "task_refs": []}
        self.manifest = base / "manifest.json"
        self.manifest.write_text(json.dumps({"version": 1, "scan_id": "synthetic-1", "candidates": [row]}))
        self.omp = base / "omp"
        self.omp.write_text("#!/usr/bin/env python3\nimport os,sys\nfrom pathlib import Path\n"
                            "assert '--no-tools' in sys.argv and '--no-extensions' in sys.argv\n"
                            "Path(os.environ['CANARY_CALLS']).open('a').write('called\\n')\n"
                            "print(os.environ['CANARY_PROPOSAL'])\n")
        self.omp.chmod(0o755)
        self.env = dict(os.environ, MESH_CLEANER_OMP_CMD=str(self.omp),
                        CANARY_CALLS=str(base / "calls"),
                        CANARY_PROPOSAL=json.dumps({"version": 1, "action": "quarantine", "path": row["path"]}))

    def run_canary(self, *, fault=None):
        env = dict(self.env)
        if fault:
            env["MESH_CLEANER_ACTION_FAULT"] = fault
        return subprocess.run([sys.executable, str(SCRIPT), "--synthetic-root", str(self.root),
                               "--state-dir", str(self.state), "--manifest", str(self.manifest),
                               "--request-id", "req1"], capture_output=True, text=True, timeout=10, env=env)

    def test_typed_proposal_executes_once_and_reuses_receipt(self):
        first = self.run_canary()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)["status"], "delivered")
        again = self.run_canary()
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual((Path(self.env["CANARY_CALLS"])).read_text().splitlines(), ["called"])
        self.assertEqual(len(list((self.state / "quarantine").rglob("old.json"))), 1)

    def test_kill_after_action_recovers_without_second_mind_or_move(self):
        killed = self.run_canary(fault="kill-after-move")
        self.assertEqual(killed.returncode, 3)
        self.assertFalse(self.source.exists())
        again = self.run_canary()
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(Path(self.env["CANARY_CALLS"]).read_text().splitlines(), ["called"])
        self.assertEqual(len(list((self.state / "quarantine").rglob("old.json"))), 1)

    def test_invalid_or_protected_proposal_never_moves(self):
        self.env["CANARY_PROPOSAL"] = json.dumps({"version": 1, "action": "shell", "path": ".firecrawl/old.json"})
        invalid = self.run_canary()
        self.assertEqual(invalid.returncode, 3)
        self.assertTrue(self.source.exists())
        self.env["CANARY_PROPOSAL"] = json.dumps({"version": 1, "action": "quarantine", "path": "scripts/protected.json"})
        protected = self.run_canary()
        self.assertEqual(protected.returncode, 3)
        self.assertTrue(self.source.exists())

    def test_hold_proposal_has_no_action(self):
        self.env["CANARY_PROPOSAL"] = json.dumps({"version": 1, "action": "hold"})
        result = self.run_canary()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "held")
        self.assertTrue(self.source.exists())


if __name__ == "__main__":
    unittest.main()
