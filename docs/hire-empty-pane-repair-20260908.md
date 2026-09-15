# Empty-pane repair — current bounded observation

- Task: `recreated-rejected-20260908-07-corrected/empty-pane-repair`
- Owner: `hire`
- Captured: `2026-09-08T14:50Z–14:51Z`
- Repository revision: `ceb56e4c` (`main`, source and deployed command paths resolve to this worktree)
- Dispatch audit: task was open/live at 14:49Z and was claimed at 14:50:20Z.

## Bounded reads

Commands were run with `timeout`: `mesh-health` (30s), `mesh-audio --verbose` (15s),
`mesh-dash --once check` (15s), and `mesh-dash --once sound` (15s).

| read | rc | elapsed | stdout | stderr | result |
|---|---:|---:|---:|---:|---|
| `mesh-health` | 0 | 10.102s | 839 B | 0 B | non-empty current fleet observation; self and phaedra PASS, other listed nodes explicitly OFFLINE |
| `mesh-audio --verbose` | 0 | 56ms | 784 B | 0 B | non-empty current sound-device inventory; 3 capture and 6 playback devices |
| `mesh-dash --once check` | 0 | 6.224s | 2,132 B | 0 B | non-empty renderer output; local load warning is explicit and non-answers remain UNKNOWN |
| `mesh-dash --once sound` | 0 | 12.400s | 13,963 B | 0 B | non-empty renderer output; ear source is fresh, last utterance 5s ago, current records are rendered |

## Interpretation

This is not an observation failure: all four bounded reads returned zero, non-empty stdout,
and empty stderr. It is also not quiet output: the sound pane reports a fresh `ear` source,
recent utterance, and current 14:50Z records. Health has real degraded/offline members, but
they are rendered as explicit states rather than an empty pane or green idle claim.

No source repair is warranted by this current observation. The existing source contains the
relevant bounded/UNKNOWN and quiet-output handling in `scripts/mesh-dash` and
`scripts/mesh-pane-consume`; live command paths resolve to `scripts/mesh-health`,
`scripts/mesh-audio`, `scripts/mesh-dash`, and `scripts/mesh-pane-consume`.

## Verification boundary

This artifact proves one bounded live read and distinguishes timeout/empty/nonzero failure
from successful quiet or non-quiet output. It does not claim that every historical dashboard
timeout is impossible, nor that audio was recorded merely because devices exist.

## Focused checks

- `mesh-pane-consume --test`: PASS (`smoke-test: ok`), including quiet-pane suppression,
  real-delta wake, failed-send honesty, predictive gating, and refractory behavior.
- `mesh-dash --test-fast`: PASS (`smoke-test: ok`).
- Full `mesh-dash --test`: bounded at 120s and terminated with rc=124 before producing a
  result; this remains an open test-suite runtime limitation, not evidence of a live empty pane.
