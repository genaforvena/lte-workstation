# LITERATURE (applied): the INTERPRETANT — landing the triadic check, and the half that makes it honest

**Area:** biosemiotics — Peirce's triadic sign, applied to `mesh-doctor`
**Angle:** landing a 2026-06-20 PROPOSAL (`knowledge/review-biosemiotics-interpretant-gap-2026-06-20.md`)
**Reviewer:** genome mind · 2026-08-10 · task `task:mesh-doctor`
**Artifact:** `scripts/mesh-doctor` (+193/-23, uncommitted — steward lands from the tree)

## What the task asked, and what was already there

The board task said: *land the interpretant-check design into `scripts/mesh-doctor` — a WARN-only
consumer-side check sibling to orphan/inverse-orphan; flag a dead vehicle only if NO external reader
AND no self-consumption by its own future runs; the temporal-self-reference exclusion is
load-bearing.*

**The sibling already existed** — the `umwelt check` (state producers with no reader in `scripts/`,
Ay & Löhr's Merkwelt-without-Wirkwelt framing), added after the proposal was written. So the task as
filed was half-stale. It was **not** rejected, because the half it named as load-bearing was exactly
the half that was missing, and because the check could not see either of the two dead vehicles the
review had verified by hand. Both are now fixed.

## Three defects, each measured

**1. The check was blind to 70% of the emitter population — including both verified cases.**
Two `.mesh/` naming conventions are live in the genome: `.foo.state` and `.foo-state`. The slug
regex `(?<=\.mesh/)\.[a-zA-Z0-9_.-]+\.state` only ever matched the first. `mesh-diskio` writes
`.diskio-state` and `mesh-wifi-quality` writes `.wifi-quality-state` — the **two cases the
2026-06-20 review named as robustly verified dead vehicles** — so the check built to catch that
class was structurally incapable of seeing either. Emitters seen: **64 → 210**.

A second blindness rode along: the mesh dir is routinely already in a variable
(`STATE="$MESH_DIR/.reclaim-mode.state"`, python `os.path.join(MESHDIR, ".witness-analyze.state")`),
so requiring a literal `.mesh/` meant those tools were visible **only when some comment happened to
spell the full path out**. `mesh-witness-analyze`'s docstring did; its visibility to the check was an
accident of prose.

**2. The temporal interpretant was missing — the review's own named trap.**
Peirce's infinite semiosis lets the interpretant be *the same system at a later time*: a tool that
writes state now and reads it back next run (edge, debounce, rate baseline) has closed a real loop.
Without that rule the check is a noise generator — the review's hand scan flagged 12/33 and disowned
its own number for this reason. Measured live: **62 producers with no external interpretant, 49 of
them self-consuming, 13 real dead vehicles.** The exclusion removes 79% of the candidate set. It is
not a refinement; it is the difference between a WARN that means something and a backlog.

**3. Writing the finding into the check silenced the finding.**
The reader scan grepped the RAW tree. Documenting `.diskio-state` and `.wifi-quality-state` in
mesh-doctor's own comment made **mesh-doctor their reader** and dropped both from the list — caught
only because the numbers moved the wrong way after a comment-only edit. A comment is not a channel.
The invoke scan was already stripped; the reader scan now uses the same corpus. Same class of trap,
same day, in `mesh-writeback-debt`: the only mention of `mesh-diskio` anywhere outside itself is a
**comment**, so its "invoker" was prose too.

## The self-consumption detector (what it does and does not claim)

Occurrence-level, not a line grep. Each occurrence of the state var is judged by what immediately
precedes it: `>`/`>>` = write (skipped), `<` = read, otherwise a reader command word earlier on the
line = read. A line grep both mis-fires on `cat foo > "$STATE"` and dies on the `|` inside
`[ -f "$STATE" ] && prev="$(cut -d'|' -f1 "$STATE")"` (mesh-audio-route, a real miss).

Three deliberate boundaries:

- **A read inside the tool's own `--test` does not count.** `mesh-heat-source` and
  `mesh-battery-energy` `stat` their live artifact there solely to assert the fixture did *not*
  stamp it; counting that would let a write-only sense earn a temporal interpretant from its own
  harness — the test forging the evidence it exists to check.
- **One level of function indirection is followed.** The genome hands state paths to helpers
  (`read_prev_label "$STATE"` in mesh-mesh-state, `load_nudge_state "$STATE_FILE"` in
  mesh-sweep-rollcall-proposes) and the read happens on the helper's `local f="$1"`. Both were real
  false dead-vehicles before this leg. Depth stays at one; deeper chains fall through to a WARN.
- **`[ -f "$STATE" ]` alone is not consumption.** Existence is not content.

**Known false-negative bias, stated rather than hidden:** an operator-facing `--state` / `--count`
dump (`mesh-wifi-contention:107`, `mesh-voice-count:218`) reads as self-consumption and suppresses
the flag, even though nothing invokes those subcommands. Distinguishing them would key on whether
the `cat` sits on the arg-dispatch line or the line below it — a verdict that would depend on the
author's line breaks. For a WARN-only check, under-flagging is the safe error; `# umwelt-ok:` stays
the explicit hatch in the other direction.

## Live result

```
interpretant check (state producers with no reader, no invoker and no self-consumption)
  210 declared emitters → 62 with no external interpretant → 49 self-consuming → 13 dead vehicles
```

`mesh-battery-energy · mesh-diskio · mesh-guitar-watch · mesh-heat-source · mesh-mem-guard ·
mesh-note3-ambient · mesh-note3-prox · mesh-phone-audio · mesh-pressure · mesh-reclaim-mode ·
mesh-sim-state · mesh-swap-drain · mesh-thermal-zone`

No coverage regression: every one of the 12 producers the old logic flags on the same corpus is
still in the union (1 dead — `mesh-heat-source` — and 11 reclassified as self-consuming). The check
loop costs ~3.7s before, ~6.5s after, inside a tool whose full run is minutes.

**`mesh-wifi-quality` — the review's second verified case is STALE, and this is a correction, not a
pass.** It is invoked by `mesh-lan-jitter`, `mesh-bt-link`, `mesh-netrate`, `mesh-wifi-mimo` and
`mesh-net-triage`, and it self-consumes `STATE_FILE` as the delta/dt rate baseline
(`mesh-wifi-quality:236-237`). It was remediated between 2026-06-20 and now. `mesh-diskio` was not.

**Side finding, NOT fixed — a declared artifact with no writer.** `mesh-phone-audio:3` declares
`# doctor-artifact: $HOME/.mesh/.audio-state 3600 phone` and `:27` assigns `STATE`, and the file is
never written anywhere in the tool. `~/.mesh/.audio-state` does not exist on this node. The artifact
check does not surface it because its `phone` reach gate renders the row n/a while the phone is
down — a permanently-n/a row hiding a permanently-absent artifact. Owner call for senses; filed
separately rather than patched here.

## Gates seen RED

Six mutants, each run from a scratch copy, each red with the message naming its own defect:

| mutant | red on |
|---|---|
| slug regex narrowed back to `.state` | `.x-state` form missed |
| declaration-line filter removed | a state path in prose read as a declared output |
| `--test` block not stripped | a read inside `--test` earned a temporal interpretant |
| function-hop leg removed | read one hop away missed |
| `um_self_reads` always true | write-only producer read as self-consuming |
| reader scan on the raw corpus | a comment naming the slug counted as a reader |

The fixtures drive the **real** `umwelt_slug`/`um_self_reads`. The block they replace
re-implemented the slug grep inline — it asserted a copy of the detector, which is why the narrow
regex survived for months behind a green test. `--test` 1.02s (was 0.33s).

## Not taken, and why

- **`.log` emitters.** The review said `.state`/`.log`. A log is read by dashes, `tail`, humans and
  cron redirection; reader-detection by basename has no purchase on it and the result would be a
  flood, not a signal. State files have one declared writer and a grep-able path; logs do not.
- **Remediating the 13.** Giving `mesh-diskio` et al. an interpretant is a senses-lane disposition
  call (what *should* consume a disk-IO rate), exactly as the 2026-06-20 review routed it. The check
  names them; it does not force-wire a consumer.

## Sources

- Tony Jappy, *Biosemiotics and Peirce*, Language and Semiotic Studies / De Gruyter 2023,
  doi:10.1515/lass-2023-0011 — the triadic sign; the interpretant as constitutive third relate.
- Peirce, infinite semiosis (the interpretant becomes a new sign) — the ground for the
  temporal-self-reference exclusion.
- Ay & Löhr, *The Umwelt of an Embodied Agent — A Measure-Theoretic Definition*, arXiv:1603.08389 —
  the Merkwelt/Wirkwelt framing already cited by the existing check.
- `knowledge/review-biosemiotics-interpretant-gap-2026-06-20.md` — the proposal this lands.
