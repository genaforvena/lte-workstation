"""The temporary dispatch-only pace bypass must not call a held governor."""
import os
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / 'scripts/mesh-dispatch').read_text()
start = source.index('if [ "${MESH_DISPATCH_NO_PACE:-0}" = 1 ]; then')
end = source.index('\n# CANDIDATE LIST', start)
gate = source[start:end]

with tempfile.TemporaryDirectory() as td:
    script = '''
mesh-pace(){ return 1; }
ts(){ printf test; }
LOG="$TEST_LOG"
n_open=1
''' + gate + '''
printf 'REACHED\\n'
'''
    env = dict(os.environ, TEST_LOG=str(Path(td) / 'dispatch.log'), MESH_DISPATCH_NO_PACE='1')
    result = subprocess.run(['bash', '-c', script], env=env, text=True, capture_output=True)
    assert result.returncode == 0 and result.stdout == 'REACHED\n', result.stdout + result.stderr
    log = Path(env['TEST_LOG']).read_text()
    assert 'PACE-BYPASS' in log and 'PACE-SKIP' not in log, log
print('PASS: dispatch-only no-pace bypass skips a held mesh-pace gate')

start = source.index('PACE_HELD=0')
end = source.index('\n# NOW:', start)
probe = source[start:end]
with tempfile.TemporaryDirectory() as td:
    script = '''
mesh-pace(){ printf called >"$TEST_CALLED"; return 1; }
N_IDLE=1
READ_ONLY=0
''' + probe + '''
test "$PACE_HELD" = 0
test ! -e "$TEST_CALLED"
'''
    env = dict(os.environ, TEST_CALLED=str(Path(td) / 'called'), MESH_DISPATCH_NO_PACE='1')
    result = subprocess.run(['bash', '-c', script], env=env, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
print('PASS: dispatch-only no-pace bypass skips the read-only pace probe')
