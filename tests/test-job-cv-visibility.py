#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "job" / "mesh-job-cv-visibility"


def run(*args):
    return subprocess.run([sys.executable, str(TOOL), *args], text=True,
                          capture_output=True)


def write_json(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


def test_authenticated_probe_has_required_evidence():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "probe.json"
        write_json(p, {"timestamp": "2026-09-21T23:00:00Z", "state": "AUTHENTICATED", "route": "/applicant/resumes",
                       "options": [{"label": "Visible to all employers", "selected": True}],
                       "evidence": "/tmp/hh-visibility.png", "sha256": "a" * 64})
        r = run("--check", str(p))
        assert r.returncode == 0, r.stderr
        assert "AUTHENTICATED" in r.stdout
        assert "ranking_claim=none" in r.stdout


def test_login_redirect_is_unknown_and_never_zero():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "probe.json"
        write_json(p, {"timestamp": "2026-09-21T23:00:00Z", "state": "LOGGED_OUT", "route": "/applicant/resumes",
                       "reason": "redirected to /login", "options": []})
        r = run("--check", str(p))
        assert r.returncode == 0, r.stderr
        assert "UNKNOWN" in r.stdout
        assert "ranking_claim=none" in r.stdout
        assert "ranking=0" not in r.stdout


def test_maintenance_requires_two_stable_reads_and_seven_day_limit():
    with tempfile.TemporaryDirectory() as td:
        history = Path(td) / "history.jsonl"
        rows = [
            {"resume": "r1", "at": "2026-09-20T10:00:00Z", "action": "visibility",
             "state": "AUTHENTICATED", "before": "all employers", "after": "all employers"},
            {"resume": "r1", "at": "2026-09-20T10:05:00Z", "action": "read",
             "state": "AUTHENTICATED", "setting": "all employers"},
            {"resume": "r1", "at": "2026-09-20T10:06:00Z", "action": "read",
             "state": "AUTHENTICATED", "setting": "all employers"},
        ]
        history.write_text("\n".join(json.dumps(x) for x in rows) + "\n", encoding="utf-8")
        r = run("--maintenance-check", "--history", str(history), "--resume", "r1",
                "--now", "2026-09-21T10:00:00Z", "--state", "AUTHENTICATED",
                "--target", "all employers", "--before", "all employers", "--after", "all employers")
        assert r.returncode != 0
        assert "7-day" in r.stdout


def test_message_tracker_rejects_duplicate_and_keeps_retryable_failure():
    with tempfile.TemporaryDirectory() as td:
        incoming = Path(td) / "incoming.json"
        ledger = Path(td) / "ledger.jsonl"
        write_json(incoming, [{"id": "m1", "actionable": True, "disposition": "answered"},
                              {"id": "m1", "actionable": True, "disposition": "answered"},
                              {"id": "m2", "actionable": True, "disposition": "retry",
                               "retry_at": "2026-09-22T00:00:00Z"}])
        r = run("--track-messages", "--input", str(incoming), "--ledger", str(ledger))
        assert r.returncode != 0
        assert "duplicate" in r.stdout
        assert "retry_at" in r.stdout


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} CV visibility policy tests")
