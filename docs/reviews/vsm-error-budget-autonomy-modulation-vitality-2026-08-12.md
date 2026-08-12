# CASE Layer-4 — the error budget that modulates autonomy: the mesh throttles on cost and heat, never on being wrong

**Live literature review · 2026-08-12 · management cybernetics / VSM applied to agentic AI → self-production metrics**
Landed: `scripts/mesh-vitality` (`error_budget()`, config block `EB_*`, new `error-budget=` field in the
vitality report line). Report-only — nothing gates on it yet, by design.

## The source

**Srinivas Telukunta, Georgios Nektarios Lilis & Lucio Baron, "The CASE Framework: A Multi-Disciplinary
Control Architecture for Governing Enterprise Agentic AI", arXiv:2608.10153 (10 Aug 2026)** —
<https://arxiv.org/abs/2608.10153>. Found by live search for current VSM/management-cybernetics work with
an *operational* mechanism (the standing instruction for this lane); read via the arXiv HTML full text.

CASE is not a VSM paper wearing new clothes — it assigns four **different** governing disciplines to four
scales of autonomous AI (L1 control theory / L2 complex-adaptive systems / L3 supervisory cybernetics /
L4 engineering operations) and imports Beer wholesale into L3: recursion, the **algedonic bypass**, Ashby's
requisite variety as an enforced inequality (`V_human × G ≥ V_agents` at peak load). That much the mesh
already has — `mesh-algedonic` is the algedonic channel with its own alarm-fatigue defense, and
`mesh-vitality channel_variety` is the variety read.

## What we do NOT have: Eq. 6 and Eq. 7

The L4 pair is the gap:

> **Eq. 6** `B = (1 − SLO) × N_decisions` — an **error budget**, denominated in *allowed bad decisions*,
> counting hallucinations, scope violations, policy breaches, cost overruns.
> **Eq. 7** `a(t) = g(B_remaining(t))` — **autonomy modulation**: expand autonomous scope while the budget
> is healthy, contract toward review as it depletes.

And the reason to want it here is CASE's cross-layer finding, which describes this mesh precisely:

> **the zero-touch deployment paradox** — "the better an organization's Layer 4, the faster it outruns a
> static Layer 3: deployment excellence mechanically manufactures the variety that oversight must absorb."

`mesh-land` + `mesh-autowire` are exactly that deployment excellence: tools land and self-wire into cron
unattended. Meanwhile **every throttle the mesh owns answers a different question**:

| throttle | axis | what it can see |
|---|---|---|
| `mesh-pace` / `mesh-spend` | **dollars** | spend hold, hard cap |
| `mesh-load` / `mesh-resource-guard` | **CPU / thermal load** | shed under saturation |
| `mesh-mode` | posture | declared operating mode |
| — | **defect rate** | *nothing* |

Grepped mesh-wide 2026-08-12 (`error.budget|error_budget|\bSLO\b|autonomy.modulat` over `scripts/` +
`docs/`): **zero hits**. A stretch of bad landings costs the mesh nothing in autonomous scope, as long as
it stays cheap and cool. `mesh-vitality` already *reports* `verify_fails` and even tags a `FAIL_JUMP`
regression — but that is a line in a report, wired to no consequence and to no notion of how many failures
this much production is *allowed*.

**Not the gap, deliberately:** CASE's L2 mechanisms — cascade branching factor `k<1`, avalanche-size
distribution monitoring for drift toward criticality — are already embodied. `mesh-criticality` reads the
branching parameter and the avalanche *shape* off the board (Beggs & Plenz lineage). Re-landing those
would be the duplicate this lane's coverage memory exists to prevent.

## What landed

`error_budget()` in `scripts/mesh-vitality`, over an `EB_WIN_H`-hour window (default 72):

- **decisions** `N` = commits landed in the genome — the mesh's autonomous production decisions;
- **errors** = revert/rollback commits in the same window (`rv`) + `[chat-review]` defect posts on the
  board (`cr`) — the mesh charging itself for work it had to undo or that another window flagged as defective;
