#!/usr/bin/env python3
"""Synthetic Mesh adapter contract against the public coordinator."""
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone


ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ["MESH_MISHE_CORE"]) if os.environ.get("MESH_MISHE_CORE") else None


class SyntheticAdapterTest(unittest.TestCase):
    def test_renderer_projection_and_observe_only_feed(self):
        if CORE is None or not (CORE / "src/mishe_tauftauf/__main__.py").is_file():
            self.skipTest("set MESH_MISHE_CORE to the Phase 1 public core worktree")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            home = base / "core"
            state = base / "synthetic-state"
            env = {**os.environ, "MESH_MISHE_HOME": str(home), "MESH_MISHE_CORE": str(CORE),
                   "MESH_MISHE_SYNTHETIC_FILE": str(state)}

            def adapter(name, *args):
                return subprocess.run([str(ROOT / "scripts" / name), *args], env=env,
                                      text=True, capture_output=True)

            init = adapter("mesh-mishe-run", "init")
            self.assertEqual(init.returncode, 0, init.stderr)
            self.assertTrue((home / "top-pains" / "synthetic").is_file())
            state.write_text("STATE: GREEN\nSECRET: fixture-private-1\n", encoding="utf-8")
            self.assertEqual(adapter("mesh-mishe-run", "once").returncode, 0)
            state.write_text("STATE: RED\nSECRET: fixture-private-2\n", encoding="utf-8")
            self.assertEqual(adapter("mesh-mishe-run", "once").returncode, 0)
            feed = (home / "feed").read_text(encoding="utf-8")
            self.assertIn("STATE: RED", feed)
            self.assertNotIn("fixture-private", feed)
            self.assertFalse((home / "minds" / "synthetic").exists())
            before = feed.count("STATE: RED")
            self.assertEqual(adapter("mesh-mishe-run", "once").returncode, 0)
            self.assertEqual((home / "feed").read_text(encoding="utf-8").count("STATE: RED"), before)
            stamp = (datetime.now(timezone.utc) + timedelta(seconds=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
            prediction = base / "prediction"
            prediction.write_text(f"Expected green.\nCheck at: {stamp}\n", encoding="utf-8")
            predicted = subprocess.run(["python3", "-m", "mishe_tauftauf", "--home", str(home),
                                        "predict", "synthetic", str(prediction)],
                                       env={**env, "PYTHONPATH": str(CORE / "src")},
                                       text=True, capture_output=True)
            self.assertEqual(predicted.returncode, 0, predicted.stderr)
            accepted = subprocess.run(["python3", "-c", "from mishe_tauftauf.feed import Feed; import sys; Feed(sys.argv[1]).append_runtime('mishe-tauftauf', 'prediction ' + sys.argv[2] + ': accepted')",
                                       str(home), predicted.stdout.strip()], env={**env, "PYTHONPATH": str(CORE / "src")},
                                      text=True, capture_output=True)
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            state.write_text("STATE: INTERMEDIATE\nSECRET: fixture-private-3\n", encoding="utf-8")
            self.assertEqual(adapter("mesh-mishe-run", "once").returncode, 0)
            time.sleep(2.2)
            self.assertEqual(adapter("mesh-mishe-run", "once").returncode, 0)
            feed = (home / "feed").read_text(encoding="utf-8")
            self.assertIn("prediction " + predicted.stdout.strip() + ": insufficient-evidence", feed)
            state.write_text("STATE: GREEN\nSECRET: fixture-private-4\n", encoding="utf-8")
            self.assertEqual(adapter("mesh-mishe-run", "once").returncode, 0)
            feed = (home / "feed").read_text(encoding="utf-8")
            self.assertNotIn("fixture-private", feed)
            self.assertIn("STATE: GREEN", feed)
            check = adapter("mesh-mishe-doctor")
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            env["MESH_MISHE_MAX_AGE"] = "0"
            stale = adapter("mesh-mishe-doctor")
            self.assertNotEqual(stale.returncode, 0)
            self.assertIn("stale", stale.stdout)
            env.pop("MESH_MISHE_MAX_AGE")
            with (home / "feed").open("a", encoding="utf-8") as stream:
                stream.write("broken feed framing\n")
            broken = adapter("mesh-mishe-doctor")
            self.assertNotEqual(broken.returncode, 0)
            self.assertIn("UNKNOWN", broken.stdout)

    def test_projection_fails_closed_for_unrecognized_or_missing_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            prev, current = base / "prev", base / "current"
            prev.write_text("STATE: GREEN\n", encoding="utf-8")
            current.write_text("SECRET: fixture-private\n", encoding="utf-8")
            result = subprocess.run([str(ROOT / "scripts/mesh-mishe-project"), str(prev), str(current)],
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn("UNKNOWN", result.stdout)
            self.assertNotIn("fixture-private", result.stdout)


if __name__ == "__main__":
    unittest.main()
