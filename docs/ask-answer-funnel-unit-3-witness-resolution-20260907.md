# Ask-answer funnel — Unit 3 witness resolution

Task: `ask-answer-funnel-implementation-20260907/unit-3-witness-resolution`

Status: complete; owner `tg`.

## Red-before-green

The focused test was first run before the implementation:

```text
tests/test-mesh-witness-ask-metrics.sh: rc=1
KeyError: 'ask_open'
```

This demonstrated that `mesh-witness --json` had no ask-resolution fields.

## Implementation

`scripts/mesh-witness` now consumes the existing `mesh-promises --json` artifact through
`MESH_PROMISES_BIN` (default `mesh-promises`). It does not reparse voice-in.log or the board.

- `ask_open`: open asks older than the artifact-derived p90 age.
- `ask_stale_h`: oldest p90-qualified open ask, or `0.0` when the valid set is empty.
- `ask_resolve`: closed asks divided by admitted asks, refused when the denominator is zero.
- `ask_den`: admitted denominator.
- `ask_p90_h`: measured p90 age gate.
- `ask_unknown`: invalid/missing age rows; invalid rows prevent a falsely precise result.

Source and deployed witness are byte-identical:

```text
scripts/mesh-witness
/home/mesh-home/.local/bin/mesh-witness
sha256=c4d9c506ac1f844ed5c208699a1e204ad4cc55b8b73510efed3eb6c4247092df
focused test sha256=0b1b729f723fdbe079063899041412c308896e3a4c3f93ae9546c23e6b907118
```

## Verification

```text
tests/test-mesh-witness-ask-metrics.sh: rc=0
  valid fixture: ask_open=1 ask_stale_h=20.0 ask_resolve=0.5 ask_den=8 ask_p90_h=17.0 ask_unknown=0
  invalid-age fixture: ask_open=UNKNOWN ask_stale_h=UNKNOWN ask_resolve=UNKNOWN ask_den=2 ask_unknown=1
  output sha256=5f85963bd1c9060309d1d8e44e77e693f4c3ba5e65cff8070d1972438996f1f0
python3 -m py_compile scripts/mesh-witness: rc=0
mesh-witness --test: rc=0
  output sha256=64b87a42b50624d2ce84523ed5e08ffccffdcfe44cc29296b9b6ab5925d93724
```

## Live wiring evidence

The deployed reflex wiring is present at `~/.mesh/reflexes.cron:145`:

```text
*/2 * * * * $HOME/.local/bin/mesh-witness --measure >> $HOME/.mesh/witness.cron.log 2>&1
```

A fresh deployed `--measure` ran `rc=0` and appended:

```text
2026-09-07T18:00:41Z ... ask_open=0 ask_stale_h=0.0 ask_resolve=0.922 ... ask_den=218 ask_p90_h=10.2 ask_unknown=0
```

Fresh ledger/output SHA256: `50993e62124509f0796a8ea13a8f726a5e6aa68ae8371e4457555fe501e1b815`.
Cron wiring SHA256: `e4aa5b25db3f263e9e12d1fae9c8976e61ab9226ebf7a6c06a95d50011799167`.
