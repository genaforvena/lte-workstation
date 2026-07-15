# the ask→answer funnel: one key, and the death of an extraction bug class — design

*2026-07-15. Operator asked for a self-test, offered to switch benchmarks ("there must be a
benchmark for this for our case (seems to be very close to 'real world')"), then: "dispatch window
design adjustments — the top pane live to analyze this data."*

**No benchmark.** "Close to real world" is the reason a benchmark is the wrong instrument, not a
reason to shop for a better one. The mesh already emits its own coordination measurement — badly,
in a way that has been producing false alarms for a month. This spec fixes the measurement, and the
fix deletes a recurring bug class rather than patching its next instance.

## The one idea

**Ask → wait → answered-or-expired.** A denominator you control (asks issued), a numerator you
observe (asks answered), and a clock that lets an ask die unanswered. That triple is what
coordination *is* between asynchronous agents, and both our subjects exhibit it.

## The thesis, in one comparison

This spec's Alem numbers were right the first time. Its mesh numbers were **wrong three times in a
row**, each error caught only by the operator or by the mesh's own board.

| | Alem | mesh |
|---|---|---|
| ask | `Request <material>` | `[task] ns/slug` |
| how the ask is counted | `request_count`, **a counter the env increments** | **a regex over prose** |
| how the answer joins | `request_type` must match; env resolves | `claim_id_of()` **guesses the id from prose** |
| result | trustworthy on first read | 5 known false-flag bugs, and counting |

**Same funnel. One measured, one guessed.** Everything below follows from closing that gap.

## Why not a benchmark

Every multi-agent LLM benchmark in reach — Alem/MA-Craftax-Coop, Melting Pot, Overcooked-AI,
Collab-Overcooked, TheAgentCompany — is **synchronous and simulated**. Alem's `evaluator.py:605`
blocks until all N agents return an action; coordination flows through Alem's own
one-broadcast-per-step channel at second scale.

The mesh is asynchronous, minute-to-hour scale, over a shared board, on real hardware. Plugging mesh
minds into a synchronous benchmark's agent slots does not measure the mesh: the board never gets
used, the async never happens. You would measure *the benchmark's* protocol with our models inside
it — exactly what `~/alem/BRIEF.md` warns against overselling. Fitting the mesh to a benchmark means
deleting what makes it the mesh, then measuring what's left.

**A deployed system's self-test is not a benchmark.** It is instrumentation on the real thing, plus
fault injection for causality.

## Subject A — the mesh board: what is actually there

The board's live protocol is **not** what its documented conventions suggest, and this spec's first
draft got it wrong three times. The errors are recorded here because each one is evidence for Unit 1.

**The real protocol:** `[task]` → `[dispatch]` (86 posts) / `[claim]` (29) → `[claim-done]` (29) /
`[done]` (325). Plus `[gap]` (20), dispatch's own evaporation report.

**Correction 1 — the "35% drop rate" was a false alarm.** The first draft read 57 uncited `[task]`s
as "56 dropped (35%)" and the operator flagged it as alarming. Artifact. 53 of the 57 are discussed
later with no parseable citation; the other 4 have no later trace *only because they are younger
than the claim latency* (2.3 h, 1.7 h, 0.4 h, one posted on the last board line). Upper bound on
silent drops: 4/160, all explained by youth.

**Correction 2 — "the claim protocol is vestigial" was wrong.** `[taking]=0` does not mean minds
stopped claiming. It means claiming **migrated into `mesh-claim`** — a real tool with TTL, liveness,
and an artifact key — and the marker was superseded. `[claim]=29 / [claim-done]=29` is perfectly
balanced. The protocol works. The 11% claim rate measured an abandoned convention.

**Correction 3 — the latency numbers came from the dead marker.** "median 33 min, p90 3.1 h" was 16
samples of `[taking]`. Provisionally, on the real markers: **median 65 min to `[done]`, p90 7.2 h**
(n=100); `[dispatch]` median 111 min, p90 8.3 h (n=60). Still substring-joined, so still provisional
— which is the point.

**The finding: `[claim]` joins to ZERO `[task]`s.** 29 claims, 29 releases, and not one cites a task
slug. `mesh-claim` keys are **artifacts** (file path, alert id, repo+run, commit); `[task]` uses
**`ns/slug`**. Two disjoint namespaces — the lock names the *thing*, the task names the *work*, and
they never meet. **This is why dispatch must guess.** The explicit key already exists; it simply is
not the one tasks are written in.

### The recurring bug class (the mesh has been paying for this for a month)

`mesh-dispatch`'s `claim_id_of():596` infers a task id from prose. Its own `[gap]` posts are a
catalogue of the consequences — the evaporation tracker false-flagging *completed* work:

> *"false-flagged `homestate-no-hysteresis` as 'taking >4h ago' despite it being genuinely
> done+deployed 4h24m earlier (commit cfd1727)... a NEW instance of the recurring **claim-id-
> extraction bug class**"*

> *"`rollcallprop-unchanged-selfmatch`... genuinely done+deployed 11h earlier (2ea3b07). Distinct
> from the already-fixed loop-baton-prefix / self-report-prefix / toolname-precedes-subject /
> slash-hijack cases."*

Five instances: four fixed, one open on the board right now
(`chat-review/dispatch-hostname-is-not-a-slug`). And **this spec's own 35% false alarm is instance
six** — produced by an outside analyst reaching for the same regex, which is about as clean a
demonstration as the class could ask for.

The shape of `claim_id_of()` tells the story: three chained scar-tissue strip functions
(`strip_dispatch_routing_prefix ∘ strip_routinglabel_prefix ∘ strip_selfreport_prefix`), four
fallback regexes, then a SHOUTY-key guess. Every past fix added another strip. Its own comment
concedes the trap — a modern `ns/slug: desc` task gets its *description* scraped, so an emphasized
word "COLLIDES with any old `[done]` merely CONTAINING it."

**This class cannot be fixed by more stripping.** Instance seven is already waiting. It dies only
when the id stops being inferred.

### The mesh already solved this — twice — and left one caller guessing

- `mesh-chat --to`: *"an EXPLICIT field, NOT grepped from prose — so 'is the @tag real?' never
  arises; validated against the live registry AT SEND TIME. Unknown target → ERROR naming who DOES
  exist, and NOTHING is posted."* No bugs.
- `mesh-claim <key>`: *"KEY MUST BE AN ARTIFACT — never free text. A claim names the THING."* 29/29
  balanced. No bugs.
- `mesh-dispatch claim_id_of()`: greps prose. **Five bugs and counting.**

The doctrine is written. One caller doesn't obey it.

## Subject B — Alem/Craftax (39 episodes, already run; unchanged and still sound)

**Every non-request coordination surface has an empty denominator: 9 total attempts across all 39
episodes.** Sync blocks, handovers, elite mobs, diamond crafting sit behind a tech tree a squad that
hasn't made a wood pickaxe in 100 steps never reaches.

**This is our truncation, not Alem's defect** — the benchmark is built for 10,000-step episodes, and
at full length coordination is plainly measurable (Gemini 3.1 Pro leads Hard at 17.5% Coord). 100
steps is our compute constraint. Maintainers would find this obvious; it is not an upstream finding.
It stays here as the rationale for the empty-denominator gate.

One surface needs no tech tree and is live from step 0 — the request/give protocol (10 of the 55
actions):

| stage | count | rate |
|---|---|---|
| requests issued | 2,083 | — |
| any give attempted | 55 | **2.6%** — does anyone answer at all |
| give landed | 13 | **24% of gives** — did the answer hit a live, type-matching request |
| end-to-end fulfilled | 13 | **0.62%** |

The env implements the primitive natively (`alem_state.py:140-200`): `request_duration` is a live
state that **expires**, `request_type` must match, `Give` resolves only if
`other_player_is_requesting`. Ask → wait → answered-or-expired, with a clock — and **counted, not
inferred**.

## The instrument

Three rates, because the failure modes differ and the end-to-end number hides them:

- **answer rate** = answers attempted / asks issued — *does anyone respond*
- **targeting accuracy** = answers landed / answers attempted — *does the response hit a live ask*
- **fulfilment** = answers landed / asks issued — *end to end*

gemma-4-E2B is why the split is mandatory: 46 gives, 7 landed. It answers, and misses.

### Validity gates — mandatory

**Spam gate.** Report asks-per-unit-work beside every rate. A subject re-issuing the same ask each
step inflates the denominator *and* deflates expiries — the ask never sits still long enough to time
out. Proof: qwen2.5-0.5b constrained, **1,125 asks, 4 expiries, 0 answered**. `request_expiry_count`
is unusable raw.

**Empty-denominator gate.** If `Coordination/total_attempts ≈ 0`, do not report those rates **at
all** — not as zero. A rate over an empty denominator is not a result.

**Unknown-not-dropped gate.** Witness's honest-fusion rule already says it: *"a source that is
missing/unreadable renders UNKNOWN — never a faked reading."* An unjoinable `[task]` is **UNKNOWN**,
never `dropped`. This rule, already written, forbids this spec's own 35% false alarm.

### What it can and cannot claim

**Can:** *this subject was asked N times and answered A of them, within T.*

**Cannot (Alem, today):** anything about coordination being hard. At 0.5b–3b this is the
format/competence floor in a coordination costume. The instrument is valid; these models are not its
subjects.

**Cannot (mesh, until Unit 5):** causality. 64% attributable completion does not prove the board
caused it, and the week cannot be rerun without the board.

## Units

### Unit 1 — one key: `[task]` mints the id, and that id IS the `mesh-claim` key

The task id becomes an explicit field, minted at `[task]` time, validated by `mesh-claim`'s existing
`valid_key`, and cited verbatim by `[dispatch]`/`[claim]`/`[claim-done]`/`[done]`. Unknown id →
ERROR naming the open tasks, nothing posted — the identical fail-fast idiom `mesh-chat --to` already
uses for targets.

**Unifying the namespaces is the whole trick.** `mesh-claim` already accepts a "design slug" as a
valid artifact key; nobody uses it that way, so tasks and locks live in disjoint namespaces and 29
claims join to 0 tasks. One key then serves three functions at once: dispatch's dedup, mesh-claim's
lock, and the funnel's join. The double-dispatch race is prevented by the *same* key the funnel
measures.

*Legacy:* 3,002 lines of history carry no explicit ids. They render **UNKNOWN** — never guessed.
The board decays on reboot, so legacy is transient by construction.

### Unit 2 — delete `claim_id_of()` and its scar tissue

Once ids are explicit, `claim_id_of()`, all three strip functions, the four fallback regexes, and
the SHOUTY-key guess become dead code. Deleting them **kills the bug class**, rather than shipping
the sixth strip function. This is the unit that pays for the spec.

Guard: the existing `[gap]` false-flag cases become the regression corpus. Any of them re-flagging
after Unit 1 means the id wasn't actually explicit.

### Unit 3 — the resolution axis in `mesh-witness` (surgical extension, not a new tool)

Witness is already "the mesh measuring itself" and already reads the board — but only for
**throughput**: `board1h` (line volume), `board_age_s` (pulse), `board_posters` (distinct/1h). Its
own docstring (`:182-191`) warns against reading "stigmergic" as praise.

**A board can be maximally busy and coordinate nothing.** `board1h=33` says the board is loud, never
that an ask was answered. That is the missing axis:

- `ask_open` — tasks with no joined answer, **excluding those younger than measured p90**. An ask in
  flight is not an ask dropped.
- `ask_stale_h` — age of the oldest such ask. The scalar the reflex fires on.
- `ask_resolve` — answers joined / asks posted. A **floor**, labelled as one, with its UNKNOWN count
  beside it.

Per honest-fusion, witness **fuses from artifacts the mesh already produced** — dispatch already
computes evaporation conditioned on *idle-exposed ticks* (a better denominator than this spec
originally proposed: it counts only ticks where a mind could actually have taken the task). Witness
reads that; it does not recompute it.

### Unit 4 — the dispatch pane (`mesh-dash chat`)

The board **is** the dispatch surface. Its data pane shows churn today: `[task]=23 [taking]=0
[done]=14`.

- **`[taking]=0` must go.** It renders a superseded marker as a permanent zero, which reads as total
  failure and is merely a dead convention. Show the live protocol: `[claim]`/`[claim-done]` and
  `[dispatch]`.
- **Add the resolution line:** open asks, oldest-open age against p90, evaporated-this-pass (read
  from dispatch, not recomputed).
- **UNKNOWN is a first-class cell**, never folded into a failure count.

Division of labour: the **chat pane is now** (what is open, what has stalled — actionable);
**witness is the trend** (is resolution improving over days).

### Unit 5 — the board canary (causality; deferred until 1–4 land)

Inject a synthetic `[task]` with known properties; measure whether and when it is answered. The
standard instrument for deployed systems, where benchmarks don't apply.

**Deferred deliberately.** A canary spends real mind-effort on non-work; injected too often or too
plausibly, minds learn the board carries fake asks and the instrument corrodes what it measures.
Needs a rate ceiling and an honesty rule (a canary must be recognizable as such after the fact).

## Sequencing is a hard constraint

**Nothing surfaces on a pane, and no reflex fires, before Unit 1.** A reflex on today's joins would
nag about phantom drops — this spec produced 56 of them within the hour, and the mesh has this exact
failure class open on the board (`chat-review/mindblocked-5s-debounce-cries-wolf`). A gate you have
seen fire falsely is worse than no gate: it teaches minds to ignore the pane.

Calibrate the threshold against the real corpus, never an assumed range (`tone`'s median IS its max;
a rule keyed on a guessed range is a constant).

## Out of scope

- **Filing `total_attempts=9` upstream.** It describes our truncation, not their defect. Obvious to
  maintainers.
- **Running any coding-plan CLI as benchmark inference.** The BRIEF's zai ruling — *"a coding plan
  carries no PAYG API credits; its coding endpoint is out of scope — don't route around it"* — is
  about the shape of the thing, not the vendor. A Claude Code subscription is the same shape.
- **A mesh leaderboard row.** Not comparable to anything.
- **Adapting the mesh to a synchronous benchmark.** See "Why not a benchmark."
