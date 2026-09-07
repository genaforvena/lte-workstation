# Pushed-fact acknowledgement and owner routing — 2026-09-07

## Pushed facts

A targeted line is delivered to its addressee. The recipient may post one targeted line beginning
with `[ack]`; that line stays in `~/.mesh/chat.log` as the audit record but is held closed by
`mesh-chat-deliver` and is not pushed back. This stops a receipt from becoming another fact that
demands a receipt. New `[task]`, artifact/result, `[taking]`, or other non-ack lines remain pushable
and reopen work.

The implementation keeps every targeted line, including `[ack]`, in the raw stream used by the
per-target cursor, then excludes `[ack]` only from the wake payload. An ACK-only batch advances the
cursor without calling `mesh-tell`. This distinction is required for upgrades: filtering before the
cursor count changes the coordinate system, so a cursor written by the old worker can skip a later
real task. The smoke regression calls the shipped classifier and delivery function, with a fixture
where an old cursor has counted `fact + ack` and a new task follows. An acknowledgement is not task
completion: the task key, artifact, and verification still govern closure.

Live evidence before the fix is in `~/.mesh/chat.log` and `~/.mesh/chat-deliver.log`: between
09:12 and 09:26 UTC, witness and vpn alternated targeted receipt/fact lines, and the delivery worker
recorded a new delivery to the opposite window after each post. At inspection time the deployed
`~/.local/bin/mesh-chat-deliver` was still the pre-filter version and differed from the genome source;
the old self-test passed because it duplicated a grep pipeline instead of calling the delivery path.

## Owner/task-key routing

The 08:52 adint line used `owner: adint` before the subject. That is an owner clause, not the task
key; the leading owner token was allowed to become the derived subject (`owner-adint-...`) while
dispatch and lifecycle accounting separately treated `adint` as the destination. The corrected
slug-first form makes the identity unambiguous: `[task] self-adint-device-capture-export: ...
owner: adint`.

The durable routing rule is: the task subject/slug and destination owner are separate fields. A
live owner that is WORKING/BUSY is still present and receives an exact-owner hold (`rc=3`) for retry;
only an actually absent window is owner-missing (`rc=4`). Neither case may generic-dispatch an
explicitly owned task. `mesh-mind-control --test` now covers both adint states.

No VPN command, route, or other substrate actuator was changed.
