"""Weekly export reads the whole text source and never probes an archive."""
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / 'scripts/mesh-board-weekly').read_text()
start = source.index('build_export(){')
end = source.index('\nif [ "${1:-}" = "--test" ]', start)
with tempfile.TemporaryDirectory() as td:
    path = Path(td) / 'chat.log'
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    path.write_text(f'{today}T00:00:00Z alpha@n :: retained\n2000-01-01T00:00:00Z alpha@n :: too old\n')
    env = dict(os.environ, BOARD=str(path), DAYS='7', TEST_OUTPUT=str(Path(td) / 'export'))
    script = 'set -o pipefail\nmesh-chat(){ echo "ARCHIVE PROBED" >&2; return 2; }\n' + source[start:end] + '\nbuild_export "$TEST_OUTPUT"\n'
    p = subprocess.run(['bash', '-c', script], env=env, text=True, capture_output=True)
    assert p.returncode == 0 and p.stdout.strip() == 'text', p.stdout + p.stderr
    output = Path(env['TEST_OUTPUT']).read_text()
    assert 'source: chat.log' in output and 'board-store.db' not in output
    assert 'retained' in output and 'too old' not in output
    path.unlink()
    p = subprocess.run(['bash', '-c', script], env=env, text=True, capture_output=True)
    assert p.returncode != 0, p.stdout + p.stderr
print('PASS: dated text-only export; missing source fails; no DB/history probe')
