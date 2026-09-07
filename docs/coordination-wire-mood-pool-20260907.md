# wire-mood-pool — lease, progress, and live-path receipt

Date: 2026-09-07  
Owner: `genome`  
Task: `tinyfleet-specialists/wire-mood-pool`  
Lease: claimed with `mesh-task take tinyfleet-specialists wire-mood-pool` before implementation.

## Landed wiring

- `scripts/mesh-tiny-fleet-pool` is a guarded candidate wrapper.
- `scripts/tiny_fleet_pool.py` verifies the independently recorded adapter hashes before loading
  either adapter through the project venv and cached SmolLM2 base.
- `scripts/mesh-relay` accepts `--pool tiny-fleet`; auto mode considers it only with
  `MESH_RELAY_TINY_FLEET=1`, then falls through to pool-0 (`groq`) and the existing chain when
  the candidate is unavailable.
- A specialist `ABSTAIN`/escalate is terminal (exit 3), so fallback cannot erase the abstention.

The verification receipt names the available adapters `lora-guitar` and `lora-sourdough`; no
separate `lora-mood` weight exists in that receipt. This artifact therefore claims wiring of the
verified adapters and honest abstention for prompts with no specialist evidence, not a fabricated
mood-specific adapter.

## Live evidence

Verified adapter inventory:

```text
guitar    68697b792b847d53945b43f502802735fb9243630c609cae16ef21f00505ebc1
sourdough ca02ca12cd773003a5b45be6f1a9fbf9dc10a614302f1723e3078f491cdd25be
```

Real GPU-backed relay path:

```text
$ timeout 180 scripts/mesh-relay --pool tiny-fleet 'Give me a beginner guitar chord progression.'
Sure, here's a simple beginner's chord progression for you:
1. Root Position Chord: ...
```

Guarded auto candidate served the same real adapter path with
`MESH_RELAY_TINY_FLEET=1`.

Forced candidate miss with the real pool-0 fallback:

```text
$ MESH_RELAY_TINY_FLEET=1 MESH_TINY_FLEET_DIR=/tmp/mesh-no-tiny-fleet \
    scripts/mesh-relay 'Reply with exactly one word: pong'
pong
```

Abstain/escalate preservation:

```text
$ MESH_RELAY_TINY_FLEET=1 scripts/mesh-relay 'What is the capital of France?'
[ABSTAIN] tiny-fleet has no specialist with sufficient routing evidence; escalate to the appropriate specialist or human.
exit=3
```

## Verification

```text
tests/test-mesh-tiny-fleet-pool.sh                         PASS
scripts/mesh-relay --test                                  PASS
bash -n scripts/mesh-relay scripts/mesh-tiny-fleet-pool   PASS
```

The focused test covers the two verified hashes, missing-candidate fallback, forced specialist
abstention, and relay-level terminal exit 3. The relay smoke test remains green after the new
pool is added.

Deployment parity was checked after sync:

```text
scripts/mesh-relay == ~/.local/bin/mesh-relay
scripts/mesh-tiny-fleet-pool == ~/.local/bin/mesh-tiny-fleet-pool
deployed ~/.local/bin/mesh-relay --pool tiny-fleet '<guitar prompt>' → real adapter response
deployed ~/.local/bin/mesh-relay 'What is the capital of France?' → ABSTAIN, exit=3
```

## Completion receipt (2026-09-07T11:04:21Z)

The live-path witness was run from the repository root after the source/deployed parity check:

```text
forced `--pool tiny-fleet` guitar prompt       PASS — real adapter response
auto `MESH_RELAY_TINY_FLEET=1` guitar prompt   PASS — guarded candidate served
auto candidate miss + pool-0 prompt `pong`     PASS — exit=0, output `pong`
forced unknown-domain prompt                   PASS — exit=3, `[ABSTAIN] ... escalate`
source/deployed mesh-relay SHA-256             ba7221dd83b197278e09e1ef23b583e77015236cf53d7b2e2e78149d35fa848a
source/deployed candidate SHA-256              1576bc20c9bd068dfb05e15de852dd3a8f33f4bd6e07d1138e59ac857b9e24b6
```

The task is complete. The recorded specialist inventory remains `lora-guitar` and
`lora-sourdough`; no separate mood adapter is claimed. The candidate is therefore guarded and
opt-in, with pool-0 fallback and terminal abstain/escalate semantics preserved.
