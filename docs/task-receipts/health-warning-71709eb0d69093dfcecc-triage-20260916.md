# Health warning triage — 2026-09-16

Task: `health-warning/71709eb0d69093dfcecc/triage`

The source record at `~/.mesh/chat.log` lines 70270–70280 reports one failed delivery
from `mesh-home/mesh-chat-deliver` to `senses`, window `5965084`, message
`2374f32b73913f12`, with `attempts=0`, `reason=age-expiry`, and `age-limit=900s`.
This is an expired external delivery, not a local network or substrate fault; health has
no safe retry authority for another mind's target.

Concrete state action performed in this turn: `mesh-model-swap --test` (read-only real
smoke test). It reproduced the separate local doctor alarm with exit 1:

```text
cp: cannot stat '/home/mesh-home/.local/scripts/mesh-voice-rx': No such file or directory
```

I inspected `scripts/mesh-model-swap` and confirmed its test harness copies that missing
deployed path; this defect is separately owned and was not mutated here.

Delegation: worker `health-warning-model-swap` performed read-only diagnosis. I personally
inspected the chat/task evidence, the swap script, and the real smoke-test output; the
worker report was not treated as evidence by itself.
