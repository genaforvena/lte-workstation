# Cross-sense fusion live verification — 2026-09-15

The existing executable `scripts/mesh-social-fusion` provides the requested derived signals from
multiple existing axes: ambient sound × BLE presence × activity derives occupancy; BLE presence ×
activity × phone social context derives operator state; and BLE presence × activity × audio path
derives media state. A measured empty BLE census (`count=0`) is distinct from an absent, stale, or
malformed presence input, which renders `UNKNOWN`/`UNREACHABLE` with zero overlap rather than an
all-clear.

## Verification

- `bash -n scripts/mesh-social-fusion` — PASS.
- `scripts/mesh-social-fusion --test` — PASS.
- `tests/test-mesh-social-fusion-occupancy.sh` — PASS.
- `tests/test-mesh-social-fusion-unreachable.sh` — PASS.
- `tests/test-mesh-social-fusion-media.sh` — PASS.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — PASS.
- Existing source is executable and already declares `# orphan-ok`; no new tool file was created.
- `mesh-autowire --test` did not produce output and exceeded a 20-second bound; it was not a new-tool
  wiring requirement for this existing source.

## Real read

At `2026-09-15T23:32:47Z`, `scripts/mesh-social-fusion --json` returned exit `2`:

```json
{"verdict":"UNCERTAIN","occupancy":"UNKNOWN","occupancy_coverage":"0/3","ambient":"MODERATE","ambient_status":"LIVE","presence":"STALE","presence_observation":"UNKNOWN","devices":"UNKNOWN","activity":"UNCERTAIN","activity_status":"LIVE","audio_path":"IDLE","audio_status":"LIVE","media_relation":"UNKNOWN","media_coverage":"0/3"}
```

This is the required visible distinction: live ambient/activity/audio evidence did not manufacture
occupancy or media state while the BLE axis was stale.

## Doctor gate

No `[sense]` post was made. The normal `mesh-doctor --quiet` invocation was skipped because the
node's existing `mesh-doctor --cron` process holds `/home/mesh-home/.mesh/.doctor.lock`. Its current
scan remains active. A fresh `mesh-doctor --test` returned exit `1` on the unrelated environment-side
sediment assertion (`--sediment`: runtime name-construction caveat). Therefore the required clean
doctor gate was not achieved, and this artifact remains an honest blocked handoff. No commit was
made.

Next action: after the active doctor run releases the lock and the sediment test is green, rerun the
focused fusion checks and real read, then run `mesh-doctor` to completion; post `[sense]` only on a
clean result with no new orphan warning.

## Fresh verification — 2026-09-16T04:01Z

The existing fusion consumer was re-verified without source changes:

- `scripts/mesh-social-fusion --test` — PASS.
- `tests/test-mesh-social-fusion-occupancy.sh` — PASS.
- `tests/test-mesh-social-fusion-unreachable.sh` — PASS.
- `tests/test-mesh-social-fusion-media.sh` — PASS.
- `tests/test-mesh-social-fusion-coupling-audit.sh` — PASS.
- `stat` — `755`, executable; the existing `# orphan-ok:` header remains present.

The fresh live read at `2026-09-16T04:01:46Z` exited `0` and returned:

```json
{"verdict":"SOCIAL_ACTIVE","relation":"CO_PRESENT_ACTIVE","coverage":"3/3","occupancy":"OCCUPIED","occupancy_coverage":"3/3","operator_state":"UNRESOLVED","operator_coverage":"3/3","media_relation":"MEDIA_IDLE","media_coverage":"3/3","ambient_status":"LIVE","presence_status":"LIVE","activity_status":"LIVE","social_status":"LIVE","audio_status":"LIVE"}
```

The relation is genuinely cross-sense: eight live BLE devices plus live moderate ambient and
activity readings yield `CO_PRESENT_ACTIVE`/`OCCUPIED`; the media relation independently combines
presence × activity × audio path. The degraded social context remains visible as `UNRESOLVED`, not
silently promoted to an operator state.

The required doctor gate remains blocked by unrelated node-wide state. A full `mesh-doctor --quiet`
timed out after 300s following the known mic/peer-SSH warnings; a bounded run also timed out. The
direct `mesh-doctor --test` exited `1` on the existing `--sediment` name-construction caveat.
The orphan census stayed at 98 entries, with no `mesh-social-fusion` match or new orphan warning.
Therefore no `[sense]` post was made and no commit was made.
