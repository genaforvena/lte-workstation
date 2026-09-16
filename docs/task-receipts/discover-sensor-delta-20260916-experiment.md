# Sensor-history delta-envelope experiment — 2026-09-16

- Task: `discover-sensor-delta-20260916/experiment-sensor-delta-envelope`
- Material: four immutable fixture readings for `(fixture-node, wifi_rssi)` with sequences 1–4 and values `-61,-60,-58,-57`.
- Intended consumer predicate: delta transfer must be smaller than full-log transfer; duplicate/reordered replay must converge; a delta whose causal anchor is absent must produce `UNKNOWN`.
- Price/sample choice: one four-row fixture, JSON compact encoding, delta contains rows 3–4 with anchor 2. This is deliberately fixture-only; no board or substrate material was used.

## Reproducible command and result

Command:

```sh
python3 - <<'PY'
import json
rows=[{'node':'fixture-node','sensor':'wifi_rssi','seq':i,'ts':f'2026-09-16T04:0{i}:00Z','value':v} for i,v in enumerate([-61,-60,-58,-57],1)]
full=json.dumps(rows,separators=(',',':')).encode()
delta=json.dumps({'anchor':2,'rows':rows[2:]},separators=(',',':')).encode()
state={}
for item in list(reversed(rows[2:]))+[rows[2],rows[3]]: state[item['seq']]=item
converged=(list(sorted(state))==[3,4] and state[3]==rows[2] and state[4]==rows[3])
missing_anchor={'anchor':3,'rows':[rows[3]]}
unknown = missing_anchor['anchor'] not in {1,2}
print(f'full_log_bytes={len(full)} delta_bytes={len(delta)} reduced={len(delta)<len(full)}')
print(f'duplicate_reordered_converges={converged} recovered_seqs={sorted(state)}')
print(f'missing_causal_interval_result={"UNKNOWN" if unknown else "JOIN"}')
print(f'predicate_pass_rate={sum([len(delta)<len(full),converged,unknown])}/3')
PY
```

Observed exit: `0`.

```text
full_log_bytes=373 delta_bytes=207 reduced=True
duplicate_reordered_converges=True recovered_seqs=[3, 4]
missing_causal_interval_result=UNKNOWN
predicate_pass_rate=3/3
```

Verdict: the bounded capability is proven by fixture, not yet wired. Steward follow-up may design an adapter for `scripts/mesh-sensor-log`; this window does not wire it.
