# Sound experiment: primary window-period fallback

Date: 2026-09-09  
Task: `sound-experiments-20260908/window-period-fallback`  
Sources: live `~/.mesh/records.log` (2169 rows, mtime 2026-09-09T02:25:40Z), live `~/.mesh/room-music-params.log`, and the current `scripts/mesh-sound-reflex`.

## Live code/state audit

The task is live and correctly specified: after `mesh-task import`, the canonical chain reported
step 10/10 open, and `mesh-task take sound-experiments-20260908 window-period-fallback` claimed it.
The current primary helper at `scripts/mesh-sound-reflex:2399` computes `win / beats * 1000` and
replaces every result outside 250..1200 ms with 500 ms. The f-side helper already abstains with a
named `na:` reason, but that is a different axis and does not repair an invalid primary window
period.

## Measurement

I classified each live record with a readable `win` and positive `beats` by the same 250..1200 ms
band used by `beat_of`. Counts are per organ because `records.log` is pruned per organ.

| organ | readable records | primary out-of-band | rate | f-side in-band among primary out-of-band |
|---|---:|---:|---:|---:|
| ear | 600 | 0 | 0.0% | n/a |
| note3 | 553 | 54 | 9.8% | 2/54 (3.7%) |
| scape | 248 | 15 | 6.0% | 0/15 (0.0%) |
| drop | 596 | 28 | 4.7% | 10/28 (35.7%) |
| ext | 91 | 0 | 0.0% | n/a |
| voice | 3 | 0 | 0.0% | n/a |

The out-of-band values are not one harmless edge: `note3` is dominated by 3000 ms records
(43/54 have `fbeats<=1` or no usable f-side period), while `drop` includes both slow values up to
17647 ms and fast values down to 200 ms. The f-side rate therefore cannot be the policy selector;
it mostly describes whether the separate whole-file scan happened to be usable.

## Clamp versus abstain: render consequence

The current clamp has real downstream effect. Joining the out-of-band hashes to the live params log
found 24 recipe rows for 22 hashes: 22 drop rows for 20 hashes and 2 scape rows for 2 hashes. No
note3 out-of-band hash has a params row in the retained render ledger. The clamp-derived recipe rows
show the synthetic-looking primary value (`beat=500` on several rows) being used to produce ordinary
grain lengths, for example drop `9a11e5d1` (`win=3`, `beats=2.25`, raw period 1333 ms) rendered
with `l=120`, and scape `3a97ac63` (`1250 ms`) rendered with `l=250`.

The retained artifact census has two matching playable MP3s (drop `99f71f3d`, 2,278,105 bytes /
569.47 s; drop `4ddff0f9`, 3,520,593 bytes / 880.09 s), but the current verdict tape has no rows
for those hashes. Thus the live evidence proves that clamp changes recipes and spends render work,
but does not support claiming that those renders sounded good. Abstaining would have prevented those
auto-render attempts; the retained verdict coverage is insufficient to justify clamp as
direction-preserving.

## Policy selection

Selected policy: **primary-period abstain for automatic window-derived rendering when the measured
window period is outside 250..1200 ms; preserve the operator-drop unconditional path, but mark its
primary period `na:out-of-band` rather than converting it to 500 ms.** A valid whole-file period may
still be blended only when the primary period is valid; f-side availability/rate is not used to
silently rescue an invalid primary.

Reason: clamping a slow period down to 500 ms and a fast period up to 500 ms reverses the direction
of the measured period in both tails. Abstention preserves the only honest statement available and
does not turn scan failure into a successful-looking duration. The operator-drop exception is
required by the sound charter's unconditional gesture rule; it is a deliberate render consequence,
not a claim that the primary period was measured.

No production code change is proposed from this audit alone. The next implementation artifact must
add a real render/verdict fixture for both tails and wire the abstention through the automatic path,
while keeping the drop path visibly marked.

## Verification

- `mesh-task import`, live status, and task claim: passed; step remained open before claim.
- Current source inspection: passed; `beat_of` clamp and `fbeat_of` abstention are present at the cited paths.
- `bash -n scripts/mesh-sound-reflex scripts/mesh-soundscape`: passed.
- `scripts/mesh-sound-reflex --test`: honest `rc=2`, refusing to forge live evidence because
  `~/.mesh/records.log.reflex.lock` is held by the running reflex.
- `mesh-series-stats --claims`: ran against the live corpus; claim 4 remains refuted (237/1304
  sub-window rows report more beats than their whole file), reinforcing that window and f-side
  counts are distinct measurements.