- `B = (1 − EB_SLO) × N` (default SLO 0.90), `rem = (B − err)/B`;
- tier: `rem ≥ EB_HI` → **FULL** · `≥ EB_LO` → **NARROWED** · below → **REVIEW** (budget spent — the honest
  response is to contract scope toward verification, not to ship faster).

Report-only, same posture as every other lens in that file: a control law must be *watched across windows*
before anything is allowed to gate on it, and the classifier that would eventually gate is the one printed.

**Live first reading** (2026-08-12T17:28Z): `REVIEW(rem=0.00,err=2[rv=0,cr=2],B=2.0,N=20)` — 20 commits in
72h buy a budget of exactly 2 bad decisions, and 2 `[chat-review]` defects spend it to the cent. Widen to
14 days and it reads `FULL(rem=0.67,err=5[rv=0,cr=5],B=15.2,N=152)`.

## Honest caveats (stated because the number reads more precise than it is)

1. **Window-sensitive by construction.** The same mesh reads REVIEW at 72h and FULL at 14d — not a
   contradiction, but the direct consequence of `B` scaling with `N`. At small `N` the budget is ~2 bad
   decisions and a single bad day pins it. **Read the trend, never one frame.** This is the axis's main
   weakness and the reason it ships report-only.
2. **Both terms are windowed FLOWS, not per-commit attribution.** A `[chat-review]` raised today may
   indict work from weeks ago. This is a defect *rate* in CASE's sense, never a per-decision verdict.
3. **`verify_fails` is deliberately excluded.** It is a point-in-time **stock** of currently-failing tools;
   adding a stock to a flow is the error `channel_variety`'s own header warns about.
4. **Below `EB_FLOOR` decisions it says `INSUFFICIENT`** rather than rendering a flattering FULL off an N
   of two.

## The gate, and the bug it caught

The `--test` gate asserts the **numbers**, not the format: clean 20-commit repo → `FULL(rem=1.00,err=0)`;
+1 revert → `NARROWED`; +3 reverts → `REVIEW` with `rem<0`; and a board `[chat-review]` charged *exactly*
like a revert (`cr=3`). Seen RED twice:

- **mutant "reverts not charged"** (`code_err = 0`) → half fixture renders `FULL(rem=1.00,err=0)` → FAIL.
- **mutant "payload never reaches python"** → `INSUFFICIENT(N=0<8)` → FAIL.

That second mutant is not hypothetical — it is **the bug this function actually shipped with for its first
draft**. The commit subjects were piped into `python3 - <<'PYEOF'`, where the heredoc *is* stdin and had
already been spent on the program text, so `sys.stdin.read()` returned nothing and a repo with 20 commits
in the window rendered a calm `INSUFFICIENT(N=0)`. A format check passes that. A "does it print a label"
check passes that. Only asserting `N=20` catches it. The payload now goes through a file.

Classification also rounds **before** comparing, so the tier is decided on the value that is printed — and
that same rounding removes the float `-0.00` render of an exactly-spent budget.

## What this does not claim

It does not claim the mesh should *now* contract its own autonomy on this number — one live frame at
`rem=0.00` on `N=20` is exactly the fragile reading caveat 1 describes. It claims the mesh had **no axis at
all** on which being repeatedly wrong could cost it scope, and now it has one, instrumented and watchable.
Whether `a(t)` ever becomes a real gate (the obvious hook is `mesh-dispatch`, next to the pace hold) is a
decision for the operator after several windows of trend, not for the review that proposed it.

## Related

`docs/reviews/vsm-power-relations-agenda-concentration-vitality-2026-07-31.md` ·
`docs/reviews/vsm-pii2-institutional-schizophrenia-card-2026-08-04.md` ·
`docs/reviews/vsm-s3-s4-homeostat-headless-chicken-2026-07-28.md` · `scripts/mesh-criticality` (the L2
branching/avalanche coverage this review deliberately did not re-land).
