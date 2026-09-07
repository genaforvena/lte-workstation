# Coordination P1 re-verification — 2026-09-07

The previously blocked ownership-suite verification is now green.

Evidence:

- `timeout 150s bash tests/test-job-dispatch-ownership.sh` — exit 0.
- `bash scripts/mesh-mind-control --test` — exit 0; all smoke assertions pass.
- `bash scripts/mesh-promises --test` — exit 0.
- `python3 job/mesh-job-cal --test` — exit 0.
- `python3 scripts/mesh-chat-deliver --test` — PASS.
- `bash scripts/test-mesh-board` — PASS.
- `bash tests/test-mesh-witness-promises.sh` — PASS.
- `git diff --check` and shell syntax checks — PASS.

The source/deployed parity check is also green for the four coordination tools:

```text
scripts/mesh-board         == ~/.local/bin/mesh-board
scripts/mesh-chat          == ~/.local/bin/mesh-chat
scripts/mesh-chat-deliver  == ~/.local/bin/mesh-chat-deliver
scripts/mesh-mind-control  == ~/.local/bin/mesh-mind-control
```

During the repair, the ownership wrapper exposed stale documentation assertions
(`exactly one link/place` and `proposed.*excluded`). The current contract says
`exactly one of --link or --place`, requires `--source`, and says proposed slots
are offers with incomplete records rejected. The test now checks those current
contract statements directly in `job/README.md`.

Remaining coordination obligations are separate from this P1 verification:
the active tiny-fleet chain is waiting on genome's live `wire-mood-pool` artifact,
and the promise ledger still shows the poster-owned historical `chose` claim and
the partially discharged `witness-vpn` hold pending their scoped redemptions.
