# Autopoiesis live review — RE-ENTRY: the fault we were doing to ourselves

**Task:** auto idea-queue — LITERATURE (live review): autopoiesis & the biology of cognition
(Maturana, Varela), from the angle of a known **CRITIQUE or failure mode** of the area.
**Date:** 2026-08-17 · owner: genome · **Landed** (uncommitted in tree; steward lands)
**Artifact:** `scripts/mesh-hw-fault-watch` — `probe=` on every radio fault line + a new
`--selfprobe` report. Report-only; no behaviour of the reflex changes.

---

## 1. The critique, and why it is live

The critique is not "autopoiesis is wrong". It is the one repeatedly aimed at every system that
*claims* the label: **operational closure without re-entry is not sense-making, it is solipsism with
a boundary**. A system that never re-introduces the system/environment distinction *into its own
operations* cannot tell **self-reference** from **other-reference** — so it reads what it did to
itself as something the world did to it.

The live source, and it is squarely in this area (Maturana & Varela's autopoiesis read through
Luhmann's re-entry, applied to artificial systems):

- **Benedikt Zönnchen, Mariya Dzhimova & Gudrun Socher, "From intelligence to autopoiesis:
  rethinking artificial intelligence through systems theory", *Frontiers in Communication* 10:1585321
  (19 May 2025)** — <https://doi.org/10.3389/fcomm.2025.1585321> (read in full 2026-08-17).

  Their charge against the existing "this technical system is autopoietic" literature, verbatim:
  such accounts *"lack a critical examination of how such systems might engage in **re-entry** — the
  reintegration of the system/environment distinction into the system's own operations which is
  essential for sense-making systems in Luhmann's theory."* Re-entry *"enables self-observation — a
  special case of what Heinz von Foerster and Margaret Mead called second-order cybernetics"*, and
  what it buys the system is *"the difference between **self-reference** and **other-reference**,
  which is essential for observing an environment"*.

  Their criteria for an autopoietic sense-making system: operational closure with self-referential
  operations · self-reference distinguishable from other-reference via re-entry · contingent
  selection among possibilities · second-order observation · internal reflection on its own
  distinctions. Verdict on LLMs: *"they do not produce or reproduce their own system/environment
  distinction."*

Lineage check (this is a live thread, not a fixed-list classic): the same argument runs through the
**ALIFE 2026 satellite tutorial "Autopoiesis & Structural Coupling"** (J-C. Letelier, Waterloo,
August 2026, <https://autopoiesistutorial.netlify.app/>), whose framing claim is that *"the
fundamental phenomenon characterizing living systems is not Autopoiesis per se, but rather
Structural Coupling"* — i.e. the same demotion of closure-alone in favour of the organism's
traffic with its environment.

## 2. What the mesh already embodies (so the new part is small and exact)

First-order self/other attribution is **not** new here — a census before proposing anything:

| where | the cut it already makes |
|---|---|
| `mesh-bt-link` | `SELF-INFLICTED` — a pairable window held open by *our own* BLE scan |
| `mesh-wifi-heat-attrib` | radio heat = RELAY-LOAD vs LOCAL-LOAD vs UNEXPLAINED |
| `mesh-psi-attrib` | which cgroup owns the stall; own-fraction per axis |
| `mesh-fitness` | the agency gate — credit only for SELF-CAUSED outcomes |
| `mesh-room-sense` | `source=` — is this node emitting the sound it hears |
| `mesh-hw-fault-watch` | **OOM lines only**: `pane=<w.p>`, the kill attributed to our own mind |

The gap is exactly one class wide, and it is in the last row. `mesh-hw-fault-watch` re-enters for
the OOM class and **not** for the PERIPHERAL class. Every `rtw_8822bu` firmware fault on this node's
**sole uplink** boarded as an environment-side event — "the dongle is faulting" — on a node whose
own reflexes drive that same combo chip every few minutes. `CLAUDE.local.md` even records the
suspicion (*"Untested suspect worth a drill: the BT half of the combo chip — our own
`bt-census`/`mesh-bt-link` poke the same silicon"*) and it stayed untested because nothing could
express it: the suspicion lived in prose, never in an observation.

## 3. The measurement

### 3.1 The cut that does NOT work — cron's journal (recorded so nobody rebuilds it)

The obvious source for "what were we doing at time T" is cron's own journal, which does log full
`CMD (...)` lines with pids. It is **not joinable**: over 14 days this node logged **317890 CMD
lines vs 317226 session-closed lines, of which only 11810 were pid-pairable — and every one of
those spans was >600s, median 4.8 DAYS** (pid reuse pairing a start to a stranger's close). Built
that way, the probe reported *"a radio probe was in flight for 99.83% of wallclock"*, which
`pgrep` refutes in one call: **zero** radio tools running at an arbitrary moment. A record that
looks like evidence of our own operations, and is not.

### 3.2 The cut that works — our own schedule

Every mesh reflex starts at second ~01 of its cron minute, and the crontab is exact, free and
unprivileged. So: for each radio-touching reflex, take its minute-set, call the first
`MESH_HW_FAULT_PROBE_WIN` (default 30) seconds of those minutes its **in-flight window**, and ask
what fraction of radio faults land inside it.

Significance is a **phase-shift null**: the same statistic recomputed at 514 circular shifts (step
7s) across the hour. A periodic label would be invariant to shifts by whole periods
(`periodic-labels-make-a-shift-null-invariant`), so the shift is in *seconds*, walking every phase;
and because the shift carries the log's real burstiness along, an hour-clustered fault storm cannot
manufacture a p-value. Events are de-bursted to one per 60s (38333 raw rtw lines → 340 events).

### 3.3 Result — `mesh-hw-fault-watch --selfprobe 7`, mesh-home, 2026-08-17

```
window 7 day(s) · 340 event(s) (de-bursted >=60s) · in-flight window 30s after each start

tool                   base    obs  enrich  nullmd       p   minus mesh-wifiscan minutes
mesh-wifiscan          5.0%  33.2%   6.65x    3.8%  0.0078   <- LEAD (ranked on enrich)
mesh-wifi-rf          10.0%  36.2%   3.62x    8.2%  0.0097    0.59x p=0.6699 (6 min/h)
mesh-imac-wifi        25.0%  52.4%   2.09x   23.2%  0.0291    0.96x p=0.3981 (24 min/h)
mesh-bt-link           5.8%  11.5%   1.97x    5.6%  0.0311    1.00x p=0.4680 (6 min/h)
mesh-wifi-quality      5.0%   9.4%   1.88x    3.8%  0.0854    1.88x p=0.0854 (6 min/h)
mesh-link-heal        50.0%  77.1%   1.54x   50.3%  0.0524    0.97x p=0.5398 (54 min/h)
mesh-bt-census         2.5%   3.5%   1.41x    2.1%  0.2311    1.41x p=0.2311 (3 min/h)
mesh-presence          5.0%   4.1%   0.82x    3.8%  0.4641    0.82x p=0.4641 (6 min/h)
mesh-wifi-mimo         5.0%   3.8%   0.76x    3.8%  0.5359    0.76x p=0.5359 (6 min/h)
mesh-proximity         5.0%   3.8%   0.76x    3.8%  0.5359    0.76x p=0.5359 (6 min/h)
mesh-wifi-link        10.0%   6.2%   0.62x    8.2%  0.7165    0.62x p=0.7165 (12 min/h)
mesh-wifi-crossval     0.8%   0.9%   1.06x    0.6%  0.3825    1.06x p=0.3825 (1 min/h)
```

**One third of this node's uplink firmware faults fall in the 5% of wallclock right after our own
`mesh-wifiscan` fires** — 6.65x, p=0.0078. Independently reproduced before the tool existed, by a
separate Python probe over the same log (6.65x, p=0.0067 over 599 one-second shifts), with a
same-geometry control label (minute%10==3, a minute nothing scans) at 0.80x, p=0.455.

The last column is the part that matters and the reason the naive table would have lied:
**overlapping schedules inherit each other's enrichment.** `mesh-wifi-rf` fires on `m%5==1`, a strict
superset of wifiscan's `m%10==6`; `mesh-link-heal` fires *every* minute. Re-run on the minutes each
tool has after removing the leader's, wifi-rf collapses **3.62x → 0.59x**, imac-wifi **2.09x →
0.96x**, bt-link **1.97x → 1.00x**, link-heal **1.54x → 0.97x**. The whole phase signal sits on
`mesh-wifiscan`'s minutes and nowhere else.

Two consequences worth naming:

- **The standing suspicion was aimed at the wrong half of the chip.** The BT tools do not carry the
  signal (`bt-link` 1.00x after de-confounding, `presence` 0.82x, `bt-census` 1.41x p=0.23). The
  wifi *scan* does. `mesh-wifiscan`'s own header already knew the cost in prose — *"a scan takes the
  radio off-channel … without hammering the radio that carries forwarded client traffic"* — and
  nothing ever checked whether that cost showed up in the fault log. A comment is not a channel to
  the reader.
- **This is co-incidence, not cause.** Enrichment says our probe was scheduled when the chip
  faulted. Settling causation needs the intervention nobody has run: pause `mesh-wifiscan` for a
  window and compare against an equal control window. The tool now says so in its own output rather
  than leaving the reader to infer a mechanism.

## 4. What landed — `scripts/mesh-hw-fault-watch`

- **`probe=` on every RADIO-driver board line** (`rtw*|iwlwifi|ath*|mt76*|brcmfmac|rtl*|hci[0-9]`):
  `probe=self:mesh-wifiscan+11s` · `probe=none` · `probe=na(no-schedule)`. Scoped to drivers whose
  silicon this mesh actually drives — a `probe=` on an nvme line would name an operation that cannot
  touch it, which is a fabricated attribution, not a cautious one.
- **Honest-na:** an unreadable schedule renders `na`, never `none`. Missing evidence must not read as
  the mesh exonerating itself.
- **The schedule is read from `crontab -l`** — the *enacted* cadence, not the declared
  `reflexes.cron`. `MESH_HW_FAULT_CRONSRC` overrides it **exclusively** (no fallback), so a test that
  set it can never silently read the live schedule and assert nothing.
- **Word boundary in `RADIO_TOOL_RE` is load-bearing:** without the trailing `( |$)`, `mesh-presence`
  also matches `mesh-presence-density` / `mesh-presence-fuse`, which read state files and never touch
  the radio.
- **`--selfprobe [days]`** — the second-order view: how much of what this tool boards is co-incident
  with the mesh's own operations, with the de-confounding column and the phase-shift null.

**Gates (all RED-first, mutants run from a scratch copy):**

| mutation | leg that caught it |
|---|---|
| drop the `( |$)` word boundary | `probe=none` leg — every fault claimed by the every-minute non-radio tool |
| drop the in-flight seconds check | the second-47 leg — a fault past the window read `self` |
| `na(no-schedule)` → `none` | the unreadable-schedule leg |
| annotate every driver, not just radio | the nvme leg |
| `--selfprobe` ignores the seconds window | late-second leg (see below) |

Five more, added with the `--legs` speed-up and each seen RED from a scratch copy: a non-exclusive
fixture override (falls through to the live source) · an unknown leg name accepted · the
module-settles short-circuit removed (reports a journal count it never read) · the leg filter
ignored (`--legs rtw` reports all ten, silently costing the 26s scan) · plus the exactly-once and
opposite-sides classification legs the fixture now drives.

**One of those mutants survived, and the reason is the finding.** `--legs rtw` **never ran inside
`--test`**: its guard was `lsmod | grep -qiE '^rtw'`, and this script runs under `set -o pipefail`,
so `grep -q` exiting at the first match SIGPIPEs `lsmod` and the pipeline returns **141** — false —
on a node with four rtw modules loaded. The block I had just written and called *live coverage* was
skipped in silence, and the leg-filter mutant sailed through green. Written with `grep -c` and a
count compare, it runs and the mutant goes red. (`pipefail-turns-sigpipe-into-a-false-verdict`.)

The `--selfprobe` gate is the substantive one: a synthetic log with faults **planted** inside the
scan window must rank `mesh-wifiscan` LEAD at ≥3x, and a **phase-uniform control log** of the same
size must not (≤2x). A report that cannot fail on uniform noise is a decoration.

**One mutant survived the first round and is why there are six legs, not five.** Deleting the
`second < WIN` term from `--selfprobe` — i.e. counting a fault anywhere in a scan *minute* —
left the suite GREEN: planted faults sit early in the minute either way, so both the planted and the
control log agree with the mutant. *A gate can be vacuous because the fixture agrees with the bug.*
The seconds term is half the claim (a scan is ~seconds long inside a 60s minute), so it needed a
fixture that disagrees: the same wifiscan minutes at **second 45**, past the window. Correct code
reads ~0x; the mutant reads a full hit. Added, and the mutant now goes RED.

**Cost:** the new legs are free. `--test` measured **33.06s at HEAD** and **33.13s after** (the
`--selfprobe` null runs at a coarse `MESH_HW_FAULT_SHIFT_STEP=60` under test, 7s in real use).

That measurement surfaced a **pre-existing** fact first reported as an out-of-scope `[fyi]` — and it
turned out to be the thing blocking this work from landing at all, so it is **fixed here**:

> **A suite that cannot finish inside its runners' timeout is unlandable and unwirable.** Both
> `mesh-land:288` (the unattended `--autoland` arm) and `mesh-autowire:273` gate on
> `timeout 30 <tool> --test`. Measured RED: `timeout 30 … --test` → **rc=124**. The tool sits in
> cron already (autowire is add-only), so nothing looked broken — the runners simply record a
> failing test, and the fix above would have stranded silently every tick.

Profiled rather than guessed: **31.7s of the 33.4s was `--legs`**, none of it this task's code.
Two measurements decided the shape — `journalctl -k -b` is **376685 lines / 26.0s** on this node
(the rtw storm this very tool watches writes ~37k lines a day into it), and the cost is **proving
ABSENCE**: `-g rtw -n 1` returns in **0.01s** because the backwards read hits a match immediately,
while `-g iwlwifi -n 1` still scans the whole boot at **22.5s**. The old shape paid the full read
unconditionally and then re-piped the 376k-line result through `grep -c` **once per leg**.

- **modules first** — a loaded module settles presence with no journal read at all, and the report
  now prints `journal-lines=not-read[module settles presence]` rather than `0`, because a `0` on a
  demonstrably-present driver is a fabricated absence.
- **one journal pass for all still-undecided legs**, streamed into a single `awk` (`tolower()`, not
  gawk's `IGNORECASE` — this node's awk is mawk).
- **`--legs [leg…]`** — ask about one leg and pay only its cost (0.01s live). Unknown names exit 2
  rather than reading as absent hardware.

`--test` **33.37s → 2.28s** (`timeout 30` now rc=0). The full live report still costs ~26s, which is
the honest price of proving two INERT legs absent; the suite no longer pays it, driving the
classification from **exclusive** fixture sources (`MESH_HW_FAULT_LEGS_MODSRC`/`_JRNLSRC`) with the
live path covered separately by the now-free single-leg read.

## 5. What this does NOT establish

- No causal claim. `probe=self:` is a co-incidence token; the header says so twice and the report
  prints it as its closing line.
- `n=340` events from a log that only starts 2026-08-15 — the day the rtw leg was *wired*, not the
  day the dongle started failing (`a-sense-being-wired-reads-like-a-fault-beginning`). Every figure
  above is re-derivable with `--selfprobe` and none of them should be quoted later; the corpus moves.
- The 30s in-flight window is a *guess about runtime*, not a measurement of it. Faults at second 47
  of a scan minute read `none` today; if scans actually run longer than 30s, that is a miss.
  `MESH_HW_FAULT_PROBE_WIN` is the knob, and the honest next step is timing the scans.
- Nothing about the *other* four Zönnchen criteria (contingency, second-order observation of the
  mesh's own distinctions) — only self-reference vs other-reference, on one fault class.

## 6. The follow-on this earns (not taken here)

A `[task]` for the substrate owner, not for genome: **run the intervention.** Pause `mesh-wifiscan`
for a measured window with `--selfprobe` before/after, on a node whose *sole uplink* is the chip
being scanned. That is a substrate change (single-writer, `mesh-dms`, reachability measured from a
vantage the change cannot sever) and it is the only thing that turns 6.65x into a cause — or kills
it.
