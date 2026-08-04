# Antifragility live review — THE NONLINEARITY OF JOINT FAILURE (2026-08-04)

**Area:** antifragility / convexity / ruin theory (Taleb), cross-domain transfer to a distributed sensor mesh.
**Landed:** `scripts/mesh-sensorium` new `--amplification` axis (report-only) + the substrate-class map
lifted to a single shared definition. Artifact of this review.

## The concept we did NOT embody

**Superadditive amplification of SIMULTANEOUS failures — and its corollary that a ranking of
single-point impacts cannot find the dangerous combinations.**

The systemic damage of a *combination* of failures is not the sum of the damages of its members. It can
be drastically larger, because the **substitutability** that made each member individually survivable
runs out when they go together. The distribution of that amplification is extremely heavy-tailed: almost
every pair is harmless, a handful are catastrophic — and *individual* impact does not predict which.

### Source (live literature, read this session)

- **The 2026 result:** J. Fialkowski, S. Havlin, S. Thurner, *"Catastrophic disruption cascades driven by
  the nonlinearity of systemic risk"*, **arXiv:2607.20068** (submitted 22 Jul 2026, econ.GN).
  Verbatim from the abstract: *"the systemic risk contributions of combinations of firm failures can be
  drastically larger than the sum of the damage caused by the firms individually … combined failures can
  produce systemic risk amplifications of up to a factor of 257. However, only a tiny fraction of 0.14% of
  pairs exhibit a more than 4-fold amplification of systemic risk. We develop a simple method to identify
  firm combinations that lead to large systemic risk amplifications. The origin of these amplifications is
  a breakdown of the substitutability of defaulted suppliers."* Measured on a firm-level reconstruction of
  the **national supply chain network of Ecuador**. The paper closes on exactly the situations that take
  several nodes at once — natural disasters and wars.
- **The single-node baseline it builds on:** C. Diem, A. Borsos, T. Reisch, J. Kertész, S. Thurner,
  *"Quantifying firm-level economic systemic risk from nation-wide supply networks"*, **Sci Rep 12:7719
  (2022)** (arXiv:2104.07260) — the ESRI, the per-firm systemic-impact index. 0.035% of firms carry
  extraordinary ESRI; **position in the network, not size, explains it**.

Two things make this load-bearing rather than "cascades are bad":

1. **Superadditivity is the measured quantity**, not a metaphor — a ratio of joint damage to the sum of
   individual damages, computable by removal.
2. **An individually-harmless node is not a safe node.** The single-point ranking — the standard
   instrument, and the *careful* one — is structurally blind to the pairs that matter.

## Where we had been (and why this is not a re-land)

The mesh's resilience reading of its own sensorium is three axes deep, and **all three are single-failure
readings**:

- `mesh-sensorium --balance` (RR efficiency↔resiliency, 2026-07-28) counts LIVE streams per
  percept-category — depth ≥ 2 reads "resilient (redundant)".
- `mesh-sensorium --degeneracy` (this same review area, 2026-07-31) asks whether those streams are
  **structurally distinct**, flagging MONOCULTURE where depth ≥ 2 rides one substrate class.
- `mesh-endogeneity` reads correlated *trials within a series*; `mesh-sensorium --exteriority` reads
  consumer fan-out.

`--degeneracy` **retires a category from worry the moment two classes back it** — correctly, for any
*one* class dying. Nothing in the mesh has ever removed **two substrates at once** and priced what dies.
That is precisely the blind spot the 2026 result names.

## The transfer

Treat each **substrate class** as a "firm" and define the systemic loss of a failure set `S`:

> **L(S)** = number of percept-categories **blinded** — every live stream in the category belongs to a
> class in `S`, so the category has no surviving pathway.

Then for each PAIR of classes, the paper's ratio:

> **A(i,j) = L({i,j}) / (L(i) + L(j))**

- `A == 1` — **additive**: substitutability holds, the parts already account for the whole.
- `A > 1` — **SUPERADDITIVE**: the joint loss beats the sum; substitutability breaks on the named categories.
- `L(i) = L(j) = 0` while `L({i,j}) > 0` — **PURE-JOINT**, amplification unbounded: costs *nothing* apart,
  blinds together, and is **invisible to every single-point ranking the mesh already runs**.

## What it says about this node (live, 2026-08-04)

Same roll, both axes:

