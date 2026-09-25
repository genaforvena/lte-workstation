#!/usr/bin/env python3
"""Privacy and event stability gate for roster channel projections."""
import importlib.machinery
import importlib.util
import hashlib
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
                pane = ("MISHE-STATE: UNKNOWN\nMISHE-SOURCE: top-pane\nMISHE-FRESHNESS: STALE\n"
                        "Private conversation and credential: " + secret.decode() + "\n")
                output = projection.fleet_projection(channel, pane).encode()
                self.assertNotIn(secret, output)
                self.assertIn(b"STATE: RED", output)
                self.assertLess(len(output), 200)

    def test_chrome_does_not_create_event(self):
        a = ("MISHE-STATE: UNKNOWN\nMISHE-SOURCE: top-pane\nMISHE-FRESHNESS: FRESH\n"
             "voice-rx UP | textin UP\nsecret one\n-- pane live first --\n")
        b = a.replace("secret one", "secret two").replace("live first", "live second")
        self.assertEqual(projection.fleet_projection("tg", a), projection.fleet_projection("tg", b))

    def test_keyed_change_strips_clock_but_tracks_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            key = Path(tmp) / "projection.key"
            key.write_bytes(b"x" * 32)
            key.chmod(0o600)
            with patch.dict(os.environ, {"MESH_MISHE_HOME": tmp}):
                a = "MISHE-STATE: UNKNOWN\nMISHE-SOURCE: top-pane\nMISHE-FRESHNESS: FRESH\nprivate fixture X\n-- pane live 2026-09-23T12:00:00Z · 30s · ticks every frame --\n"
                b = "MISHE-STATE: UNKNOWN\nMISHE-SOURCE: top-pane\nMISHE-FRESHNESS: FRESH\nprivate fixture X\n-- pane live 2026-09-23T12:01:00Z · 30s · ticks every frame --\n"
                c = b.replace("fixture X", "fixture Y")
                first = projection.fleet_projection("pub", a)
                self.assertEqual(first, projection.fleet_projection("pub", b))
                self.assertNotEqual(first, projection.fleet_projection("pub", c))
                self.assertNotIn("fixture", first)
                key.chmod(0o644)
                self.assertNotIn("view-change=", projection.fleet_projection("pub", a))

    def test_shared_pane_identity_is_private_and_uses_legacy_wake_rule(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / "projection.key").write_bytes(b"k" * 32)
            (home / "projection.key").chmod(0o600)
            rules = home / "rules"
            rules.mkdir()
            (rules / "tg").write_text("^status=")
            tick = "a" * 32
            secret = "fixture-private-operator-message"
            env = {**os.environ, "MESH_MISHE_HOME": tmp, "MESH_MISHE_TICK_ID": tick,
                   "MESH_WAKE_RULE_DIR": str(rules)}
            first = f"status=UP\n{secret}\n-- pane live 2026-09-23T12:00:00Z · 30s · ticks every frame --\n"
            second = first.replace(secret, "another-private-message").replace("12:00:00", "12:01:00")
            helper = ROOT / "scripts/mesh-pane-consume"
            def identity(frame):
                result = subprocess.run([str(helper), "--pane-identity", "tg"], input=frame,
                                        env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout.strip()
            expected = identity(first)
            self.assertEqual(identity(second), expected)
            self.assertEqual(len(expected), 64)
            frame = home / "frame"
            frame.write_text("MISHE-STATE: UNKNOWN\nMISHE-SOURCE: top-pane\nMISHE-FRESHNESS: FRESH\n" + first + "MISHE-END-PANE\n")
            projected = subprocess.run([str(PROJECT), "--channel", "tg", str(frame), str(frame)],
                                       env=env, capture_output=True, text=True)
            self.assertEqual(projected.returncode, 0, projected.stderr)
            staged = (home / "parity/staged/tg").read_bytes()
            self.assertEqual(json.loads(staged)["event_id"], expected)
            self.assertNotIn(secret.encode(), staged + projected.stdout.encode())

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
            self.assertIn("MISHE-SOURCE: top-pane\nMISHE-FRESHNESS: FRESH", good.stdout)
            self.assertTrue((Path(tmp) / ".mesh-mishe-seen-tg").exists())
            stale = subprocess.run([str(render), "tg", "tg"],
                                   env={**env, "MOCK_PANE": pane.replace(stamp, "2020-01-01T00:00:00Z")},
                                   capture_output=True, text=True)
            self.assertIn("MISHE-SOURCE: top-pane\nMISHE-FRESHNESS: STALE", stale.stdout)
            self.assertNotIn(secret, stale.stdout)
            malformed = subprocess.run([str(render), "tg", "tg"],
                                       env={**env, "MOCK_PANE": pane.replace("ticks every frame", "broken lease")},
                                       capture_output=True, text=True)
            self.assertIn("MISHE-SOURCE: unavailable\nMISHE-FRESHNESS: UNKNOWN", malformed.stdout)
            self.assertNotIn(secret, malformed.stdout)
            wrong = subprocess.run([str(render), "tg", "tg"],
                                   env={**env, "MOCK_META": 'tg|0|0|"exec /safe/mesh-dash pub"'},
                                   capture_output=True, text=True)
            self.assertIn("MISHE-SOURCE: unavailable\nMISHE-FRESHNESS: UNKNOWN", wrong.stdout)
            self.assertNotIn(secret, wrong.stdout)

    def test_each_non_witness_role_uses_real_source_age_not_repaint(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmux = Path(tmp) / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then "
                            "printf '%s\\n' \"$MOCK_META\"; else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            audit = Path(tmp) / "task-audit"
            audit.write_text("#!/bin/sh\nexit 0\n")
            audit.chmod(0o755)
            pane_epoch = int(time.time())
            stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(pane_epoch))
            pane = ("PRIVATE-goal-secret\nMISHE-VALUE: goal STALE\n"
                    f"-- pane live {stamp} · 30s · ticks every frame --")
            goal_dir = Path(tmp) / "goals"
            goal_dir.mkdir()
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_RENDER_SOURCE": "pane", "MESH_MISHE_HOME": tmp,
                   "MESH_MISHE_GOAL_DIR": str(goal_dir), "MESH_MISHE_SEMANTIC_DIR": tmp,
                   "MESH_MISHE_TASK_AUDIT_CMD": str(audit),
                   "MESH_MISHE_SESSION": "fixture", "MOCK_PANE": pane}
            for channel, role in projection.CHANNEL_ROLES.items():
                if channel in ("witness", "cleaner"):
                    continue
                with self.subTest(channel=channel):
                    source = "comments" if channel == "pub" else "goal"
                    current = goal_dir / (".pub-right.cache" if channel == "pub" else f".goal-{channel}.cache")
                    current.write_text("unchanged source")
                    os.utime(current, (pane_epoch - 10, pane_epoch - 10))
                    if channel == "pub":
                        env["MESH_MISHE_PUB_CACHE"] = str(current)
                    env["MOCK_META"] = f'{channel}|0|0|"exec /safe/mesh-dash {role}"'
                    fresh = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), channel, role],
                                           env=env, capture_output=True, text=True)
                    self.assertEqual(fresh.returncode, 0, fresh.stderr)
                    self.assertIn(f"MISHE-VALUE: {source} FRESH\n", fresh.stdout)
                    healthy = projection.fleet_projection(channel, fresh.stdout)
                    self.assertIn(f"{source}=fresh", healthy)
                    self.assertNotIn("STATE: RED", healthy)
                    old = time.time() - (1200 if channel == "pub" else 360)
                    os.utime(current, (old, old))
                    stale = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), channel, role],
                                           env=env, capture_output=True, text=True)
                    self.assertIn(f"MISHE-VALUE: {source} STALE\n", stale.stdout)
                    event = projection.fleet_projection(channel, stale.stdout)
                    self.assertIn("STATE: RED", event)
                    self.assertIn(f"{source}=stale", event)
                    self.assertNotIn("PRIVATE-goal-secret", event)
                    self.assertEqual(projection.fleet_projection(channel, stale.stdout), event)
                    current.write_text("unchanged source")
                    os.utime(current, (pane_epoch - 10, pane_epoch - 10))
                    recovered = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), channel, role],
                                               env=env, capture_output=True, text=True)
                    self.assertIn(f"{source}=fresh", projection.fleet_projection(channel, recovered.stdout))
                    current.unlink()
                    unknown = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), channel, role],
                                             env=env, capture_output=True, text=True)
                    self.assertIn(f"{source}=unknown", projection.fleet_projection(channel, unknown.stdout))


    def test_roz_intake_cursor_distinguishes_quiet_from_stalled_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmux = Path(tmp) / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then "
                            "printf '%s\\n' \"$MOCK_META\"; else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            directory = Path(tmp)
            (directory / ".goal-tg-roz.cache").write_text("goal")
            incoming = directory / "tg-strangers.log"
            incoming.write_text("private-old-line\n")
            offset = directory / ".roz-channel.offset"
            offset.write_text("1\n")
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_HOME": tmp, "MESH_MISHE_SEMANTIC_DIR": tmp,
                   "MESH_MISHE_GOAL_DIR": tmp, "MESH_MISHE_RENDER_SOURCE": "pane",
                   "MESH_MISHE_SESSION": "fixture",
                   "MOCK_META": 'tg-roz|0|0|"exec /safe/mesh-dash tg-roz"',
                   "MOCK_PANE": "PRIVATE-rozi-text\n-- pane live " + stamp +
                                " · 30s · ticks every frame --"}
            def observe():
                result = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), "tg-roz", "tg-roz"],
                                        env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                event = projection.fleet_projection("tg-roz", result.stdout)
                self.assertNotIn("PRIVATE-rozi-text", event)
                self.assertNotIn("private-old-line", event)
                return event
            self.assertIn("semantic=roz-intake:fresh", observe())
            os.utime(offset, (time.time() - 180, time.time() - 180))
            with incoming.open("a") as stream:
                stream.write("private-pending-line\n")
            stalled = observe()
            self.assertIn("STATE: RED", stalled)
            self.assertIn("semantic=roz-intake:stale", stalled)
            offset.write_text("2\n")
            self.assertIn("semantic=roz-intake:fresh", observe())
            offset.write_text("not-a-cursor\n")
            self.assertIn("semantic=roz-intake:unknown", observe())

    def test_cleaner_uses_matching_live_inventory_and_dry_run_not_pane_repaint(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmux = Path(tmp) / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then "
                            "printf '%s\\n' \"$MOCK_META\"; else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            store = Path(tmp) / "cleaner"
            store.mkdir()
            scan = store / "scan-record.json"
            scan.write_text(json.dumps({"version": 1, "repository": str(ROOT), "scan_id": "fixture",
                                        "candidate_count": 0, "candidates": [], "head": "fixture"}))
            (store / "latest.json").symlink_to(scan.name)
            settle = store / "settle-latest.json"
            settle.write_text(json.dumps({"version": 1, "scan_id": "fixture",
                                          "apply": False, "mutations": 0, "outcomes": []}))
            stamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_DIR": tmp, "MESH_REPO": str(ROOT), "MESH_MISHE_HOME": tmp,
                   "MESH_MISHE_RENDER_SOURCE": "pane", "MESH_MISHE_SESSION": "fixture",
                   "MOCK_META": f'cleaner|0|0|"{ROOT}/scripts/mesh-mishe-cleaner-run watch"',
                   "MOCK_PANE": ("PRIVATE-cleaner-candidate\n-- pane live " + stamp +
                                 ".123456Z · refresh 5s · ticks every frame --")}
            render = ROOT / "scripts/mesh-mishe-render"
            def measure():
                result = subprocess.run([str(render), "cleaner"], env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout, projection.fleet_projection("cleaner", result.stdout)
            fresh, event = measure()
            self.assertIn("MISHE-VALUE: cleaner FRESH\n", fresh)
            self.assertIn("MISHE-CLEANER: REVIEW_REQUIRED\n", fresh)
            self.assertIn("STATE: RED\n", event)
            self.assertIn("review=review_required", event)
            self.assertNotIn("PRIVATE-cleaner-candidate", event)
            old = time.time() - 1900
            os.utime(scan, (old, old))
            stale, event = measure()
            self.assertIn("MISHE-VALUE: cleaner STALE\n", stale)
            self.assertIn("STATE: RED\n", event)
            self.assertIn("cleaner=stale", event)
            os.utime(scan, None)
            settle.write_text(json.dumps({"version": 1, "scan_id": "other",
                                          "apply": False, "mutations": 0, "outcomes": []}))
            unknown, event = measure()
            self.assertIn("MISHE-VALUE: cleaner UNKNOWN\n", unknown)
            self.assertIn("STATE: UNKNOWN\n", event)
            self.assertIn("cleaner=unknown", event)

    def test_periodic_semantic_source_stall_and_recovery_for_each_owner(self):
        sources = {
            "tg": ((".voice-rx-state", ".textin-cycle"), 120),
            "health": ((".fleet-health.cache",), 600),
            "genome": (("vitality.log",), 10800),
            "senses": (("sense-map.txt",), 1800),
            "minds": ((".mind-state-watch.cache",), 300),
            "sound": ((".records-tick",), 300),
            "vpn": (("vpn-health.log",), 1800),
            "discover": (("study.log",), 43200),
            "job": (("job-act.log",), 10800),
        }
        with tempfile.TemporaryDirectory() as tmp:
            tmux = Path(tmp) / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then "
                            "printf '%s\\n' \"$MOCK_META\"; else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            restore = Path(tmp) / "restore.env"
            restore.write_text('export MESH_MIND_CHANNELS="minds"\n')
            epoch = int(time.time())
            stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch))
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_SEMANTIC_DIR": tmp, "MESH_MISHE_GOAL_DIR": tmp,
                   "MESH_MISHE_RESTORE_ENV": str(restore),
                   "MESH_MISHE_HOME": tmp, "MESH_MISHE_RENDER_SOURCE": "pane",
                   "MESH_MISHE_SESSION": "fixture",
                   "MOCK_PANE": ("PRIVATE-operator-message\n-- pane live " + stamp +
                                 " · 30s · ticks every frame --")}
            for channel, (filenames, limit) in sources.items():
                with self.subTest(channel=channel):
                    role = projection.CHANNEL_ROLES[channel]
                    env["MOCK_META"] = f'{channel}|0|0|"exec /safe/mesh-dash {role}"'
                    goal = Path(tmp) / f".goal-{channel}.cache"
                    goal.write_text("static healthy goal")
                    for filename in filenames:
                        source = Path(tmp) / filename
                        source.write_text("" if filename == ".records-tick" else "static healthy source")
                        os.utime(source, (epoch - limit - 10, epoch - limit - 10))
                    def check():
                        frame = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), channel, role],
                                               env=env, capture_output=True, text=True)
                        self.assertEqual(frame.returncode, 0, frame.stderr)
                        event = projection.fleet_projection(channel, frame.stdout)
                        self.assertNotIn("PRIVATE-operator-message", event)
                        return event
                    stale = check()
                    self.assertIn("STATE: RED\n", stale)
                    self.assertIn(f"semantic={projection.SEMANTIC_SOURCES[channel]}:stale", stale)
                    for filename in filenames:
                        source = Path(tmp) / filename
                        os.utime(source, (epoch - 10, epoch - 10))
                    fresh = check()
                    self.assertNotIn("STATE: RED\n", fresh)
                    self.assertIn(f"semantic={projection.SEMANTIC_SOURCES[channel]}:fresh", fresh)
                    (Path(tmp) / filenames[0]).unlink()
                    unknown = check()
                    self.assertIn(f"semantic={projection.SEMANTIC_SOURCES[channel]}:unknown", unknown)
                    for filename in filenames[1:]:
                        (Path(tmp) / filename).unlink()
                    goal.unlink()
            restore.write_text('export MESH_MIND_CHANNELS="minds"\n'
                               'export MESH_MIND_CHANNELS="__operator_stopped__" # live assignment\n')
            (Path(tmp) / ".goal-minds.cache").write_text("static goal")
            env["MOCK_META"] = 'minds|0|0|"exec /safe/mesh-dash minds"'
            suspended = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), "minds"],
                                       env=env, capture_output=True, text=True)
            self.assertIn("MISHE-SEMANTIC: mind-wall SUSPENDED\n", suspended.stdout)
            event = projection.fleet_projection("minds", suspended.stdout)
            self.assertIn("semantic=mind-wall:suspended", event)
            self.assertIn("STATE: UNKNOWN\n", event)
            gate = subprocess.run([str(ROOT / "scripts/mesh-mishe-source-health"), "--channel", "minds"],
                                  env=env, capture_output=True, text=True)
            self.assertEqual(gate.returncode, 0, gate.stderr)
            self.assertIn("0 observed channels; suspended=minds", gate.stdout)

    def test_event_driven_sources_do_not_forge_staleness_from_silence(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmux = Path(tmp) / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then "
                            "printf '%s\\n' \"$MOCK_META\"; else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            audit = Path(tmp) / "task-audit"
            audit.write_text("#!/bin/sh\nexit 0\n")
            audit.chmod(0o755)
            stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_GOAL_DIR": tmp, "MESH_MISHE_SEMANTIC_DIR": tmp,
                   "MESH_MISHE_HOME": tmp, "MESH_MISHE_TASK_AUDIT_CMD": str(audit),
                   "MESH_MISHE_RENDER_SOURCE": "pane", "MESH_MISHE_SESSION": "fixture",
                   "MOCK_PANE": ("PRIVATE-static-value\n-- pane live " + stamp +
                                 " · 30s · ticks every frame --")}
            for channel in ("adint", "hire", "wake", "haunt", "tg-roz"):
                with self.subTest(channel=channel):
                    env["MOCK_META"] = f'{channel}|0|0|"exec /safe/mesh-dash {channel}"'
                    goal = Path(tmp) / f".goal-{channel}.cache"
                    goal.write_text("unchanged goal")
                    result = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), channel],
                                            env=env, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    event = projection.fleet_projection(channel, result.stdout)
                    self.assertIn(f"semantic={projection.SEMANTIC_SOURCES[channel]}:unknown", event)
                    self.assertIn("STATE: UNKNOWN\n", event)
                    self.assertNotIn("PRIVATE-static-value", event)
                    goal.unlink()

    def test_overdue_owner_obligation_is_stale_without_aging_quiet_pipelines(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmux = Path(tmp) / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then "
                            "printf '%s\\n' \"$MOCK_META\"; else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            audit = Path(tmp) / "task-audit"
            audit.write_text("#!/bin/sh\nprintf '%s\\n' \"$AUDIT_ROW\"\nexit \"${AUDIT_RC:-0}\"\n")
            audit.chmod(0o755)
            stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_HOME": tmp, "MESH_MISHE_GOAL_DIR": tmp,
                   "MESH_MISHE_RENDER_SOURCE": "pane", "MESH_MISHE_SESSION": "fixture",
                   "MESH_MISHE_TASK_AUDIT_CMD": str(audit),
                   "MOCK_PANE": ("PRIVATE-owner-fixture\n-- pane live " + stamp +
                                 " · 30s · ticks every frame --")}
            for channel in ("adint", "hire", "wake", "haunt"):
                with self.subTest(channel=channel):
                    (Path(tmp) / f".goal-{channel}.cache").write_text("unchanged goal")
                    env["MOCK_META"] = f'{channel}|0|0|"exec /safe/mesh-dash {channel}"'
                    def observe(row, rc="0"):
                        result = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), channel],
                                                env={**env, "AUDIT_ROW": row, "AUDIT_RC": rc},
                                                capture_output=True, text=True)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        projected = projection.fleet_projection(channel, result.stdout)
                        self.assertNotIn("PRIVATE-owner-fixture", projected)
                        self.assertNotIn("fixture-obligation", projected)
                        return projected
                    overdue = f"OVERDUE\t{channel}\tfixture-obligation\tlease=2026-09-24T00:00:00Z"
                    stalled = observe(overdue)
                    self.assertIn("STATE: RED", stalled)
                    self.assertIn("semantic=obligations:stale", stalled)
                    self.assertIn("semantic=obligations:unknown", observe(
                        "OVERDUE\tother\tfixture-obligation\tlease=2026-09-24T00:00:00Z"))
                    self.assertIn("semantic=obligations:unknown", observe(
                        f"DONE\t{channel}\tfixture-obligation\tlease=2026-09-24T00:00:00Z"))
                    self.assertIn("semantic=obligations:unknown", observe(overdue, rc="2"))

    def test_source_health_names_stalled_producer_without_private_pane_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmux = Path(tmp) / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then printf '%s\\n' "
                            "'tg|0|0|\"exec /safe/mesh-dash tg\"'; else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            goal = Path(tmp) / ".goal-tg.cache"
            goal.write_text("unchanged goal")
            epoch = int(time.time())
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_HOME": tmp, "MESH_MISHE_GOAL_DIR": tmp,
                   "MESH_MISHE_SESSION": "fixture",
                   "MOCK_PANE": ("PRIVATE-operator-fixture\n"
                                 f"-- pane live {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(epoch))} "
                                 "· 30s · ticks every frame --")}
            command = [str(ROOT / "scripts/mesh-mishe-source-health"), "--channel", "tg"]
            def verdict():
                result = subprocess.run(command, env=env, capture_output=True, text=True)
                self.assertNotIn("PRIVATE-operator-fixture", result.stdout + result.stderr)
                return result
            old = epoch - 360
            os.utime(goal, (old, old))
            stale = verdict()
            self.assertEqual(stale.returncode, 1)
            self.assertIn("stale=tg", stale.stdout)
            fresh = epoch - 10
            os.utime(goal, (fresh, fresh))
            self.assertEqual(verdict().returncode, 0)
            goal.unlink()
            unknown = verdict()
            self.assertEqual(unknown.returncode, 1)
            self.assertIn("unknown=tg", unknown.stdout)

    def test_publisher_async_cache_refresh_does_not_look_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmux = Path(tmp) / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then "
                            "printf '%s\\n' 'pub|0|0|\"exec /safe/mesh-dash pub\"'; "
                            "else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            cache = Path(tmp) / ".pub-right.cache"
            cache.write_text("newly refreshed external status")
            epoch = int(time.time())
            os.utime(cache, (epoch - 5, epoch - 5))
            stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch - 30))
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_RENDER_SOURCE": "pane", "MESH_MISHE_HOME": tmp,
                   "MESH_MISHE_PUB_CACHE": str(cache), "MESH_MISHE_SESSION": "fixture",
                   "MOCK_PANE": f"private comment body\n-- pane live {stamp} · 75s · ticks every frame --"}
            result = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), "pub", "pub"],
                                    env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("MISHE-VALUE: comments FRESH\n", result.stdout)
            projected = projection.fleet_projection("pub", result.stdout)
            self.assertIn("comments=fresh", projected)
            self.assertNotIn("private comment body", projected)

    def test_shared_goal_cache_newer_than_pane_is_healthy(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmux = Path(tmp) / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then "
                            "printf '%s\\n' 'tg|0|0|\"exec /safe/mesh-dash tg\"'; "
                            "else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            goal = Path(tmp) / ".goal-tg.cache"
            goal.write_text("updated by another reader")
            epoch = int(time.time())
            os.utime(goal, (epoch - 5, epoch - 5))
            stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch - 40))
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_RENDER_SOURCE": "pane", "MESH_MISHE_HOME": tmp,
                   "MESH_MISHE_GOAL_DIR": tmp, "MESH_MISHE_SESSION": "fixture",
                   "MOCK_PANE": f"private goal text\n-- pane live {stamp} · 30s · ticks every frame --"}
            result = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), "tg", "tg"],
                                    env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("MISHE-VALUE: goal FRESH\n", result.stdout)
            projected = projection.fleet_projection("tg", result.stdout)
            self.assertIn("goal=fresh", projected)
            self.assertNotIn("private goal text", projected)

    def test_witness_trusted_journal_age_not_private_prose_drives_stale_and_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmux = Path(tmp) / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then "
                            "printf '%s\\n' 'witness|0|0|\"exec /safe/mesh-dash witness\"'; "
                            "else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_RENDER_SOURCE": "pane", "MESH_MISHE_HOME": tmp,
                   "MESH_MISHE_SESSION": "fixture"}
            previous, current = Path(tmp) / "previous", Path(tmp) / "current"
            previous.write_text("")
            render = ROOT / "scripts/mesh-mishe-render"

            def frame(age, status, *, malformed=False, pane_age=0, issues=0, digest="0" * 16):
                now = int(time.time())
                epoch = now - age
                source_stamp = ("UNKNOWN" if status == "UNKNOWN" else
                                time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch)))
                lease_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - pane_age))
                source = (f"materialized view: /private/journal-secret · source age={age - pane_age}s · "
                          f"authority=explicit task-state events · mtime={epoch} · "
                          f"MISHE-VALUE: journal {status} {source_stamp}")
                if malformed:
                    source = source.replace("mtime=" + str(epoch), "mtime=0")
                return ("WITNESS TASKS — fixture\n" + source + "\n"
                        "tasks: 0 total · 0 unfinished · 0 rejected · 0 done · "
                        "[RUNNING=0 UNOWNED=0 QUEUED=0 BLOCKED=0 HREJ=0 HEXP=0]\n"
                        "next-up: UNKNOWN · dispatch age=0s\n"
                        f"mishe: {issues} unfinished · id={digest} · next=fixture\n"
                        "chat.log: showing private tail\n"
                        "MISHE-VALUE: journal STALE 2020-01-01T00:00:00Z\n"
                        "private-operator-secret\n"
                        f"-- pane live {lease_stamp} · 15s · ticks every frame --")

            def projected(raw):
                result = subprocess.run([str(render), "witness", "witness"],
                                        env={**env, "MOCK_PANE": raw}, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                current.write_text(result.stdout)
                projected = subprocess.run([str(PROJECT), "--channel", "witness", str(previous), str(current)],
                                           env=env, capture_output=True, text=True)
                self.assertEqual(projected.returncode, 0, projected.stderr)
                self.assertNotIn("private-operator-secret", projected.stdout)
                self.assertNotIn("journal-secret", projected.stdout)
                previous.write_text(result.stdout)
                return projected.stdout

            healthy = projected(frame(20, "FRESH"))
            self.assertIn("journal=fresh", healthy)
            self.assertNotIn("STATE: RED", healthy)
            self.assertIn("journal=fresh", projected(frame(600, "FRESH", pane_age=30)))
            self.assertEqual(projected(frame(20, "FRESH")), healthy)
            issue = projected(frame(20, "FRESH", issues=2, digest="a" * 16))
            self.assertIn("STATE: RED", issue)
            self.assertIn("mishe-issues=2", issue)
            self.assertEqual(projected(frame(20, "FRESH", issues=2, digest="a" * 16)), issue)
            self.assertEqual(projected(frame(20, "FRESH")), healthy)
            unknown_source = projected(frame(20, "UNKNOWN"))
            self.assertIn("journal=unknown", unknown_source)
            self.assertNotIn("STATE: RED", unknown_source)
            stale = projected(frame(800, "STALE"))
            self.assertIn("STATE: RED", stale)
            self.assertIn("journal=stale", stale)
            self.assertEqual(projected(frame(800, "STALE")), stale)
            restored = projected(frame(20, "FRESH"))
            self.assertEqual(restored, healthy)
            unknown = projected(frame(20, "FRESH", malformed=True))
            self.assertIn("value-coverage=unknown", unknown)
            self.assertNotIn("journal=stale", unknown)

    def test_one_shot_observe_deduplicates_expired_lease_and_emits_recovery(self):
        core = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))
        if not (core / "src/mishe_tauftauf/__main__.py").exists():
            self.skipTest("public core absent")
        from sys import path as import_path
        import_path.insert(0, str(core / "src"))
        from mishe_tauftauf.feed import parse_feed
        import_path.remove(str(core / "src"))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            roster = root / "roster.json"
            roster.write_text(json.dumps({"status": "PASS", "channels": [
                {"channel": "tg", "renderer_role": "tg", "state": "active", "poll_seconds": 60}]}))
            tmux = root / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then "
                            "printf '%s\\n' 'tg|0|0|\"exec /safe/mesh-dash tg\"'; "
                            "else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_HOME": str(home), "MESH_MISHE_CORE": str(core),
                   "MESH_MISHE_PYTHON": "python3", "MESH_REPO": str(ROOT),
                   "MESH_MISHE_ROSTER_JSON": str(roster), "MESH_MISHE_SESSION": "fixture",
                   "MESH_MISHE_MANUAL_SHADOW": "1"}
            run = ROOT / "scripts/mesh-mishe-run"
            for mode in ("init", "enroll-fleet"):
                result = subprocess.run([str(run), mode], env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            unsafe = subprocess.run([str(run), "once", "--channel", "tg"],
                                    env={**env, "MOCK_PANE": "PRIVATE-fixture"},
                                    capture_output=True, text=True)
            self.assertEqual(unsafe.returncode, 2)
            self.assertIn("disabled local judge", unsafe.stderr)
            env["MESH_MISHE_JUDGE"] = "/bin/false"

            def tick(stamp):
                pane = (f"voice-rx UP | textin UP\n-- conversation (last 3 each):\n"
                        f"constant healthy value\n-- pane live {stamp} · 30s · ticks every frame --")
                result = subprocess.run([str(run), "once", "--channel", "tg"],
                                        env={**env, "MOCK_PANE": pane}, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                entries = parse_feed((home / "feed").read_bytes())
                return [entry.body for entry in entries if entry.source == "observation/tg"]

            fresh = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            expired = "2020-01-01T00:00:00Z"
            first = tick(fresh)
            self.assertEqual(len(first), 1)
            self.assertIn("freshness=fresh", first[-1])
            self.assertEqual(tick(fresh), first)
            stale = tick(expired)
            self.assertEqual(len(stale), 2)
            self.assertIn("STATE: RED\nOBSERVATION: source=top-pane/tg freshness=stale", stale[-1])
            self.assertEqual(tick(expired), stale)
            recovered = tick(fresh)
            self.assertEqual(len(recovered), 3)
            self.assertEqual(recovered[-1], first[0])
            self.assertNotIn("constant healthy value", (home / "feed").read_text())

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
                {"channel": "health", "renderer_role": "check", "state": "suspended-data-only", "poll_seconds": 60},
                {"channel": "tg", "renderer_role": "tg", "state": "active", "poll_seconds": 60},
                {"channel": "witness", "renderer_role": "witness", "state": "one-shot-data-only", "poll_seconds": 60},
                {"channel": "tiny-fleet", "renderer_role": None, "state": "configured-inactive"}]}
            roster.write_text(json.dumps(data))
            enrolled = subprocess.run([str(run), "enroll-fleet"], env=env, capture_output=True, text=True)
            self.assertEqual(enrolled.returncode, 0, enrolled.stderr)
            self.assertTrue((home / "top-pains/health").exists())
            self.assertTrue((home / "projectors/tg").exists())
            self.assertTrue((home / "top-pains/witness").exists())
            self.assertFalse((home / "top-pains/tiny-fleet").exists())
            self.assertEqual((home / "projection.key").stat().st_mode & 0o777, 0o600)
            (home / ".fleet-shadow-hold").write_text("profile pending\n")
            feed_before = (home / "feed").read_bytes()
            held = subprocess.run([str(run), "once"], env=env, capture_output=True, text=True)
            self.assertEqual(held.returncode, 0)
            self.assertIn("fleet shadow held", held.stdout)
            self.assertEqual((home / "feed").read_bytes(), feed_before)
            self.assertEqual(subprocess.run([str(run), "--freshness"], env=env, capture_output=True).returncode, 2)
            for channel in ("health", "tg", "witness"):
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
                renderer.write_text("#!/bin/sh\nprintf '%s\\n' 'MISHE-STATE: UNKNOWN' 'MISHE-SOURCE: top-pane' 'MISHE-FRESHNESS: FRESH' '" + secret + "'\n")
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

    def test_single_channel_runner_binds_pane_identity_to_feed_sequence(self):
        core = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))
        if not (core / "src/mishe_tauftauf/__main__.py").exists():
            self.skipTest("public core absent")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            home = base / "home"
            roster = base / "roster.json"
            roster.write_text(json.dumps({"status": "PASS", "channels": [
                {"channel": "tg", "renderer_role": "tg", "state": "active", "poll_seconds": 60}]}))
            tmux = base / "tmux"
            tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then printf '%s\\n' 'tg|0|0|\"exec /safe/mesh-dash tg\"'; else printf '%s\\n' \"$MOCK_PANE\"; fi\n")
            tmux.chmod(0o755)
            secret = "fixture-private-runner-message"
            stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            pane = f"voice-rx UP | textin UP\n{secret}\n-- pane live {stamp} · 30s · ticks every frame --"
            corpus_root = base / "private-corpus"
            for source in (".goal-tg.cache", ".voice-rx-state", ".textin-cycle"):
                (base / source).write_text(secret)
            env = {**os.environ, "PATH": tmp + ":" + os.environ["PATH"],
                   "MESH_MISHE_HOME": str(home), "MESH_MISHE_CORE": str(core),
                   "MESH_MISHE_PYTHON": "python3", "MESH_REPO": str(ROOT),
                   "MESH_DIR": str(base), "MESH_MISHE_CORPUS_ROOT": str(corpus_root),
                   "MESH_MISHE_ROSTER_JSON": str(roster), "MESH_MISHE_SESSION": "fixture",
                   "MESH_MISHE_MANUAL_SHADOW": "1", "MESH_MISHE_JUDGE": "/bin/false",
                   "MOCK_PANE": pane}
            run = ROOT / "scripts/mesh-mishe-run"
            for args in (("init",), ("enroll-fleet",)):
                result = subprocess.run([str(run), *args], env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            (home / ".fleet-corpus-capture").write_text("candidate-only\n")
            result = subprocess.run([str(run), "once", "--channel", "tg"], env=env,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("mishe corpus: captured=1", result.stdout)
            status = subprocess.run([str(ROOT / "scripts/mesh-mishe-s1-corpus"), "status",
                                     "--home", str(home), "--evidence-root", str(corpus_root)],
                                    env=env, capture_output=True, text=True)
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            self.assertIn("captured_candidates=1 distinct_capture_keys=1 reviewed_labels=0", status.stdout)
            self.assertNotIn(secret, result.stdout + status.stdout)
            tape = home / "parity/projected.jsonl"
            rows = [json.loads(line) for line in tape.read_text().splitlines()]
            self.assertEqual(len(rows), 1)
            self.assertEqual((rows[0]["channel"], rows[0]["kind"], rows[0]["source"]),
                             ("tg", "pane", "top-pane"))
            self.assertGreater(rows[0]["feed_seq"], 0)
            self.assertNotIn(secret.encode(), tape.read_bytes() + (home / "feed").read_bytes())
            case_dir = next((corpus_root / "cases").iterdir())
            candidate = json.loads((case_dir / "case.json").read_text())
            bound_raw = (case_dir / "s0-bound.json").read_bytes()
            bound = json.loads(bound_raw)
            self.assertEqual(candidate["provenance_phase"], "s0_projection_hash_matched")
            self.assertEqual(candidate["bound_sha256"], hashlib.sha256(bound_raw).hexdigest())
            self.assertEqual(bound["feed_seq"], rows[0]["feed_seq"])
            self.assertEqual(bound["projected_sha256"],
                             hashlib.sha256(candidate["projected_view"].encode()).hexdigest())
            self.assertEqual([source["sha256"] for source in bound["sources"]],
                             [hashlib.sha256((base / name).read_bytes()).hexdigest()
                              for name in (".goal-tg.cache", ".voice-rx-state", ".textin-cycle")])
            refused = subprocess.run([str(run), "once", "--channel", "tg"],
                                     env={**env, "MESH_MISHE_SKIP_AUTO_DRAIN": "1"},
                                     capture_output=True, text=True)
            self.assertEqual(refused.returncode, 2)
            (home / ".fleet-shadow-hold").write_text("fixture hold\n")
            unsafe = subprocess.run([str(run), "once", "--channel", "tg"],
                                    env={**env, "MESH_MISHE_SKIP_AUTO_DRAIN": "1",
                                         "MESH_MISHE_JUDGE": ""},
                                    capture_output=True, text=True)
            self.assertEqual(unsafe.returncode, 2)
            self.assertIn("disabled local judge", unsafe.stderr)
            allowed = subprocess.run([str(run), "once", "--channel", "tg"],
                                     env={**env, "MESH_MISHE_SKIP_AUTO_DRAIN": "1",
                                          "MESH_MISHE_JUDGE": "/bin/false"},
                                     capture_output=True, text=True)
            self.assertEqual(allowed.returncode, 0, allowed.stderr)


if __name__ == "__main__":
    unittest.main()
