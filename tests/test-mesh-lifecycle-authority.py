#!/usr/bin/env python3
"""Exercise both native lifecycle CLIs with isolated panes and real authority reads."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


REPO = Path(__file__).resolve().parents[1]
ENGINES = ("omp", "codex")


class LifecycleAuthorityTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.mesh = self.home / "mesh"
        self.bin = self.home / "bin"
        self.bin.mkdir()
        self.authority = self.home / "mishe/authority"
        self.authority.mkdir(parents=True)
        self.effects = self.home / "effects"
        self.env = {**os.environ, "HOME": str(self.home), "MESH_DIR": str(self.mesh),
                    "MESH_BIN": str(self.bin), "PATH": str(self.bin) + ":/usr/bin:/bin",
                    "MESH_MISHE_HOME": str(self.home / "mishe"),
                    "MESH_MISHE_AUTHORITY_BIN": str(REPO / "scripts/mesh-mishe-authority"),
                    "MESH_MISHE_AUTO_EVENTS_BIN": str(REPO / "scripts/mesh-mishe-auto-events"),
                    "MESH_WINDOW": "synthetic", "TMUX_PANE": "%fixture",
                    "FIXTURE_HOME": str(self.home), "MESH_TELL_ALLOW_SHELL": "1",
                    "MESH_TELL_WAL": str(self.home / "tell-wal"),
                    "MESH_TELL_SOURCE": "lifecycle-test", "MESH_TELL_FRESH_READY_SECS": "1"}
        for key in ("MESH_MISHE_INVOCATION", "MISHE_TAUFTAUF_INVOCATION"):
            self.env.pop(key, None)
        tool = self.bin / "fixture-tool"
        tool.write_text(f"#!{sys.executable}\n" + '''import json, os, pathlib, subprocess, sys, time
root = pathlib.Path(os.environ["FIXTURE_HOME"])
name = pathlib.Path(sys.argv[0]).name
args = sys.argv[1:]
if name == "tmux":
    if args[0] == "display-message":
        print("synthetic")
    elif args[0] == "list-panes":
        print("0 0\\n20 1")
    elif args[0] == "capture-pane":
        screen = root / "screen"
        print(screen.read_text() if screen.exists() else "Finished work")
    elif args[0] == "send-keys":
        (root / "send-attempt").write_text("attempted")
        sys.exit(1)
    else:
        sys.exit(1)
elif name == "mesh-mind-state":
    print("IDLE\\tfixture")
else:
    with (root / "effects").open("a") as stream:
        stream.write(name + " " + " ".join(args) + "\\n")
    if os.environ.get("FIXTURE_HOLD") == name:
        (root / "entered").touch()
        deadline = time.monotonic() + 10
        while not (root / "release").exists():
            if time.monotonic() > deadline:
                sys.exit(2)
            time.sleep(0.01)
    if name == "mesh-clear":
        if os.environ.get("FIXTURE_START"):
            engine = os.environ["FIXTURE_ENGINE"]
            key = "session-id" if engine == "omp" else "session_id"
            subprocess.run([os.environ["FIXTURE_START"], "--start"],
                           input=json.dumps({key: "after-clear"}), text=True, check=True,
                           timeout=5)
        (root / "screen").write_text("New chat\\nAsk Codex to do anything\\nidle composer")
''')
        tool.chmod(0o755)
        for name in ("tmux", "mesh-task", "mesh-handoff", "mesh-clear", "mesh-mind-state",
                     "mesh-land", "mesh-wip-commit"):
            (self.bin / name).symlink_to(tool)
        for engine in ENGINES:
            (self.bin / f"mesh-{engine}-lifecycle").symlink_to(REPO / f"scripts/mesh-{engine}-lifecycle")

    def state(self, engine):
        return self.mesh / f"{engine}-lifecycle"

    def command(self, engine, mode, session="root"):
        script = str(REPO / f"scripts/mesh-{engine}-lifecycle")
        if mode == "--start":
            key = "session-id" if engine == "omp" else "session_id"
            return [script, mode], json.dumps({key: session})
        if mode == "--receipt":
            event = self.event(engine, session)
            return ([script, mode], json.dumps(event)) if engine == "omp" else ([script, json.dumps(event)], None)
        return [script, mode], None

    def invoke(self, engine, mode, session="root", **env):
        command, payload = self.command(engine, mode, session)
        return subprocess.run(command, input=payload, text=True, capture_output=True,
                              env={**self.env, **env}, timeout=15)

    def event(self, engine, session="root"):
        key = "session-id" if engine == "omp" else "thread-id"
        return {"type": "agent-turn-complete", key: session, "turn-id": 7,
                "last-assistant-message": "artifact: isolated useful result"}

    def seed_pending(self, engine, session="root"):
        directory = self.state(engine) / "synthetic"
        directory.mkdir(parents=True, exist_ok=True)
        (self.state(engine) / "synthetic.thread").write_text(session)
        (self.state(engine) / "synthetic.native").write_text("original birth")
        key = hashlib.sha256((session + ":7").encode()).hexdigest()
        record = directory / (key + ".json")
        record.write_text(json.dumps({**self.event(engine, session), "window": "synthetic",
                                      "received_at": 1, "status": "pending"}) + "\n")
        return record

    def set_authority(self, mode):
        path = self.authority / "synthetic.json"
        if mode == "unknown":
            path.write_text("{corrupt")
        elif mode == "unreadable":
            path.mkdir()
        else:
            path.write_text(json.dumps({"channel": "synthetic", "generation": 1,
                                        "authority": mode, "active_feed_seq": 0,
                                        "installed_at": "2026-09-24T00:00:00Z"}))

    def wait_for(self, predicate):
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(0.02)
        self.fail("isolated lifecycle did not reach the expected state")

    def test_disposable_callbacks_do_not_acquire_or_replace_roots(self):
        for engine in ENGINES:
            path = self.seed_pending(engine)
            original = path.read_bytes()
            for marker in ("MESH_MISHE_INVOCATION", "MISHE_TAUFTAUF_INVOCATION"):
                for mode in ("--start", "--receipt", "--drain", "--end"):
                    with self.subTest(engine=engine, marker=marker, mode=mode):
                        result = self.invoke(engine, mode, **{marker: "fixture-invocation"})
                        self.assertEqual(result.returncode, 3, result.stderr)
                        self.assertEqual(path.read_bytes(), original)
                        self.assertEqual((self.state(engine) / "synthetic.thread").read_text(), "root")
                        self.assertEqual((self.state(engine) / "synthetic.native").read_text(), "original birth")
                        self.assertFalse(path.with_suffix(".md").exists())
            self.assertFalse(self.effects.exists())
        # omp's first completion must not lazily adopt a disposable invocation.
        identity = self.state("omp") / "synthetic.thread"
        identity.unlink()
        result = self.invoke("omp", "--receipt", MESH_MISHE_INVOCATION="")
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertFalse(identity.exists())

    def test_wrong_or_unknown_authority_preserves_pending_and_root(self):
        for authority in ("mishe", "unknown", "unreadable", "unavailable-reader"):
            authority_path = self.authority / "synthetic.json"
            if authority_path.is_dir():
                authority_path.rmdir()
            elif authority_path.exists():
                authority_path.unlink()
            extra = {}
            if authority == "unavailable-reader":
                extra["MESH_MISHE_AUTHORITY_BIN"] = str(self.home / "absent-reader")
            else:
                self.set_authority(authority)
            for engine in ENGINES:
                path = self.seed_pending(engine)
                original = path.read_bytes()
                # Even a stale root stays pending while another authority owns the channel.
                (self.state(engine) / "synthetic.thread").write_text("newer-root")
                for mode in ("--start", "--receipt", "--drain", "--end"):
                    with self.subTest(authority=authority, engine=engine, mode=mode):
                        result = self.invoke(engine, mode, session="newer-root", **extra)
                        self.assertEqual(result.returncode, 3, result.stderr)
                        self.assertEqual(path.read_bytes(), original)
                        self.assertEqual((self.state(engine) / "synthetic.thread").read_text(), "newer-root")
                        self.assertEqual((self.state(engine) / "synthetic.native").read_text(), "original birth")
                        self.assertEqual(list(path.parent.glob("*.json")), [path])
                        self.assertFalse(path.with_suffix(".md").exists())
                ready = subprocess.run([str(self.bin / f"mesh-{engine}-lifecycle"), "--ready", "synthetic"],
                                       env=self.env, capture_output=True, timeout=5)
                self.assertEqual(ready.returncode, 3)
                (self.state(engine) / "synthetic.thread").unlink()
                self.assertEqual(self.invoke(engine, "--receipt", **extra).returncode, 3)
                self.assertFalse((self.state(engine) / "synthetic.thread").exists())
            self.assertFalse(self.effects.exists())
            self.assertFalse((self.mesh / "spend.log").exists())

    def test_legacy_roots_complete_and_auxiliary_receipts_do_not(self):
        for engine in ENGINES:
            with self.subTest(engine=engine):
                # Isolate the synthetic turn ID, reused by both engine fixtures,
                # from the previous engine's shared spend tape.
                (self.mesh / "spend.log").unlink(missing_ok=True)
                self.assertEqual(self.invoke(engine, "--start", "old-root").returncode, 0)
                started = self.invoke(engine, "--start")
                self.assertEqual(started.returncode, 0, started.stderr)
                identity = self.state(engine) / "synthetic.thread"
                self.assertEqual(identity.read_text(), "root")
                auxiliary = self.invoke(engine, "--receipt", "auxiliary")
                self.assertEqual(auxiliary.returncode, 0, auxiliary.stderr)
                self.assertFalse((self.state(engine) / "synthetic").exists())
                if engine == "omp":
                    identity.unlink()  # SessionStartEvent may not carry a session identity.
                task = self.mesh / "task-context/synthetic.json"
                task.parent.mkdir(exist_ok=True)
                task.write_text('[{"task":"fixture/work","owner":"synthetic","status":"done"}]')
                # The second engine also needs a visibly different pre-clear screen.
                (self.home / "screen").write_text("Completed root turn")
                result = self.invoke(engine, "--receipt")
                self.assertEqual(result.returncode, 0, result.stderr)
                directory = self.state(engine) / "synthetic"
                self.wait_for(lambda: any(json.loads(p.read_text())["status"] == "cleared"
                                          for p in directory.glob("*.json")))
                path, = directory.glob("*.json")
                receipt = json.loads(path.read_text())
                self.assertTrue(receipt["counted"])
                self.assertTrue(receipt["handoff"])
                self.assertIn("isolated useful result", path.with_suffix(".md").read_text())
                self.assertEqual(identity.read_text(), "root")
                self.assertFalse(task.exists())
                turns = (self.mesh / "spend.log").read_text()
                self.assertEqual(turns.count(f" {engine} openai "), 1)
                self.assertEqual(self.invoke(engine, "--drain").returncode, 0)
                self.assertEqual((self.mesh / "spend.log").read_text(), turns)

    def test_pending_receipt_recovers_after_legacy_authority_returns(self):
        for engine in ENGINES:
            with self.subTest(engine=engine):
                # The spend tape is shared, but these two fixtures reuse the same
                # synthetic event ID instead of distinct production session IDs.
                (self.mesh / "spend.log").unlink(missing_ok=True)
                path = self.seed_pending(engine)
                original = path.read_bytes()
                self.set_authority("mishe")
                fenced = self.invoke(engine, "--drain")
                self.assertEqual(fenced.returncode, 3, fenced.stderr)
                self.assertEqual(path.read_bytes(), original)
                self.assertFalse(path.with_suffix(".md").exists())

                self.set_authority("legacy")
                (self.home / "screen").write_text("Completed root turn")
                recovered = self.invoke(engine, "--drain")
                self.assertEqual(recovered.returncode, 0, recovered.stderr)
                self.assertEqual(json.loads(path.read_text())["status"], "cleared")
                self.assertTrue(path.with_suffix(".md").exists())
                turns = (self.mesh / "spend.log").read_text()
                self.assertEqual(turns.count(f" {engine} openai "), 1)
                self.assertEqual(self.invoke(engine, "--drain").returncode, 0)
                self.assertEqual((self.mesh / "spend.log").read_text(), turns)

    def test_start_holds_authority_until_root_is_recorded(self):
        for engine in ENGINES:
            with self.subTest(engine=engine):
                for name in ("entered", "release"):
                    (self.home / name).unlink(missing_ok=True)
                command, payload = self.command(engine, "--start")
                process = subprocess.Popen(command, env={**self.env, "FIXTURE_HOLD": "mesh-task"},
                                           text=True, stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    process.stdin.write(payload)
                    process.stdin.close()
                    process.stdin = None
                    self.wait_for(lambda: (self.home / "entered").exists())
                    self.assertFalse((self.state(engine) / "synthetic.thread").exists())
                    with (self.authority / "synthetic.lock").open("w") as lock:
                        with self.assertRaises(BlockingIOError):
                            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    (self.home / "release").touch()
                    _, error = process.communicate(timeout=10)
                    self.assertEqual(process.returncode, 0, error)
                    self.assertEqual((self.state(engine) / "synthetic.thread").read_text(), "root")
                finally:
                    (self.home / "release").touch()
                    if process.poll() is None:
                        process.kill()
                        process.communicate()

    def test_clear_lease_excludes_switch_but_allows_session_start_and_ready(self):
        for engine in ENGINES:
            with self.subTest(engine=engine):
                path = self.seed_pending(engine)
                for name in ("entered", "release"):
                    (self.home / name).unlink(missing_ok=True)
                (self.home / "screen").write_text("Before clear")
                command, _ = self.command(engine, "--drain")
                process = subprocess.Popen(command, env={**self.env, "FIXTURE_HOLD": "mesh-clear"},
                                           text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    self.wait_for(lambda: (self.home / "entered").exists())
                    with (self.authority / "synthetic.lock").open("w") as lock:
                        with self.assertRaises(BlockingIOError):
                            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    # A clear can trigger SessionStart before the old drain releases its locks.
                    started = self.invoke(engine, "--start", "next-root")
                    self.assertEqual(started.returncode, 0, started.stderr)
                    self.assertEqual((self.state(engine) / "synthetic.thread").read_text(), "next-root")
                    ready = subprocess.run([str(self.bin / f"mesh-{engine}-lifecycle"), "--ready", "synthetic"],
                                           env=self.env, capture_output=True, timeout=3)
                    self.assertEqual(ready.returncode, 3)
                    (self.home / "release").touch()
                    _, error = process.communicate(timeout=10)
                    self.assertEqual(process.returncode, 0, error)
                    self.assertEqual(json.loads(path.read_text())["status"], "cleared")
                finally:
                    (self.home / "release").touch()
                    if process.poll() is None:
                        process.kill()
                        process.communicate()

    def test_automatic_fresh_can_restore_before_sending_under_shared_lease(self):
        for engine in ENGINES:
            with self.subTest(engine=engine):
                (self.home / "send-attempt").unlink(missing_ok=True)
                result = subprocess.run([str(REPO / "scripts/mesh-tell"), "--automatic", "--fresh",
                                         "synthetic", "isolated fixture nudge"],
                                        env={**self.env, "FIXTURE_ENGINE": engine,
                                             "FIXTURE_START": str(self.bin / f"mesh-{engine}-lifecycle")},
                                        text=True, capture_output=True, timeout=15)
                # tmux deliberately rejects the final send. The important proof is that
                # the real nested --ready and SessionStart completed before attempting it.
                self.assertTrue((self.home / "send-attempt").exists(), result.stderr)
                identity = self.state(engine) / "synthetic.thread"
                self.assertTrue(identity.exists(), result.stderr)
                self.assertEqual(identity.read_text(), "after-clear")
                self.assertNotIn("UNCLEARED", result.stderr)
                self.assertNotIn("still WORKING", result.stderr)


if __name__ == "__main__":
    unittest.main()
