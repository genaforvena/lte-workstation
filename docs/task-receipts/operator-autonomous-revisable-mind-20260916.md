# Operator autonomy directive — 2026-09-16

Ask key: `ask:tg-1686bf2070e5a6973a98fb24` (refined by subsequent operator confirmations).

Changed `scripts/mesh-pane-consume` so generated wake prompts now instruct the mind to act
proactively and autonomously: make the next justified move, create or advance exact-owner tasks,
discuss changes with peer minds, revise decisions when evidence changes, and never wait for the
operator to begin. The mandatory final `mesh-wake-expect` prediction ritual was removed. The
explicit `mesh-wake-expect` tool remains available for opt-in use elsewhere.

Delegation: launched `tg-unblock-audit` for an independent non-mutating audit. Personally inspected
its returned turn; it stopped at `Login expired`, so that report was not used as evidence. The worker
was stopped and its shim removed.

Verification performed:

- `bash -n scripts/mesh-pane-consume` — exit 0.
- `rg` source inspection — autonomy directive present; generated prompt contains neither the removed
  prediction suffix nor the old mandatory `mesh-wake-expect senses` requirement.
- `timeout 180 scripts/mesh-pane-consume --test` — exit 0; focused suite reports `smoke-test: ok`.
