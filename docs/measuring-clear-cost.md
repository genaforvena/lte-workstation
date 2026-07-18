# Measuring what a `/clear` costs — without a judge model

*Draft (pub). Methodology essay. The measured cost figures are gated on a shadow-week
ledger that has not filled yet; every number-carrying claim below is marked **[GATED]**
and must not ship until `~/.mesh/clear-loss.log` has real rows.*

## The problem

Long-running coding agents (Claude Code, the Ralph loop, any "clear-after-every-stop"
driver) periodically drop their context and carry work forward through a **handoff** — a
short written snapshot of "what's done / what's next / key paths," restored into the fresh
session. The bet is that the handoff is a lossless-enough compression of the turn: clear,
restore, keep going.

The obvious way to check that bet is a **shadow mode** — run the clear machinery without
acting on it, and confirm the plumbing fires. Shadow mode is necessary and it is not
enough. Worse, it *lies about loss*, and it lies in a specific, seductive way.

## Why "coverage" is near-tautological

The tempting liveness check is: *did the handoff cover the scrollback?* Ask a small model
"does this handoff capture what happened in this pane?" and gate on yes.

The trap: **the handoff is extracted _from_ the scrollback.** It is a summary of the very
text you are asking it to cover. So the coverage question is close to "is this summary a
summary of the thing it summarized," and a cooperative model almost always says yes. A gate
that nearly always passes is not measuring anything — it is a green light wired to the
wall. (This is the same family as a self-grepping test that asserts its own source line:
the check can't fail, so it certifies nothing.)

Coverage answers *"is the handoff plausibly about the turn?"* The question that actually
matters is different and sharper.

## The real question is a serialization round-trip

Clearing is a **serialize → drop → deserialize** step. The failure mode is not "the handoff
is off-topic." It is: **a mid-turn discovery — a constraint the mind established in step 1
that step 2's correct answer depends on — does not survive the round-trip.** The mind
learned "the port is 8022, not the default 22" at 11:04, cleared at 11:30, and at 11:31
confidently uses 22 because the handoff mentioned "SSH to the phone" but not the number.

You cannot detect that by grading the *handoff*. You detect it by grading **step 2's
behavior against a ground truth planted in step 1** — and here you can escape the judge
model entirely.

## The meter: two arms, a real predicate, no judge in the scoring path

`mesh-clear-loss --canary` runs canaries. Each canary:

1. **Plants a constraint `C` in step 1** — e.g. "use port 8022 for this host." Step 1's
   output establishes it.
2. **Runs step 2**, whose *correct* answer must honor `C` **without step 2 restating it**
   (step 2 asks "now SSH in and grab the battery" — a correct answer uses 8022; it does not
   re-announce the port).
3. **Verifies step 2's output with a real predicate** — a `violation_regex` / concrete check
   that encodes `C`. Reality grades it. **No LLM sits in the scoring path**, so the score
   cannot be flattered by the same cooperativeness that made coverage tautological.

Every canary runs on **two arms, always both**:

- **recycled arm** — run step 1 → extract a handoff (the *real* extractor, `mesh-clear`'s
  `_extract_handoff`, sourced verbatim — one extractive path, not a forked copy) → **discard
  the step-1 context** → restore the handoff only → run step 2 → verify.
- **control arm** — identical, but **no clear** between step 1 and step 2 (full context
  retained) → verify.

## The number that means something is a *difference*

```
cost(task_type) = failrate_recycled − failrate_control
```

The control arm is the point. A mind flunks some canaries with **no clear at all** — the
task was ambiguous, or it just forgot. That baseline is not a clearing cost; charging it to
`/clear` would inflate the meter. Subtracting the control isolates **the loss attributable
to the round-trip**, denominated in *dropped directives* rather than vibes.

Because the **same reasoner runs both arms**, the differential is meaningful even when the
absolute failure rate is reasoner-dependent — a weak stand-in reasoner fails more on both
arms, and the *gap* between them is still the quantity of interest. (A v2 routes the two arms
to real mind panes instead of a stand-in.)

## Why this is the honest instrument

- **Judge-free scoring.** The grade is a predicate over step-2 output, not a model's opinion.
  The one place a model *could* creep in — coverage — is exactly the place we removed,
  because that is where the tautology lived.
- **A differential, not an absolute.** The control arm subtracts the no-clear baseline, so
  the figure is "extra failures caused by clearing," not "failures."
- **The gate has been seen to fail.** `--test` is RED-first: pure-verify + arm-wiring +
  a **known-dropped calibration** — a canary whose constraint is deliberately absent from the
  handoff *must* fail on the recycled arm and pass on the control. A meter that cannot detect
  loss when loss is present is not a meter; the calibration proves it can.

## What is NOT yet claimed — **[GATED]**

The methodology above stands on its own. The following require a filled ledger and are held:

- **[GATED]** the measured `cost(task_type)` figures — the ledger
  (`~/.mesh/clear-loss.log`) is empty at time of writing; no shadow-week rows yet.
- **[GATED]** any claim of the form "clearing costs X% of mid-turn discoveries" or "task-type
  T is safe / unsafe to clear."
- **[GATED]** comparison against the Ralph loop's own clear cadence.

When the ledger fills, this draft graduates from *methodology* to *result* — and the result
section cites `mesh-clear-loss --report` output directly, not a remembered number.

---

*Tooling: `mesh-clear-loss` (`scripts/mesh-clear-loss`, commits `74c5ad8` / `350e324`).
Related: `mesh-clear` (the gated `/clear`), `mesh-handoff` (the durable snapshot restored by
the SessionStart hook). Audience: agent-engineering / long-running-loop practitioners.*
