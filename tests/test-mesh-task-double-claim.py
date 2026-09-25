#!/usr/bin/env python3
import importlib.machinery
import importlib.util
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"
import sys
sys.path.insert(0, str(ROOT / "scripts"))




class DoubleClaimGuardTests(unittest.TestCase):
    def test_live_lease_wins_over_stale_replay_before_taking_emit(self):
        with tempfile.TemporaryDirectory() as td:
            os.environ.update({
                "MESH_DIR": td,
                "MESH_TASK_DIR": str(Path(td) / "chains"),
                "MESH_TASK_ACTOR": "health",
            })
            loader = importlib.machinery.SourceFileLoader("mesh_task_double_claim", str(TASK))
            spec = importlib.util.spec_from_loader(loader.name, loader)
            module = importlib.util.module_from_spec(spec)
            loader.exec_module(module)
            data = {
                "version": 2,
                "chain": "demo",
                "status": "open",
                "current": 0,
                "steps": [{
                    "id": "demo/work", "slug": "work", "owner": "health",
                    "status": "open", "description": "work",
                }],
            }
            active = dict(data)
            active["status"] = "active"
            active["steps"] = [dict(data["steps"][0], status="active",
                                      lease_until=module.future())]
            module.load = lambda chain: (Path(td) / "demo.json", data)
            module.latest_chain_record = lambda chain: {"data": active, "revision": 2}
            module.require_emit = lambda *args: self.fail("duplicate [taking] emission")
            with redirect_stdout(io.StringIO()) as output:
                module.take("demo", "work")
            self.assertIn("already active demo/work", output.getvalue())
            self.assertEqual(data["steps"][0]["status"], "open")


if __name__ == "__main__":
    unittest.main()
