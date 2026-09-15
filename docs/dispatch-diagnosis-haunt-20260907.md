# Dispatch diagnosis: `haunt`

Checked 2026-09-07 UTC after repeated owner-task delivery failures.

## Finding

The task lines intended for this window use the ambiguous/misleading form
`owner: mesh-task/haunt` and also append `owner:haunt`. The owner resolver gives
slash-form tags precedence. It interprets the first tag as a code-fix route,
then redirects the non-code-capable `haunt` segment to an idle code window.

Observed resolver evidence:

```text
mesh-mind-control --owner-route 'task:foo owner: mesh-task/haunt' -> senses
```

The live architecture-drift task therefore does not have a direct `haunt`
route. The correct non-code owner form is `owner:haunt` without the
`mesh-task/` prefix.

## Separate live condition

The `haunt` tmux pane and Codex process exist. At inspection it reported
`WORKING`, with two background terminals. A correctly routed bare-owner task
would be held while this window is busy and retried later; it should not be
treated as delivered merely because `dispatch=sent` is present.

## Evidence

- `~/.mesh/dispatch.log`: repeated `resurface delivery FAILED/NO-ACK
  (haunt...)` and `dispatch FAILED (mesh-tell haunt — pane gone / refused?)`.
- `~/.mesh/chat.log`: the three haunt tasks were claimed at 23:04–23:05Z with
  leases ending 23:34Z; lifecycle audit recorded them `EXPIRED` at 23:35Z.
- `mesh-task audit`: current haunt work is `EXPIRED` or `OPEN_UNOWNED` while
  chain records still say `dispatch=sent`.
- Source/deployed `mesh-dispatch` hashes match:
  `bd91374bb924513aadf5af856d53d685f6b8c1c782731715e99d235b0de8540d`.

No source or substrate change was made by this diagnosis.
