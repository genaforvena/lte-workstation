#!/usr/bin/env bash
set -euo pipefail
repo="${MESH_REPO:-$HOME/lte-workstation}"
dash="$repo/scripts/mesh-dash"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
home="$tmp/home"
mesh="$tmp/mesh"
lane="$home/finnegans-fake/wake"
mkdir -p "$lane" "$mesh"
: >"$mesh/chat.log"
python3 - "$lane" <<'PY'
import json, os, sys
lane=sys.argv[1]

def record(run, window, delta):
    return {
        'name': run+'/'+window,
        'cond': {
            'own': {'novel': {'npc': 0.2}},
            'foreign': {'novel': {'npc': 0.2+delta}},
        },
    }

def score(path, run, windows):
    with open(os.path.join(lane,path),'w') as f:
        json.dump({'budget':157,'records':[record(run,w,0.01+i*0.001) for i,w in enumerate(windows)]},f)

for i,suffix in enumerate(['','rs1','rs2','rs3','rs4','rs5']):
    run='ft47'+suffix
    adapter=run[2:]
    os.makedirs(os.path.join(lane,'fold-lora-'+adapter),exist_ok=True)
    with open(os.path.join(lane,'fold-lora-'+adapter,'trainlog.json'),'w') as f:
        json.dump({'n_train':47,'args':{'rank':16,'seed':i},'history':[]},f)
    base_windows=['full%d-%02d'%(i,j) for j in range(8)] if i<4 else ['w%02d'%j for j in range(8)]
    score('recs-'+run+'-e3.json',run+'-e3',base_windows)
    if i<4:
        score('recs-'+run+'-e3-common-w00-w07.json',run+'-e3',['w%02d'%j for j in range(8)])

for i,run in enumerate(['ft99','ft99rs1']):
    adapter=run[2:]
    os.makedirs(os.path.join(lane,'fold-lora-'+adapter),exist_ok=True)
    with open(os.path.join(lane,'fold-lora-'+adapter,'trainlog.json'),'w') as f:
        json.dump({'n_train':99,'args':{'rank':16,'seed':i},'history':[]},f)
    score('recs-'+run+'-e3.json',run+'-e3',['disjoint%d-%02d'%(i,j) for j in range(8)])
with open(os.path.join(lane,'teacher-folds.json'),'w') as f:
    json.dump([],f)
PY
frame="$(HOME="$home" MESH_DIR="$mesh" MESH_REPO="$repo" "$dash" --once wake 2>&1)"
printf '%s\n' "$frame" | grep -Fq 'floor: 6x 47 rows @ep3 (8 win)' \
  || { printf '%s\n' "$frame"; echo 'FAIL: six distinct 47-row trainings did not use their shared common-window scores'; exit 1; }
printf '%s\n' "$frame" | grep -Fq 'floor: 2x 99 rows @ep3 UNMEASURED (no common windows)' \
  || { printf '%s\n' "$frame"; echo 'FAIL: genuinely disjoint family was not kept UNMEASURED'; exit 1; }
if printf '%s\n' "$frame" | grep -Fq 'floor: 4x 47 rows'; then
  printf '%s\n' "$frame"
  echo 'FAIL: duplicate common-window score files were counted as extra trainings'
  exit 1
fi
echo 'test-mesh-dash-wake-common-window-floor: PASS (six independent shared-window runs; disjoint family remains UNMEASURED)'
