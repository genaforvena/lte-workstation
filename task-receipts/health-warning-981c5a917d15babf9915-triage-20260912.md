# Health warning triage: discover wedged input

Chain: `health-warning/981c5a917d15babf9915/triage`  
Checked: 2026-09-12 09:00 UTC on `mesh-home`  
Source: `mind-state@mesh-home` reported discover input stuck for at least two ticks as `lear`, never submitted, with the pane classified IDLE.

## Recovery

- `mesh-tell --peek discover` showed the bottom discover pane's composer containing exactly `lear` after context compaction.
- Sent `C-u` to `mesh-home:discover.1`, the bottom composer pane, to clear the unsent line.
- Ran `mesh-tell discover 'lear'`; it exited 0 and reported `[told discover @ local]`.
- A follow-up `mesh-tell --peek discover` showed the submission in the scrollback and discover `Working`, with the composer prompt available again.

## Disposition

The captured text was re-submitted exactly as observed; I did not infer or expand it to a different command. The stuck composer is cleared and the submission was accepted. No substrate state was changed.
