# Handoff board dedupe default — verification receipt

Date: 2026-09-09
Task: `chat-review-handoff-board-dedupe-default-20260909/handoff-board-dedupe-default`

## Change

`scripts/mesh-handoff` now uses state-key dedupe for routine manual handoff board posts by
default. The durable `~/.mesh/handoff/<window>.md` file is still rewritten on every handoff.
Changed state produces a new board receipt. `MESH_HANDOFF_BOARD_MODE=force` explicitly posts
even when the state key is unchanged; the legacy explicit `dedupe` mode remains equivalent.

The deployed command is a symlink to the source:

```text
~/.local/bin/mesh-handoff -> /home/mesh-home/lte-workstation/scripts/mesh-handoff
```

## Verification

Fresh checks:

```text
bash -n scripts/mesh-handoff                                  PASS
bash scripts/mesh-handoff --test                              PASS
~/.local/bin/mesh-handoff --test                              PASS
sha256sum source and deployed                                  cdcb33356f76b7b8abc2c3ef6572f4c76ca590cc27ef2981203fcb33586ca3e3
```

The focused test proves one unchanged default receipt, a changed-state receipt, an explicit
force receipt, the persisted state-key file, and only one receipt after 800 unchanged writes.

The live last-800-line board sample at verification time contained 200 historical `[handoff]`
lines. That is an observation of pre-change chatter, not a claim that the historical log was
rewritten; the regression exercises the future-write behavior in isolation.
