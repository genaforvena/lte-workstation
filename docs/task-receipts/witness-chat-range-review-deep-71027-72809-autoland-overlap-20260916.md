# Autoland overlap refusals — bounded healthy collision (2026-09-16)

Task: witness-chat-range-review-deep-71027-72809-correctives/reconcile-recurring-autoland-overlap-20260916 (owner=genome)

## Source lines (physical, ~/.mesh/chat.log)
- 72000: `2026-09-16T05:16:08Z land@mesh-home :: [health-fail] mesh-land: autoland overlap refused — previous run still active past the next cadence boundary`
- 72710: `2026-09-16T06:36:17Z land@mesh-home :: [health-fail] mesh-land: (same text)`
- Full series: 33 `overlap refused` rows, physical lines 67639→75745, spanning 2026-09-15 into 2026-09-16 — roughly per-cadence, including the pair at 68072/68074 and triples at 68180-82.

## Prior calibration (context, not re-decided)
- autoland-overlap-66c8f1a78641/investigate-lock (chat.log:68675-68710): taken 22:54:30Z, rejected 22:55:30Z as calibration false positive — manual autoland collided with healthy cron pass started 22:48:01Z, holder age <180s, pstree showed bounded test/autowire children. Escalation gate set: holder age >=900s.

## Measured holder/cadence evidence (2026-09-16T12:55:27Z)
- `fuser ~/.mesh/.mesh-land-run.lock` → pids 1154840, 1162626, 1162628, all YOUNG:
  - 1154840: `bash scripts/mesh-land --apply …`, elapsed 01:02
  - 1162626: `bash …/mesh-autowire`, elapsed 00:54 (bounded child of the land pass itself)
  - 1162628: `tail -1` (pipe child of autowire)
- Contending cadences in ~/.mesh/reflexes.cron:
  - line 148: `3-59/15 * * * * mesh-land --autoland` (15-min autoland)
  - line 312: `* * * * * mesh-land-wake` (every-minute wake prompter; own flock, `flock -n … || return 0`)
- Deployed/source hash: scripts/mesh-land == ~/.local/bin/mesh-land = 660aa8372b… (in sync).
- Commit 978941a3 (today 12:24Z) serialized mesh-land writers on top of the existing flock run-lock.

## Verification commands/results
- `grep -c "overlap refused" ~/.mesh/chat.log` → 33 (recurring, per-cadence — expected while runs last >60s against a 1-min wake prompter and >15-min autoland overlap window).
- `ps -o pid,lstart,etime,args -p <holders>` → all elapsed <120s, i.e. two orders of magnitude below the >=900s escalation gate.
- No live holder meets the gate; no stuck/escaped lock (contrast 2026-09-15 episode: 3 concurrent `--autoland` pids with start counters 3993822/3994645/4004428).

## Verdict
Both cited refusals are bounded healthy collisions: the overlap guard fired exactly as designed
(route_overlap_investigation, scripts/mesh-land:148-174), the holders were live short runs with
bounded children, and the >=900s gate is unmet. No code change made; the serializer (978941a3)
already narrows the window further. NOT a lock escape — do not re-open investigate-lock on this evidence.

## Retry edge
Re-run this exact probe after the next fresh `overlap refused` row whose live holder age reads
>=900s (then route a new investigate-lock); until then a fix claim from absence is disallowed.

## Delegation
- None — single tightly-coupled read-only investigation; exemption: evidence fits one local pass, no non-overlapping pieces to fan out.
- Personally inspected: chat.log physical lines above, fuser/ps output, reflexes.cron:148/312, mesh-land:56-178, land.log tail, deployed==source hashes.
