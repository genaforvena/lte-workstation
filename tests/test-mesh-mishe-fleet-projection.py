#!/usr/bin/env python3
"""Privacy and event stability gate for roster channel projections."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "scripts/mesh-mishe-project"
loader = importlib.machinery.SourceFileLoader("mesh_mishe_project", str(PROJECT))
spec = importlib.util.spec_from_loader(loader.name, loader)
projection = importlib.util.module_from_spec(spec)
loader.exec_module(projection)


class FleetProjectionTest(unittest.TestCase):
    def test_private_fixture_bytes_never_enter_projection(self):
        for channel in projection.CHANNEL_ROLES:
            with self.subTest(channel=channel):
                secret = f"PRIVATE-{channel}-fixture-ε".encode()
                pane = ("MISHE-STATE: RED\nMISHE-SOURCE: top-pane\nPrivate conversation and credential: " + secret.decode()
                        + "\n-- pane live 2026-09-23T12:00:00Z --\n")
                output = projection.fleet_projection(channel, pane).encode()
                self.assertNotIn(secret, output)
                self.assertIn(b"STATE: RED", output)
                self.assertLess(len(output), 200)

    def test_chrome_does_not_create_event(self):
        a = "MISHE-STATE: RED\nMISHE-SOURCE: top-pane\nsecret one\n-- pane live first --\n"
        b = "MISHE-STATE: RED\nMISHE-SOURCE: top-pane\nsecret two\n-- pane live second --\n"
        self.assertEqual(projection.fleet_projection("tg", a), projection.fleet_projection("tg", b))

    def test_keyed_change_strips_clock_but_tracks_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            key = Path(tmp) / "projection.key"
            key.write_bytes(b"x" * 32)
            key.chmod(0o600)
            with patch.dict(os.environ, {"MESH_MISHE_HOME": tmp}):
                a = "MISHE-STATE: UNKNOWN\nMISHE-SOURCE: top-pane\nprivate fixture X\n-- pane live 2026-09-23T12:00:00Z · 30s · ticks every frame --\n"
                b = "MISHE-STATE: UNKNOWN\nMISHE-SOURCE: top-pane\nprivate fixture X\n-- pane live 2026-09-23T12:01:00Z · 30s · ticks every frame --\n"
                c = b.replace("fixture X", "fixture Y")
                first = projection.fleet_projection("pub", a)
                self.assertEqual(first, projection.fleet_projection("pub", b))
                self.assertNotEqual(first, projection.fleet_projection("pub", c))
                self.assertNotIn("fixture", first)
                key.chmod(0o644)
                self.assertNotIn("view-change=", projection.fleet_projection("pub", a))

    def test_ambiguous_or_missing_marker_is_unknown(self):
        for pane in ("private text\n", "private text\nMISHE-STATE: RED\n",
                     "MISHE-STATE: BAD\n"):
            self.assertEqual(projection.fleet_projection("vpn", pane), "STATE: UNKNOWN\n")

    def test_cli_rejects_unenrolled_channel(self):
        with tempfile.TemporaryDirectory() as tmp:
            frame = Path(tmp) / "frame"
            frame.write_text("MISHE-STATE: RED\nMISHE-SOURCE: top-pane\n")
            result = subprocess.run([str(PROJECT), "--channel", "private-extra", str(frame), str(frame)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)

    def test_renderer_binds_health_to_check_role(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "scripts"
            scripts.mkdir()
            dash = scripts / "mesh-dash"
            dash.write_text("#!/bin/sh\nprintf 'role=%s\\n' \"$2\"\n")
            dash.chmod(0o755)
            env = {**os.environ, "MESH_REPO": tmp}
            good = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), "health", "check"],
                                  env=env, capture_output=True, text=True)
            self.assertEqual((good.returncode, good.stdout), (0, "MISHE-STATE: UNKNOWN\nMISHE-SOURCE: dashboard\nrole=check\n"))
            bad = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), "tg", "check"],
                                 env=env, capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2)
            self.assertEqual(bad.stdout, "")

    def test_pane_capture_rejects_stale_or_unowned_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmux = Path(tmp) / "tmux"
            tmux.write_text("#!/bin/sh\n"
                            "if [ \"$1\" = display-message ]; then printf '%s\\n' \"$MOCK_META\"; "
                            "else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            secret = "fixture-private-operator-message"
            pane = secret + "\n-- pane live " + stamp + " · 30s · ticks every frame --"
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_RENDER_SOURCE": "pane", "MESH_MISHE_SESSION": "fixture",
                   "MESH_MISHE_HOME": tmp, "MOCK_META": 'tg|0|0|"exec /safe/mesh-dash tg"',
                   "MOCK_PANE": pane}
            render = ROOT / "scripts/mesh-mishe-render"
            good = subprocess.run([str(render), "tg", "tg"], env=env, capture_output=True, text=True)
            self.assertEqual(good.returncode, 0)
            self.assertIn("MISHE-SOURCE: top-pane", good.stdout)
            self.assertTrue((Path(tmp) / ".mesh-mishe-seen-tg").exists())
            stale = subprocess.run([str(render), "tg", "tg"],
                                   env={**env, "MOCK_PANE": pane.replace(stamp, "2020-01-01T00:00:00Z")},
                                   capture_output=True, text=True)
            self.assertIn("MISHE-SOURCE: unavailable", stale.stdout)
            self.assertNotIn(secret, stale.stdout)
            wrong = subprocess.run([str(render), "tg", "tg"],
                                   env={**env, "MOCK_META": 'tg|0|0|"exec /safe/mesh-dash pub"'},
                                   capture_output=True, text=True)
            self.assertIn("MISHE-SOURCE: unavailable", wrong.stdout)
            self.assertNotIn(secret, wrong.stdout)

    def test_enrollment_uses_checked_roster(self):
        core = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))
        if not (core / "src/mishe_tauftauf/__main__.py").exists():
            self.skipTest("public core absent")
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "core"
            roster = Path(tmp) / "roster.json"
            env = {**os.environ, "MESH_MISHE_HOME": str(home), "MESH_MISHE_CORE": str(core),
                   "MESH_MISHE_PYTHON": "python3", "MESH_REPO": str(ROOT),
                   "MESH_MISHE_ROSTER_JSON": str(roster)}
            run = ROOT / "scripts/mesh-mishe-run"
            init = subprocess.run([str(run), "init"], env=env, capture_output=True, text=True)
            self.assertEqual(init.returncode, 0, init.stderr)
            data = {"status": "PASS", "channels": [
                {"channel": "health", "renderer_role": "check", "state": "active", "poll_seconds": 60},
                {"channel": "tg", "renderer_role": "tg", "state": "active", "poll_seconds": 60},
                {"channel": "tiny-fleet", "renderer_role": None, "state": "configured-inactive"}]}
            roster.write_text(json.dumps(data))
            enrolled = subprocess.run([str(run), "enroll-fleet"], env=env, capture_output=True, text=True)
            self.assertEqual(enrolled.returncode, 0, enrolled.stderr)
            self.assertTrue((home / "top-pains/health").exists())
            self.assertTrue((home / "projectors/tg").exists())
            self.assertFalse((home / "top-pains/tiny-fleet").exists())
            self.assertEqual((home / "projection.key").stat().st_mode & 0o777, 0o600)
            (home / ".fleet-shadow-hold").write_text("profile pending\n")
            feed_before = (home / "feed").read_bytes()
            held = subprocess.run([str(run), "once"], env=env, capture_output=True, text=True)
            self.assertEqual(held.returncode, 0)
            self.assertIn("fleet shadow held", held.stdout)
            self.assertEqual((home / "feed").read_bytes(), feed_before)
            self.assertEqual(subprocess.run([str(run), "--freshness"], env=env, capture_output=True).returncode, 2)
            for channel in ("health", "tg"):
                (home / f".mesh-mishe-seen-{channel}").write_text(str(time.time_ns()))
            self.assertEqual(subprocess.run([str(run), "--freshness"], env=env, capture_output=True).returncode, 0)
            data["channels"][1]["renderer_role"] = "check"
            roster.write_text(json.dumps(data))
            refused = subprocess.run([str(run), "enroll-fleet"], env=env, capture_output=True, text=True)
            self.assertEqual(refused.returncode, 1)
            self.assertIn("unrecognized channel/renderer", refused.stderr)

    def test_private_bytes_do_not_reach_core_feed(self):
        core = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))
        if not (core / "src/mishe_tauftauf/__main__.py").exists():
            self.skipTest("public core absent")
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = {**os.environ, "PYTHONPATH": str(core / "src"), "MESH_MISHE_HOME": str(home)}
            base = ["python3", "-m", "mishe_tauftauf", "--home", str(home)]
            init = subprocess.run([*base, "init"], env=env, capture_output=True, text=True)
            self.assertEqual(init.returncode, 0, init.stderr)
            (home / "projection.key").write_bytes(b"x" * 32)
            (home / "projection.key").chmod(0o600)
            private = ("tg", "tg-roz", "pub", "vpn", "health", "job", "witness")
            secrets = []
            for channel in private:
                secret = "fixture-private-" + channel + "-α"
                secrets.append(secret.encode())
                renderer = home / "top-pains" / channel
                renderer.write_text("#!/bin/sh\nprintf '%s\\n' 'MISHE-STATE: UNKNOWN' 'MISHE-SOURCE: top-pane' '" + secret + "'\n")
                renderer.chmod(0o755)
                projector = home / "projectors" / channel
                projector.write_text("#!/bin/sh\nexec '" + str(PROJECT) + "' --channel " + channel + " \"$@\"\n")
                projector.chmod(0o755)
            run = subprocess.run([*base, "run", "--once", "--launcher", "headless", "--observe-only"],
                                 env=env, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            feed = (home / "feed").read_bytes()
            for secret in secrets:
                self.assertNotIn(secret, feed)
            self.assertIn(b"STATE: UNKNOWN", feed)


if __name__ == "__main__":
    unittest.main()
