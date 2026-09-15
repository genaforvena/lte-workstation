# Parked autostash alarm deduplication — 2026-09-15

Task: `land-parked-autostash-20260915/fix-stale-autostash-alarm`

`scripts/mesh-land` now keys the parked-autostash refusal alarm by the stable stash
ref and object ID. The refusal remains loud in the local trace, but an unchanged
parked object emits one `[strand]` board alarm; a newly parked object gets a new
alarm. The stale replay refusal and untouched `HEAD` safety boundary remain intact.

Verification:

- `bash -n scripts/mesh-land` — pass.
- `git diff --check -- scripts/mesh-land` — pass.
- `bash scripts/mesh-land --test` — `smoke-test: ok`; the fixture drives the same
  stale refusal twice and asserts exactly one board alarm.
- `mesh-land --check` — rc=1 with existing held backlog; the live `~/.mesh/land.log`
  records the held candidates and overlap refusal, so this is not treated as green.
