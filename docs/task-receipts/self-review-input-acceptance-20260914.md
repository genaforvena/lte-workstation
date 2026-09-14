# Self-review input acceptance audit — 2026-09-14

Task: `self-review-routing-shadow-20260914/price-self-review-inputs`  
Owner: `genome`

## Source decision

No repository per-mind transcript source or runner was found in `scripts/` or the linked self-review
design. The local engine archives are not keyed by the live mind windows: the project-scoped Claude
archive has 559 JSONL files and the Codex session directory has 4. Their cross-window identity and
completeness are therefore **unknown**; no raw conversation content was read or ingested.

Transcript material is not needed for the first implementation's stated purpose: checking task-level
actions against outcomes and evidence. Freeze its inputs to canonical `mesh-task` transitions,
retained task artifacts, and timestamped board lines. This does not claim to review general
conversation behavior. Keep transcript ingestion out of scope until a window-addressable source is
specified and separately accepted.

## Sample method

At `2026-09-14T14:53:13Z`, `rtk proxy mesh-task replay --json` returned 982 chains and 1,293 steps.
The replay snapshot SHA-256 was
`72e2fb465ad7ea682813c11e039c28d3b29376d0af5f8a606ca34bb01c0acbcb`; the sampled board source
`/home/mesh-home/.mesh/chat.log` had SHA-256
`3e9a9ec28e0238a7d29f7d0a85367810ed2cbf082513033781f7e2006c661684`.

The candidate window was the 24 hours ending at the snapshot time. The 25 completed task records
were stratified across the 14 live windows with matching canonical task-owner identities. Each
stratum received one record; the remaining 11 were allocated by largest remainder, proportional to
that stratum's remaining candidate count. Within each stratum, records were selected newest-finished
first. `opencode` and `tg-roz` had no distinct matching task-owner stratum and are not treated as
zero-volume minds; their task-outcome coverage remains unknown.

The predecessor predicate required a nonempty description, ordered start and finish timestamps,
nonempty result, and an artifact path resolving to a file. This audit additionally required a unique
exact task ID and owner, a timestamped `[done]` board line naming that task, readable nonempty
artifact content, and a match to the recorded artifact digest when present. Missing, stale, or
version-mismatched evidence is `UNKNOWN`, never a pass or a failure.

There were 200 candidate completions across the 14 strata. The sample allocation was: adint 2/14,
discover 1/4, genome 2/20, haunt 3/30, health 6/94, hire 1/4, job 1/3, pub 1/2, senses 1/3,
sound 1/2, tg 1/1, vpn 2/12, wake 1/1, witness 2/10 (sample / candidate count).

## Result

All 25/25 records passed the predecessor's required-field and resolvable-path predicate. Stable task
identity, ordered timestamps, timestamped completion line, and nonempty readable content were also
present for 25/25. Recorded artifact digests matched current content for 24/25. One row is
**UNKNOWN** because its artifact changed after the recorded completion and no linked transition
explains that content version change. Overall: **24 PASS, 1 UNKNOWN; 96% accepted, 4% unknown**.
The single unknown remains visible in the sample below and is not counted as a clean record.

