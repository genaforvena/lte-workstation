# Design/audit task sweep — 2026-09-07

## Scope

This sweep covers executable Markdown plans in `docs/superpowers/plans/` and `docs/plans/`,
plus current repository design/audit artifacts that describe work rather than merely recording a
closed result. Literature reviews and historical result-only reports are not silently treated as
implementation plans; they are listed as excluded scope and need an explicit operator ask before
becoming code work.

## Findings

The plan checkboxes are not authoritative. Seven older implementation plans still contain only
`[ ]` markers even though corresponding tools and landed commits exist. Conversely, the three
2026-09-07 expansion plans explicitly say `plan only`, and the scripts layout chain is still open
at `propose-layout-and-tasks`. The ledger therefore needs a reconciliation task per plan, with a
real artifact and an explicit `DONE`, `BLOCKED`, or `DECLINED` disposition for every internal step.

The sweep chain is `design-audit-task-sweep-20260907`. Its TSV contains one ordered task for each
plan/design family. A task may close only after it has checked the plan's internal steps against
code, artifacts, wiring, and verification evidence; a green self-test alone is insufficient.

## Initial evidence

- `rtk python3 scripts/mesh-task --test` passed.
- `tests/test-mesh-task-ledger-sync.sh` passed.
- `tests/test-mesh-task-audit-complete.sh` passed.
- The model plan's Python entrypoints were incorrectly invoked through `bash` during the sweep;
  both `scripts/mesh-model-bench --test` and `scripts/mesh-model-resolve --test` exited 2 with
  shell syntax errors. This is recorded as an open repair task, not a pass.
- `tg-scripts-layout-audit-20260907` remains active at `inventory-and-map`/`propose-layout-and-
  tasks`; its map explicitly forbids bulk moves before enumerator and installed-path evidence.

## Required disposition

Every row in `docs/plans/2026-09-07-design-audit-task-sweep.tsv` is a durable mesh task. For each
row, the owner must either execute the plan's remaining work, or publish a concrete refusal/block
with the missing authority, dependency, or safety boundary. “Design exists” and “tests exist” are
not closure evidence.

## Sound collage — current disposition (16:31Z)

The stale no-mp3 blocker is superseded. The owning sound lane produced a fresh playable artifact:
`/home/mesh-home/grainneukeln/output/l220_w8_ss1.25_s0.5_c40-400_k3_n8_2026_09_07_1628.mp3`
(741,645 bytes, SHA-256
`a57a48045f916bbaf7ea4c8d1d5bc241dffbbc44b854e21c6bff175924cc6776`, ffprobe 37.044s/16kHz
mono, full ffmpeg decode OK). `mesh-sound-reflex --status` is PASS and `records.log` has fresh
16:30 reflex rows (`cc4d2368`, `3447c431`).

Witness independently rechecked three additional fresh owner renders after 16:23:46Z: size
2,551,685 / SHA-256 `c7e0e5d2ba5ded13fb71b2855de445f254fa6ea329138f3b49c50fbe2eef3788`,
duration 63.764898s; SHA-256
`4554f608000f2178f75b874b5c9dbb4b2a3c13a46c94882d516ca4a3c647a3`, duration 1224.751020s
(size not reported in the receipt); and SHA-256
`9fcc96b0f9c09d945171d3d7c47bcc730856a04079aeb0c6d8de7f61e545bf26`, duration 84.506122s.
All three are ffprobe-valid.

The plan's step-by-step audit is not complete: a longer focused `mesh-sound-reflex --test` retry
also reached its 60-second bound (`rc=124`, output ended with `Terminated`) after exercising the
smoke sections. The task remains BLOCKED on a completed focused test and reconciliation of every
plan checkbox; no full-plan closure is claimed from the mp3 alone.

## Sound collage — focused retry (16:46Z)

A quiet-window retry of `mesh-sound-reflex --test` completed successfully: `rc=0`, ending with
`smoke-test: ok`. The output exercised the real render/verify, delivery, retry, corpus-ranking,
coverage, and re-pick paths. This discharges the focused test dependency.

The task remains BLOCKED because the full sound-plan checklist and its corresponding artifact
reconciliation are still incomplete. The prior timeout is retained as historical evidence; it is
superseded by this successful focused retry. No full-plan `[done]` is claimed yet.

The per-step disposition is now published at
`docs/design-audit-sound-collage-checklist-20260907.md`. It records the directly evidenced focused
test steps as DONE, missing mutation/wiring/dry-run evidence as BLOCKED, and commit-only steps as
DECLINED; the sound task remains BLOCKED until the blocked steps are evidenced.

The fresh 17:23Z owner retry is recorded in that checklist: bounded `--test` rc=0 and source/
deployed drift match pass, but the real rc=0 tick produced no fresh MP3 and the durable sound log
remains stale. Mutation-red, sandbox dry-run, and settled live-collage evidence are still absent.
