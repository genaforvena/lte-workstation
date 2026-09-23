#!/usr/bin/env python3
"""Synthetic Mesh adapter contract against the public coordinator."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone


ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ["MESH_MISHE_CORE"]) if os.environ.get("MESH_MISHE_CORE") else None


class SyntheticAdapterTest(unittest.TestCase):
    def test_scheduled_judge_uses_cache_and_refresh_is_explicit(self):
        if CORE is None or not (CORE / "src/mishe_tauftauf/__main__.py").is_file():
            self.skipTest("set MESH_MISHE_CORE to the public core")
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "core"
            state = Path(tmp) / "state"
            state.write_text("STATE: RED\n", encoding="utf-8")
            count = Path(tmp) / "calls"
            judge = Path(tmp) / "judge"
            judge.write_text("#!/usr/bin/env python3\nfrom pathlib import Path\n"
                             f"p = Path({str(count)!r})\n"
                             "n = int(p.read_text()) + 1 if p.exists() else 1\n"
                             "p.write_text(str(n))\n"
                             "print('probability 0.9' if n % 2 else 'probability 0.1')\n",
                             encoding="utf-8")
            judge.chmod(0o755)
            env = {**os.environ, "MESH_MISHE_HOME": str(home), "MESH_MISHE_CORE": str(CORE),
                   "MESH_MISHE_PYTHON": "python3", "MESH_REPO": str(ROOT),
                   "MESH_MISHE_SYNTHETIC_FILE": str(state)}

            def run(mode, configured=True):
                selected = {**env, **({"MESH_MISHE_JUDGE": str(judge)} if configured else {})}
                return subprocess.run([str(ROOT / "scripts/mesh-mishe-run"), mode],
                                      env=selected, text=True, capture_output=True)

            self.assertEqual(run("init").returncode, 0)
            self.assertEqual(run("refresh-controls", configured=False).returncode, 2)
            first = run("once")
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertFalse(count.exists(), "scheduled pass must not refresh missing controls")
            refresh = run("refresh-controls")
            self.assertEqual(refresh.returncode, 0, refresh.stderr)
            self.assertEqual(int(count.read_text()), 12)
            self.assertTrue((home / "control-cache.json").is_file())
            again = run("once")
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(int(count.read_text()), 12)

    def test_default_state_path_works_without_shell_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "core"
            home.mkdir()
            (home / "synthetic.state").write_text("STATE: GREEN\n", encoding="utf-8")
            env = {**os.environ, "MESH_MISHE_HOME": str(home)}
            env.pop("MESH_MISHE_SYNTHETIC_FILE", None)
            result = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), "synthetic"],
                                    env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "STATE: GREEN\n")

    def test_renderer_projection_and_observe_only_feed(self):
        if CORE is None or not (CORE / "src/mishe_tauftauf/__main__.py").is_file():
            self.skipTest("set MESH_MISHE_CORE to the Phase 1 public core worktree")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            home = base / "core"
            state = base / "synthetic-state"
            env = {**os.environ, "MESH_MISHE_HOME": str(home), "MESH_MISHE_CORE": str(CORE),
                   "MESH_MISHE_PYTHON": "python3", "MESH_REPO": str(ROOT),
                   "MESH_MISHE_SYNTHETIC_FILE": str(state)}

            def adapter(name, *args):
                return subprocess.run([str(ROOT / "scripts" / name), *args], env=env,
                                      text=True, capture_output=True)

            self.assertEqual(adapter("mesh-mishe-run", "--test").returncode, 2)
            init = adapter("mesh-mishe-run", "init")
            self.assertEqual(init.returncode, 0, init.stderr)
            self.assertTrue((home / "top-pains" / "synthetic").is_file())
            gate = adapter("mesh-mishe-run", "--test")
            self.assertEqual(gate.returncode, 0, gate.stdout + gate.stderr)
            self.assertFalse((home / ".mesh-mishe-pass").exists())
            missing_python = subprocess.run([str(ROOT / "scripts/mesh-mishe-run"), "--test"],
                                            env={**env, "MESH_MISHE_PYTHON": str(base / "missing-python")},
                                            text=True, capture_output=True)
            self.assertEqual(missing_python.returncode, 2)
            fake_home = base / "fake-home"
            bin_dir = fake_home / ".local/bin"
            bin_dir.mkdir(parents=True)
            (fake_home / ".mesh").mkdir()
            (fake_home / ".mesh-card").write_text("  minds: codex\n", encoding="utf-8")
            (bin_dir / "mesh-mishe-run").symlink_to(ROOT / "scripts/mesh-mishe-run")
            fake_repo = fake_home / "genome"
            (fake_repo / "scripts/lib").mkdir(parents=True)
            (fake_repo / "job").mkdir()
            for relative in ("scripts/mesh-manifest", "scripts/lib/mesh-manifest-reader.sh",
                             "scripts/mesh-mishe-run", "scripts/mesh-mishe-render", "scripts/mesh-mishe-project"):
                shutil.copy2(ROOT / relative, fake_repo / relative)
            autowire = subprocess.run([str(ROOT / "scripts/mesh-autowire"), "--check"],
                                      env={**env, "HOME": str(fake_home), "MESH_REPO": str(fake_repo),
                                           "MESH_AUTOWIRE_CRONTAB_SRC": "/dev/null", "MESH_LIVENESS_SRC": ""},
                                      text=True, capture_output=True)
            self.assertEqual(autowire.returncode, 0, autowire.stderr)
            self.assertIn("WOULD WIRE:", autowire.stdout)
            self.assertIn("mesh-mishe-run once", autowire.stdout)
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
            # Observation timestamps can be old while stable passes remain fresh.
            feed_path = home / "feed"
            old_feed = feed_path.read_text(encoding="utf-8")
            old_feed = re.sub(r"^(\d{20}) \d{4}-\d\d-\d\dT[^ ]+ (observation/synthetic ::)$",
                              r"\1 2020-01-01T00:00:00.000000Z \2", old_feed, flags=re.MULTILINE)
            feed_path.write_text(old_feed, encoding="utf-8")
            self.assertEqual(adapter("mesh-mishe-run", "once").returncode, 0)
            self.assertEqual(adapter("mesh-mishe-doctor").returncode, 0)
            (home / ".mesh-mishe-pass").write_text("0\n", encoding="ascii")
            stale_pass = adapter("mesh-mishe-doctor")
            self.assertNotEqual(stale_pass.returncode, 0)
            self.assertIn("stale", stale_pass.stdout)
            self.assertEqual(adapter("mesh-mishe-run", "once").returncode, 0)
            self.assertEqual(adapter("mesh-mishe-doctor").returncode, 0)
            appended = subprocess.run(["python3", "-c", "from mishe_tauftauf.feed import Feed; import sys; Feed(sys.argv[1]).append_runtime('observation/synthetic', sys.argv[2])",
                                      str(home), "UNKNOWN — event projector synthetic invalid-size"],
                                     env={**env, "PYTHONPATH": str(CORE / "src")},
                                     text=True, capture_output=True)
            self.assertEqual(appended.returncode, 0, appended.stderr)
            self.assertNotEqual(adapter("mesh-mishe-doctor").returncode, 0)
            state.write_text("STATE: RED\nSECRET: fixture-private-recovery\n", encoding="utf-8")
            self.assertEqual(adapter("mesh-mishe-run", "once").returncode, 0)
            self.assertEqual(adapter("mesh-mishe-doctor").returncode, 0)
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
            self.assertEqual(adapter("mesh-mishe-run", "--test").returncode, 2)

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

    def test_cleaner_projection_is_bounded_and_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            previous, current = base / "previous", base / "current"
            previous.write_text("", encoding="utf-8")
            current.write_text(
                "cleaner scan=2026-09-23T03:45:01Z head=" + "a" * 40 +
                " candidates=2 held=1 actionable=1 delete=0 oldest=private-secret-name\n"
                "unknowns=0 count-drift=candidates:+1\n"
                "TASK: PRESENT\n"
                "TASK-EPOCH: 42\n"
                "TASK-EVENT-COUNT: 1\n"
                "TASK-EVENTS: 42:open\n"
                "held-reasons=protected-root:1\n"
                "actionable-paths=private-secret-name\n"
                "held-paths=private-secret-name\n"
                "unknown-paths=none\n", encoding="utf-8")
            result = subprocess.run([str(ROOT / "scripts/mesh-mishe-project"), "--channel", "cleaner",
                                     str(previous), str(current)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("STATE: INTERMEDIATE", result.stdout)
            self.assertIn("candidates=2 held=1 actionable=1 delete=0 unknowns=0", result.stdout)
            self.assertIn("task=present", result.stdout)
            self.assertIn("task-epoch=42", result.stdout)
            self.assertIn("task-event-count=1", result.stdout)
            self.assertIn("task-events=42:open", result.stdout)
            self.assertNotIn("private-secret-name", result.stdout)
            previous.write_text("TASK-EPOCH: 99\nTASK-EVENT-COUNT: 2\n", encoding="utf-8")
            rewind = subprocess.run([str(ROOT / "scripts/mesh-mishe-project"), "--channel", "cleaner",
                                     str(previous), str(current)], text=True, capture_output=True)
            self.assertEqual(rewind.stdout, "STATE: UNKNOWN\n")
            current.write_text("cleaner scan=invalid candidates=2 held=1 actionable=1 delete=0\n",
                               encoding="utf-8")
            malformed = subprocess.run([str(ROOT / "scripts/mesh-mishe-project"), "--channel", "cleaner",
                                        str(previous), str(current)], text=True, capture_output=True)
            self.assertEqual(malformed.stdout, "STATE: UNKNOWN\n")

    def test_cleaner_enrollment_observes_without_dispatch(self):
        if CORE is None:
            self.skipTest("set MESH_MISHE_CORE")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            home, repo = base / "core", base / "repo"
            (repo / "scripts").mkdir(parents=True)
            for name in ("mesh-mishe-render", "mesh-mishe-project", "mesh-mishe-parity", "mesh-mishe-task-bridge"):
                shutil.copy2(ROOT / "scripts" / name, repo / "scripts" / name)
            (repo / "scripts/mesh-dash").write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' 'cleaner scan=2026-09-23T03:45:01Z head=" + "a" * 40 +
                " candidates=1 held=1 actionable=0 delete=0 oldest=private-secret-name' "
                "'unknowns=0 count-drift=candidates:+1' 'held-paths=private-secret-name'\n",
                encoding="utf-8")
            (repo / "scripts/mesh-dash").chmod(0o755)
            chat_log = base / "chat.log"
            chat_log.write_text("2026-09-23T03:45:01Z [task-ledger] /chain=s:test | /current=i:0 | /status=s:open | /steps/0/owner=s:cleaner | /steps/0/status=s:open\n",
                                encoding="utf-8")
            env = {**os.environ, "MESH_MISHE_HOME": str(home), "MESH_MISHE_CORE": str(CORE),
                   "MESH_MISHE_PYTHON": "python3", "MESH_REPO": str(repo),
                   "PATH": "/usr/bin:/bin",
                   "MESH_MISHE_CHAT_LOG": str(chat_log)}

            def run(*args):
                return subprocess.run([str(ROOT / "scripts/mesh-mishe-run"), *args], env=env,
                                      text=True, capture_output=True)

            self.assertEqual(run("init").returncode, 0)
            (home / "synthetic.state").write_text("STATE: GREEN\n", encoding="utf-8")
            enrolled = run("enroll-cleaner")
            self.assertEqual(enrolled.returncode, 0, enrolled.stderr)
            self.assertTrue((home / "top-pains/cleaner").is_file())
            observed = run("once")
            self.assertEqual(observed.returncode, 0, observed.stderr)
            feed = (home / "feed").read_text(encoding="utf-8")
            self.assertIn("CLEANER: candidates=1 held=1 actionable=0", feed)
            self.assertIn("task=present", feed)
            self.assertIn("task-epoch=1", feed)
            self.assertIn("task-event-count=1", feed)
            self.assertIn("task-events=1:open", feed)
            self.assertNotIn("private-secret-name", feed)
            self.assertFalse((home / "minds/cleaner").exists())
            baseline = subprocess.run(["python3", str(ROOT / "scripts/mesh-mishe-task-bridge"), "baseline"],
                                      env=env, text=True, capture_output=True)
            self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)
            with chat_log.open("a", encoding="utf-8") as stream:
                stream.write("2026-09-23T03:45:02Z [task-ledger] /chain=s:test | /current=i:0 | /status=s:complete | /steps/0/owner=s:cleaner | /steps/0/status=s:complete\n")
            first_transition = run("once")
            self.assertEqual(first_transition.returncode, 0, first_transition.stdout + first_transition.stderr)
            feed = (home / "feed").read_text(encoding="utf-8")
            self.assertIn("cleaner task-ledger epoch=2 status=complete", feed)
            self.assertIn("for top-pain cleaner: wake", feed)
            self.assertIn("wake requested top-pain cleaner for entry", feed)
            self.assertLess(feed.index("cleaner task-ledger epoch=2 status=complete"),
                            feed.index("task-events=1:open,2:complete"))
            self.assertIn("task-epoch=2", feed)
            self.assertIn("task-event-count=2", feed)
            self.assertIn("task-events=1:open,2:complete", feed)
            with chat_log.open("a", encoding="utf-8") as stream:
                for number in range(3, 21):
                    status = "open" if number % 2 else "complete"
                    stream.write(f"2026-09-23T03:45:03Z [task-ledger] /chain=s:test | /current=i:0 | /status=s:{status} | /steps/0/owner=s:cleaner | /steps/0/status=s:{status}\n")
            burst = run("once")
            self.assertEqual(burst.returncode, 0, burst.stdout + burst.stderr)
            feed = (home / "feed").read_text(encoding="utf-8")
            self.assertIn("task-event-count=20", feed)
            self.assertIn("task-events=5:open", feed)
            self.assertIn("20:complete", feed)
            (home / "cleaner-parity-baseline.json").write_text(
                '{"epoch":0,"time":"2026-09-23T03:45:00Z"}', encoding="utf-8")
            doctor = subprocess.run([str(ROOT / "scripts/mesh-mishe-doctor")], env=env,
                                    text=True, capture_output=True)
            self.assertNotEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)
            self.assertIn("parity: FAIL covered=18 missing=2 pending=0", doctor.stdout)
            (home / "cleaner-parity-baseline.json").write_text(
                '{"epoch":20,"time":"2026-09-23T03:45:03Z"}', encoding="utf-8")
            with chat_log.open("a", encoding="utf-8") as stream:
                stream.write("2026-09-23T03:45:04Z [task-ledger] /chain=s:test | /current=i:0 | /status=s:open | /steps/0/owner=s:cleaner | /steps/0/status=s:open\n")
            self.assertEqual(run("once").returncode, 0)
            doctor = subprocess.run([str(ROOT / "scripts/mesh-mishe-doctor")], env=env,
                                    text=True, capture_output=True)
            self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)
            self.assertIn("parity: PASS covered=1 missing=0 pending=0", doctor.stdout)
            self.assertIn("judge-view: projected-publish-v1", doctor.stdout)
            self.assertIn("task bridge: PASS", doctor.stdout)
            self.assertIn("cleaner=shadow; authority=legacy", doctor.stdout)
            delta_env = {**env, "MESH_MISHE_DELTA_VIEW": "1"}
            delta = subprocess.run([str(ROOT / "scripts/mesh-mishe-run"), "once"], env=delta_env,
                                   text=True, capture_output=True)
            self.assertEqual(delta.returncode, 0, delta.stdout + delta.stderr)
            delta_doctor = subprocess.run([str(ROOT / "scripts/mesh-mishe-doctor")], env=delta_env,
                                          text=True, capture_output=True)
            self.assertEqual(delta_doctor.returncode, 0, delta_doctor.stdout + delta_doctor.stderr)
            self.assertIn("judge-view: projected-pair-v1", delta_doctor.stdout)
            self.assertIn("parity: PASS", delta_doctor.stdout)
            (home / ".mesh-mishe-view").write_text("cleaner=disabled\n", encoding="utf-8")
            unsafe = subprocess.run([str(ROOT / "scripts/mesh-mishe-doctor")], env=env,
                                    text=True, capture_output=True)
            self.assertNotEqual(unsafe.returncode, 0)
            self.assertIn("judge-view: UNKNOWN", unsafe.stdout)
            self.assertEqual(run("once").returncode, 0)
            self.assertEqual(subprocess.run([str(ROOT / "scripts/mesh-mishe-doctor")],
                                            env=env, text=True, capture_output=True).returncode, 0)
            venv_python = Path.home() / ".mesh/venvs/mishe-tauftauf/bin/python"
            if venv_python.is_file():
                cron_env = {**env, "MESH_MISHE_PYTHON": str(venv_python)}
                cron_env.pop("MESH_MISHE_CORE", None)
                cron_env.pop("PYTHONPATH", None)
                cron = subprocess.run([str(ROOT / "scripts/mesh-mishe-doctor")], env=cron_env,
                                      text=True, capture_output=True)
                self.assertEqual(cron.returncode, 0, cron.stdout + cron.stderr)
                self.assertIn("parity: PASS covered=1 missing=0 pending=0", cron.stdout)


if __name__ == "__main__":
    unittest.main()
