"""Identity gates use exact tags; alert dedup stays distinct without a tag."""
import os
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / 'scripts/mesh-mind-control').read_text()
start = source.index('  local xid; xid="$(claim_id_of "${MESH_DISPATCH_RAW_TASK:-$task}")"')
end = source.index('\n  #', source.index('\n    fi\n  fi', start) + 10)
consult = source[start:end]
start = source.index('_dispatch_noack_announce_once() {')
end = source.index('\nowner_hold_announce()', start)
announce = source[start:end]
with tempfile.TemporaryDirectory() as td:
    env = dict(os.environ, MESH_DIR=td, MESH_MC_CHATLOG=str(Path(td) / 'chat.log'),
               MESH_NOACK_STATE_DIR=td, CLAIM_LIB=str(root / 'scripts/mesh-claim-shape.sh'))
    prelude = '''. "$CLAIM_LIB"
SESS=test
mesh-chat(){ printf '%s\\n' "$*" >> "$MESH_DIR/posts"; }
mesh-trace(){ :; }
dispatch_echo_summary(){ printf '%s' "$1"; }
'''
    script = prelude + 'probe(){ local task="$1" now; now=$(date +%s); local DISPATCH_ACK_TIMEOUT=1800\n' + consult + '''
return 8
}
stamp=$(date -u +%FT%TZ)
printf '%s  worker@peer  ::  [done] sibling task:chain/repair-extra\\n' "$stamp" > "$MESH_MC_CHATLOG"
probe 'work task:chain/repair'; test "$?" = 8 || exit 1
printf '%s  worker@peer  ::  [done] exact task:chain/repair\\n' "$stamp" >> "$MESH_MC_CHATLOG"
probe 'work task:chain/repair'; test "$?" = 0 || exit 1
probe 'untagged UNKNOWN prose'; test "$?" = 8 || exit 1
''' + announce + '''
_dispatch_noack_announce_once hire codex 'first untagged task'
_dispatch_noack_announce_once hire codex 'second untagged task'
_dispatch_noack_announce_once hire codex 'first untagged task'
_dispatch_noack_announce_once hire codex 'explicit task:chain/repair'
_dispatch_noack_announce_once hire codex 'explicit task:chain/repair'
'''
    run = subprocess.run(['bash', '-c', script], env=env, capture_output=True, text=True)
    assert run.returncode == 0, run.stdout + run.stderr
    assert len((Path(td) / 'posts').read_text().splitlines()) == 3
    assert (Path(td) / '.noack-announced-hire-chain%2Frepair').exists()
print('PASS: exact completion identity and separate, persistent failure notices')
