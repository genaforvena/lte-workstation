# Self-ADINT expansion plan — 2026-09-07

## Scope and north star

Expand `~/self-adint` from a tested study skeleton into a complete, reproducible measurement
loop: establish what demand-stack information is exposed about the operator's own device, keep
unknowns and blind spots explicit, and only cross irreversible boundaries after the operator's
per-step go. This is a plan for the separate self-adint repository; nothing in this document
authorizes code, mesh wiring, router changes, seat onboarding, payment, letters, or GAID reset.

The governing privacy boundary is the disk: only the operator's device may become persistent
data; foreign requests may exist transiently to answer an auction but must not reach logs,
metrics, aggregates, panic output, or reports. The VM remains outside the mesh, and the router
remains read-only/instruction-only.

## Current evidence and expansion hypotheses

The 2026-09-07 review reports the safe implementation loop present: passive collection has two
ordered IP-echo attempts with explicit all-provider failure; the device importer is an explicit
read-only SCP handoff with provenance and no partial artifact; and `tools/adint-study` renders
measured, blocked, unknown, no-basis, and operator-gated states. Step 0 is measured, Step 1 has
the 2026-08-30 receiver corpus, Step 4-device is blocked on an operator-exported PCAPdroid CSV,
and Step 6 has no baseline. The separate repository has uncommitted 2026-09-07 study/runbook
work, so every implementation phase must begin by reconciling that working tree rather than
assuming the draft is complete.

Hypotheses to test, not conclusions:

1. **Entry-point hypothesis:** the device export can rank observed `bundle → demand-stack entry
   point` traffic, but cannot identify sale volume or mediation's downstream exchange. DNS and
   URL-path blind spots will produce `UNKNOWN`, not absence.
2. **Receiver safety hypothesis:** the Go receiver persists only target-IFA rows, never request
   bodies or foreign identifiers, while still serving a decoy bid and stopping at the hard spend
   cap.
3. **Exposure hypothesis:** a real passive bid-request corpus contains a non-empty, attributable
   audience/profile signal for the target device; an empty or hashed payload is a valid result,
   not a failed run.
4. **Vantage hypothesis:** RU/mobile and comparison vantages are sufficiently independent for a
   contrast, and any shared upstream or cached replay is detectable from provenance rather than
   treated as corroboration.
5. **Persistence hypothesis:** observed profile fields have a measurable retention/recovery curve;
   a last-seen time is only a right-censored lower bound, not a TTL claim.
6. **Intervention hypothesis:** a harmless, typical, uniquely marked input can distinguish a
   return path from code inertia, but only after passive baseline, payload-safety review, and the
   operator's explicit go.

## Sequenced work packages

### 0. Reconcile the implementation baseline (read-only first)

Inspect the separate repo's dirty diff, `PLAN.md`, the 2026-09-07 full-study review, runbooks,
receiver fixtures, and the last relevant commits. Record which draft changes are retained,
reverted, or superseded. Run the existing offline suite before changing behavior.

**Artifact:** a dated baseline note in `~/self-adint/docs/` containing git revision, dirty paths,
test commands/results, and the current `data/study-status.json` interpretation.

**Exit:** no ambiguous ownership of the existing 2026-09-07 changes; unrelated work remains
untouched.

### 1. Close the immediate device-lane blocker

Ask for exactly one complete PCAPdroid CSV export from the operator's device, with reachable host
and explicit device label. Use `tools/adint-device-capture --dry-run` first, then the read-only
pull/import. Do not drive Android UI, start/stop VPN capture, guess an address, or merge overlapping
exports without deduplication and provenance.

**Artifacts:** source SHA-256 manifest; append-only `device-observations.jsonl`; bundle-to-entry-
point TSV; coverage/overlap report; explicit blocked artifact if export or reachability is absent.

**Exit:** every row has source/device/time provenance, no foreign device is persisted, and the
status coordinator changes only from `BLOCKED_OPERATOR_EXPORT` to `MEASURED` when those artifacts
exist. A missing export remains a named blocker.

### 2. Make Step 1 a release-quality receiver gate

