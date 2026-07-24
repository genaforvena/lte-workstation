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

## Next step

A ROM per STANDING claim, in the `mesh-spearman` shape: the ROM owns the reduction and its
domain, a 64-bit twin cross-checks it, and the claim is re-derived from the live corpus
rather than quoted. Claims 4 and 5 need their source ledgers read first (`mesh-clear-log`
and a fresh loop measurement respectively) — they are listed unchecked rather than quietly
dropped.
