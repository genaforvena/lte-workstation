# the ask→answer funnel: one coordination instrument, two subjects — design

*2026-07-15. Operator ask: "i still would love to have self-tests if applicable. if it means
changing to some other benchmark - that's fine but there must be a benchmark for this for our
case (seems to be very close to 'real world')."*

**The answer to the operator's ask is: no benchmark.** The instinct that our case is "very close
to real world" is right, and it is the reason a benchmark is the wrong instrument rather than a
reason to shop for a better one. The mesh is already emitting the measurement. This spec defines
the instrument that reads it, and applies the same instrument to Alem — where it also turns out to
be the only coordination surface our budget can reach.

## The one idea

**Ask → wait → answered-or-expired.** A denominator you control (asks issued), a numerator you
observe (asks answered), and a clock that lets an ask die unanswered. That triple is what
coordination *is* when agents are asynchronous, and it is the only coordination shape both our
subjects actually exhibit at budgets we can afford.

Everything below is that one funnel, instantiated twice.

## Why not a benchmark

Every multi-agent LLM benchmark within reach — Alem/MA-Craftax-Coop, Melting Pot, Overcooked-AI,
Collab-Overcooked, TheAgentCompany — is **synchronous and simulated**. Alem's `evaluator.py:605`
blocks until all N agents return an action; coordination flows through Alem's own one-broadcast-
per-step channel at second scale.

The mesh is asynchronous, minute-scale, over a shared board, on real hardware. Plugging mesh minds
into a synchronous benchmark's agent slots does not measure the mesh: the board never gets used,
the async never happens, the minute scale never happens. You would measure *the benchmark's*
coordination protocol with our models inside it — which is exactly what `~/alem/BRIEF.md` already
warns against overselling.

Fitting the mesh to a benchmark means deleting the properties that make it the mesh, then
measuring what's left. A clean number about a system that isn't ours.

**A deployed system's self-test is not a benchmark.** It is instrumentation on the real thing, plus
fault injection for causality. That is what this spec builds.

## Findings that motivate it (all from data already on disk, zero new inference)

### Subject A — the mesh board (`~/.mesh/chat.log`, 3,002 lines, 2026-07-08 → 07-15)

| stage | count | rate |
|---|---|---|
| distinct tasks posted (`[task]`) | 160 | — |
| claimed (`[taking]`, by citation) | 18 | **11.2%** |
| finished (`[done]`, by citation) | 103 | **64.4%** |
| finished *without* ever being claimed | 86 | — |
| no citing marker at all | 57 | **unattributable — NOT dropped** |
| └ of those, discussed later without citation | 53 | — |
| └ of those, no later trace at all | **4** | **2.5%, and all <2.5 h old** |

Time-to-claim: **median 33 min, p90 3.1 h, max 4.2 h.** The BRIEF's "minute scale" is now measured
rather than asserted.

**The drop rate is not measurable, and is nowhere near 35%.** The first cut of this analysis read
the 57 uncited tasks as "35% dropped" and the operator — correctly, given the claim — called it
alarming. It was an artifact. 53 of the 57 are discussed later on the board with no parseable
citation, and the remaining 4 have *no later trace only because they are younger than the p90 claim
latency* (2.3 h, 1.7 h, 0.4 h, and one posted on the last board line). Upper bound on silent drops:
4/160, all explained by youth.

This is the `isp-health` lesson inverted — an empty log returned the ALL-CLEAR; **unparseable
markers returned a FALSE ALARM.** Both are the same bug: a measurement that reports confidently
about evidence it does not have.

Three readings:

1. **The claim protocol is vestigial.** 11% claimed vs 64% finished — minds skip `[taking]` and just
   do the work. The board's collision-avoidance is documented but not running; two minds taking the
   same task would be prevented by nothing.
2. **The board is a reporting surface more than a dispatch surface.** 186 of 325 `[done]`s answer no
   `[task]` at all. Most mesh work is not board-originated. Know this before claiming the board
   coordinates the mesh.
3. **The board cannot measure itself, and the measurement is the problem — not the coordination.**
   Task IDs are grepped out of prose; 8/26 `[taking]`s and 186/325 `[done]`s cite nothing parseable.
   64% is *attributable* completion, a floor rather than an estimate. **This defect is the finding**,
   and it is why Unit 1 precedes every pane and every reflex: a surfaced number this soft would have
   driven minds to chase 56 ghosts. One of the four fresh "silent" tasks is, without irony,
   `chat-review/mindblocked-5s-debounce-cries-wolf`.

### Subject B — Alem/Craftax (39 episodes already run)

