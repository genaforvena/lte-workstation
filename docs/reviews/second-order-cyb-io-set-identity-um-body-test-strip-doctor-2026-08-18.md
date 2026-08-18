# Live literature review — second-order cybernetics

**Area:** second-order cybernetics (von Foerster, Pask, Beer) · **Angle:** a RECENT result (2023–2026)
**Date:** 2026-08-18 · **Organ:** `scripts/mesh-doctor` · **Status:** review + **landed** (uncommitted, steward lands)

---

## Why this is not the standing discard

`~/.mesh/knowledge/review-second-order-cybernetics-AREA-MINED-frontier-2026-07-02.md` declares this area
MINED and instructs: *"do not re-search unless >1 month has passed or a genuinely new primary result is
named."* Both conditions hold — it is 6.5 weeks later, and the area has in fact kept yielding (22
`second-order-cyb-*` / `vsm-*` reviews now sit in `docs/reviews/`, most of them **after** that verdict). That
same doc names the one sub-thread it left unwalked: **Pask's entailment meshes** — "his own
knowledge-representation formalism, distinct from conversation theory… pointers only, not reviewed here."
This review walks it.

## The concept we do not embody

**I/O-SET IDENTITY — a node is distinct from another precisely when their input/output sets differ.**

> Ju Wu & Calvin K. L. Or, *"Position Paper: Towards Open Complex Human-AI Agents Collaboration Systems
> for Problem Solving and Knowledge Management"*, [arXiv:2505.00018](https://arxiv.org/abs/2505.00018)
> (v1 Apr 2025, v2 Oct 2025) — read in full via `pdftotext`, §3.3–3.4 and Tables 9/20–21.

The paper's knowledge backbone is Pask's **entailment mesh** (non-directed clusters) folded, *under the
bootstrapping axiom*, into a **directed entailment net** — and it states the identity rule verbatim:
*"nodes are distinct precisely when their respective input/output sets differ"*, with three weighted link
rules (direct, transitive, symmetric) and the CT operator dials **saturate / bifurcate / prune**
(Pask 1976; Heylighen 2001). It also names the failure mode of the whole coherence-side approach:
*"Risk of coherence drift if mutual support lacks epistemic checks."*

**What the mesh does instead:** it identifies everything by **name**. Tools are distinct because their
filenames differ; state artifacts because their slugs differ. Doctrine keeps re-discovering the cost of
that one case at a time — *"do NOT mint a sixth usb tool"*, *"never add a second librosa analyzer"*,
`[[writer-redundancy-blinds-mtime-liveness]]`, `[[a-self-describing-artifact-with-no-writer]]` — each a
name-based fix for an I/O-set problem. Nothing in the genome asks the I/O question directly.

## Applying it produced a scan — and the scan found the organ was blind

Built the I/O relation the criterion needs: **declarer → declared artifact**, over all 630 mesh tools,
using `mesh-doctor`'s own `umwelt_slug` (the declaration) and `um_body` (the tool's body with its
`--test` block and comments stripped) to classify each declarer as **WRITER** or **consumer**.

First run: **2 apparent co-writers** — `mesh-node-power` writing `mesh-conservation`'s
`.conservation-state`, and `mesh-activity` writing `mesh-room-sense`'s `.room-sense.state`. Both would
have been textbook `writer-redundancy-blinds-mtime-liveness`. **Both were false.** Each "write" was a
`--test` sandbox line that `um_body` failed to strip.

### The finding: `um_body` knew one of three test-block openers

`um_body` exists precisely to prevent *"the test forging the evidence it exists to check"* — its own
header says so. It matched only `if/elif … --test … then` (→ bare `fi`) and the case arm `--test)`
(→ bare `;;`). Census over the live corpus, this date:

| opener form | tools | seen by the old `um_body`? |
|---|---|---|
| `if/elif … --test … ; then` | 430 | yes |
| `--test)` case arm | 185 | yes |
| `[ "${1:-}" = --test ] && { … }` brace group | **49** | **no** |
| `--test) MODE=test ;;` … later `if [ "$MODE" = "test" ]` | **7** | **no** |

