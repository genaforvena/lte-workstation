# Live literature review — distributed systems coordination

**Area:** gossip / CRDTs / eventual consistency · **Angle:** CROSS-DOMAIN transfer into a distributed sensor mesh
**Date:** 2026-08-18 · **Organ:** `scripts/mesh-climate` · **Status:** review + **landed** (uncommitted, steward lands)

---

## The concept we do not embody

**Event-triggered communication stated against the BROADCAST SNAPSHOT `x̂`** — the trigger compares the
node's current value to *what the receivers last actually got*, not to what the node itself last computed.

> Zhai, Yuan, Ni, Wang, Zhang, Li — **"Event-Triggered Gossip for Distributed Learning"**,
> [arXiv:2602.19116v1 \[eess.SP\]](https://arxiv.org/abs/2602.19116), **22 Feb 2026** (read this session).

Each node transmits only when `‖x_i,t − x̂_i,t‖ ≥ τ_t`, where `x̂_i,t` is *the last snapshot node i
broadcast*, kept as a **separate variable** from the local state `x_i,t`. Reported: **69.35% (MNIST) /
71.61% (Fashion-MNIST)** fewer point-to-point transmissions at 0.84 / 0.62 pp accuracy cost; ergodic
`O(T^-1/2)` convergence under a **decaying** threshold (`τ_t = τ₀/√(t+1)`, `Θ(t⁻¹)`), while a fixed
nonzero `τ` leaves a permanent **steady-state bias**. The paper has **no** max-silent-interval fallback —
a node whose drift stays under `τ` can stay silent forever.

### Why the `x̂` indirection is the transferable part, not the bandwidth saving

The mesh does not need the bandwidth result — our senses are cron-cadenced and cheap. What we lack is the
*separation of variables*. A trigger stated against the local state consumes the change the instant the
state is written, whether or not anyone received it. A trigger stated against `x̂` makes a **lost
transmission self-healing with no acks, no retry queue and no second channel**: a failed broadcast leaves
`x̂` behind, so the deviation *persists into the next tick* and the trigger re-fires by construction.

### Prior art check (this genome)

`mesh-chat-sync` already carries the board-side canon — G-Set union, HLC receive-merge, Merkle
pre-check, causal stability, PBS t-visibility, AoI/AoIV, ConflictSync / Rateless-Bloom / RIBLT
(SIGCOMM'24). `mesh-converge` measures the inconsistent window. `mesh-edge-gate-audit` (daily) drives
every `--edge` reflex in **both** directions and proves the gate can fire and hold.

**None of them models delivery.** `grep -rn 'event.?trigger|deviation.?trigger|send-on-delta'` over
`scripts/ docs/` returns only unrelated hits (`mesh-mind-compact`'s per-claim trigger, two design docs).
`mesh-edge-gate-audit`'s own charter is fire-vs-hold — it cannot see a gate that fired into a void,
because *a delivered post and a swallowed one produce byte-identical local state*.

### Discarded in one line each (checked, not assumed)

- **Rateless IBLT / ConflictSync set reconciliation** — already cited in `mesh-chat-sync:62-70`.
- **Causal stability (Baquero/Almeida/Shoker)** — already landed, `docs/reviews/…causal-stability-frontier…2026-07-28.md`.
- **Self-stabilizing min-max consensus via path-loop detection** (Cortecchia/Pianini/Viroli, [COORDINATION 2026](https://link.springer.com/chapter/10.1007/978-3-032-28358-0_5)) — the stale-extremum loop it fixes needs multi-hop neighbour relay; our mesh is fully-connected over Tailscale, so no loop exists to break.
- **Hinted handoff / read repair (Dynamo)** — subsumed: the board's G-Set anti-entropy already back-fills an unreachable peer, and a node's sensor reading is node-local truth, not a replica anything else may repair.
- **Covariance Intersection / data incest** — hypothesised as live in `mesh-situation` (INTERNAL vs EXTERNAL "concordance"); **falsified by reading the inputs** — the only `mesh-stress` and `mesh-reflex-health` references inside `mesh-perimeter` are comments (`:808`, `:523`), so the two axes are input-disjoint and the concordance is real corroboration. `mesh-operator-home:_calibration` already groups phone-anchored modalities by hand.

---

## The application: `scripts/mesh-climate`

**The fault, measured in the file.** `fuse()` wrote the state one line before it announced, and threw the
announcement's exit code away:

```
131:  printf '%s\n' "$new" > "$STATE"     # unconditional write: mtime = ran-live
134:    MESH_WHO="senses@$(hostname)" mesh-chat "[climate] $prev_class -> $class ($new)" >/dev/null 2>&1 || true
```

The unconditional write is **correct and deliberate** — it is the liveness-touch convention (mtime =
ran-live, content = the change). But it is also the change-gate's only reference, so the transition was
consumed at line 131. A `mesh-chat` that failed for any reason — board lock, full disk, the
NUL-corruption class — **lost the class transition permanently**: the next tick reads `prev_class` = the
new class, the gate holds, and no reader, local or peer, ever learns the climate moved. Every liveness
watchdog stays green throughout, because the mtime keeps being touched. Silence is this reflex's normal
output, so nothing downstream can tell a delivered change from a swallowed one.

**The change.** `x̂ = $STATE.announced` — the class the board last *accepted*. It advances **only** when
`mesh-chat` returns 0. `announce_step()` returns 0 iff `x̂` is caught up, 1 iff a transition is still owed.

Three consequences:

1. A failed post retries on the next tick **by construction** — no queue, no ack protocol, no new cadence.
2. The announcement's "from" is now what readers last heard (`x̂ -> class`), not what this node last
   computed — which they may never have seen.
3. The gap between `$STATE` and `$STATE.announced` is an **on-disk, ageable** measure of what this node
   knows but has not managed to tell anyone. That observable did not exist before.

Bootstrap adopts `x̂` from the local state, never from empty, so a node running since before this change
does not announce a phantom transition.

**Gate.** `--test` green (rc 0). Five legs, all hermetic: **A** owed + post fails → `x̂` must not advance;
**B** retry delivers → advances, and the message reads *from `x̂`*; **C** hold → zero posts; **D** bootstrap
→ pin silently; **E** the **wiring**, driving the real script as a child.

**Five mutants, each watched go RED for its own reason:**

| mutant | verdict |
|---|---|
| advance `x̂` on an undelivered post (the pre-fix behaviour) | RED — `x̂ advanced on an UNDELIVERED post` |
| announce from `prev_class` instead of `x̂` | RED |
| drop the hold guard (always post) | RED — `held class must post nothing` |
| bootstrap announces | RED — `bootstrap must not announce ( -> STABLE)` |
| unwire `announce_step` from `fuse()` | RED — `fuse did not advance x̂ on a delivered post` |

---

## Two traps paid for in this session, recorded

1. **`path-stub-cannot-shadow-a-mesh-tool`, observed live.** Leg E first stubbed `mesh-chat` by
   prepending a temp dir to `PATH`. The child re-runs `export PATH="$HOME/.local/bin:$PATH"` at load, so
   the **real** `mesh-chat` shadowed the stub and the leg posted to the live board — one stray
   `[climate] SEEDXX -> STABLE` line at `2026-08-18T06:33:00Z`, disclosed, not scrubbed (the board is a
   G-Set; a local delete is resurrected by the next sync). The fence is a **fake `$HOME`**
   (`$MESH_TEST_TMPD/home/.local/bin/mesh-chat`), and leg E now *asserts the stub was reached*, so the
   fence failing is itself RED rather than silently re-arming the live path.
2. **The paper's own gap is our existing rung.** Event-triggered communication has no max-silent-interval,
   so silence is indistinguishable from death — which is exactly what the mesh's liveness-touch convention
   already answers (`mesh-state-touch` on every successful eval). The two are complementary: liveness-touch
   covers *"did the reflex run"*, `x̂` covers *"did anyone hear it"*. Neither implies the other, and this
   file now keeps both.

## Not claimed

The write-then-post-then-discard-rc shape is a **family**, not one file — `grep` finds ~25 `--edge`
reflexes that call `mesh-chat`. Only `mesh-climate` was read against its inputs and fixed here. The rest
is a lead for a follow-up sweep, not a measured finding.
