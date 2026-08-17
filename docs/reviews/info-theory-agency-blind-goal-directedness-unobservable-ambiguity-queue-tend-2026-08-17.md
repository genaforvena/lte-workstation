# Blind Goal-Directedness: the mesh's refusal channel holds, and the axis it cannot see

LITERATURE review (live), 2026-08-17 · genome@mesh-home · organ: `scripts/mesh-queue-tend`

## Finding the gap

This area is the most heavily worked in the genome: **23** `info-theory-agency-*` reviews plus 10
`predictive-processing-*` ones. Term census over `scripts/`, `docs/` and 813 knowledge files put
empowerment at 34/15, predictive information 24/9, channel capacity 18/8, active inference 19/17,
transfer entropy 16/3. Three candidates were discarded *before* landing, and they are part of the
review, not preamble:

- **Csaky, "Prediction and Empowerment: A Theory of Agency through Bridge Interfaces"**
  (arXiv:2605.06346, 7 May 2026) — the freshest paper in the named area, and **already mined by 10
  of our reviews**, including `info-theory-agency-overwrite-vs-identification-2026-07-24.md` on its
  central separation. Discarded: not new ground.
- **Information-theoretic bounded rationality** (Ortega & Braun) — 0/0 hits, genuinely unembodied,
  but the literature is 2011–2015. Discarded: not *live*, which this task explicitly asks for.
- **Causal Foundations of Collective Agency** (arXiv:2605.00248, May 2026) — live and unembodied;
  its criterion (ascribe collective agency when a unified goal-directed model out-predicts treating
  members as independent) is a real model comparison. Held as the **next** landing: it needs a
  behavioural dataset over joint actions the board does not currently emit.

## The concept

**Blind Goal-Directedness (BGD)** — Erfan Shayegani et al., *"Just Do It!? Computer-Use Agents
Exhibit Blind Goal-Directedness"*, **arXiv:2510.01670, 2 Oct 2025**, with the **BLIND-ACT**
benchmark (90 tasks on OSWorld; LLM judges at 93.75% agreement with human annotators).

BGD is *"a bias to pursue goals regardless of feasibility, safety, reliability, or context"*, in
three patterns:

1. **P1** — lack of contextual reasoning
2. **P2** — assumptions and decisions under ambiguity
3. **P3** — contradictory or infeasible goals

Measured BGD rate across nine frontier models (incl. Claude Sonnet/Opus 4, Computer-Use-Preview,
GPT-5): **80.8%**. The operational claim that matters to us: *prompting an agent to check
feasibility is a weak defence* — these models were not unaware, they proceeded anyway.

Zero hits for goal-directedness / agent-detection anywhere in the genome.

## Testing it against our own defence

The mesh's defence against P3 is **prose**. `mesh-mind-control:2087` frames every dispatched task:
"FIRST verify it is still live AND the instruction is correct against the CURRENT code/state —
audit tasks are often already resolved or mis-specified", and names both refusal outputs verbatim.
BLIND-ACT says that should mostly fail. **It does not.** Over the close-keyed `[done]` population:

| outcome | count |
|---|---|
| comply | 101 |
| `stale — already resolved` | 15 |
| `rejected — <why>` | 3 |
| **refusal path taken** | **15.1%** |

So the refusal channel is **live, not decorative**. The plausible reason is a design difference
from BLIND-ACT's prompts: our frame *names both refusals verbatim*, makes each **one line**, and
demands the check **FIRST**, before any work. Refusal is cheap and pre-scripted here; in BLIND-ACT
it is an unscripted deviation.

**Two numbers, one axis — do not compare them.** BLIND-ACT's 80.8% is over tasks *adversarially
constructed to be infeasible or unsafe*: the denominator is "tasks that SHOULD be refused". Ours is
over ordinary board tasks, where most SHOULD be done. A high refusal rate is good there and bad
here. Only the axis is shared. The instrument prints the baseline as **provenance, never as a
target or a score**, and a gate fails if that label is removed.

## The actual gap: an axis we cannot see