So for **56 tools** the entire smoke test was handed to the callers as production code. Those callers are
not decorative: `um_self_reads` (the umwelt check's *load-bearing half* by its own comment) and
`--supersede`'s knob-dependency scan. A tool could earn a "temporal interpretant" or a knob dependency
from its own harness.

The MODE form was wrong in **both directions at once**: `--test) MODE=test ;;` matched the case-arm
opener, so `intest` went high on an *arg-parse* line and stayed high until the next bare `;;` — eating
innocent parse arms — while the real test body further down was never recognised at all.

Corpus effect, measured old vs new over all 630 tools:

| | old | new |
|---|---|---|
| test block leaked into the body (`smoke-test: FAIL` present) | 98 | **62** |
| body over-stripped (kept < total/12) | 6 | **2** |

(The residual 62 is an over-count: tools that embed a Python program keep their `smoke-test: FAIL` string
in genuine production text. The residual 2 are named, not hidden: `mesh-forage`, `mesh-ss-clients`.)

### The fix (`scripts/mesh-doctor`, `um_body`)

Three openers, and **the terminator is derived from the opener** (`&& {` → brace depth · `then`/if-form →
column-0 `fi` · case arm → bare `;;`) instead of any terminator ending any block. Three details each
earned by a failure seen live:

1. **Brace depth, not a line pattern.** `mesh-land` closes its test with `echo "smoke-test: ok"; exit 0; }`
   — the `}` is the tail of a code line, and the block is full of `|| { echo FAIL; exit 1; }` one-liners.
   Neither "a bare `}`" nor "ends with `}`" can find that edge; net depth can.
2. **Shell-group braces only, quote-aware.** Counting every `{`/`}` never closes (`${1:-}`, awk programs,
   `[{]`). Skip double-quoted spans **first** — an apostrophe inside one (`"the bit's own contract"`,
   real, `mesh-egress-health:92`) otherwise flips a single-quote toggle and swallows the closing brace,
   which over-stripped that whole 648-line file to 1 line.
3. **A one-line construct opens nothing.** `--test) MODE=test ;;` is arg parsing;
   `if [ "$1" = --test ] || [ "$SANDBOX" = 1 ]; then LOCK=…; fi` is a sandbox knob. Both were read as
   openers, and since their terminator sits on the same line the "block" ran to the next unrelated
   `fi`/`;;` (this is what over-stripped `mesh-gpu-lid`, `mesh-turbo-lid`, `mesh-convexity`,
   `mesh-ss-clients`).

### Gate

Four new fixtures in the existing interpretant harness, each driving the **real** `um_body` /
`um_self_reads` / `umwelt_slug`, and each asserting **both** directions — the test half stripped *and* the
production half kept, so an over-stripping "fix" cannot pass by eating the file. `mesh-doctor --test`
green (rc 0).

**Old vs new, same four fixtures, side by side:**

| fixture | old `um_body` | new |
|---|---|---|
| brace-group block | **LEAK** (test read counted) | stripped |
| brace-group production write after it | kept | kept |
| MODE-dispatch block | stripped | stripped |
| sibling `--json)` parse arm | **SWALLOWED** | kept |
| one-line `if … --test …; fi` knob | **OVER-STRIPPED** | kept |
| apostrophe in a double-quoted string | kept | kept |

**Four mutants, each watched RED for its own reason:** drop the one-line guard · drop the double-quote
skip · drop the MODE opener · replace depth with a bare-`}` terminator. A fifth mutant (restore the
pre-fix `um_body` wholesale) is also RED but at an **earlier, flaky gate** (`run-stamp`,
`[[doctor-test-has-two-flaky-gates-that-eat-mutants]]`) — so the side-by-side table above is the evidence,
not that mutant.

## What the corrected scan says

Re-run with the fixed `um_body`: **14 multi-declarer artifacts, ZERO co-writers** — both apparent
mtime-blinding leads evaporated. The fix turned a 2-false-positive scan into a 0-false-positive one, which
is the sharpest evidence it was needed.

Two artifacts remain where **every declarer is a consumer** — `.op-home.state` (`mesh-arrivals`,
`mesh-motion-attribution`) and `.promises-state` (`mesh-promises`, `mesh-promises-watch`) — i.e. named by
readers while their writer declares a different slug or none. That is `a-self-describing-artifact-with-no-writer`
and it is exactly the case `--supersede`'s ownership heuristic silently resolves (`mesh-doctor:1554-1555`:
*"where a declarer's own name is the artifact's stem it wins; otherwise the first declarer stands"*).
**Lead, not a finding** — not chased here.

## Not claimed

- The `--supersede` co-declaration *report* (surfacing the collapsed declarers instead of picking a winner)
  is the natural next step of this concept and is **not** built. Only the prerequisite landed.
- The census figures are this date's answer on a live, growing corpus — the CLAIM is the gate; re-derive,
  never quote (`[[records-log-is-a-sliding-window]]` discipline).
