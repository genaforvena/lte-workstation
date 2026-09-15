# Operator-state I/O Congestion Link Implementation Plan

**Goal:** Close the live producer→consumer link from `mesh-io-congestion` to `mesh-operator-state`.

**Architecture:** `mesh-operator-state` reads the producer's existing state artifact with a bounded freshness check and validates its label. A new joint `AT-DESK` × I/O-stall verdict is derived only from a fresh, real producer artifact; absent, stale, malformed, and unreachable inputs remain `UNKNOWN`.

**Tech Stack:** Bash, existing shell fixture tests, `/proc`-backed `mesh-io-congestion` artifact.

## Global Constraints

- Do not create a new tool file or add another hardware probe.
- Missing, stale, malformed, and unreachable I/O evidence must never become a calm/healthy value.
- Preserve unrelated working-tree changes and do not commit.
- Verify both the producer's live artifact and the consumer's end-to-end live output.
- Run `mesh-doctor`; do not post `[sense]` unless it passes without a new orphan warning.

---

### Task 1: Consume the live I/O-congestion relation in operator-state

**Files:**
- Modify: `scripts/mesh-operator-state`
- Test: embedded `scripts/mesh-operator-state --test`

**Interfaces:**
- Consumes: `~/.mesh/.io-congestion.state`, first field `label=<label>`, refreshed by `mesh-io-congestion`.
- Produces: `io_congestion_state` in operator-state text/JSON and a distinct desk/I/O-stall joint label.

- [ ] Add failing classifier tests for `AT-DESK + COUPLED`, non-desk, and `UNKNOWN` input.
- [ ] Add failing fixture tests for fresh accepted state and stale/missing/malformed state returning `UNKNOWN`.
- [ ] Implement the bounded reader and pass its value into the existing fusion.
- [ ] Run the focused test and syntax check.
- [ ] Read the producer live, run the consumer live, and verify the consumed field plus joint output behavior against a real artifact.
- [ ] Run `mesh-doctor`; post `[sense]` only if it passes with no new orphan warning.