```
--degeneracy :  ROOM       depth 6  degen 2 [audio phone]   FSS 0.53
                SITUATION  depth 2  degen 2 [derived net]   FSS 1.00
                → "2 truly-degenerate (common-mode resilient)"

--amplification:
  single-point loss (what the mesh could already see):
    phone   blinds 1 — BODY        audio   blinds 0
    ble     blinds 1 — PRESENCE    net     blinds 0
    derived blinds 2 — HOUSEHOLD COORDINATION
  joint pairs, worst first:
    phone + audio    L 1 + 0 -> 2   amp 2.00x  ⚠ SUPERADDITIVE — breaks on ROOM
    derived + net    L 2 + 0 -> 3   amp 1.50x  ⚠ SUPERADDITIVE — breaks on SITUATION
    (7 further pairs, all exactly 1.00x additive)
  posture: SUPERADDITIVE — 2 of 9 blinding pairs cost more together than apart
```

The two categories `--degeneracy` certifies as **common-mode resilient are exactly the two superadditive
pairs**. That verdict is true of either death alone and false of both — which is the whole finding,
landing on live data rather than a fixture. `audio` and `net` each blind **nothing** on their own: on the
single-point ranking they are the two safest substrates on the node, and each is half of a superadditive
pair.

## Honest boundaries (stated, not omitted)

1. **The loss unit is percept-categories blinded** — coarse, deliberately: it needs nothing beyond the
   roll `--degeneracy` already parses. A finer unit (consumers downstream, which `--exteriority` already
   counts per stream) would sharpen the ratio; HELD until the fan-out map is worth wiring.
2. **Blinding is FIRST-ORDER.** A `derived` category whose upstream classes all died still reads live
   here as long as its own `.state` is fresh — so this **understates** the cascade. The printed
   amplification is a floor, never a ceiling. Naming the direction of the error is the obligation; a
   second-order cascade needs a **verified** per-derived-sense upstream map, not a guessed one.
3. **A is a ratio of small integers on a 6-category sensorium.** The paper's 257× lives on a national
   supply network. Do not quote a magnitude here as if it were theirs.

## Gates (RED-first, all three mutants seen red before landing)

`mesh-sensorium --test` drives the **real black box** against three crafted rolls (the readable-`$2` path),
pinning all three branches and the *arithmetic*, not just the flags:

| fixture | roll | must read |
|---|---|---|
| pure-joint | `ROOM room=CALM · context=SOLO` | `amp UNBOUNDED` · PURE-JOINT blinds ROOM · exit 3 |
| superadditive | `BODY motion=STILL` + `ROOM room=CALM · context=SOLO` | exactly `amp 2.00x` (L 1+0→2) · `0 PURE-JOINT` · exit 3 |
| additive | `BODY motion=STILL` + `PRESENCE n=3` | `amp 1.00x` · `posture: additive` · no SUPERADDITIVE · exit 0 |

Falsifiers run from a scratch copy, each **observed RED**:

- **joint loss := sum of singles** (`lij=lossOf(S)` → `lij=L[i]+L[j]`) — the axis stops removing two
  classes at once and merely re-adds single points: pure-joint fixture goes red (`exit 0`, "additive").
  This is the whole content of the axis.
- **substrate map collapsed** (`audio` folded into `phone`) — no cross-class pair left to remove; the
  pure-joint fixture goes red (`exit 0`) and `--degeneracy`'s own degenerate fixture goes red too.
- **always-flag** (`amp>1` → `amp>=1`) — the additive fixture goes red. A superadditive verdict on
  substitutable classes would be a lie, and the gate refuses it.

## Also landed: one map, two readers

The substrate-class map was inlined in `--degeneracy`'s awk `BEGIN`. `--amplification` needs the identical
map, and a second copy would rot out of agreement — each axis would then be measuring a different mesh
(*a rule asserted at one call site is not asserted*). It now lives once, as `SUBSTRATE_CLASS_MAP` above
both blocks, parsed by each reader. `--degeneracy`'s output is byte-identical across the refactor and its
own fixtures still gate it.

## Not landed (deliberate)

- **No cron, no board post, no kill/defer.** Report-only, on-demand — same posture as `--degeneracy`.
  The precautionary/absorbing-barrier **gate** remains open in this area.
- **Triples and larger sets.** The paper is explicit about pairs; the machinery generalizes (`lossOf`
  takes a set), but a claim about triples on 6 categories would be arithmetic dressed as a finding.

**Cite:** Fialkowski, Havlin & Thurner, arXiv:2607.20068 (2026); Diem, Borsos, Reisch, Kertész & Thurner,
Sci Rep 12:7719 (2022). WebSearch + arXiv abstracts read 2026-08-04.
