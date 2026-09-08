"""Roll-call consumes only the durable text board, without database probes."""
import os
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / 'scripts/mesh-roll-call').read_text()
start = source.index('board_corpus(){')
end = source.index('\nsettled_check(){', start)
with tempfile.TemporaryDirectory() as td:
    path = Path(td) / 'chat.log'
    path.write_text('2026-09-08T00:00:00Z alpha@n :: [fyi] history\n')
    env = dict(os.environ, MESH_DIR=td)
    script = 'docstore_bin(){ echo "DB PROBED" >&2; return 1; }\n' + source[start:end] + '\nboard_corpus "$MESH_DIR/result"\n'
    result = subprocess.run(['bash', '-c', script], env=env, text=True, capture_output=True)
    assert result.returncode == 0 and not result.stderr, result.stdout + result.stderr
    assert result.stdout.strip() == 'text=1 source=chat.log', result.stdout
    assert (Path(td) / 'result').read_bytes() == path.read_bytes()
    path.unlink()
    result = subprocess.run(['bash', '-c', script], env=env, text=True, capture_output=True)
    assert result.returncode != 0 and 'unreadable' in result.stderr
print('PASS: text-only corpus; no DB probes; missing source fails visibly')
