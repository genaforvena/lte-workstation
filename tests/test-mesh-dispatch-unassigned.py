"""Unassigned queue rows reach only the caller's measured free-worker pool."""
import os
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / 'scripts/mesh-mind-control').read_text()
start = source.index('_pick_agentic() {')
end = source.index('\n# _owner_target', start)
script = source[start:end] + '''
WORKERS=default-genome
AGENTIC_FALLBACK=default-witness
state_of(){ printf IDLE; }
engine_of(){ printf codex; }
health_of(){ printf HEALTHY; }
pick_recency(){ case "$1" in recent) printf 200;; older) printf 100;; *) printf 0;; esac; }
MESH_DISPATCH_CANDIDATES='recent older'
test "$(_pick_agentic)" = "$(printf 'older\\tfree:codex')" || exit 1
MESH_DISPATCH_CANDIDATES=''
test -z "$(_pick_agentic)" || exit 1
MESH_DISPATCH_CANDIDATES=older
state_of(){ printf UNKNOWN; }
test -z "$(_pick_agentic)" || exit 1
'''
result = subprocess.run(['bash', '-c', script], capture_output=True, text=True)
assert result.returncode == 0, result.stdout + result.stderr

source = (root / 'scripts/mesh-dispatch').read_text()
start = source.index('ledger_open_tasks(){')
end = source.index('\nif [ "${MESH_DISPATCH_LEDGER', start)
script = '''
BOARD_QUERY=fixture
LOG=/dev/null
fixture(){ printf '%s\\n' "$(printf -- '-\\tfree-task\\tnormal\\twork without owner')" "$(printf 'alpha\\tfixed-task\\tnormal\\tassigned work')"; }
priority_order(){ cat; }
''' + source[start:end] + '\nledger_open_tasks\n'
result = subprocess.run(['bash', '-c', script], capture_output=True, text=True)
assert result.returncode == 0, result.stderr
lines = result.stdout.splitlines()
assert len(lines) == 2 and 'owner:' not in lines[0] and 'owner: alpha' in lines[1], lines
print('PASS: optional owner survives queue; measured pool and fair idle tie-break enforced')
