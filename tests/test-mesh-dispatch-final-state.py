"""Exercise the real final delivery gate against canonical log changes."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'scripts'))
from mesh_task_log import encode
source = (root / 'scripts/mesh-mind-control').read_text()
start = source.index('  # Re-read canonical state at the delivery boundary')
end = source.index('  # DELIVERY-VERIFIED SEND', start)
gate = source[start:end]
with tempfile.TemporaryDirectory() as td:
    path = Path(td) / 'chat.log'
    env = dict(os.environ, MESH_DIR=td, MESH_MC_CHATLOG=str(path),
               CLAIM_LIB=str(root / 'scripts/mesh-claim-shape.sh'),
               MESH_TASK_CHECK_CMD=str(root / 'scripts/mesh-task'))
    script = '. "$CLAIM_LIB"\nprobe(){\nlocal task="plan-work: queued earlier" win="$TARGET" remote_win=""\n' + gate + '\nprintf "DELIVER\\n"\n}\nprobe\n'
    def run(status, target, expected):
        data = dict(chain='plan', current=0, status=status, steps=[
            dict(id='plan/work', slug='work', owner='haunt', status=status, description='evidence')])
        path.write_text('2026-09-08T00:00:00Z haunt@n :: ' + encode(data, 1) + '\n')
        p = subprocess.run(['bash', '-c', script], env=dict(env, TARGET=target), text=True, capture_output=True)
        assert p.returncode == expected, p.stdout + p.stderr
        assert ('DELIVER' in p.stdout) == (expected == 0), p.stdout + p.stderr
    for status in ('blocked', 'active', 'done'):
        run(status, 'haunt', 2)
    run('open', 'senses', 2)
    run('open', 'haunt', 0)
    path.unlink()
    p = subprocess.run(['bash', '-c', script], env=dict(env, TARGET='haunt'), text=True, capture_output=True)
    assert p.returncode == 2 and 'DELIVER' not in p.stdout
print('PASS: final delivery rejects stale state, wrong owner and unreadable source; current open owner passes')

start = source.index('  local xid; xid=')
end = source.index('  # OWNER-FIRST:', start)
early = source[start:end]
with tempfile.TemporaryDirectory() as td:
    path = Path(td) / 'chat.log'
    env = dict(os.environ, MESH_DIR=td, MESH_MC_CHATLOG=str(path),
               CLAIM_LIB=str(root / 'scripts/mesh-claim-shape.sh'),
               MESH_TASK_CHECK_CMD=str(root / 'scripts/mesh-task'))
    script = '. "$CLAIM_LIB"\nprobe(){\nlocal task="plan/work: task:plan/work" now=1788825610 DISPATCH_ACK_TIMEOUT=300\n' + early + '\nprintf "CONTINUE\\n"\n}\nprobe\n'
    data = dict(chain='plan', current=0, status='open', steps=[
        dict(id='plan/work', slug='work', owner='haunt', status='open', description='evidence')])
    prose = ('2026-09-08T00:00:01Z haunt@n :: [taking] plan/work: provisional task:plan/work\n'
             '2026-09-08T00:00:02Z haunt@n :: [done] plan/work: provisional task:plan/work\n')
    path.write_text(prose + '2026-09-08T00:00:00Z haunt@n :: ' + encode(data, 1) + '\n')
    p = subprocess.run(['bash', '-c', script], env=env, text=True, capture_output=True)
    assert p.returncode == 0 and 'CONTINUE' in p.stdout, p.stdout + p.stderr
    path.write_text(path.read_text() + '2026-09-08T00:00:03Z mind-control@n :: [dispatch] plan/work: delivered task:plan/work\n')
    p = subprocess.run(['bash', '-c', script], env=env, text=True, capture_output=True)
    assert p.returncode == 0 and 'CONTINUE' not in p.stdout, p.stdout + p.stderr
    path.write_bytes(b'2026-09-07T00:00:00Z old@n :: damaged prose \xff\x00\n' + path.read_bytes())
    p = subprocess.run(['bash', '-c', script], env=env, text=True, capture_output=True)
    assert p.returncode == 0 and 'CONTINUE' not in p.stdout, p.stdout + p.stderr
print('PASS: early dedup ignores provisional taking/done for committed open task, but retains delivery cooldown')