Run and, if necessary, tighten the Go receiver's corpus around the privacy and money boundaries:
target IFA, foreign IFA, absent IFA, malformed request, panic with foreign IFA in scope, win with
expanded price, win with zero/unexpanded price, cap crossing, and concurrent writes. Verify the
receiver's real HTTP path, not only pure functions. Keep raw request bodies out of access logs,
panic output, and metrics.

**Artifacts:** red-before-green mutation evidence; receiver JSONL corpus; win counter; first
non-zero-win alert; zero-price marker; spend-cap result; test transcript.

**Exit:** foreign rows are absent from every persistent artifact; target rows are present and
parseable; malformed/panic paths fail safely; both zero-price and non-zero spend are loud; cap
prevents further bidding; the full receiver suite is green.

### 3. Establish the passive baseline and report contract

Run the passive browser lane across its declared cells with independent egress evidence, provider
attempt order, timing, profile treatment, and per-site yield. Preserve `UNKNOWN` for provider,
coverage, payload, or attribution gaps. Separate exploratory data from holdout data before looking
at the result. Price the material before designing any reachability path for stranded data.

**Artifacts:** append-only passive ledger; corpus/schema validation report; per-cell egress and
coverage table; exploratory/holdout split manifest; baseline report with n, missingness, freshness,
and site-level denominators; generated public/private report distinction.

**Exit:** every headline has a denominator and vantage; no control/holdout leakage; a zero yield is
retained; all-provider failure is distinct from no demand; the report can be regenerated from disk.

### 4. Decide whether the active oracle is eligible

Only after Step 3, inspect whether the passive payload is empty or hashed and whether the return
vantage is independent of the injection path. Select a mark from the observed field distribution,
make it globally unique in its key space, and document why it is harmless downstream. Keep the
oracle one-sided: absence is `UNKNOWN`, not `NOT`; a positive requires an independent return path.

**Artifacts:** payload verdict (`empty_or_hashed`, or a named refusal); independence assessment;
mark-selection distribution and uniqueness proof; harm review; operator-go record tied to this
exact intervention; active-run ledger with censoring metadata.

**Exit:** if payload is readable, stop and ask the operator the specific next question instead of
 injecting; if eligible but no operator go exists, status is `READY_OPERATOR_GO`; if approved,
 every active record is attributable to the marked treatment and no active run silently falls back.

### 5. Measure persistence without overclaiming

For an approved intervention, sample repeated occasions at a declared cadence and model the
result as right-censored survival data. Separate true disappearance from no occasion, provider
failure, cache eviction, and overwritten marks. Use an independent holdout arm for negative
evidence; the healer/collector's own tape cannot prove its absence.

**Artifacts:** signed treatment/control schedule; event and run rows (including failed/refused
 attempts); freshness/occasion-rate table; retention lower-bound or survival estimate with censor
 flags; independent holdout report.

**Exit:** no TTL or recovery claim is published without censoring and occasion-rate fields; a
 missing row is rendered `UNKNOWN`; treatment and holdout remain separable.

### 6. Handle operator-gated branches separately

Keep seat onboarding/agreement/payment, outbound DSAR letters/mailbox, and GAID reset as distinct
branches. For each, prepare the cheapest reversible evidence and an exact operator question, but
do not execute the irreversible step. GAID reset is downstream of a measured passive baseline;
letters use only capture-derived facts; seat work records the chosen exchange and contract scope.

**Artifacts:** question/decision ledger; draft letter evidence blocks; baseline hash and reset
precondition; seat/contract checklist; explicit `GATED_OPERATOR_GO` status per branch.

**Exit:** no branch advances on a general project go; the operator can authorize one named step,
with its cost and rollback limits visible.

### 7. Publish reproducibility and handoff

Update the separate repo's index and reproduction guide only from artifacts that exist. Include
software revision, device label without secret material, source hashes, command lines, schema
versions, blind spots, and unresolved obligations. Keep private `data/` and node identifiers out
of committed public material. Post the adint board completion/yield line and write the handoff.

**Artifacts:** reproducible report bundle; schema/checksum manifest; redacted reproduction guide;
test transcript; status JSON; board line; `mesh-handoff adint` record.

**Exit:** a fresh checkout can run offline tests and regenerate the non-private report; every
unmeasured claim is labeled; the next action is one exact command or one exact operator question.

