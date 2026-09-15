# Window data lease and conditional diff feed plan audit — 2026-09-12

## Verdict

The checked implementation steps in `docs/superpowers/plans/2026-09-06-window-data-lease-diff-feed.md`
match the current source and live mesh. The live supervisor discovers 15 two-pane data/mind
windows, all 15 have a running consumer driver, and every corresponding top pane currently shows
an advancing `pane live` footer. The consumer log shows both changed-pane wake decisions and
unchanged-pane holds. No implementation change was needed.

The plan's two historical red-first claims cannot be reproduced from current state: the plan only
records checked boxes, not the original failing output. Current tests confirm the implemented
contract. One coverage limit remains: the `tg` discovery assertion is conditional on `tg` already
being discovered, so it is not a hermetic regression test for omission of `tg` on a future node.

## Step-by-step audit

| Plan item | Current evidence | Result |
|---|---|---|
| Task 1, Step 1: failing live-discovery / no-`tg`-exclusion test | `scripts/mesh-consume-all --test` checks the live `channel_windows` list and, when `tg` is present, requires a matching channel entry. The live set includes `tg`. The assertion does not construct a fixture with `tg` absent/present, so its historical red run and future-node coverage cannot be independently established. | Current behavior covered; red-first history unverified; conditional test limitation recorded. |
| Task 1, Step 2: observe expected failure | No failing transcript or fixture is stored with the plan. Re-running after implementation passes, so the historical failure is not reproducible without reverting code. | Historical claim unverified, not contradicted. |
| Task 1, Step 3: live discovery and override behavior | `channel_windows` requires at least two panes and recognizes the top-pane data-renderer command. `channel_entries` starts from that live set and overlays matching cadence/routing values; the supervisor's ensure/status/kick/stop loops consume those entries. `MESH_CONSUME_CHANNELS` therefore does not remove a live channel. | Verified against current source and live membership. |
| Task 1, Step 4: focused smoke and shell syntax | `scripts/mesh-consume-all --test` and `bash -n scripts/mesh-consume-all scripts/mesh-pane-consume scripts/mesh-dash` pass in this audit. | Verified. |
| Task 1, Step 5: supervisor status and tmux windows | `mesh-consume-all --status` reports drivers for `genome`, `tg`, `senses`, `health`, `pub`, `discover`, `sound`, `vpn`, `witness`, `tg-roz`, `job`, `adint`, `hire`, `haunt`, and `wake`. Each is a two-pane window with a data renderer in pane 0 and a mind in pane 1. The one-pane `opencode` window is correctly excluded. | Verified live. |
| Task 2, Step 1: architecture contract wording | `docs/mesh-architecture.md` describes the top pane's advancing `pane live` footer as its lease, and says normalized top-pane meaning conditionally wakes the bottom mind subject to consumer gates. Current code implements those roles. | Accurate. |
| Task 2, Step 2: smoke tests and syntax | `scripts/mesh-dash --test-fast`, `scripts/mesh-pane-consume --test`, and `scripts/mesh-consume-all --test` all pass. Shell syntax checks pass for all three scripts. | Verified. |
| Task 2, Step 3: inspect diff and live status | Current `git diff` has no changes to this plan or the architecture contract. The only diff among the inspected implementation scripts is an unrelated task-state display change in `scripts/mesh-dash`; it was left untouched. Live driver and lease state is summarized below. | Verified with unrelated pre-existing work preserved. |

## Source, deployed copies, and live behavior

Source and deployed executable SHA-256 values match on this node:

| Executable | SHA-256 (source = `~/.local/bin`) |
|---|---|
| `mesh-consume-all` | `31d7a6be9e0429417d7cd39a90f901a9abea5a6e6cf7cb779379b36d571165f5` |
| `mesh-dash` | `63b2de2bd27d0832cf93ccb71d7f95fe56cb00ab55a3d82b0972191b54b49f0f` |
| `mesh-pane-consume` | `c84d8b3dc49a17b547afb8e52f49ce3a43d23227c0df3dd8883d9ffd426253d9` |
| `mesh-pub-dash` | `29f95828e8c81cc298727b15bf6c13327d3584bfc3c1fd653c9d15b364e0b2b1` |

The latest pane captures showed advancing lease timestamps for all 15 discovered windows. Refresh
cadences were 15 seconds for `witness`, 75 seconds for `pub`, and 30 seconds for the other panes.
The current `~/.mesh/pane-consume.log` tail recorded `SURPRISE` decisions for changed panes and
`pane unchanged — no wake` for an unchanged pane; several candidate sends were then held by
refractory or busy-mind guards. The smoke test exercises the actual diff decision path and checks
the successful-send log through a stubbed `mesh-tell`; it does not inject a new wake into a live
mind during this audit.

Verification run:

- `scripts/mesh-consume-all --test` — PASS.
- `scripts/mesh-pane-consume --test` — PASS.
- `scripts/mesh-dash --test-fast` — PASS.
- `bash -n scripts/mesh-consume-all scripts/mesh-pane-consume scripts/mesh-dash` — PASS.
- `mesh-consume-all --status` plus per-window `tmux list-panes` and top-pane captures — 15/15
  discovered channels have drivers and advancing lease footers.
- Source/deployed SHA-256 comparison — all four renderer/supervisor/consumer pairs match.

No source or deployed file was changed by this audit. The existing `scripts/mesh-dash` worktree
diff was preserved.
