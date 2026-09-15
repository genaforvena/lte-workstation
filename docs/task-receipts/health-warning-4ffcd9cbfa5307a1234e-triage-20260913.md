# Health warning triage: `health-warning/4ffcd9cbfa5307a1234e`

- Checked: `2026-09-13T14:58Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/4ffcd9cbfa5307a1234e/triage`
- Source warning: `2026-09-13T14:01:53Z`, `channel-keepalive@mesh-home`
  reported `mesh-home:pub` holding `› /clear` with `UNATTRIBUTABLE` status.

## Finding

The warning is still live, not stale: `mesh-tell --composer pub` returns
`HOLDS\t› /clear`, and the latest composer sweep continues to count one held
composer. The current `mesh-mind-state pub` result is `UNKNOWN` for that same
text, so there is no current positive `WEDGED-INPUT` signal authorizing a
recovery action.

The keepalive's safety behavior is correct. `strand_attribution()` strips the
composer marker and refuses to attribute bodies shorter than
`MESH_STRAND_MIN_CHARS` (default 16); `/clear` is six characters, so this case
returns `UNATTRIBUTABLE` before scanning the WAL. The warning therefore does
not establish whether `/clear` came from an operator or a mesh-tell delivery.
The `REDRIVE` branch posts a holding warning and leaves un-attributed composer
text untouched; actual resubmission requires both a `STRANDED` WAL match and
an independent `WEDGED-INPUT` result. No pane input or substrate state was
changed.

This is a known attribution blind spot for short composer text, not evidence
that the intended `/clear` was delivered or that it is safe to submit it.

## Evidence

- `/home/mesh-home/.mesh/chat.log:59366` — original `mind-holding` alert;
  `/home/mesh-home/.mesh/chat.log:59367` — open task-ledger row.
- `scripts/mesh-channel-keepalive` — `strand_attribution()` has the 16-character
  floor; `strand_sweep()`'s non-`STRANDED` branch leaves text untouched.
- Live at `2026-09-13T14:57Z`: `mesh-tell --composer pub` returned
  `HOLDS\t› /clear`; `mesh-mind-state pub` returned `UNKNOWN`.
- `/home/mesh-home/.mesh/composer-sweep.log` — `14:57:27Z RUN swept=15
  held=1 blind=0 acted=0`; the sweep remains live and sees this hold.
- `mesh-task check dispatch health-warning/4ffcd9cbfa5307a1234e/triage health`
  exited 0; the exact owned step was then claimed.

## Disposition

Close the triage as investigated. Preserve the current no-touch behavior. The
remaining uncertainty is whether the short `/clear` is operator input or an
intended delivery; resolving it would require stronger attribution evidence,
not an automatic keypress.
