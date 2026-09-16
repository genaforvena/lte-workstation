#!/usr/bin/env python3
"""Delivery without a canonical take must remain eligible for retry."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/mesh-dispatch").read_text()
start = source.index("# LEDGER-PATH STATE FILTER")
end = source.index("\nfi\n# HELD PARTITION", start)
gate = source[start:end]
with tempfile.TemporaryDirectory() as td:
    state = Path(td) / "state"
    state.write_text("unclaimed\tdelivered\t1\nhuman\thuman-owned\t1\n")
    script = r'''
set -euo pipefail
norm(){ printf '%s' "$1"; }
OPEN=(unclaimed human fresh)
NL=$'\n'
STATE_BLOB=$(cut -f1 "$STATE")
STATE_NL="$NL$STATE_BLOB$NL"
''' + gate + r'''
printf '%s\n' "${OPEN[@]}"
'''
    result = subprocess.run(["bash", "-c", script], env=dict(os.environ, STATE=str(state)),
                            text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == ["unclaimed", "fresh"], result.stdout
print("PASS: delivery is retryable while canonical task stays open; human refusal remains excluded")
