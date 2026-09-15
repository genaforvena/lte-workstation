#!/usr/bin/env python3
"""Regression: bank answers must not replace argparse's CLI options in _main."""
import contextlib
import importlib.util
import io
import pathlib
import sys
from importlib.machinery import SourceFileLoader


ROOT = pathlib.Path(__file__).resolve().parents[1]
source = ROOT / "job/mesh-job-reply"
sys.path.insert(0, str(source.parent))
spec = importlib.util.spec_from_loader("mesh_job_reply", SourceFileLoader("mesh_job_reply", str(source)))
reply = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = reply
spec.loader.exec_module(reply)

row = {"vacancy_id": "shadow-regression", "title": "Engineer", "employer": "Fixture"}
reply.invited = lambda limit=None: [row]
reply.load = lambda: {}
reply.save = lambda _state: None
reply.chat_id_for = lambda _employer, _title: "fixture-chat"
reply.drive = lambda _args, timeout=120: None
reply.thread_state = lambda _cid: ("ok", {reply.K_TEXT: "What are your salary expectations?"})
reply.bank_answer = lambda _question: "The salary range is not specified."
reply.free_slots_text = lambda: "Tue 15 Sep 12:00 (МСК)"
extras = []


def compose(_slots, extra=""):
    extras.append(extra)
    return "fixture reply"


reply.compose = compose
sys.argv = ["mesh-job-reply", "--dry", "--json", "--max", "1"]
stdout = io.StringIO()
with contextlib.redirect_stdout(stdout):
    try:
        reply._main()
    except SystemExit as exit_status:
        result = exit_status.code
    else:
        result = 0

assert result == 0, "dry run should return successfully"
assert extras == ["The salary range is not specified."], extras
assert '"answered"' in stdout.getvalue(), stdout.getvalue()
