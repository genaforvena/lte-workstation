# Witness chat review — Telegram backlog routing — 2026-09-08

## Finding

At 2026-09-08T11:30:03Z, the live board reported `tg-inbound BACKLOG` on
mesh-home with `queue=1`, `unit=active/running`, `proc=1`, and
`conflict=0/0ln/15min`. This is a current red condition: Telegram is holding an
update while the poller is not draining it.

The current source confirms the communication gap. In
`scripts/mesh-tg-inbound`, `decide()` emits the BACKLOG verdict at lines
246–247, but `pass()` routes every red result only through the generic
debounced `[fyi]` call at lines 284–290. No owner, next action, or task route is
included, so the condition can be visible without becoming owned work.

## Stale and duplicate checks

`mesh-task audit` passed before filing. Searches of `~/.mesh/chat.log` found no
existing `[task]` or recent `[chat-review]` for a Telegram-backlog ownership
route. This is distinct from the existing `tg-inbound-noear-is-node-local`
task, which concerns host scoping of NOEAR, not backlog dispatch.

## Proposed fix

Route BACKLOG as an owner-addressed board event with an explicit next action,
or have the responsible routing window create/attach a durable task while
preserving the existing debounce. The owner should be
`mesh-tg-inbound/tg`.
