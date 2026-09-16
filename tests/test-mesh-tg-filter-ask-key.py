#!/usr/bin/env python3
"""Inbound replay keeps one ask identity; same-second distinct messages do not alias."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def frame(line):
    run = subprocess.run([str(ROOT / "scripts/mesh-tg-filter")], input=line + "\n",
                         text=True, capture_output=True)
    assert run.returncode == 0, run.stderr
    return run.stdout


def key(prompt):
    match = re.search(r"^Operator request key: (ask:tg-[a-f0-9]{24})$", prompt, re.M)
    assert match, prompt
    return match.group(1)


line = "2026-09-16T00:00:00Z  TEXT  prepare the report and send the file"
prompt = frame(line)
assert key(prompt) == key(frame(line))
assert key(prompt) != key(frame(line.replace("the report", "the chart")))
assert key(prompt) != key(frame(line.replace("00:00:00", "00:00:01")))
assert "mesh-task create <chain> <plan.tsv>" in prompt
assert "mesh-operator-followthrough" in prompt
assert "A reply or handoff alone does not queue or complete work." in prompt
assert key(frame(line.replace("TEXT", "DOCUMENT")))
assert not frame("2026-09-16T00:00:00Z  SENT  some reply")
assert not frame("2026-09-16T00:00:00Z  TEXT  /mesh-tv pause")
print("PASS: stable distinct ask identities, lifecycle directive, and suppression preserved")