**Every non-request coordination surface has an empty denominator: 9 total attempts across all 39
episodes.** Sync blocks, handovers, elite mobs, diamond crafting all sit behind a tech tree a squad
that hasn't made a wood pickaxe in 100 steps never reaches. `Coord% = 0.00` is therefore not the
team failing to coordinate — it is the team never being *offered* the chance. Not a measurement of
failure; the absence of a measurement.

One surface needs no tech tree and is live from step 0 — the request/give protocol, 10 of the 55
actions (`Request Food|Drink|Wood|Stone|Iron|Coal|Diamond|Ruby|Sapphire`, `Give`):

| stage | count | rate |
|---|---|---|
| requests issued | 2,083 | — |
| any give attempted | 55 | **2.6%** — does anyone answer at all |
| give actually landed | 13 | **24% of gives** — did the answer hit a live, type-matching request |
| end-to-end fulfilled | 13 | **0.62%** |

The env implements the full primitive natively (`alem_state.py:140-200`): `request_duration` is a
live state that **expires**, `request_type` must match, and `Give` only resolves if
`other_player_is_requesting`. Ask → wait → answered-or-expired, with a clock. The same triple as
the board.

## The instrument

Three rates, because the failure modes are genuinely different and the end-to-end number hides them:

- **answer rate** = answers attempted / asks issued — *does anyone respond*
- **targeting accuracy** = answers landed / answers attempted — *does the response hit a live ask*
- **fulfilment** = answers landed / asks issued — *end to end*

gemma-4-E2B is why the split is mandatory: 46 gives, 7 landed. It answers, and misses. Invisible in
fulfilment, obvious in the split.

| | Subject A (mesh board) | Subject B (Alem) |
|---|---|---|
| ask | `[task]` post | `Request <material>` |
| answer | `[taking]` / `[done]` | `Give` |
| landed | done, citing the task | `request_received_count` |
| expired | never claimed nor done | `request_expiry_count` |
| clock | wall time to claim | `request_duration` ticks |

### Validity gates — mandatory, both learned the hard way

**Spam gate.** Report asks-per-unit-work alongside every rate
(`Cooperation/requests_per_100_actionable_agent_steps`; for the board, `[task]`s per active hour). A
subject that re-issues the same ask every step inflates the denominator *and* silently deflates
expiries — the ask never sits still long enough to time out. Live proof: qwen2.5-0.5b constrained,
**1,125 asks, 4 expiries, 0 answered**. **`request_expiry_count` is unusable raw** and the analyzer
must refuse to print it ungated.

**Empty-denominator gate.** If `Coordination/total_attempts ≈ 0`, do not report sync/handover/craft/
elite rates **at all** — not as zero. A rate over an empty denominator is not a result. This
generalizes the BRIEF's existing "never report 3/93 as a result" lesson from a remembered anecdote
into a mechanical rule the code enforces.

### What it can and cannot claim

**Can:** *this subject was asked N times and answered A of them, within T.* A throughput fact about
the ask→answer loop, with a denominator that is actually full.

**Cannot (Subject B, today):** anything about coordination being hard. At 0.5b–3b this is still the
format/competence floor wearing a coordination costume — "can a small model operate a give protocol"
is not "is coordination difficult." Same discipline the BRIEF applies to achievement%. The
instrument is valid; these models are not the subjects it is for.

**Cannot (Subject A, ever, without Unit 3):** causality. 64% completion does not prove the board
caused it — minds might have done that work anyway, and the week cannot be rerun without the board.
Observational until a canary exists.

## Units

### Unit 1 — explicit task IDs (the enabling fix)

`mesh-chat`'s own header already argues this, for a different field:

> *The addressee is an EXPLICIT field (`--to <tgt>`), NOT grepped from prose — so "is the @tag real?"
> never arises; we just validate `<tgt>` against the live registry AT SEND TIME. Unknown target →
> ERROR naming who DOES exist, and NOTHING is posted.*

Task IDs get the identical discipline, and currently don't. `[task]` mints an ID; `[taking]`/`[done]`
must cite one; the citation is validated against open tasks **at send time**; an unknown ID errors,
names the open tasks, and posts nothing. Same fail-fast idiom, same reason, one field over.

Consistent with existing marker doctrine: anchored at body start (memory
`board-marker-grep-must-anchor-to-body`).

*Why first:* until markers are machine-readable, every number in this spec stays a heuristic. This
is the cheapest change with the largest effect on measurability, and it makes the funnel exact and
continuous forever after.

### Unit 2 — the resolution axis in `mesh-witness` (a surgical extension, not a new tool)

