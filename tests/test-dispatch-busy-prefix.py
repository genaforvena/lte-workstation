"""Execute the production offer loop with five held tasks before a free owner."""
from pathlib import Path
import os
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[1]
source = (repo / "scripts/mesh-dispatch").read_text()
loop = source[source.index("# CANDIDATE LIST, not a single pick"):]
setup = r'''
OPEN=(busy1 busy2 busy3 busy4 busy5 ready later)
owner_task=""
n_open=${#OPEN[@]}
STATE="$FIXTURE/state"
LOG="$FIXTURE/log"
norm(){ printf '%s' "$1"; }
idof(){ printf '%s' "$1"; }
ts(){ printf 'fixture'; }
mesh-mind-control(){
    printf '%s\n' "$MESH_DISPATCH_RAW_TASK" >> "$FIXTURE/offers"
    case "$MESH_DISPATCH_RAW_TASK" in busy*) return 3;; esac
    return 0
}
'''
with tempfile.TemporaryDirectory() as directory:
    result = subprocess.run(["bash", "-c", setup + loop],
                            env={**os.environ, "FIXTURE": directory},
                            text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    offers = (Path(directory) / "offers").read_text().splitlines()
    assert offers == ["busy1", "busy2", "busy3", "busy4", "busy5", "ready"], offers
    state = (Path(directory) / "state").read_text().splitlines()
    assert len(state) == 1 and state[0].startswith("ready\tdelivered\t"), state
print("dispatch busy prefix: PASS (later owner reached; one delivery; holds unsealed)")