## Test matrix

| Surface | Green case | Red/mutation case | Required artifact |
|---|---|---|---|
| Device import | declared CSV imports with manifest | SCP failure, malformed CSV, wrong label, partial write | manifest + JSONL or explicit failure, never empty success |
| Privacy filter | target IFA persists | foreign/absent IFA reaches sink, panic/access log leaks body | receiver corpus and leak scan |
| Receiver protocol | valid bid/no-bid/win path | malformed JSON, panic, missing floor, cap crossed | HTTP transcript + JSONL |
| Money safety | non-zero win alerts once | zero/unexpanded price consumes alert latch; win storm crosses cap | alert, zero marker, counter |
| Passive egress | first provider works; second is fallback | both fail, stale echo, shared upstream | ordered attempt rows and `UNKNOWN` verdict |
| Profile arms | cold/warm treatment is visible per row | profile stamp deleted; warm profile applied to cold arm | arm ledger with age and split |
| Study status | artifacts yield `MEASURED` | missing artifact reads `UNKNOWN`/`BLOCKED`/`NO-BASIS`, never false success | `data/study-status.json` |
| Holdout | holdout remains unseen until lock | treatment leakage or post-hoc split | split manifest and audit |
| Active oracle | marked positive returns through independent path | no return, cached replay, shared vantage | active ledger with `UNKNOWN` and provenance |
| Persistence | repeated occasions and censor flags are recorded | no occasion misreported as deletion/TTL | survival/retention report |
| Publication | report rebuilds from committed method + allowed artifacts | private IDs, raw payload, or node secrets enter public tree | checksum/redaction audit |

## Risks and mitigations

- **Privacy leakage:** foreign IFA/body can escape through framework logs or panic recovery. Keep
  the parser-before-buffer boundary, disable body logging, test panic with foreign input, and scan
  every output artifact.
- **False demand inference:** an SDK/mediation hostname is not an exchange or sale volume. Call it
  a demand-stack entry point and preserve blind spots.
- **Vantage dependence and cache replay:** independent routing is a precondition for a positive;
  record egress and profile age on every row and use a holdout.
- **Silent fallback:** provider defaults, empty reports, and zero prices can look healthy. Make
  failed attempts, zero-price wins, and absent artifacts explicit and loud.
- **Irreversible contamination:** active marks, seat onboarding, letters, and GAID reset alter the
  baseline or create external obligations. Require exact per-step operator gates and finish the
  cheapest passive evidence first.
- **Selection and timing bias:** hour, geography, warm profile, and cell loss can split responses.
  Preserve cells, denominators, coverage, and declared exploratory/holdout boundaries.
- **Dirty-tree drift:** current 2026-09-07 work is uncommitted in `~/self-adint`. Reconcile before
  implementation and never overwrite unrelated changes.
- **Mesh boundary violation:** self-adint must remain a separate repo; no `mesh-*` tool, cron,
  reflex header, credentials, or Tailscale route may be added.

## Acceptance criteria for the expansion

The expansion is accepted only when all are true:

1. The device entry-point artifact is either measured from a complete operator export or explicitly
   blocked with the one missing action; no absent export is reported as no demand.
2. Receiver, importer, passive lane, and status coordinator tests pass, with mutation evidence for
   privacy leakage, silent fallback, zero-price alerting, and status misclassification.
3. Every report row has provenance, treatment/vantage, freshness or age, and an interpretable
   missingness state; headline claims have denominators and do not call mediation an exchange.
4. The payload gate, independence check, harmless-mark review, holdout split, and censoring model
   are artifacts before any active intervention.
5. Seat/payment, outbound letters, and GAID reset remain visibly gated per step, and no irreversible
   branch runs without the operator's exact go.
6. A clean reproduction path regenerates the public report without private `data/`, credentials,
   raw foreign traffic, node-specific identifiers, mesh wiring, or router mutation.
7. The final handoff cites the artifacts, tests, unresolved obligations, and one exact next action.

## Immediate next action

Reconcile the dirty `~/self-adint` tree, run its existing offline tests, then ask the operator for
one complete PCAPdroid CSV export and reachable host so Step 4-device can produce the first real
`bundle → demand-stack entry point` artifact.
