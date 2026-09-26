#!/usr/bin/env python3
"""Private unreviewed capture must agree with a live reread and owner evidence."""
import importlib.machinery
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import shutil
import tempfile
import time
import unittest
from unittest.mock import patch
from scripts import mesh_mishe_provenance as provenance

ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ.get("MESH_MISHE_CORE", "/home/mesh-home/mishe-tauftauf"))
loader = importlib.machinery.SourceFileLoader("mesh_mishe_corpus", str(ROOT / "scripts/mesh-mishe-s1-corpus"))
spec = importlib.util.spec_from_loader(loader.name, loader)
corpus = importlib.util.module_from_spec(spec)
loader.exec_module(corpus)


class CorpusTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.mesh = self.base / ".mesh"
        self.mesh.mkdir(mode=0o700)
        self.home = self.mesh / "mishe-tauftauf"
        self.home.mkdir(mode=0o700)
        self.evidence = self.base / "private"
        self.stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.secret = "PRIVATE-BODY-NEVER-IN-OUTPUT-9987"
        self.tmux = self.base / "tmux"
        self.tmux.write_text("#!/bin/sh\nif [ \"$1\" = display-message ]; then "
                             "printf '%s\\n' \"$MOCK_META\"; else "
                             "printf '%s\\n' \"$MOCK_PANE\"; fi\n")
        self.tmux.chmod(0o755)
        self.env = {**os.environ, "MESH_MISHE_CORE": str(CORE), "MESH_REPO": str(ROOT),
                    "MESH_DIR": str(self.mesh), "MESH_MISHE_GOAL_DIR": str(self.mesh),
                    "MESH_MISHE_SEMANTIC_DIR": str(self.mesh), "MESH_MISHE_SESSION": "fixture",
                    "PATH": str(self.base) + ":" + os.environ["PATH"],
                    "MESH_MISHE_RENDER_SOURCE": "pane"}
        self.before_env = dict(os.environ)
        os.environ.update(self.env)
        self.addCleanup(lambda: (os.environ.clear(), os.environ.update(self.before_env)))

    def configure(self, channel="health", audit=None):
        role = "check" if channel == "health" else channel
        self.env["MOCK_META"] = f'{channel}|0|0|"exec /safe/mesh-dash {role}"'
        self.env["MOCK_PANE"] = self.secret + "\n-- pane live " + self.stamp + " · 30s · ticks every frame --"
        os.environ.update(self.env)
        goal = self.mesh / f".goal-{channel}.cache"
        goal.write_text(self.secret)
        if channel == "health":
            (self.mesh / ".fleet-health.cache").write_text(self.secret)
        if audit is not None:
            path = self.base / "audit"
            path.write_text("#!/bin/sh\nprintf '%s\\n' \"$MOCK_AUDIT\"\n")
            path.chmod(0o755)
            self.env["MESH_MISHE_TASK_AUDIT_CMD"] = str(path)
            self.env["MOCK_AUDIT"] = audit
            os.environ.update(self.env)
        # Feed the actual projector output from an actual pane-renderer invocation.
        with tempfile.TemporaryDirectory() as sandbox:
            env = {**self.env, "MESH_MISHE_HOME": sandbox}
            rendered = subprocess.run([str(ROOT / "scripts/mesh-mishe-render"), channel, role],
                                      env=env, capture_output=True, check=True)
            frame = Path(sandbox) / "frame"
            frame.write_bytes(rendered.stdout)
            projected = subprocess.run([str(ROOT / "scripts/mesh-mishe-project"), "--channel", channel,
                                        str(frame), str(frame)], env=env, capture_output=True, check=True).stdout
        return projected.decode()

    def event(self, body, channel="health", event_id="a" * 64):
        stamp = "2026-09-25T00:00:00.000000Z"
        (self.home / "feed").write_text(
            f"v1 {1:020d} {stamp} observation/{channel} ::\n" +
            "".join("    | " + line + "\n" for line in body.splitlines()) + "    .\n")
        parity = self.home / "parity"
        parity.mkdir(exist_ok=True)
        (parity / "projected.jsonl").write_text(json.dumps({
            "channel": channel, "event_id": event_id, "kind": "pane", "at": stamp,
            "source": "top-pane", "feed_seq": 1}) + "\n")

    def bind(self, body, channel="health", event_id="a" * 64, seq=1, audit=None):
        paths = corpus.sources_module().provenance_files(channel, self.mesh, ROOT)
        stamp = {"version": 1, "tick": "b" * 32, "event_id": event_id,
                 "channel": channel, "projected_sha256": hashlib.sha256(body.encode()).hexdigest(),
                 "feed_seq": seq,
                 "sources": [{"origin": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                              "mtime_ns": path.stat().st_mtime_ns} for path in paths],
                 "audit_sha256": hashlib.sha256((audit + "\n").encode()).hexdigest() if audit else None}
        bound = self.home / "parity/source-bound"
        bound.mkdir(exist_ok=True)
        target = bound / f"{seq:020d}.json"
        target.write_text(json.dumps(stamp))
        target.chmod(0o600)
        return target

    def cases(self):
        return list((self.evidence / "cases").iterdir())

    def run_capture(self, *options):
        return subprocess.run([str(ROOT / "scripts/mesh-mishe-s1-corpus"), "capture", "--after", "0",
                               "--home", str(self.home), "--evidence-root", str(self.evidence), *options],
                              env=self.env, text=True, capture_output=True)

    def run_status(self):
        return subprocess.run([str(ROOT / "scripts/mesh-mishe-s1-corpus"), "status",
                               "--home", str(self.home), "--evidence-root", str(self.evidence)],
                              env=self.env, text=True, capture_output=True)


    def test_candidate_private_source_and_replay_without_label_or_dispatch(self):
        body = self.configure()
        self.event(body)
        self.bind(body)
        result = self.run_capture()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("captured=1", result.stdout)
        self.assertNotIn(self.secret, result.stdout + result.stderr)
        cases = list((self.evidence / "cases").iterdir())
        self.assertEqual(len(cases), 1)
        manifest = json.loads((cases[0] / "case.json").read_text())
        self.assertEqual(manifest["version"], 2)
        self.assertEqual(manifest["provenance_phase"], "s0_projection_hash_matched")
        self.assertEqual(manifest["status"], "candidate_unreviewed")
        self.assertEqual(manifest["original_feed_seq"], 1)
        self.assertEqual(manifest["projected_view"], body)
        self.assertNotIn("label", json.dumps(manifest))
        self.assertNotIn("authority", manifest)
        bound_bytes = (self.home / "parity/source-bound/00000000000000000001.json").read_bytes()
        self.assertEqual((cases[0] / "s0-bound.json").read_bytes(), bound_bytes)
        self.assertEqual(manifest["bound_sha256"], hashlib.sha256(bound_bytes).hexdigest())
        self.assertIn(self.secret, (cases[0] / "sources/0").read_text())
        for path in [self.evidence, self.evidence / "cases", cases[0], cases[0] / "case.json",
                     cases[0] / "sources/0", cases[0] / "s0-bound.json"]:
            self.assertEqual(path.stat().st_mode & 0o077, 0)
        status = self.run_status()
        self.assertEqual(status.returncode, 0, status.stdout)
        self.assertIn("captured_candidates=1 distinct_capture_keys=1 reviewed_labels=0", status.stdout)
        self.assertIn("s0_bound_candidates=1 historical_candidates=0", status.stdout)
        self.assertNotIn(self.secret, status.stdout)
        replay = self.run_capture()
        self.assertEqual(replay.returncode, 0, replay.stdout)
        self.assertIn("duplicate=1", replay.stdout)
        idle = subprocess.run([str(ROOT / "scripts/mesh-mishe-s1-corpus"), "capture",
                               "--after", "1", "--home", str(self.home),
                               "--evidence-root", str(self.evidence)],
                              env=self.env, text=True, capture_output=True)
        self.assertEqual(idle.returncode, 0, idle.stdout)
        self.assertIn("captured=0 duplicate=0 skipped=0", idle.stdout)
        self.assertIn("last_capture_status=idle", self.run_status().stdout)
        self.assertEqual(list((self.evidence / "cases").iterdir()), cases)
        self.assertFalse((self.home / ".mesh-mishe-seen-health").exists())
        self.assertFalse((self.home / "parity/staged").exists())

    def test_empty_sound_tick_is_bound_without_admitting_empty_other_sources(self):
        tick = self.mesh / ".records-tick"
        tick.touch()  # mesh-records' real liveness marker has zero bytes; mtime is its evidence.
        body = self.configure("sound")
        self.assertIn("semantic=archivist:fresh", body)
        self.event(body, "sound")
        sentinel = self.home / ".fleet-corpus-capture"
        sentinel.touch(mode=0o600)
        stamp = provenance.source_stamp("sound", "a" * 64, "b" * 32, self.home, ROOT, body)
        self.assertIsNotNone(stamp, "the opted-in S0 producer must bind the real empty tick")
        self.assertEqual(stamp["sources"][1]["sha256"], hashlib.sha256(b"").hexdigest())
        self.bind(body, "sound")
        result = self.run_capture()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("captured=1", result.stdout)
        case = self.cases()[0]
        self.assertEqual((case / "sources/1").read_bytes(), b"")
        self.assertEqual(json.loads((case / "case.json").read_text())["provenance_phase"],
                         "s0_projection_hash_matched")

    def test_empty_sound_tick_update_after_s0_stamp_preserves_original_provenance(self):
        tick = self.mesh / ".records-tick"
        tick.touch()
        body = self.configure("sound")
        self.event(body, "sound")
        sentinel = self.home / ".fleet-corpus-capture"
        sentinel.touch(mode=0o600)
        stamp = provenance.source_stamp("sound", "a" * 64, "b" * 32, self.home, ROOT, body)
        self.assertIsNotNone(stamp)
        self.assertEqual(stamp["sources"][1]["sha256"], hashlib.sha256(b"").hexdigest())
        bound = self.home / "parity/source-bound"
        bound.mkdir(parents=True, exist_ok=True)
        target = bound / "00000000000000000001.json"
        target.write_text(json.dumps({**stamp, "feed_seq": 1}))
        target.chmod(0o600)

        original_mtime_ns = stamp["sources"][1]["mtime_ns"]
        os.utime(tick, ns=(original_mtime_ns + 1_000_000_000,
                           original_mtime_ns + 1_000_000_000))
        result = self.run_capture()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        case = self.cases()[0]
        manifest = json.loads((case / "case.json").read_text())
        self.assertEqual(json.loads((case / "s0-bound.json").read_text()),
                         {**stamp, "feed_seq": 1})
        self.assertEqual(manifest["sources"][1]["mtime_ns"], original_mtime_ns)
        self.assertEqual((case / "sources/1").read_bytes(), b"")

        other = self.mesh / ".fleet-health.cache"
        other.touch()
        with tempfile.TemporaryDirectory() as snapshot_dir:
            with self.assertRaisesRegex(corpus.Unavailable, "source_unavailable"):
                corpus.snapshot((other,), Path(snapshot_dir), "health", corpus.sources_module())

    def test_bound_source_survives_rotating_pane_identity_not_historical(self):
        self.configure()
        key = self.home / "projection.key"
        key.write_bytes(b"k" * 32)
        key.chmod(0o600)
        body = corpus.render_projection("health", ROOT, {
            **self.env, "MESH_MISHE_HOME": str(self.home)})
        self.event(body)
        self.bind(body)
        self.env["MOCK_PANE"] = (self.secret + "\nNEW-TOP-SIGNAL\n-- pane live " +
                                 self.stamp + " · 30s · ticks every frame --")
        os.environ.update(self.env)
        current = corpus.render_projection("health", ROOT, {
            **self.env, "MESH_MISHE_HOME": str(self.home)})
        safe_fleet_view, _ = corpus.core_modules()
        self.assertNotEqual(body, current)
        self.assertEqual(safe_fleet_view(body, "health"), safe_fleet_view(current, "health"))
        historical = self.run_capture("--allow-historical-corroboration")
        self.assertEqual(historical.returncode, 2, historical.stdout)
        self.assertIn("skipped reason=projection_mismatch", historical.stdout)
        bound = self.run_capture()
        self.assertEqual(bound.returncode, 0, bound.stdout)
        self.assertIn("captured=1", bound.stdout)
        self.assertEqual(json.loads((self.cases()[0] / "case.json").read_text())["projected_view"], body)

    def test_status_rejects_corrupted_private_snapshot(self):
        body = self.configure()
        self.event(body)
        self.bind(body)
        self.assertEqual(self.run_capture().returncode, 0)
        case = next((self.evidence / "cases").iterdir())
        (case / "sources/0").write_text("mutated archived source")
        invalid = self.run_status()
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("UNKNOWN reason=existing_case_invalid", invalid.stdout)
        self.assertNotIn(self.secret, invalid.stdout + invalid.stderr)

    def test_status_rejects_tampered_bound_artifact(self):
        body = self.configure()
        self.event(body)
        self.bind(body)
        self.assertEqual(self.run_capture().returncode, 0)
        artifact = self.cases()[0] / "s0-bound.json"
        artifact.write_text("{}")
        status = self.run_status()
        self.assertEqual(status.returncode, 2)
        self.assertIn("UNKNOWN reason=existing_case_invalid", status.stdout)
        self.assertNotIn(self.secret, status.stdout)


    def test_bound_stamp_required_and_source_bytes_match_original_projection(self):
        body = self.configure()
        self.event(body)
        missing = self.run_capture()
        self.assertEqual(missing.returncode, 2, missing.stdout)
        self.assertIn("skipped reason=bound_stamp_missing", missing.stdout)
        self.assertEqual(self.cases(), [])
        bound = self.bind(body)
        self.assertEqual(self.run_capture().returncode, 0)
        self.assertEqual(len(self.cases()), 1)
        shutil.rmtree(self.cases()[0])
        source = self.mesh / ".fleet-health.cache"
        source.write_text("different private producer bytes")
        changed = self.run_capture()
        self.assertEqual(changed.returncode, 2, changed.stdout)
        self.assertIn("skipped reason=bound_source_mismatch", changed.stdout)
        self.assertEqual(self.cases(), [])
        self.assertNotIn(self.secret, changed.stdout + changed.stderr)
        source.write_text(self.secret)
        prior_ns = json.loads(bound.read_text())["sources"][1]["mtime_ns"]
        os.utime(source, ns=(prior_ns + 1_000_000_000, prior_ns + 1_000_000_000))
        touched = self.run_capture()
        self.assertEqual(touched.returncode, 2, touched.stdout)
        self.assertIn("skipped reason=bound_source_mismatch", touched.stdout)
        self.assertEqual(self.cases(), [])
        self.assertTrue(bound.exists())

    def test_bound_stamp_rejects_mismatched_identity_and_malformed_records(self):
        body = self.configure()
        self.event(body)
        bound = self.bind(body)
        original = json.loads(bound.read_text())
        variants = (
            {**original, "projected_sha256": "0" * 64},
            {**original, "feed_seq": 2},
            {**original, "channel": "wake"},
            {**original, "event_id": "c" * 64},
            {**original, "sources": original["sources"] + original["sources"][:1]},
            {**original, "sources": [{**original["sources"][0], "mtime_ns": "bad"}]},
            {**original, "audit_sha256": "f" * 64},
        )
        for invalid in variants:
            with self.subTest(invalid=invalid):
                bound.write_text(json.dumps(invalid))
                result = self.run_capture()
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn("skipped reason=bound_stamp_invalid", result.stdout)
                self.assertEqual(self.cases(), [])

    def test_historical_opt_in_is_separate_and_version_one_remains_historical(self):
        body = self.configure()
        self.event(body)
        historical = self.run_capture("--allow-historical-corroboration")
        self.assertEqual(historical.returncode, 0, historical.stdout)
        case = self.cases()[0]
        manifest_path = case / "case.json"
        historical_manifest = json.loads(manifest_path.read_text())
        self.assertEqual(historical_manifest["provenance_phase"], "post_observation_reprojection")
        self.assertNotIn("bound_sha256", historical_manifest)
        self.assertFalse((case / "s0-bound.json").exists())
        self.assertNotIn("label", historical_manifest)
        # A persisted v1 case is recognized but never rewritten or promoted by a later bound stamp.
        historical_manifest["version"] = 1
        del historical_manifest["provenance_phase"]
        manifest_path.write_text(json.dumps(historical_manifest))
        self.bind(body)
        replay = self.run_capture()
        self.assertEqual(replay.returncode, 2, replay.stdout)
        self.assertIn("skipped reason=historical_case_exists", replay.stdout)
        self.assertEqual(json.loads(manifest_path.read_text()), historical_manifest)
        self.assertEqual(self.run_status().returncode, 2)  # latest attempt was UNKNOWN, case still valid
        self.assertIn("captured_candidates=1", self.run_status().stdout)
        self.assertIn("s0_bound_candidates=0 historical_candidates=1", self.run_status().stdout)
        second = ("v1 00000000000000000002 2026-09-25T00:00:01.000000Z observation/health ::\n"
                  + "".join("    | " + line + "\n" for line in body.splitlines()) + "    .\n")
        with (self.home / "feed").open("a") as stream:
            stream.write(second)
        with (self.home / "parity/projected.jsonl").open("a") as stream:
            stream.write(json.dumps({"channel": "health", "event_id": "a" * 64,
                                     "kind": "pane", "at": "2026-09-25T00:00:01.000000Z",
                                     "source": "top-pane", "feed_seq": 2}) + "\n")
        self.bind(body, seq=2)
        result = self.run_capture()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("captured=1", result.stdout)
        self.assertEqual(len(self.cases()), 2)
        self.assertEqual({json.loads((case / "case.json").read_text()).get("provenance_phase",
                          "post_observation_reprojection") for case in self.cases()},
                         {"post_observation_reprojection", "s0_projection_hash_matched"})
        self.assertIn("distinct_capture_keys=2", self.run_status().stdout)
        self.assertIn("s0_bound_candidates=1 historical_candidates=1", self.run_status().stdout)

    def test_bad_parity_and_symlink_source_fail_closed(self):
        self.event(self.configure(), event_id="not-an-id")
        bad = self.run_capture()
        self.assertEqual(bad.returncode, 2)
        self.assertIn("UNKNOWN reason=invalid_parity", bad.stdout)
        self.assertNotIn(self.secret, bad.stdout)
        body = self.configure()
        self.event(body)
        source = self.mesh / ".fleet-health.cache"
        self.bind(body)
        source.rename(self.mesh / "real-source")
        source.symlink_to("real-source")
        unsafe = self.run_capture()
        self.assertEqual(unsafe.returncode, 2)
        self.assertIn("skipped reason=invalid_input_file", unsafe.stdout)
        with tempfile.TemporaryDirectory() as snapshot_dir:
            with self.assertRaisesRegex(corpus.Unavailable, "invalid_input_file"):
                corpus.snapshot((source,), Path(snapshot_dir), "health", corpus.sources_module())
        self.assertFalse(list((self.evidence / "cases").iterdir()))

    def test_real_source_mutation_between_snapshot_and_rerender(self):
        body = self.configure()
        self.event(body)
        self.bind(body)
        registry = corpus.sources_module()
        safe, parse = corpus.core_modules()
        row = corpus.parity_rows(self.home)[(1, "health")]
        entry = parse((self.home / "feed").read_bytes())[0]
        corpus.private_root(self.evidence)
        cases = self.evidence / "cases"
        corpus.private_root(cases)
        original = corpus.render_projection
        calls = 0

        def mutate_after_snapshot(channel, repo, env):
            nonlocal calls
            calls += 1
            if calls == 2:
                source = self.mesh / ".fleet-health.cache"
                source.write_text("changed actual producer bytes")
            return original(channel, repo, env)

        with patch.object(corpus, "render_projection", side_effect=mutate_after_snapshot):
            with self.assertRaisesRegex(corpus.Unavailable, "source_changed"):
                corpus.capture(entry, row, self.home, self.mesh, ROOT, cases, safe, registry)
        self.assertEqual(list(cases.iterdir()), [])

    def test_event_audit_exact_owner_and_stale_semantic_only(self):
        overdue = "OVERDUE\twake\tpath/task\tlease=2026-09-24T00:00:00Z"
        wrong = "OVERDUE\thire\tpath/other\tlease=2026-09-24T00:00:00Z"
        body = self.configure("wake", audit=wrong + "\n" + overdue)
        self.assertIn("semantic=obligations:stale", body)
        self.event(body, channel="wake")
        self.bind(body, channel="wake", audit=overdue)
        good = self.run_capture()
        self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
        case = next((self.evidence / "cases").iterdir())
        self.assertEqual((case / "sources/1").read_text(), overdue + "\n")
        self.assertNotIn(wrong, (case / "sources/1").read_text())
        self.assertNotIn("label", (case / "case.json").read_text())
        shutil.rmtree(case)
        self.env["MOCK_AUDIT"] = overdue.replace("path/task", "path/changed")
        os.environ.update(self.env)
        changed = self.run_capture()
        self.assertEqual(changed.returncode, 2, changed.stdout)
        self.assertIn("skipped reason=bound_audit_mismatch", changed.stdout)
        self.env["MOCK_AUDIT"] = wrong
        os.environ.update(self.env)
        # A separately isolated zero-overdue lane cannot be treated as healthy evidence.
        with self.assertRaisesRegex(corpus.Unavailable, "audit_no_overdue"):
            corpus.audit_rows("wake", ROOT, self.env)
        self.assertEqual(self.run_capture().returncode, 2)
        self.assertEqual(list((self.evidence / "cases").iterdir()), [])

    def test_distinct_sequences_same_capture_key_not_independent_cases(self):
        body = self.configure()
        self.event(body)
        self.bind(body)
        self.assertEqual(self.run_capture().returncode, 0)
        second = ("v1 00000000000000000002 2026-09-25T00:00:01.000000Z observation/health ::\n"
                  + "".join("    | " + line + "\n" for line in body.splitlines()) + "    .\n")
        with (self.home / "feed").open("a") as stream:
            stream.write(second)
        with (self.home / "parity/projected.jsonl").open("a") as stream:
            stream.write(json.dumps({"channel": "health", "event_id": "a" * 64,
                                     "kind": "pane", "at": "2026-09-25T00:00:01.000000Z",
                                     "source": "top-pane", "feed_seq": 2}) + "\n")
        self.bind(body, seq=2)
        replay = self.run_capture()
        self.assertEqual(replay.returncode, 0, replay.stdout)
        self.assertIn("duplicate=2", replay.stdout)
        self.assertEqual(len(list((self.evidence / "cases").iterdir())), 1)
        self.assertIn("captured_candidates=1 distinct_capture_keys=1 reviewed_labels=0",
                      self.run_status().stdout)


if __name__ == "__main__":
    unittest.main()
