# uxn-doctrine-sweep — inventory of quantitative claims in CLAUDE.md

Step 1 of uxn-doctrine-sweep (operator 2026-07-24): enumerate every quantitative claim in
the doctrine **before** putting a ROM behind any of them, with quote and line number, and
with **no silent top-N** — the total is stated and every candidate is classified, including
the ones ruled out.

Method: `CLAUDE.md` is 502 lines. A mechanical scan for number-shaped tokens (percentages,
counts, `n=`, decimals, multi-digit integers, durations, sizes) matched **49 lines**.
Dropping lines whose only numbers are dates leaves **32 candidates**. All 32 appear below.

Classification:

- **STANDING** — asserts a number about the mesh's own measured behaviour, still load-bearing,
  and checkable now. These are the ROM targets.
- **HISTORICAL** — an explicitly dated incident record. Not a standing claim; a ROM would be
  checking the past. Left alone deliberately.
- **CONFIG** — a default or an example value (`900s`, `8022`, `10/8`), not a measurement.

## STANDING (5)

> **These verdicts are now RE-DERIVED, not stored (2026-08-24).** Every status in the table
> below was hand-written once from a single sweep, while `mesh-series-stats --claims` — the tool
> built to keep them live — printed only a ROM-vs-twin *arithmetic* verdict and rendered a bare
> `[AGREE]` beside claim 2 on a corpus holding `cnt(act>=0.55)=133`. The word `DRIFT` appeared in
> that tool's header and in the sound dash's legend and in **no code path**, so the gate could not
> fail in the one direction it existed for. Each claim now carries a predicate and emits its own
> `=>` verdict (`HOLDS` / `DRIFT` / `REFUTED` / `UNKNOWN`) on every sound-dash frame, separate from
> `[arith:]`. Every predicate is parameter-free — the claim's own operative consequence, never an
> invented tolerance: a **bound** tests `cnt(>=t)==0`; a **median** tests whether it still splits
> the live corpus, against the binomial null `0.5 ± 3·(0.5/√n)`, a band derived from n rather than
> chosen — and the deviation is printed in that null's own sd units (`z=+9.8 sd`), because the
> verdict FLAPS at the edge: `dyn` sat at 3.0 sd and crossed HOLDS→DRIFT between two dash frames
> two minutes apart. Without `z` a reader cannot separate that jitter from a real move and would
> reach for a wider band — an invented constant — to quiet it. A verdict inside 1 sd of the edge
> is marked `MARGINAL`. A **comparison** tests DIRECTION and reports its magnitude as explicitly NOT GATED,
> because the ROM yields no dispersion term and no honest band exists there. An empty or
> ROM-refused series renders `UNKNOWN`, never `HOLDS`.
>
> Live at the time of writing (n≈1614, vs the n=651 sweep recorded below): claim 2 **REFUTED**
> (133 rows exceed 0.55, up from 24); claim 3 `act` **DRIFT** (z=+6.3), `move` **DRIFT** (z=+9.8), `dyn` **DRIFT but MARGINAL** (z=+3.6, flapping);
> claim 1 **HOLDS (direction)** with the separation continuing to collapse — 3.39x → 1.5x at
> n=651 → **1.16x** now. Do not quote those numbers: re-run `mesh-series-stats --claims`.


| # | line | claim | status |
|---|------|-------|--------|
| 1 | 434 | "over n=215 records, score≥55 averages **3.6 beats** vs **12.2** for everything else" | **REFUTED as stated** — direction survives, magnitude does not |
| 2 | 435 | "`mesh-soundscape`'s own `act > 0.55` → \"busy\" tag can never fire — act never exceeds .544 on real material" | **REFUTED** |
| 3 | 435 | "real medians are dyn .265 / act .319 / move .141" | **STALE** — two of three moved materially |
| 4 | 227 | "The gate is over-blocking-but-safe (permits ~43% of covered clears, loses zero threads)" | unchecked — needs the clear-log |
| 5 | 291 | "Cycle at a 60s delay measured ~122s — budget roughly +60s scheduling latency" | unchecked — needs a fresh loop measurement |

### 1 — score≥55 vs beats (line 434)

