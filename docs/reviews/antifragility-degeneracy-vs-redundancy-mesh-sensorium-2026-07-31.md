# Antifragility live review — DEGENERACY vs REDUNDANCY (2026-07-31)

**Area:** antifragility / convexity / ruin theory (Taleb), cross-domain transfer to a distributed sensor mesh.
**Landed:** `scripts/mesh-sensorium` new `--degeneracy` axis (report-only). Artifact of this review.

## The concept we did NOT embody

**Functional DEGENERACY as distinct from REDUNDANCY.**

- **Redundancy** = the same function delivered by **identical** elements.
- **Degeneracy** = the same function delivered by **structurally different** elements.

The distinction is invisible in calm conditions and decisive under **correlated / common-mode
failure**: identical replicas share a platform, stack, or dependency, so *one* disruption invalidates
*several* apparent backups at once. Counting replicas therefore **overestimates** resilience.

### Sources (live literature, read this session)

- **Root (biology):** G. M. Edelman & J. A. Gally, "Degeneracy and complexity in biological systems,"
  *PNAS* **98**(24):13763–13768 (2001). Degeneracy is ubiquitous in robust biological systems (genetic
  code, immune repertoire) and is what redundancy is *not*: different structures, same function.
- **Live cross-domain transfer (2026):** M. K. Hassan & I. Dey, "Degeneracy-Aware Functional and
  Algorithmic Resilience in Virtualized 6G Networks Under Correlated Failures," **arXiv:2605.03035**
  (2026). Central claim: *"redundancy counts alone overestimate resilience because replicas often share
  platforms, software stacks, and dependencies — a single disruption can invalidate several apparent
  backups at once."* Gives the **Functional Substitution Score** `FSS(f) = fraction of realization pairs
  that are structurally distinct`, plus a Multi-Layer Degeneracy Index. Results: degeneracy-aware systems
  sustain function where redundancy collapses, especially past ~30% targeted removal.

This is a Taleb-adjacent antifragility mechanism (it is *how* a system stays convex under shocks: a
diversity of substitutable pathways is optionality realized in structure) and it is **not** any of the
axes we already carry — `mesh-convexity` (Jensen gap / left-tail direction), `mesh-endogeneity`
(correlated *trials* in a payoff series), `mesh-resource-guard` (Parisian dwell), or the RR
efficiency↔resiliency `--balance` axis.

## Where we'd been — and the gap

`mesh-sensorium --balance` already reads **efficiency ↔ resiliency**: it counts, per percept-category,
how many cached streams are LIVE (`depth`), and calls `depth ≥ 2` **"resilient (redundant)."** That is a
pure **redundancy count**. It never asks whether those ≥2 streams are structurally distinct.

Concretely, on this node right now `--balance` reads:

- **BODY** `depth 3` (motion + light + power) → "resilient."
- **ROOM** `depth 6` → very "resilient."

But BODY's three streams all ride the **one phone over the one SSH/termux transport**. One
phone-unreachable event (memory: `mesh-home-eyes-loss-usb-webcam-wedge`; the Note3 `adb SIGABRT` the
crash-watch reflex surfaced this morning) blinds the *entire* "resilient" category at once. That is the
exact common-mode trap Hassan & Dey name — and `--balance` scored it as our strongest category.

## The transfer — `mesh-sensorium --degeneracy`

Reuses the `--cached` roll-call (same source of truth as `--balance`), then groups each category's LIVE
streams into **common-mode classes** by the failure-carrying substrate they share, and reports:

- `depth` = live streams (**redundancy**, `--balance`'s axis)
- `degen` = number of **distinct** common-mode classes (**degeneracy**)
- `FSS` = cross-class pairs / all pairs `= 1 − Σ mᵢ(mᵢ−1) / [depth(depth−1)]`
- **MONOCULTURE** flag when `depth ≥ 2` but `degen == 1`: `--balance`'s "resilient" is an overestimate.

### Substrate-class map (grounded in verified producers, not guessed)

| class | streams | common-mode dependency |
|-------|---------|------------------------|
| `phone` | motion, light, power, prox, **tempo**, **context** | phone reachable over SSH/termux |
| `audio` | room, ambient, audio-path, media | mic + STT/audio stack |
| `ble` | presence (n/top) | BLE radio scan |
| `net` | watchtower | network reachability |
| `derived` | mode, home-state, operator-home, situation, perimeter, interruptibility | on-node fusion of other categories |
| `node` | HW | on-node procfs/hw |

`tempo` and `context` were the trap: a naive read files them under `audio` (they live on the ROOM line).
Checking their real producers — `mesh-activity-tempo` fuses tamper + body-motion + light (all **phone**
axes; its live value is `DEGRADED reason=axes-dark` precisely because the phone is offline), and
`mesh-body-context` = body-motion + ambient light (**phone**) — moves them to `phone`. That correction
*matters*: it turns ROOM from a false audio-monoculture into a genuinely 2-class degenerate category
(audio 4 + phone 2). The map's honesty is the whole point of the axis. An unmapped field falls to its own
class (conservative: can only *add* degeneracy, never manufacture a false monoculture).

### Live finding on mesh-home

```
BODY         depth 3  degen 1 [phone]          FSS 0.00 ⚠ MONOCULTURE
ROOM         depth 6  degen 2 [audio phone]    FSS 0.53
HOUSEHOLD    depth 3  degen 1 [derived]        FSS 0.00 ⚠ MONOCULTURE
SITUATION    depth 3  degen 2 [derived net]    FSS 0.67
posture: REDUNDANCY-OVERESTIMATE — 2 categories read redundant but rest on a SINGLE substrate
```

`--balance` calls BODY (depth 3) and HOUSEHOLD (depth 3) resilient; degeneracy shows both are
common-mode monocultures — one phone-down / one upstream-fusion-death takes each whole category together.

## Test (RED-first, gated in `mesh-sensorium --test`)

Two crafted-roll fixtures drive the real black-box: a single-substrate depth-3 category must read
`MONOCULTURE`/exit 3; a cross-substrate category must read `degen 2 / FSS 1.00` and NOT flag. Both map
directions are gated — **collapsing** the map (two classes → one) turns the degenerate fixture RED;
**exploding** it (every field its own class) turns the monoculture fixture RED. Verified RED both ways,
then restored green. So the classifier must actually *discriminate*, not always-flag.

## Scope / honesty

Report-only — no verdict, kill, or board post touched; a new visibility axis beside `--balance`. Degeneracy
is undefined for `depth < 2` (single-stream categories print `degen 1` untagged). The `derived` monoculture
(HOUSEHOLD) is a softer claim than the `phone` one — those streams are on-node derivations sharing upstream
fate, not independent senses; the flag is honest but the reader should weight it as such. Not wired to cron
(on-demand read like `--balance`/`--exteriority`).
