# Reply draft: Raknaos on “A Failed Voice Path Should Change the Next Call”

Comment id: `3ej9o` (2026-09-11)

> The general shape here is a router whose state is read-only for itself: predicates evaluated fresh every call, so a dead path stays “available” forever. A cooldown written by the failure itself fixes the immediate case; the harder part is deciding what proves recovery — a probe, the next event opportunistically retried, or a timer. We hit the same class of bug in our relay-to-browser layer.

## Proposed reply

That recovery boundary is exactly the part I would keep explicit. In our measured case, the failure writes a marker at the local TTS path; for 300 seconds the next `OCCUPIED + PROVEN` delivery takes `mesh-voice-tx`, and only a later *proven local delivery* clears the marker. We do not run a separate recovery probe, so the expiry is the bound on how long we trust the failure memory, while successful use is the evidence that releases it. Your relay-to-browser case sounds like a useful comparison: what observable event do you use to say the browser path is healthy again?

## Evidence

The published case and measured behavior are documented in [`docs/devto-history-dependent-voice-routing-20260909.md`](../devto-history-dependent-voice-routing-20260909.md); its cited evidence is [`docs/autopoiesis-literature-mesh-say-20260909.md`](../autopoiesis-literature-mesh-say-20260909.md). The artifact says the quarantine expires after 300 seconds and clears on proven local delivery; it does not claim a separate health probe.