Doctrine: n=215, score≥55 averages 3.6 beats vs 12.2.
Measured 2026-07-24 on n=651: score≥55 (n=33) averages **6.52** beats, score<55 (n=618)
averages **9.73**. The gap is real but is 1.5x, not the 3.4x the doctrine records.

The stronger correction is the one `mesh-spearman` produced (commit 0b3778e, re-measured at
n=651 in 518590c): the global rank correlation between score and beats is **+0.109 ordinal /
+0.136 midrank** — *positive*. Read as a global claim "anti-correlated" is wrong. Read as a
claim about the upper tail it holds: within the top score decile rho = **-0.196**. The
doctrine's prose does not make that distinction and so overstates.

### 2 — `act > 0.55` can never fire (line 435)

Doctrine: "act never exceeds .544 on real material", so the busy tag is dead code.
Measured 2026-07-24 on n=651: **act max = 1.000, and 24 records exceed 0.55.** The tag fires.
The original figure came from n=29; the structural claim ("can never") did not survive n=651.
This is the cleanest refutation in the sweep — a universal quantifier falsified by a counterexample.

### 3 — the axis medians (line 435)

| axis | doctrine (n=29) | measured (n=651) |
|------|-----------------|------------------|
| dyn  | .265 | **.133** |
| act  | .319 | **.301** |
| move | .141 | **.226** |

