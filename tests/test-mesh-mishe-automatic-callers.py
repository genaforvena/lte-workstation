#!/usr/bin/env python3
"""Every inventoried automatic tell caller opts into the destination fence."""
import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AutomaticCallerTest(unittest.TestCase):
    def test_inventory_is_fenced_and_manual_ingress_is_distinct(self):
        result = subprocess.run([str(ROOT / "scripts/mesh-mishe-channels"), "--json"],
                                text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        callers = json.loads(result.stdout)["direct_callers"]
        self.assertGreaterEqual(len(callers), 20)
        for item in callers:
            source = Path(item["path"]).read_text(encoding="utf-8")
            if item["class"] in ("manual control", "operator ingress"):
                self.assertNotIn("export MESH_TELL_AUTOMATIC=1", source, item["path"])
            else:
                self.assertTrue("export MESH_TELL_AUTOMATIC=1" in source or "--automatic" in source,
                                item["path"])


if __name__ == "__main__":
    unittest.main()
