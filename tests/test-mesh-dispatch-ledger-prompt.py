#!/usr/bin/env python3
"""Exercise queue rendering and delivered instructions using production functions."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/mesh-dispatch").read_text()
render = source[source.index("ledger_open_tasks(){"):source.index('\nif ! _ledger_tasks=', source.index("ledger_open_tasks(){"))]
identity = next(line for line in source.splitlines() if line.startswith("idof(){"))
start = source.index('_cid="$(idof "$task")"', source.index('for task in "${_cands[@]}"'))
frame = source[start:source.index("# RAW-TASK OUT-OF-BAND", start)]

with tempfile.TemporaryDirectory() as td:
    env = dict(os.environ, LOG=str(Path(td) / "log"),
               CLAIM_LIB=str(ROOT / "scripts/mesh-claim-shape.sh"))
    script = r'''
set -euo pipefail
. "$CLAIM_LIB"
# A prose-derived identity is deliberately distinct from the ledger identity.
slugof(){ printf mesh-owned; }
keyof(){ printf fallback; }
queue(){
  printf 'witness\tchain/review\t0\tDo mesh-owned work; quoted task:other/work\n'
  printf '%s\t%s\t%s\t%s\n' - chain/second 0 'Another independent request'
}
TASK_QUEUE=queue
''' + identity + '\n' + render + r'''
mapfile -t rows < <(ledger_open_tasks)
for task in "${rows[@]}"; do
''' + frame + r'''
  printf '%s\n' "$_cid" "$framed"
done
'''
    result = subprocess.run(["bash", "-c", script], env=env, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert lines[0] == "chain/review", result.stdout
    assert lines[2] == "chain/second", result.stdout
    for step, prompt in [("review", lines[1]), ("second", lines[3])]:
        for expected in (f"task:chain/{step}", f"mesh-task take chain {step}",
                         f"mesh-task done chain {step} <artifact>",
                         f"mesh-task reject chain {step} <reason>",
                         "A board [done] line alone does not close the task ledger."):
            assert expected in prompt, (expected, prompt)
        assert "post '[done]" not in prompt, prompt
print("PASS: canonical identities survive prose and every ledger prompt carries lifecycle commands")
