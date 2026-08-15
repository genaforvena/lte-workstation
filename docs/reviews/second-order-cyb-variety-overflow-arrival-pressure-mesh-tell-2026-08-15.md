# Second-order cybernetics live review — VARIETY OVERFLOW at the receiving mind

**Date:** 2026-08-15 · **Lane:** LITERATURE (live review), idea-queue · **Landed in:** `scripts/mesh-tell`
(`--pressure`, report-only) · **Status:** uncommitted in the tree, steward lands.

## The search (what "live" meant here)

The coverage map ([[second-order-cybernetics-coverage]]) warned that arXiv is nearly empty on this area
and that the live literature sits in *Kybernetes* / *Constructivist Foundations* / *Enacting
Cybernetics*. Confirmed again today: `all:"second-order cybernetics"` on the arXiv API returns **2**
papers, both already landed here (2504.16225, 2506.23032). So the sweep went to the journals.

What is actually new right now:

- *Kybernetes* has an open call, **"Beyond Doomsday — Heinz von Foerster's legacy"** (submissions
  1 Jan – 30 Jun 2026, for the 115th-birthday issue, 13 Nov 2026) — i.e. this area's 2026 output is
  still in press, which is itself the answer to "what's new".
- **Enacting Cybernetics 3(1)** (the Cybernetics Society's journal, Nov 2025) is the freshest
  *published* issue: Kaleida, *Tangled Hierarchies and Resonant Phase Spaces for Intelligent Systems*
  (doi:10.58695/ec.14); Neese & Penabaz-Wiley, *The Requisite Variety of Presence* (doi:10.58695/ec.20);
  Manning, *A Concept Must Be Some Kind of Process* (doi:10.58695/ec.19).
- Adjacent arXiv 2026 that came up and was **not** taken: 2607.04277 *Self-Reference in LLMs: the
  Introspection Threshold for Recursive Self-Improvement* (5 Jul 2026 — the strongest alternative, held:
  operationalising "introspection" over our autopoiesis lane needs a proxy for self-access that would
  rot, and the doctrine's own warning about fuzzy source-derived proxies applies); 2603.16586 *Runtime
  Governance for AI Agents: Policies on Paths*; 2607.05463 *Governable Individuals*.

Both Enacting Cybernetics PDFs were read in full. Kaleida's paper is a philosophical argument
(intelligence as border activity between modelled and unmodelled; T ⊂ N) with no operational criterion
— **discarded**: nothing in it becomes a gate on an organ without inventing the criterion ourselves.

## The concept landed

**Source:** Brett Neese & Sofia Penabaz-Wiley, *The Requisite Variety of Presence: A Cybernetic
Intervention in Knowledge Work's Attention Crisis*, **Enacting Cybernetics 3(1): Article 2**,
18 Nov 2025, doi:10.58695/ec.20.

**VARIETY OVERFLOW** — "an excess of incoming information without corresponding mechanisms for
effective filtering". The criterion it leans on is **Glanville's (2009, p.70) corollary to Ashby**:
"the variety of the controller and the controlled must, for effective control to take place, be the
same." Overflow is that parity breaking in the arrivals' favour: "unstructured messages arrive faster
than humans can process them", so "homeostatic maintenance becomes impossible". Its empirical anchor
is the field figure it quotes — workers "interrupted every 15 minutes by email and every 18 minutes
via instant message", 41% answering email in under 2 seconds (Iqbal & Horvitz 2007). Its intervention
(the `buddylist` case) is a **receiver-declared presence signal that senders read** — attenuation at
the source instead of absorption at the sink.

**Why this is new ground for us.** We have landed requisite variety twice, both times on the
*regulator's* side: `mesh-vitality channel_variety` (board inflow vs closure) and `mesh-relay
metabolism_variety` (independence of the absorbers). Neither is about arrivals at a receiver. And the
mesh measures **the operator's** interruptibility exhaustively — `mesh-interruptibility` fuses 8
senses to answer "may the mesh speak to the human?" — while never once asking it about a **mind**.

## The gap

Every send is regulated on the **sender's** side: `--ack` (did it land), `--fresh` (park + clear
first), `dead_shell_guard` (dead/shed pane), `mesh-dispatch`'s idle/thermal/pace holds. All of these
ask *can this send be delivered*. None asks *how often is this mind being poked*.

`~/.mesh/tell-wal.log` has journalled every arrival at every mind pane since 2026-07-20 — ts, pid,
phase, who, node, window, payload. Its **only** reader is `--replay`, which prints the last N sends
one at a time: a per-send audit view that structurally cannot surface a rate. The arrival stream
existed in full, for weeks, and the question was never put to it.

## What landed

`mesh-tell --pressure [<window>]` — report-only, never gates, delays or reorders a send.

```
tell-wal: 12.0d window · 994 arrival(s) · level=full · /home/mesh-home/.mesh/tell-wal.log
  span/n come from the log, which is a SLIDING window (trimmed at 4000 lines to 2000): a current answer, not a reproducible population.
  reference 15 min = the field interval at which knowledge workers were interrupted by email (Iqbal & Horvitz 2007), quoted in
  Neese & Penabaz-Wiley 2025, Enacting Cybernetics 3(1):2 doi:10.58695/ec.20. A CITED anchor — not a mesh-tuned threshold.
  CLAIM: arrival pressure AT the pane. NOT goal interference — the WAL never recorded what the mind was doing when the prompt landed.

  win            arr  med_gap_min  burst<5m  pressure
  genome         349         10.0       24%  overflow-risk
  sound          134         30.0        6%  paced
  health         110         60.5        8%  paced
  senses          71         89.2       19%  paced
  discover        69         91.7        4%  paced
  pub             65         93.3        5%  paced
  witness         52        145.3       10%  paced
  vpn             40        198.4        3%  paced
  tg              35        300.0        6%  paced
  tg-roz          34        300.0       15%  paced
  adint           18          4.0       65%  overflow-risk
  job             16         73.2        7%  paced
  opencode         1          n-a       n-a  n-a (<8 arrivals)
```

**The live finding: `genome`'s median inter-arrival is 10.0 minutes — SHORTER than the 15-minute field
interval at which the human knowledge workers of the paper's attention crisis were interrupted by
email.** 24% of its arrivals land within 5 minutes of the previous one; 68% within 20. The mesh's
busiest mind is poked harder than the workers whose overflow the paper was written about, and until
now nothing in the mesh could have said so. (`adint` at 4.0 min is a two-day burst of hand-driving,
not a standing cadence — n=18 over a short span; it is reported as measured, not smoothed away.)

Definitions, kept narrow on purpose:

- **arr** — completed arrivals (`sent` records). An `intent` with no outcome never reached the pane and
  is not an arrival. Consecutive records sharing pid+win within 60 s are ONE invocation: a retry is not
  a second interruption. (Measured 0 such pairs in the live log — the rule is for the shape, not the
  data.)
- **med_gap_min** — *median* inter-arrival gap. Not the mean: one overnight silence would otherwise
  launder a day of two-minute pokes into a calm average.
- **burst<5m** — share of gaps under 5 minutes, reported raw, with no band of its own.
- **pressure** — `paced` | `overflow-risk` | `n-a`. Two bands and one cited constant; no invented
  thresholds.

## Three honesty constraints, each a doctrine failure this axis could have walked into

1. **`level=off` renders n/a, never a calm zero.** At that WAL level the node journals nothing, so an
   empty (or stale) log is a *configuration*, not evidence that no mind was interrupted — the
   silent-fallback shape, a default indistinguishable from a success. The gate is driven against a
   **populated** log so a level check that only fired on an empty file would still go red.
   `redact`/`minimal` thin only the payload column, so timing survives and pressure stays fully
   readable there; they are reported, not refused (leg 7 is that opposite direction).
2. **The reference interval is cited, not tuned.** 15 min is Iqbal & Horvitz's measured human figure as
   quoted by the paper, printed in the output *beside its citation*, so it can never be read as a
   mesh-calibrated threshold somebody may quietly retune ([[a-constant-outlives-its-reader]],
   [[a-safety-knob-named-in-prose]]). Span and n come from the log, which is a sliding window — no
   figure here is reproducible; the claim is the gate, the number is only its current answer
   ([[records-log-is-a-sliding-window]]).
3. **It claims ARRIVAL PRESSURE, not goal interference.** The WAL records what was injected and when,
   never what the mind was doing when it landed; an arrival at an idle pane is a feed, not an
   interruption. Claiming the wider thing would be a sub-axis standing in for a verdict
   ([[a-sub-axis-is-not-the-verdict]]).

## RED-first

8 legs, all synthetic WALs with hand-placed timestamps (no dependence on what the live log happens to
hold). 6 mutants run from **scratch copies** (chmod +x — the file re-invokes `"$0"`), each `rc=1` and
each failing on its own leg's message, not on collateral:

| mutant | change | leg that went red |
|---|---|---|
| m1 | `level=off` guard disabled | level=off reported `fastwin` as a live rate |
| m2 | same-pid collapse removed | `arr` doubled to 24, hourly window flipped to overflow-risk |
| m3 | `intent` counted as an arrival | dangling-intent log produced a window row and rc=0 |
| m4 | MIN_N branch removed | 4 arrivals were given an overflow verdict |
| m5 | band inverted | 5-min arrivals read `paced`, hourly read `overflow-risk` |
| m6 | citation dropped from output | reference printed without Iqbal & Horvitz |

The full `--test` is green on the tree copy, and its pre-existing sandbox-honesty leg (the real
injection log must not grow during a test) still passes.

## Held, deliberately

**The receiver-declared attenuator itself — `buddylist`'s half of the paper.** A mind publishing "hold
non-incident sends", which `mesh-tell`/`mesh-dispatch` would honour, changes *what gets delivered*, and
the mesh had no measurement of arrival pressure to weigh that against until this axis has run. Measure
first, then decide whether the genome mind's 10-minute cadence is a problem or the price of being the
busiest lane. Also held: joining arrivals against the receiver's state at send time (which would turn
arrival pressure into real goal interference) — `mesh-mind-state` knows the state, the WAL does not
record it, and welding them is a change to the send path, not a read of the log.

See also [[second-order-cybernetics-coverage]], [[vsm-beer-review-coverage]].
