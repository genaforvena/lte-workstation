"""Exercise the production resume block with isolated delivery and board sinks."""
import os
import subprocess
import tempfile
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / 'scripts/mesh-mind-control').read_text()
start = source.index('  if [ -z "$remote_win" ]; then\n    local rsf;')
end = source.index('  # Re-read canonical state at the delivery boundary', start)
block = source[start:end]
with tempfile.TemporaryDirectory() as td:
    script = '''
mesh-tell(){ printf 'sent\\n' >> "$MESH_DIR/sends"; }
mesh-chat(){ :; }
dispatch_echo_summary(){ printf '%s' "$1"; }
_open_taking_of(){ printf '%s\\t2400\\twork\\n' "$TEST_CLAIM"; }
probe(){
local win=hire now=100000 remote_win='' task=fresh SESS=test
''' + block + '''
return 0
}
probe
first=$?
probe
second=$?
test "$first" = 2 && test "$second" = 0
'''
    env = dict(os.environ, MESH_DIR=td, MESH_RESURFACE_STATE_DIR=td,
               TEST_CLAIM='ba260907-05-workspace/repair')
    run = subprocess.run(['bash', '-c', script], env=env, capture_output=True, text=True)
    assert run.returncode == 0, run.stdout + run.stderr
    assert (Path(td) / '.resurfaced-hire-ba260907-05-workspace%2Frepair').read_text().strip() == '100000'
    assert (Path(td) / 'sends').read_text().splitlines() == ['sent']
    env['TEST_CLAIM'] = 'ba260907-05-workspace%2Frepair'
    run = subprocess.run(['bash', '-c', script], env=env, capture_output=True, text=True)
    assert run.returncode == 0, run.stdout + run.stderr
    assert (Path(td) / '.resurfaced-hire-ba260907-05-workspace%252Frepair').exists()
print('PASS: slash IDs persist cooldown; repeats suppressed; percent IDs remain distinct')

# Drive the real claim parser and open-taking scan: UNKNOWN is not a claim ID.
start = source.index('_open_taking_of() {')
end = source.index('\n# _ack_timeout_for_load', start)
with tempfile.TemporaryDirectory() as td:
    env = dict(os.environ, MESH_DIR=td, MESH_MC_CHATLOG=str(Path(td) / 'chat.log'),
               CLAIM_LIB=str(root / 'scripts/mesh-claim-shape.sh'))
    scan = '. "$CLAIM_LIB"\nSESS=test\n' + source[start:end] + '''
stamp=$(date -u -d '@97600' +%FT%TZ)
printf '%s  hire@test  ::  [taking] legacy prose without a task ID\\n' "$stamp" > "$MESH_MC_CHATLOG"
if _open_taking_of hire 100000; then exit 1; fi
printf '%s  hire@test  ::  [taking] repair task:chain/repair\\n' "$stamp" >> "$MESH_MC_CHATLOG"
printf '%s  hire@test  ::  [done] sibling task:chain/repair-extra\\n' "$stamp" >> "$MESH_MC_CHATLOG"
_open_taking_of hire 100000
printf '%s  hire@test  ::  [done] exact task:chain/repair\\n' "$stamp" >> "$MESH_MC_CHATLOG"
if _open_taking_of hire 100000; then exit 1; fi
'''
    run = subprocess.run(['bash', '-c', scan], env=env, capture_output=True, text=True)
    assert run.returncode == 0 and run.stdout.startswith('chain/repair\t2400\t'), run.stdout + run.stderr
print('PASS: unknown identity cannot hold work; explicit chain ID can resume')

# Historical prose may contain damaged bytes. It must not turn valid receipts
# into grep's "binary file matches" summary and silently erase an open claim.
with tempfile.TemporaryDirectory() as td:
    path = Path(td) / 'chat.log'
    taking = b'1970-01-02T03:06:40Z  hire@test  ::  [taking] repair task:chain/repair\n'
    done = b'1970-01-02T03:06:41Z  hire@test  ::  [done] exact task:chain/repair\n'
    damaged = b'1970-01-02T03:00:00Z  old@test  ::  old prose \xff\x00\n'
    env = dict(os.environ, MESH_DIR=td, MESH_MC_CHATLOG=str(path),
               CLAIM_LIB=str(root / 'scripts/mesh-claim-shape.sh'), LC_ALL='C')
    scan = '. "$CLAIM_LIB"\nSESS=test\n' + source[start:end] + '\n_open_taking_of hire 100000\n'
    path.write_bytes(damaged + taking)
    run = subprocess.run(['bash', '-c', scan], env=env, capture_output=True, text=True)
    assert run.returncode == 0 and run.stdout.startswith('chain/repair\t2400\t'), run.stdout + run.stderr
    path.write_bytes(damaged + taking + done)
    run = subprocess.run(['bash', '-c', scan], env=env, capture_output=True, text=True)
    assert run.returncode == 1 and not run.stdout, run.stdout + run.stderr
print('PASS: damaged old prose cannot hide valid taking or completion receipts')

sys.path.insert(0, str(root / 'scripts'))
from mesh_task_log import encode
with tempfile.TemporaryDirectory() as td:
    path = Path(td) / 'chat.log'
    data = dict(chain='chain', current=0, status='blocked', steps=[
        dict(id='chain/repair', slug='repair', owner='hire', status='blocked', description='repair')])
    path.write_text('1970-01-02T03:06:40Z  hire@test  ::  [taking] repair task:chain/repair\n'
                    + '1970-01-02T03:06:41Z  hire@test  ::  ' + encode(data, 1) + '\n')
    env = dict(os.environ, MESH_DIR=td, MESH_MC_CHATLOG=str(path),
               CLAIM_LIB=str(root / 'scripts/mesh-claim-shape.sh'),
               MESH_TASK_CHECK_CMD=str(root / 'scripts/mesh-task'))
    scan = '. "$CLAIM_LIB"\nSESS=test\n' + source[start:end] + '\n_open_taking_of hire 100000\n'
    result = subprocess.run(['bash', '-c', scan], env=env, text=True, capture_output=True)
    assert result.returncode == 1 and not result.stdout, result.stdout + result.stderr
    path.write_text(path.read_text() + '1970-01-02T03:06:42Z hire@test :: [task-state] broken\n')
    result = subprocess.run(['bash', '-c', scan], env=env, text=True, capture_output=True)
    assert result.returncode == 2, result.stdout + result.stderr
print('PASS: canonical block suppresses old taking; malformed state is a scan failure')
