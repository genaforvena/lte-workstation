#!/usr/bin/env python3
"""Read-only live admission adapters, exercised with deterministic command fixtures."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class EligibilityTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.probe = self.root / "staffing"
        self.probe.write_text("#!/usr/bin/env python3\nimport json,os,sys,datetime\n"
                              "kind=os.path.basename(sys.argv[0]); a=sys.argv[1:]\n"
                              "if kind=='staffing':\n"
                              " print(json.dumps({'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'windows':[{'window':'cleaner','live':True,'protected':os.environ.get('PROTECTED')=='1','active_holds':int(os.environ.get('HOLDS','0')),'eligible':True,'reason':os.environ.get('STAFF_REASON','eligible')}]})); sys.exit(0)\n"
                              "if kind=='mind': print(os.environ.get('MIND_STATE','IDLE')); sys.exit(0)\n"
                              "if kind=='task': sys.exit(int(os.environ.get('TASK_RC','0')))\n"
                              "if kind=='pace': sys.exit(int(os.environ.get('PACE_RC','0')))\n")
        self.probe.chmod(0o755)
        for kind in ("mind", "task", "pace"):
            (self.root / kind).symlink_to(self.probe)
        self.env = {**os.environ, "MESH_MISHE_STAFFING_BIN": str(self.root / "staffing"),
                    "MESH_MISHE_MIND_STATE_BIN": str(self.root / "mind"),
                    "MESH_MISHE_TASK_BIN": str(self.root / "task"),
                    "MESH_MISHE_PACE_BIN": str(self.root / "pace"),
                    "MESH_WAKE_STAMP_DIR": str(self.root)}

    def check(self, kind="telemetry", task=None):
        args = [str(ROOT / "scripts/mesh-mishe-eligibility"), "cleaner", kind]
        if task:
            args.append(task)
        return subprocess.run(args, env=self.env, text=True, capture_output=True)

    def test_idle_telemetry_and_exact_task_admit(self):
        self.assertEqual(json.loads(self.check().stdout)["status"], "eligible")
        self.assertEqual(json.loads(self.check("task", "chain-step").stdout)["status"], "eligible")
        self.env["TASK_RC"] = "2"
        self.assertEqual(json.loads(self.check("task", "chain-step").stdout)["status"], "held")
        self.assertEqual(json.loads(self.check("task").stdout)["status"], "unknown")

    def test_protected_busy_refractory_and_pace_hold(self):
        self.env["PROTECTED"] = "1"
        self.assertEqual(json.loads(self.check().stdout)["status"], "refused")
        self.env.pop("PROTECTED")
        self.env["MIND_STATE"] = "WORKING"
        self.assertEqual(json.loads(self.check().stdout)["reason"], "mind-busy")
        self.env["MIND_STATE"] = "IDLE"
        (self.root / ".wake-stamp-cleaner").touch()
        self.assertEqual(json.loads(self.check().stdout)["reason"], "refractory")
        self.env["MESH_WAKE_REFRACTORY"] = "0"
        self.env["PACE_RC"] = "1"
        self.assertEqual(json.loads(self.check("self-pick").stdout)["reason"], "pace")

    def test_unreadable_evidence_is_unknown(self):
        self.env["MIND_STATE"] = "UNRECOGNIZED"
        self.assertEqual(self.check().returncode, 2)
        self.env["MIND_STATE"] = "IDLE"
        self.env["STAFF_REASON"] = "human-owned"
        self.assertEqual(json.loads(self.check().stdout)["status"], "refused")


if __name__ == "__main__":
    unittest.main()
