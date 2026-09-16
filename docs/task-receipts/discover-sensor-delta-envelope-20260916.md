# Sensor delta-envelope experiment — 2026-09-16

Task: `discover-sensor-delta/experiment-sensor-delta-envelope`

## Material price and acceptance result

The fixture contained 12 immutable `(node, sensor, sequence, value)` readings for
`fixture-phone/room-motion`, split into three four-reading intervals with causal anchors
`0`, `4`, and `8`.

| predicate | result |
|---|---|
| delta material is smaller than the full log | FAIL: full `868` bytes; envelopes `930` bytes; `-62` bytes (`-7.14%`) |
| duplicate and reordered replay converges | PASS: replay statuses `UNKNOWN, APPLIED, APPLIED, APPLIED, APPLIED`; `12` unique rows; frontier `12` |
| missing causal interval is explicit UNKNOWN | PASS: after applying interval 1 (frontier `4`), interval anchored at `8` returned `UNKNOWN` |

Verdict: **REJECT the proposed transport design for this sample.** The causal behavior is
sound, but the self-describing envelope costs more bytes than the full log. No code, reflex,
board substrate, or second synchronization substrate was changed.

## Reproduction

Run from the repository root:

```bash
python3 - <<'PY'
import json
rows=[{'node':'fixture-phone','sensor':'room-motion','seq':i,'value':('MOVED' if i%3==0 else 'STILL')} for i in range(1,13)]
full=json.dumps(rows,separators=(',',':')).encode(); env=[]
for start in (1,5,9): env.append({'anchor':start-1,'rows':rows[start-1:start+3]})
enc=[json.dumps(x,separators=(',',':')).encode() for x in env]; state={}
def apply(e):
    frontier=max(state,default=0)
    if e['anchor']>frontier:return 'UNKNOWN'
    state.update({r['seq']:r['value'] for r in e['rows']}); return 'APPLIED'
statuses=[apply(env[1]),apply(env[0]),apply(env[0]),apply(env[1]),apply(env[2])]
print('rows=12 full_bytes=%d delta_bytes=%d reduction_bytes=%d reduction_pct=%.2f'%(len(full),sum(map(len,enc)),len(full)-sum(map(len,enc)),100*(len(full)-sum(map(len,enc)))/len(full)))
print('replay_statuses=%s converged=%s unique_rows=%d frontier=%d'%(statuses,len(state)==12 and sorted(state)==list(range(1,13)),len(state),max(state)))
state={}; apply(env[0]); missing={'anchor':8,'rows':[rows[8]]}; print('gap_status=%s frontier_before_gap=%d'%(apply(missing),max(state)))
PY
```

Observed exit `0` and output:

```text
rows=12 full_bytes=868 delta_bytes=930 reduction_bytes=-62 reduction_pct=-7.14
replay_statuses=['UNKNOWN', 'APPLIED', 'APPLIED', 'APPLIED', 'APPLIED'] converged=True unique_rows=12 frontier=12
gap_status=UNKNOWN frontier_before_gap=4
```