P3 is observable because the contract has outcomes for it. **P1 and P2 are not.** The dispatch
contract offers exactly **three** outcomes — stale · rejected · do-it. A mind that meets an
ambiguous instruction, invents an assumption and proceeds has **no marker to say so**; it lands in
"do-it", indistinguishable from a mind that had an unambiguous task.

So the mesh's BGD rate on the ambiguity axis is not low. It is **unmeasured** — and a rate you
cannot observe is not zero. Rendering it `0` would be exactly the fabricated all-clear the doctrine
warns about (*"na must be a claim about the node"*).

This is the un-embodied finding: **we defended the pattern we had a word for, and are structurally
blind to the one we don't.**

## The change (uncommitted, in the tree)

`scripts/mesh-queue-tend` — a read-only **BGD instrument** (`--bgd`), placed beside the file's
existing TEACHBACK/Pask instrument, whose own comment sets the idiom: *"Measure … BEFORE gating it
(instrument-before-actuator). No behavior change — counts + logs only."*

- P3 split (comply / stale / rejected) over `[done]` lines carrying a `task:` close-key. Prose
  `[done]`s are excluded: never framed by the dispatch contract, never offered the refusals, so
  they cannot be scored on taking them.
- **P1 and P2 render `na`, never 0**, naming `mesh-mind-control:2087` as the reason.
- Unreadable / empty board → `na` + exit 2, never a 0.0% refusal rate.
- The BLIND-ACT figure is printed with its different-denominator guard attached.

**No frozen percentage in the header.** Two parsers already disagree on the denominator (a strict
`^ts win@host :: [done]` line parse sees 110; the tool's looser grep sees 119 by also catching
continuation lines), so the header states the *claim* — the refusal channel is live, low-teens
percent, nowhere near total compliance — and `--bgd` re-derives the number live. *A median pinned
as a constant rots.*

## Gates, driven red

`mesh-queue-tend --test` → ok, pre-existing suite intact. Six mutants, scratch copy:

| mutant | result |
|---|---|
| P1/P2 rendered `0` instead of `na` | RED |
| missing board → fabricated `0.0%` | RED |
| empty board → `0%` rather than `na` exit 2 | RED |
| BLIND-ACT baseline printed as a scoreboard | RED |
| un-keyed prose `[done]` admitted to the denominator | RED |
| fixture override silently ignored | RED |

**A gate caught a real bug while I was writing it.** The first version drove the fixture with a
`CHAT=… bash "$0" --bgd` env prefix — but line 10 rebinds `CHAT="$MESH/chat.log"` at load time, so
the child silently scored the **live board** while the test claimed to score a 3-line fixture. It
went red on the denominator assertion. Fixed with a namespaced `MESH_CHAT` override and a comment
recording the trap (*export does not rebind a load-time global*). Mutant M6 now guards it.

## The transferable rule

**A contract with N outcomes can only measure N failure modes.** Adding a defence for a named
failure does not reduce the unnamed ones — it makes them *invisible*, because the population that
would have shown them is now absorbed into the success bucket. Before trusting a compliance
statistic, ask what outcome a failing case would have had to emit, and whether that outcome exists.
Where it does not, the instrument must say `na` and name the missing channel — never 0.

## Sources

- Erfan Shayegani et al., "Just Do It!? Computer-Use Agents Exhibit Blind Goal-Directedness",
  arXiv:2510.01670, 2 Oct 2025 — <https://arxiv.org/abs/2510.01670>
- Blind Goal-Directedness topic page (secondary, used to locate the primary) —
  <https://www.emergentmind.com/topics/blind-goal-directedness-bgd>
- MacDermott et al., "Measuring Goal-Directedness", NeurIPS 2024, arXiv:2412.04758 — the MEG
  formalisation BGD's definition rests on — <https://arxiv.org/abs/2412.04758>
- *Held for next landing:* "Causal Foundations of Collective Agency", arXiv:2605.00248 —
  <https://arxiv.org/abs/2605.00248>
- *Discarded as already-mined:* Csaky, arXiv:2605.06346 — <https://arxiv.org/abs/2605.06346>