`act` is close; `dyn` halved and `move` went up ~60%. Any rule tuned to the old medians is
mis-centred. Note this vindicates the *lesson* of that bullet ("calibrate against the REAL
corpus, never an assumed 0..1") while falsifying its *numbers* — which is exactly why the
lesson says to rank against the live corpus rather than pin a constant.

## HISTORICAL (13)

Dated incident records, not standing claims: lines 80, 82, 83, 85 (the `|| echo 500` beat
fallback), 102 (`guardian.log` at :23), 111 (Telegram unread 01:28→04:32), 117, 121 (whisper
rc=127, Groq 403), 136–137 (**33 of 52** self-grep gates, swept 2026-07-15 — see note below),
149–150 (55 commits sat local for 11h), 223–224 (the coverage-model bench, false-YES 0/7 /
over-block 4/7 / 7/7), 288–289 (the /clear wakeup tick timestamps).

Note on 136–137: the sweep is dated, so the number is a record rather than a claim — but the
ratchet has since moved to **21 of 46** (commits 1d42944, 950ef8d). The prose is not wrong;
it is just no longer the current state, and a reader could take it for one.

## CONFIG (14)

Not measurements: lines 41, 44, 45, 47, 48 (`PHONE_SSH_PORT` 8022, `-l 10`), 162
(`--tail 20`), 172 (`10/8`, `172.16/12`, `192.168/16`, `100.64/10`), 216 (`900s` default),
307 (1200–1800s guidance), 317 ("10+ window sprawl"), 410 (`10.9.0.0/24`), 433 (retention
"2d"), 435 ("0..1" as a named anti-pattern rather than a measurement).

## Step 2 — a ROM behind the standing claims (2026-07-24)

`series-stats.tal` + `mesh-series-stats` + `test-series-stats`, in the `mesh-spearman`
shape: the ROM owns the reduction and its domain, a 64-bit twin cross-checks it, and the
claim is re-derived from the live corpus rather than quoted.

The ROM takes a threshold, `n`, and `n` **non-decreasing** integers and answers
`min max med2 cnt sum mean1000`. Domain `1 <= n <= 2343`, every token `<= 9999`, values
sorted; anything else is `NA` rc=2. Sorting is the host's job — the same split as spearman,
where the host owns ranking and the ROM owns the formula — and the ROM *verifies* it, so a
host that forgets to sort gets a refusal rather than a plausible wrong median.

Three design points worth keeping:

- **`med2` is twice the median, deliberately.** For even `n` the median is the mean of the
  two central elements and can end in `.5`, which an integer ROM cannot say. Halving in the
  host is exact; rounding in the ROM would be a lie the caller could not see.
- **`mean1000` is rounded, not truncated** — the same bug spearman had, where truncation
  cost exactly 1 in the last place and made the ROM disagree with its twin on 2 of 11 live
  windows. A fourth fractional digit decides.
- **The sum is why `arith32` is here.** 2343 values of 9999 sum to 23,427,657, nine times
  past a 16-bit word. A 16-bit accumulator would not error; it would wrap, and the mean
  would come back small and entirely believable.

Gate: `test-series-stats` — 17 truth-table rows, `rom == source`, **5 source-mutants
required RED** (sortedness guard defeated · per-token ceiling loosened · rounding →
truncation · lower median index `(n-1)/2` → `n/2` · `cnt >= T` weakened to `> T`), the
domain pinned from both sides, 8 random series against the 64-bit twin, the host required
to refuse rather than silently window, and 3 double-word carries required to change the
answer through the real reduction.

**`n=255` is load-bearing in the carry section, not a round number.** `w-mul16` is reached
here only through `n*place` in the mean's long division, and its low-word carry fires only
for particular `n`: at `n=100` the partials do not overflow, the mutant answers identically,
and the section reads green against a real bug. At `n=255 x 1000` they do overflow
(`t0=59160` plus `(mid&0xff)<<8 = 64768` wraps), so the deleted carry costs 65536 and the
quotient loop takes a different path. A carry test is only a test on inputs that *can* carry
— the same lesson as step 1's, where the max-domain input turned out to be the weakest place
to hunt a carry.

### Result: claims 1–3 are now re-derived, and ROM == twin on every one

```
source: ~/.mesh/records.log (650 rows, mtime 2026-07-24T02:54:56Z)
  act:               n=643  max=1.000  median=0.301  cnt(>=0.55)=24  mean=0.3256  [AGREE]
  dyn:               n=643  max=1.000  median=0.134  cnt(>=0.5)=9    mean=0.1608  [AGREE]
  move:              n=643  max=1.000  median=0.228  cnt(>=0.5)=57   mean=0.2627  [AGREE]
  beats [score>=55]: n=33   max=26     median=6                      mean=6.515   [AGREE]
  beats [score<55]:  n=617  max=44     median=7                      mean=9.729   [AGREE]
```

Claim 2 stays REFUTED (act reaches 1.000; 24 records clear 0.55). Claim 3's numbers stay
STALE against the doctrine's n=29 figures. Claim 1's direction survives and its magnitude
does not, exactly as step 1 found.

### The finding step 2 actually produced: the corpus is a SLIDING WINDOW

Step 1 measured at `n=651` and wrote that number into `CLAUDE.md`. **It is not
reproducible, and it never will be.** `mesh-records` prunes `records.log` per organ to
`LOG_KEEP` rows on every sweep (`scripts/mesh-records`, the `awk -v k="$LOG_KEEP"` block) —
so the ledger is a per-organ sliding window, not an archive. The row count moves **down** as
well as up, and the population itself turns over.

Measured across ~25 minutes of one session today, with no intervention:

| | first read | second read |
|---|---|---|
| ledger rows | 658 | 650 |
| axis rows (`n`) | 651 | 643 |
| `dyn` median | .135 | .134 |
| `move` median | .228 | .228 |
| `beats [score<55]` mean | 9.621 | 9.729 |
| `beats [score<55]` n | 625 | 617 |

This is the strongest argument the sweep has produced for the whole exercise. The doctrine's
own bullet already says "rank against the live corpus, never pin a constant" — the sliding
window makes that not merely good practice but the *only* option: **any `n=` quoted from
this ledger is stale before the prose is committed.** So the standing claims should cite the
gate and treat the printed figures as the gate's current answer, never as the claim itself.

### Claims 4 and 5

- **Claim 4** ("the gate permits ~43% of covered clears") — the *number* checks out, from
  `~/.mesh/model-bench.log`: `gemma4:e2b-it-qat` scores error 0.571 on the coverage fixture,
  i.e. 3 of 7 permitted = 42.9%. But its **subject does not**: that is a 7-row *fixture
  bench*, while "of covered clears" reads as a rate over the live clear stream. The figure is
  right and the sentence it sits in is broader than the measurement. Not refuted — mis-scoped.
- **Claim 5** ("a 60s loop delay measured ~122s") — still unchecked. Measuring it costs two
  scheduled wakeups, i.e. two paid turns, and the loop is task-scoped by doctrine. Listed
  unchecked rather than quietly dropped.

## Next step

Step 3: wire `mesh-series-stats --claims` somewhere it is *read* — the drift it detects is
only useful if something looks. The natural home is the sound-studio dash pane, since that
is the role whose thresholds these numbers calibrate.
