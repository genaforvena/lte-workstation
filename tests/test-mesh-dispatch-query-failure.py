"""A failed queue query, including partial output, must never route work."""
import os
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / 'scripts/mesh-dispatch').read_text()
start = source.index('ledger_open_tasks(){')
end = source.index('\nelse\n', start)
snippet = source[start:end] + '\nfi\n'
with tempfile.TemporaryDirectory() as td:
    for result in (0, 9):
        env = dict(os.environ, LOG=str(Path(td) / 'dispatch.log'), QUERY_RESULT=str(result))
        script = '''set -uo pipefail
BOARD_QUERY=/bin/false
# Intercept the executable in the same shell, retaining the executable-path gate.
/bin/false(){
  if [ "$QUERY_RESULT" != 0 ]; then
    printf 'genome\\tpartial-task\\tnormal\\tpartial result\\n'
  fi
  return "$QUERY_RESULT"
}
priority_order(){ cat; }
ts(){ printf test; }
''' + snippet + '''
test "${#OPEN[@]}" = 0
'''
        run = subprocess.run(['bash', '-c', script], env=env, capture_output=True, text=True)
        assert run.returncode == (0 if result == 0 else 1), run.stdout + run.stderr
    assert 'REFUSED ledger-query failed' in (Path(td) / 'dispatch.log').read_text()
print('PASS: empty queue succeeds; failed partial query refuses dispatch')
