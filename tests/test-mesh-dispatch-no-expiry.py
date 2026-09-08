"""An old unclaimed legacy task remains dispatchable; only explicit closure ends it."""
import os
import subprocess
import tempfile
from pathlib import Path


root = Path(__file__).resolve().parents[1]
source = (root / "scripts/mesh-dispatch").read_text()
start = source.index("is_open(){")
end = source.index("\n# READ-ONLY gate", start)
is_open = source[start:end]

script = r'''
set -uo pipefail
norm(){ printf old-task; }
keyof(){ printf OLD; }
slugof(){ printf old-task; }
claim_closes_id(){ return 1; }
idle_exposure_tick(){ printf 1; }
idle_exposure_count(){ printf 1; }
effective_stale_ticks(){ printf 1; }
task_is_incident(){ return 1; }
task_not_due(){ return 1; }
_refiled_after(){ return 1; }
route_orphan_tool_of(){ :; }
_route_orphan_resolved_after(){ return 1; }
claim_body_if(){ return 1; }
claim_id_of(){ :; }
claim_ts(){ :; }
evaporated_post(){ printf called >"$EVAP_CALL"; }
STATE_BLOB=''
STATE_NL=$'\n\n'
NL=$'\n'
CLAIMS=''
NOW=20000
N_IDLE=1
READ_ONLY=0
PACE_HELD=0
STALE_TICKS=1
STALE_TTL=1
EVAP_REASON_DONE=done
EVAP_REASON_DONE_FRESH=done
EVAP_REASON_REFILED=refiled
EVAP_REASON_RESOLVED=resolved
''' + is_open + r'''
is_open 'old-task: must remain until explicitly done or ignored' 1
test ! -e "$EVAP_CALL"
'''

with tempfile.TemporaryDirectory() as td:
    result = subprocess.run(["bash", "-c", script], env=dict(os.environ, EVAP_CALL=str(Path(td) / "evaporated")),
                            text=True, capture_output=True)
    assert result.returncode == 0, f"rc={result.returncode}\n{result.stdout}{result.stderr}"
print("PASS: old unclaimed task stays dispatchable without an explicit terminal record")
