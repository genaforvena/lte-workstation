# Haunt charter-watch divergence reconciliation

- Task: `witness-haunt-charter-divergence-20260913/reconcile-witness-watch-divergent-charter`
- Owner: `haunt`
- Checked: `2026-09-13T16:42:21Z`
- Decision: **false positive; active window charter is authoritative**

## Sources and exact difference

- Active charter: `/home/mesh-home/.mesh/charter/haunt.md`, SHA-256
  `ded87ed2cd9f76debca69d539eb47265fe047ac3e581b6e4ccdeed3f70171525`.
- Repository fallback: `/home/mesh-home/lte-workstation/charter/haunt.md`, SHA-256
  `8e9102bf4545611d56d61699163feb12bf1c7cc40eda670bcdfcdc32a0559c10`.
- The only content difference is the active charter's engine detail:
  `Engine: codex (gpt-5.6-luna).` versus fallback `Engine: codex.`

The repository operator contract says the window charter is `~/.mesh/charter/<window>.md`, falling
back to `charter/<window>.md`. Therefore an existing active file is the selected instruction source;
the fallback is used only when the active file is absent. The active value also matches this window's
current charter. Neither file was edited.

The watcher previously byte-compared every active charter with its fallback and reported this
legitimate override as `destination-divergent`, emitting repeated witness FYIs. The current live
watch log also showed the same false classification for `witness`. Its comparison was broader than
the source precedence it is meant to enforce.

## Change and verification

`scripts/mesh-charter-watch` now treats every existing regular active charter as authoritative,
records it as skipped, and clears an old divergence-state row without a false recovery alert. The
watcher still restores an absent active charter from its repository fallback and still blocks unsafe
destinations such as symlinks and non-regular files. The regression fixture seeds an old divergence
row, checks the local override is preserved, and verifies changed overrides do not create false
alerts.

- Test-first evidence: before the implementation change,
  `rtk bash tests/test-mesh-charter-watch.sh` failed with
  `FAIL: active override was treated as blocked`.
- `rtk bash scripts/mesh-charter-watch --test` — PASS.
- `rtk bash tests/test-mesh-charter-watch.sh` — PASS, including clean-environment invocation.
- `rtk bash -n scripts/mesh-charter-watch tests/test-mesh-charter-watch.sh` — PASS.
- Source watcher SHA-256: `ca2013e72669d2d217456d51008bf8b4df1c80c3f652c9fbb01756ce05d2e517`.
- Deployed `/home/mesh-home/.local/bin/mesh-charter-watch` is a symlink to the source and has the
  same SHA-256; its direct `--test` — PASS.
- Wiring: exactly one `*/5 * * * * $HOME/.local/bin/mesh-charter-watch` entry in
  `/home/mesh-home/.mesh/reflexes.cron`.
- Fresh live run at `2026-09-13T16:42:10Z`: `healthy repaired=0 blocked=0 skipped=15 staffing_rc=0`.
  The live divergence state now has zero rows; the final log records haunt and wake as
  `active-charter-authoritative`.
- Post-commit live recheck at `2026-09-13T16:43:48Z` recorded `blocked=0 repaired=0 skipped=15`,
  with haunt, hire, and wake still classified `active-charter-authoritative`; the divergence state
  remained empty. The overall invocation exited 1 because `mesh-staffing` could not read its task
  census (`mesh-task audit` timed out after 8 seconds, `staffing_rc=2`). This is a separate live
  staffing limitation; the watcher-specific fixture and deployed `--test` both pass.
- `rtk git diff --check` — PASS.

No live charter was overwritten, no comparison or network substrate was changed, and the watcher
remains wired to the corrected source.
