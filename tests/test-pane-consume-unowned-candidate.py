#!/usr/bin/env python3
"""The real wake entrypoint must preserve claimable shared-pool candidates."""
import os
from pathlib import Path
import subprocess
import tempfile

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/mesh-pane-consume"
with tempfile.TemporaryDirectory() as raw:
    home = Path(raw)
    bindir = home / ".local/bin"
    bindir.mkdir(parents=True)
    (home / ".mesh").mkdir()
    stub = bindir / "mesh-task"
    stub.write_text('''#!/bin/sh
if [ "$1" = queue ]; then
  printf 'bob\\tother/work\\t90\\treserved\\n-\\tpool/work\\t80\\tunowned\\n'
elif [ "$1" = check ]; then
  printf '%s\\n' "$*" >> "$HOME/checks"
  [ "$3" = pool/work ] && [ "$4" = alice ] && [ "${REFUSE:-0}" = 0 ]
else exit 64
fi
''')
    stub.chmod(0o755)
    env = {**os.environ, "HOME": raw, "PATH": f"{bindir}:/usr/bin:/bin"}
    got = subprocess.run([str(SCRIPT), "--task-candidate", "alice"], env=env,
                         text=True, capture_output=True)
    assert got.returncode == 0 and got.stdout.startswith("-\tpool/work\t"), (
        "claimable ownerless task was filtered out of wake path", got.stdout, got.stderr)
    assert (home / "checks").read_text().splitlines() == ["check dispatch pool/work alice"]
    refused = subprocess.run([str(SCRIPT), "--task-candidate", "alice"],
                             env={**env, "REFUSE": "1"}, text=True, capture_output=True)
    assert refused.returncode != 0 and not refused.stdout, "refused shared task must stay excluded"
print("PASS: wake sees unowned candidate, excludes other owners, honors exact claim check")