Witness is already "the mesh measuring itself... a continuous ledger of its own vital signs," and it
already reads the board log. But it only measures **throughput**: `board1h` (line volume),
`board_age_s` (pulse), `board_posters` (distinct posters/1h). Its own docstring (`:182-191`) already
warns against reading "stigmergic" as praise and notes these answer density, not resolution.

**A board can be maximally busy and coordinate nothing.** `board1h=33` says the board is loud. No
metric says whether an ask is ever answered. That is the axis the funnel adds, and witness is its
home — no new tool, no new store, same ledger.

New scalars, obeying witness's existing cost discipline (computed in `--measure` on the `*/2` reflex
cadence; the pane only tails):

- `ask_open` — `[task]`s posted with no later trace of their slug, **excluding those younger than
  the measured p90 claim latency**. An ask in flight is not an ask dropped.
- `ask_stale_h` — age of the oldest such ask. This is the scalar a reflex fires on.
- `ask_resolve` — attributable answers / asks posted. A **floor**, not an estimate, and labelled so.

**Witness's honest-fusion rule is what makes this safe, and it is not optional here:** *"A source
that is missing/unreadable renders UNKNOWN for that metric — never a faked reading."* An uncited
`[task]` is **UNKNOWN, never `dropped`.** That rule, already written, forbids the exact 35% false
alarm this spec's first draft produced. Until Unit 1 lands, `ask_resolve` renders as a floor with its
unattributable count shown beside it — a true statement that creates pressure to fix the markers,
rather than a scary one that sends minds chasing ghosts.

Ground truth is the marker lines themselves — never mtime order, never a derived cache (the BRIEF's
aggregator lesson: a path that never existed returned zero rows, silently). Print the denominator
beside every rate; refuse to print a rate whose denominator is empty. The gates are the instrument's
job, not the reader's.

### Unit 3 — the stall reflex (what the operator actually asked for)

*Operator: "incorporate this sort of data into witness or chat pane so that reflexes would drive
them to resolve these processes issues we have."*

The reflex fires on `ask_stale_h` **exceeding the measured p90 claim latency (3.1 h)** — not on a
fixed guess, and not on a raw open-count. Calibration against the real corpus is doctrine here
(`tone`'s median IS its max; a rule keyed on an assumed range is a constant). An ask still inside
p90 is behaving normally; an ask past it has genuinely stalled, and *that* is a process issue worth
a mind's attention.

**Sequencing is a hard constraint, not a preference.** This reflex cannot precede Unit 1. A reflex
built on today's markers would have nagged about 56 phantom drops — and the mesh has this exact
failure class open on the board right now (`chat-review/mindblocked-5s-debounce-cries-wolf`). A gate
you have not seen fail is not a gate; a gate you have seen fire *falsely* is worse than none,
because it teaches minds to ignore the pane.

### Unit 4 — the board canary (causality; deferred until Units 1–3 land)

Inject a synthetic `[task]` with known properties; measure whether and when it is claimed. A
controlled experiment on the real system — the standard instrument for deployed distributed
systems, where benchmarks don't apply.

**Deferred deliberately, and not only for sequencing.** A canary spends real mind-effort on
non-work. Injected too often, or too plausibly, minds learn the board carries fake asks — and the
instrument corrodes the thing it measures. Needs a rate ceiling and an honesty rule (a canary must
be *recognizable as such after the fact*) before it runs. Design it once Unit 2 says what the
baseline is.

## Alem side — the two write-ups

**Into PR #8's body (on-topic, 2 sentences):** the request funnel independently confirms the
degeneracy caveat already written there. Constrained qwen2.5-0.5b: **1,125 asks, 0 answered.** A
sharper statement of "valid but degenerate" than the action histogram, from a second instrument.

**NOT into PR #8 — its own upstream issue:** `total_attempts = 9 / 39 episodes`. This is not a claim
about constrained decoding; it is a claim that *the benchmark's coordination metrics are
unmeasurable at short budgets*. Burying it in a decoding PR is scope creep and the wrong venue for
a confrontational finding to be argued on its merits. File separately, or hold. Operator's call.

## Out of scope

- **Running any coding-plan CLI as benchmark inference.** The BRIEF's dead-end ruling on zai — *"a
  coding plan carries no PAYG API credits; its coding endpoint is out of scope — don't route around
  it"* — is about the shape of the thing, not the vendor. A Claude Code subscription is the same
  shape. Swapping vendors is routing around it.
- **A mesh leaderboard row.** Not comparable to anything, and the BRIEF's framing (harness
  contribution, not vanity row) already rules it out.
- **Adapting the mesh to a synchronous benchmark.** See "Why not a benchmark."
