# promise-writeoff Component B verification — manual-writeoff-reroute — 2026-09-12

- Step: promise-writeoff-implementation-20260912/manual-writeoff-reroute (owner witness).
- Finding: the implementation was already landed at HEAD (5d7ee5ed, +472/-16 on
  scripts/mesh-promises) via the step-0 autoland lane. No new code was written by
  this turn; the work was to verify the landed code satisfies the step, not to
  re-implement it. Worktree is clean for scripts/mesh-promises — nothing to land.

## Evidence (all read from disk / executed, 2026-09-12T03:2xZ)

- `~/.local/bin/mesh-promises --test` → rc 0, 19 `ok:` lines, zero FAIL
  (log: /tmp/witness-promises-test.log).
- Spec tests 1/2/3/4/4b present as suite blocks 51–56 in do_test() and green:
  - 51: writeoff of open reflex-broadcast claim closes via equity:claims:writeoff
    (not equity:claims), `hledger check` balances, no expenses:claims:uncollectible
    leakage (narrow bad-debt path preserved and separate).
  - 52: nonexistent slug / unknown family / missing owner-slug / missing --reason
    all refused non-zero with mesh-chat never invoked (absence-guard-above-dispatch).
  - 53: reroute moves unrouted promise score→witness, same-slug reopen threads in
    --all, old leg books equity:promises:reroute; exactly two board lines.
  - 54: reroute onto non-roster window refused with the --check roster message, no post.
  - 55 (4b): `--reroute hold` refused outright before lookup, message points at
    `--writeoff hold`; `--writeoff hold` on the same fixture succeeds.
  - 56: claim reroute + self-address guard (no self-addressed [verify] successor gap).
- Deployed parity: scripts/mesh-promises == ~/.local/bin/mesh-promises (cmp clean).
- Identity default per spec: commands post as caller via mesh-chat, no impersonation;
  MESH_PROMISE_NO_POST hard refusal present on both paths.

## Disposition

Step requirements met by the landed implementation. Closed with this receipt as
artifact. Remaining chain steps (suggested-owner-hints, gated-auto-reaction) are
separate open scope, untouched.