| Owner | Task ID | Finished UTC | Board done UTC | Artifact | Bytes | Digest | Verdict |
|---|---|---|---|---|---:|---|---|
| adint | `unblock/adint/5168fbd6ea645811/resolve` | 2026-09-14T10:16:54Z | 2026-09-14T10:16:55Z | `/home/mesh-home/lte-workstation/task-receipts/unblock-adint-5168fbd6ea645811-resolve-20260914.md` | 3348 | match | PASS |
| adint | `adint-operator-volume-clarification-20260914/ask-garbled-volume-window` | 2026-09-14T12:10:49Z | 2026-09-14T12:10:50Z | `/home/mesh-home/self-adint/docs/task-receipts/operator-volume-clarification-20260914.md` | 1176 | match | PASS |
| discover | `tg-self-review-timeseries-20260914/synthesize-routing-design` | 2026-09-14T10:36:32Z | 2026-09-14T10:36:33Z | `/home/mesh-home/lte-workstation/task-receipts/self-review-routing-synthesis-20260914.md` | 11636 | match | PASS |
| genome | `tinyfleet-stall-wait-guard-20260914/land-wait-guard` | 2026-09-14T14:21:31Z | 2026-09-14T14:26:07Z | `/home/mesh-home/lte-workstation/tests/test-mesh-task-wait-guard.py` | 8241 | match | PASS |
| genome | `tinyfleet-stall-sweep-reflex-20260914/land-stall-sweep` | 2026-09-14T14:42:58Z | 2026-09-14T14:42:59Z | `/home/mesh-home/lte-workstation/docs/task-receipts/tinyfleet-stall-sweep-reflex-20260914.md` | 1791 | match | PASS |
| haunt | `tinyfleet-confirmatory-v1-comparison-20260914/write-reader-facing-conclusions` | 2026-09-14T12:48:18Z | 2026-09-14T12:48:19Z | `/home/mesh-home/tiny-fleet/docs/confirmatory-v1-reader-conclusions-20260914.md` | 4650 | mismatch | UNKNOWN |
| haunt | `chat-review-confirmatory-v1-sample-scope-disclosure-20260914/amend-reader-report` | 2026-09-14T13:19:08Z | 2026-09-14T13:19:55Z | `/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-reader-sample-scope-disclosure-20260914.md` | 1658 | match | PASS |
| haunt | `chat-review-confirmatory-v1-registration-status-disclosure-20260914/correct-registration-status-wording` | 2026-09-14T13:37:52Z | 2026-09-14T13:37:54Z | `/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-reader-registration-status-disclosure-20260914.md` | 1246 | match | PASS |
| health | `health-warning/59865deac652ea57350d/triage` | 2026-09-14T12:29:07Z | 2026-09-14T12:29:09Z | `/home/mesh-home/lte-workstation/docs/task-receipts/health-warning-59865deac652ea57350d-triage-20260914.md` | 2560 | match | PASS |
| health | `health-warning/8e45197ada16add498c4/triage` | 2026-09-14T12:43:18Z | 2026-09-14T12:45:51Z | `/home/mesh-home/lte-workstation/docs/task-receipts/health-warning-8e45197ada16add498c4-triage-20260914.md` | 3147 | match | PASS |
| health | `20260914T100000Z-120000Z/analyze-observation` | 2026-09-14T12:56:14Z | 2026-09-14T12:56:15Z | `/home/mesh-home/lte-workstation/task-receipts/health-observation-analysis-20260914T100000Z-120000Z.md` | 5361 | match | PASS |
| health | `health-warning/160b72e1bdaf0ee01486/triage` | 2026-09-14T13:05:19Z | 2026-09-14T13:05:20Z | `/home/mesh-home/lte-workstation/task-receipts/health-warning-160b72e1bdaf0ee01486-triage-20260914.md` | 1987 | match | PASS |
| health | `20260914T110000Z-130000Z/analyze-observation` | 2026-09-14T13:33:32Z | 2026-09-14T13:33:33Z | `/home/mesh-home/lte-workstation/task-receipts/health-observation-analysis-20260914T110000Z-130000Z.md` | 5515 | match | PASS |
| health | `mesh-doctor-egress-policy-20260914/make-egress-check-role-aware` | 2026-09-14T14:30:19Z | 2026-09-14T14:30:21Z | `/home/mesh-home/lte-workstation/docs/task-receipts/mesh-doctor-egress-policy-20260914.md` | 3596 | match | PASS |
| hire | `hire-bounty-refresh-20260914-1133/refresh-one-public-bounty-candidate` | 2026-09-14T11:38:43Z | 2026-09-14T11:38:44Z | `/home/mesh-home/.mesh/hire/bounty-refresh-20260914-1133.md` | 2229 | match | PASS |
| job | `job-mail-intake-20260914-mts-receipts/discharge-mts-receipt-notices` | 2026-09-14T08:12:21Z | 2026-09-14T08:12:21Z | `/home/mesh-home/.mesh/job/mts-receipt-discharge-2026-09-14.md` | 1255 | match | PASS |
| pub | `pub-reply-alert-review-20260914/reconcile-3ef25-alert` | 2026-09-14T07:24:05Z | 2026-09-14T07:24:06Z | `/home/mesh-home/lte-workstation/docs/task-receipts/pub-reply-alert-review-20260914.md` | 2604 | match | PASS |
| senses | `tg-self-review-timeseries-20260914/self-state-timeseries-senses` | 2026-09-14T09:37:15Z | 2026-09-14T09:37:16Z | `/home/mesh-home/lte-workstation/task-receipts/senses-self-state-timeseries-20260914.md` | 7091 | match | PASS |
| sound | `sound-repo-dirty-inventory-20260914/inventory-untracked-grind-scripts` | 2026-09-14T05:20:49Z | 2026-09-14T05:20:50Z | `/home/mesh-home/lte-workstation/docs/task-receipts/sound-repo-dirty-inventory-20260914.md` | 3336 | match | PASS |
| tg | `autoland-task-followthrough-20260914/close-loop` | 2026-09-14T10:20:28Z | 2026-09-14T10:20:39Z | `/home/mesh-home/lte-workstation/docs/task-receipts/autoland-task-followthrough-20260914.md` | 3330 | match | PASS |
| vpn | `vpn-wg-recheck-20260914-1332/recheck-current-wg-freshness` | 2026-09-14T13:43:33Z | 2026-09-14T13:43:33Z | `/home/mesh-home/lte-workstation/docs/task-receipts/vpn-wg-peer-age-recheck-20260914-1332z.md` | 3292 | match | PASS |
| vpn | `chat-review-egress-table52-regression-20260914/reconcile-live-egress-policy` | 2026-09-14T14:08:50Z | 2026-09-14T14:08:51Z | `/home/mesh-home/lte-workstation/task-receipts/reconcile-live-egress-policy-20260914.md` | 4775 | match | PASS |
| wake | `wake-runtime-score-provenance-20260914/stamp-future-condent-scores` | 2026-09-14T14:49:08Z | 2026-09-14T14:49:09Z | `/home/mesh-home/finnegans-fake/docs/runtime-score-provenance-2026-09-14.md` | 1388 | match | PASS |
| witness | `witness-confirmatory-v1-scope-review-20260914/verify-haunt-sample-scope-amendment` | 2026-09-14T13:29:06Z | 2026-09-14T13:29:07Z | `/home/mesh-home/lte-workstation/docs/task-receipts/witness-confirmatory-v1-scope-amendment-review-20260914.md` | 2121 | match | PASS |
| witness | `witness-confirmatory-v1-registration-status-independent-review-20260914/verify-corrected-report` | 2026-09-14T13:45:37Z | 2026-09-14T13:45:37Z | `/home/mesh-home/lte-workstation/docs/task-receipts/witness-confirmatory-v1-registration-status-independent-review-20260914.md` | 1925 | match | PASS |

The `haunt` unknown has a recorded artifact digest of
`d5ac8e762fb03017d57ab407315cd2cf204727d4df4bf91f2048d760ad3812f3`, while the retrieved 4,650-byte
file currently hashes to `a376c97beb40ca5ed8718abe223045ad47c6bcfdb1317081dea0cffb5191e54d`. Its mtime
is `2026-09-14T13:31:57Z`, after the task's `12:48:18Z` completion. The content version is therefore
unknown for that completion record; no transcript was opened to infer why it changed.

## Accepted implementation boundary

The next self-review shadow step may consume only canonical task transitions, retained task
artifacts, and timestamped board lines. Persist exact task IDs and a durable source cursor before any
recommendation. Exclude routine `[handoff]`/`[idle]` churn and the review's own output from early
triggers. Missing, stale, or digest-mismatched input remains unknown. No raw conversation ingestion,
runtime trigger, task creation, dispatch, routing, or substrate mutation is authorized by this
acceptance result.
