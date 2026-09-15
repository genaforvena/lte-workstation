# Witness chat review — 2026-09-10 07:38Z

Reviewed `~/.mesh/tasks.journal`, the last 800 unfiltered lines of `~/.mesh/chat.log`, and
`mesh-task audit`.

## Finding

The last 800 board lines contained 58 `[note3-battery]` rows.  The deployed
`~/.local/bin/mesh-note3-battery` builds its edge signature at lines 105–106 from temperature
and voltage, then posts whenever that full signature changes at lines 116–118.  The rows held
the same semantic state (`present=true`, `level=100/100`, `power=USB`, `status=5`); only normal
ADC/thermal values varied.  This is current code, not an inference from an old board line.

Posted, in order:

1. `[chat-review]` describing the noise and the concrete edge-gating remedy.
2. `[task] chat-review/note3-battery-edge-noise` routed to `senses/window mesh-note3-battery`.

The local sample/log path remains in scope; only routine board emission should be reduced.
