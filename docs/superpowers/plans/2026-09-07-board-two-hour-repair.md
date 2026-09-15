# Two-hour board coordination repair implementation plan

> **For agentic workers:** Use superpowers:executing-plans to execute these separate tasks. Hire is the operator-appointed coordinator and implementer; preserve exact original owners when settling their tasks.

**Goal:** Repair the task/dispatch/restoration gaps evidenced between 2026-09-07T21:36:38Z and 2026-09-07T23:36:38Z, with separately accountable Ledger tasks owned by hire.
**Architecture:** Existing board, hledger promise journal and mesh-task remain authoritative. Repair identity, delivery, owner progress and restoration boundaries in place; each task has its own artifact and acceptance evidence.
**Tech Stack:** Existing Bash/Python mesh tools, tmux, Git, hledger and filesystem task JSON.

## Scope and evidence

Frozen board: /home/mesh-home/.mesh/audits/board-20260907T233638Z.log (308 timestamped rows). 91 rows begin with [handoff], 87 with [fyi], 20 with [idle]; these counts do not classify nested targeted markers and do not by themselves prove wasted work.
Live follow-up evidence files: /home/mesh-home/.mesh/audits/board-20260907T233638Z-live-{ledger,staffing,dispatch,task-audit,git,haunt-context}.txt.
At first live check: 8 promises, 10 holds, 46 asks; ledger parity and replay agreement PASS. Staffing succeeds with 15 windows and 8 eligible workers. Semantic dispatch/progress failures coexist with arithmetic parity.
Already repaired within the interval: missing charters, stale worker-pool override and staffing census input failure. Historical PACE-SKIP was a measured governor hold; this audit does not authorize bypassing pacing.
The live Git defect is an additional follow-up finding, outside the frozen interval. The cause is not established.
Board coverage is the retained timestamped board interval; no completeness claim about missing private communications, eviction gaps, or unsynchronized clock events. Board clock UNSYNCED at 23:19:01 warns against treating lease times around restart as perfect elapsed-time measurements.

## Global constraints

- User explicitly assigned this repair program to hire; no extra execution-choice approval is needed.
- All eleven tasks below are separate one-step mesh-task chains owned by hire, with distinct short IDs to avoid current alias collisions. Original upstream tasks remain open until their own owner settles them.
- Execute one bounded task at a time; other repair tasks remain open, not falsely active. Use typed block + retry event and durable progress to move around a blocker.
- Before any shared code/object mutation, inspect current state and coordinate the writer. Preserve dirty/untracked files, index, WIP refs, local charters and other minds' work.
- Do not introduce an OOM-specific detector: operator correction at 22:57:16 requires generic task/progress continuity.
- Do not bypass spend, substrate, protected-role or communication-window gates.
- No test may write production board/measurement tapes. Establish hermetic isolation before exercising a suspected leaking test.
- Hire never impersonates witness/haunt/TG or writes their owner receipts. Hire does not access ~/.mesh/job* or operator job accounts.
- These are evidence-driven repair work packages; the exact patch is to be derived from the cited source and a failing fixture, not fabricated from the board alone.
- Each child completion artifact: /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-<NN>.md, including cause, changes/revision, test commands/results, source/deployed equality where applicable, live wiring/owner evidence, and remaining obligations.
- Shared repository recovery is first mutation priority. Once safe, implement each bounded patch, run its focused checks and coordinate landing through the existing writer; do not blindly commit all workspace changes.

## Execution order

01 first for repository mutation safety. Then 02 → 03; 05 and 04 together for continuity; 06 completes the old pilot. 07 reconciles outstanding intake. 09 precedes any 08 charter test. 10 and 11 are independent once code edits are safe.
All tasks are posted now so dependent work cannot disappear behind an unmaterialized plan. Hire starts 01 and reports the selected next task in durable progress; ownership of an open queue does not mean all eleven are running.

## Posting and start verification — 23:43–23:44Z

All eleven chain creation commands returned success. After materialization, mesh-promises --check passed parity, replay agreement and roster checks (19 open promises at that check); mesh-promises --balance showed eleven distinct hire liabilities. Frozen board SHA-256: 2e39284aa8f42a416827012dd5eb5ca624e55131b83799e7dde39e27e0da86e7.

Hire acknowledged msg:e7bd410e22e0019c at 23:43:45Z, posted the canonical ba260907-01-git/repair taking at 23:43:46Z, and supplied the next command at 23:43:54Z. The chain is active with lease until 2026-09-08T00:13:45Z; the live pane is inspecting Git damage. Receipt and full liability list: /home/mesh-home/.mesh/audits/board-20260907T233638Z-hire-receipt.txt.

Audit and assignment are complete. Repair results are not yet verified. No code repair, commit or push was performed by this audit; Git object corruption prevents an honest clean-worktree/commit claim. Next: hire preserves and repairs the object database under task 01, publishes its result artifact, then follows the dependency order above. Witness keeps the original staffing pilot obligation visible through task 06.

## 01-git: Preserve and recover the repository object database

Ledger: `ba260907-01-git/repair`; owner: hire; priority: P0.

Evidence: Live follow-up 23:37–23:39Z: git status fails with bad object HEAD; git cat-file cannot read HEAD; .git/objects/dc/edd2fa6b96040865b717c8849531ab2db2b0a6 is zero bytes. This is outside the frozen board interval and is not attributed to the earlier restart without evidence.

Files and state: scripts/mesh-land, scripts/mesh-genome-sync, scripts/mesh-wip-commit; .git object database (coordinate its writer).

Dependencies: First mutation priority; other tasks may inspect and coordinate while recovery proceeds.

- [ ] Inspect and reproduce the cited failure against the current source/deployed state; record whether it has already changed.
- [ ] Coordinate the existing landing/sync writer; preserve working files, index, refs, WIP refs and object evidence before repair. Inspect verified local bare anchors/peers for the exact missing object. Recover from a verified source or use an isolated verified checkout; never reset the shared worktree or discard stash/WIP. Establish the writer/cause if observable and report UNKNOWN otherwise.
- [ ] Add or strengthen a hermetic regression for the stated failure; see it fail on the broken behavior before applying the bounded repair. For coordination-only work, retain the actual owner receipt and artifact instead of writing a synthetic test.
- [ ] Acceptance: git cat-file -t HEAD returns commit; git status reads successfully; scoped fsck verifies the recovered reachable graph; before/after preservation inventory proves dirty and untracked work survived. Repair receipt names exact object/source, writer coordination, remaining corrupt objects and next action.
- [ ] Run the focused commands below plus the new regression; record exact outcomes. A nonzero/timeout is an unresolved result, not a PASS.

```bash
rtk proxy git cat-file -t HEAD
rtk proxy git status --short
rtk proxy git fsck --connectivity-only
```

- [ ] Write /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-01.md; update progress/typed block with exact next action and next update. Coordinate source/deployed verification and landing for code changes.
- [ ] As hire, settle only after acceptance: `MESH_TASK_ACTOR=hire mesh-task done ba260907-01-git repair /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-01.md "verified outcome with remaining obligations"`.

## 02-identity: Keep canonical task identity and closure consistent through Ledger dispatch

Ledger: `ba260907-02-identity/repair`; owner: hire; priority: P1.

Evidence: 21:37:43 and 21:38:40 full chain steps close; 22:24:09 and 22:47:19 truncated -tur/-wir aliases dispatch again; 22:24:40 and 22:48:05 genome spends turns rejecting them. Live mesh-dispatch --status still renders generic promise-opened prose and shortened keys. Ledger arithmetic passes but does not prove semantic identity.

Files and state: scripts/mesh-board, scripts/mesh-promises, scripts/mesh-dispatch, scripts/mesh-task, scripts/mesh-witness-promises; tests/test-mesh-task-ledger-sync.sh, tests/test-mesh-dispatch-hledger-gate.sh.

Dependencies: 01 for shared-repository code changes.

- [ ] Inspect and reproduce the cited failure against the current source/deployed state; record whether it has already changed.
- [ ] Trace the exact ID from chain JSON through journal account/metadata, board query, dispatch prompt, receipt and completion. Preserve full canonical task IDs and original instruction/artifact fields; reconcile historical aliases explicitly. Never let a shortened display key or UNKNOWN close a sibling obligation. Make witness receipt matching owner-qualified and canonical.
- [ ] Add or strengthen a hermetic regression for the stated failure; see it fail on the broken behavior before applying the bounded repair. For coordination-only work, retain the actual owner receipt and artifact instead of writing a synthetic test.
- [ ] Acceptance: Replay cited full-ID closure plus alias dispatch rows in an isolated fixture: no completed step is offered again, two shared-prefix siblings remain distinct, wrong-owner receipt cannot satisfy start, exact active step remains actionable. Live mesh-board and mesh-task agree on those chains after targeted reconciliation.
- [ ] Run the focused commands below plus the new regression; record exact outcomes. A nonzero/timeout is an unresolved result, not a PASS.

```bash
rtk proxy bash tests/test-mesh-task-ledger-sync.sh
rtk proxy bash tests/test-mesh-dispatch-hledger-gate.sh
rtk proxy mesh-promises --check
```

- [ ] Write /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-02.md; update progress/typed block with exact next action and next update. Coordinate source/deployed verification and landing for code changes.
- [ ] As hire, settle only after acceptance: `MESH_TASK_ACTOR=hire mesh-task done ba260907-02-identity repair /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-02.md "verified outcome with remaining obligations"`.

## 03-delivery: Resolve failed deliveries without replaying superseded work

Ledger: `ba260907-03-delivery/repair`; owner: hire; priority: P1.

Evidence: Seven genome delivery-failed rows at 21:37:01, 21:44:01, 21:49:01, 21:54:02, 22:00:03, 22:01:01, 22:02:01; witness/genome repeatedly recheck completed steps around 21:40–21:48. This establishes stale retry/backlog trouble, not universal present delivery failure.

Files and state: scripts/mesh-chat-deliver, scripts/mesh-tell, scripts/mesh-dispatch, scripts/mesh-board; ~/.mesh/tell-wal.log and delivery receipts.

Dependencies: 02 canonical join; coordinate with 06 so one bounded live pilot supplies both evidence sets.

- [ ] Inspect and reproduce the cited failure against the current source/deployed state; record whether it has already changed.
- [ ] Join the seven message IDs to original prompts, canonical tasks, current chain state, WAL outcomes and owner receipts. Retire only demonstrably superseded delivery attempts; retain the underlying still-open task. Distinguish posted, submitted, received, started and progress states; retry failed live work without duplicating active work. Preserve pacing and pending-reset gates.
- [ ] Add or strengthen a hermetic regression for the stated failure; see it fail on the broken behavior before applying the bounded repair. For coordination-only work, retain the actual owner receipt and artifact instead of writing a synthetic test.
- [ ] Acceptance: Produce a seven-row disposition table with exact evidence. Isolated refused/busy/reset delivery stays retryable; a stale prompt is suppressed after canonical completion. A bounded live delivery reaches an owner-authored receipt and fresh artifact, with failure/retry evidence; ACK alone does not settle work.
- [ ] Run the focused commands below plus the new regression; record exact outcomes. A nonzero/timeout is an unresolved result, not a PASS.

```bash
rtk proxy mesh-tell --replay -n 30 genome
rtk proxy mesh-tell --peek hire
```

- [ ] Write /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-03.md; update progress/typed block with exact next action and next update. Coordinate source/deployed verification and landing for code changes.
- [ ] As hire, settle only after acceptance: `MESH_TASK_ACTOR=hire mesh-task done ba260907-03-delivery repair /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-03.md "verified outcome with remaining obligations"`.

## 04-continuity: Make restart recovery resume progress, with bounded owner concurrency

Ledger: `ba260907-04-continuity/repair`; owner: hire; priority: P1.

Evidence: 22:52:29 reports durable records survived but ownership continuity failed. 22:57:16 explicitly requires generic recovery and rejects an OOM-specific detector. At 23:04 haunt takes three tasks; at 23:35 all leases expire. Live task-context/haunt.json has artifact, next_action and next_update null for all three.

Files and state: scripts/mesh-task, scripts/mesh-witness-promises, scripts/mesh-dispatch, scripts/mesh-handoff, scripts/mesh-codex-lifecycle, scripts/mesh-pane-consume; tests/test-mesh-task-audit-complete.sh, tests/test-mesh-witness-lifecycle.sh.

Dependencies: 02 identity; 05 task context; no OOM-specific implementation.

- [ ] Inspect and reproduce the cited failure against the current source/deployed state; record whether it has already changed.
- [ ] Use canonical open task + exact owner + fresh progress as the recovery input after any restart/death. Resume the owner's current bounded task or safely yield/reassign with a visible reason. Queue additional tasks rather than claiming all of them merely to silence audits. Preserve all pending task pointers across handoff/reset; route expiry to a corrective action and owner receipt rather than only an FYI. A renewed lease must identify meaningful progress or a typed block.
- [ ] Add or strengthen a hermetic regression for the stated failure; see it fail on the broken behavior before applying the bounded repair. For coordination-only work, retain the actual owner receipt and artifact instead of writing a synthetic test.
- [ ] Acceptance: Isolated restart between take and progress preserves all obligations, starts at most the configured allowed concurrency, and resumes one exact next action. Stale owner and wrong-owner cases do not fabricate progress. Observe a safe non-production restart/restore fixture plus live owner progress artifact and wired audit receipt. Do not kill production minds to test this.
- [ ] Run the focused commands below plus the new regression; record exact outcomes. A nonzero/timeout is an unresolved result, not a PASS.

```bash
rtk proxy bash tests/test-mesh-task-audit-complete.sh
rtk proxy bash tests/test-mesh-witness-lifecycle.sh
rtk proxy mesh-task audit
```

- [ ] Write /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-04.md; update progress/typed block with exact next action and next update. Coordinate source/deployed verification and landing for code changes.
- [ ] As hire, settle only after acceptance: `MESH_TASK_ACTOR=hire mesh-task done ba260907-04-continuity repair /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-04.md "verified outcome with remaining obligations"`.

## 05-workspace: Bind restoration and receipts to the task's repository and scope

Ledger: `ba260907-05-workspace/repair`; owner: hire; priority: P1.

Evidence: 22:58:49 closeout explicitly names /home/mesh-home/tiny-fleet. At 23:04:57 haunt instead cites /home/mesh-home/src/hyperhauntology_for_kids@811bd8d; 23:07:15 TG calls this recovery succeeded. The earlier 22:57:10 rejection used that unrelated release too.

Files and state: scripts/mesh-task, scripts/mesh-handoff, scripts/mesh-codex-context, scripts/mesh-dispatch; ~/.mesh/task-chains/tinyfleet-*.json and ~/.mesh/task-context/haunt.json; preserve node-local charter overrides.

Dependencies: Can coordinate immediately; integrate schema changes with 02/04 under one writer.

- [ ] Inspect and reproduce the cited failure against the current source/deployed state; record whether it has already changed.
- [ ] Carry expected repository, task scope, artifact path, current revision and next command in durable task context and prompts. Reconcile the specific Tiny Fleet rejection/receipts with haunt using the explicitly named repository. A general window charter must not silently replace task scope. Keep unrelated work and charters intact; obtain an owner correction and correct-repository progress.
- [ ] Add or strengthen a hermetic regression for the stated failure; see it fail on the broken behavior before applying the bounded repair. For coordination-only work, retain the actual owner receipt and artifact instead of writing a synthetic test.
- [ ] Acceptance: A two-repository fixture restores the explicitly targeted repo despite another default charter/worktree; wrong-repo receipt is visibly rejected as insufficient. Haunt produces a current Tiny Fleet artifact under /home/mesh-home/tiny-fleet and corrected task state. Hire coordinates, never posts as haunt.
- [ ] Run the focused commands below plus the new regression; record exact outcomes. A nonzero/timeout is an unresolved result, not a PASS.

```bash
rtk proxy mesh-task status tinyfleet-publishable-closeout-20260907
rtk proxy mesh-tell --peek haunt
```

- [ ] Write /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-05.md; update progress/typed block with exact next action and next update. Coordinate source/deployed verification and landing for code changes.
- [ ] As hire, settle only after acceptance: `MESH_TASK_ACTOR=hire mesh-task done ba260907-05-workspace repair /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-05.md "verified outcome with remaining obligations"`.

## 06-pilot: Complete the staffing pilot after its blocker was repaired

Ledger: `ba260907-06-pilot/repair`; owner: hire; priority: P1.

Evidence: 21:41:09 pilot blocked on missing adint charter; 22:36:02 and 22:41:27 report repaired census and pool. Yet 22:45:12 says ABANDONED and live chain still has an expired active witness step. Plan document retains BLOCKED plus appended repair narrative.

Files and state: docs/coordination-tg-presence-and-ledger-dispatch-20260907.md; ~/.mesh/task-chains/tg-presence-ledger-dispatch-20260907.json; tests/test-mesh-staffing.sh, tests/test-mesh-tg-dispatch-policy.sh.

Dependencies: 02/03; witness remains original pilot owner unless explicitly reassigned through supported workflow.

- [ ] Inspect and reproduce the cited failure against the current source/deployed state; record whether it has already changed.
- [ ] Coordinate the witness-owned pilot: recheck current census, run the missing bounded owner receipt/artifact and failed-delivery/retry arms with controlled fixtures, update the verdict from current evidence, and have the exact owner settle or type-block its existing step. Keep spend governor holds explicitly separate from broken delivery. Do not reopen already repaired missing-charter work.
- [ ] Add or strengthen a hermetic regression for the stated failure; see it fail on the broken behavior before applying the bounded repair. For coordination-only work, retain the actual owner receipt and artifact instead of writing a synthetic test.
- [ ] Acceptance: One pilot report links allowed and excluded staffing candidates, failure/retry outcomes, real owner start/progress/artifact, source/deployed parity and ledger checks. Existing pilot chain and document agree; no expired active pilot remains without a reason and retry event.
- [ ] Run the focused commands below plus the new regression; record exact outcomes. A nonzero/timeout is an unresolved result, not a PASS.

```bash
rtk proxy bash tests/test-mesh-staffing.sh
rtk proxy bash tests/test-mesh-tg-dispatch-policy.sh
rtk proxy mesh-staffing --json
rtk proxy mesh-task status tg-presence-ledger-dispatch-20260907
```

- [ ] Write /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-06.md; update progress/typed block with exact next action and next update. Coordinate source/deployed verification and landing for code changes.
- [ ] As hire, settle only after acceptance: `MESH_TASK_ACTOR=hire mesh-task done ba260907-06-pilot repair /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-06.md "verified outcome with remaining obligations"`.

## 07-intake: Turn actionable designs and aged detections into owned work

Ledger: `ba260907-07-intake/repair`; owner: hire; priority: P1.

Evidence: TG design tasks expire 21:45:12–13 and become ABANDONED 22:45:09–10; token accounting opens 22:33:07 but remains unowned. 22:03:09 repo/BIN drift and 22:28:40 explicit landing proposals lack visible corresponding task posts in the interval. 23:29:04 promises witness wiring verification; 23:35:19 repeats operator report of stuck dispatch. Live TG has four promises while communication windows are excluded from generic workers.

Files and state: scripts/mesh-witness-promises, scripts/mesh-board, scripts/mesh-task; docs/tg-operator-intake-design-20260907.md; existing design-audit, design-spec, token-usage and ask-answer-funnel chains.

Dependencies: 02/04; inspect archive for preexisting tasks before creating any.

- [ ] Inspect and reproduce the cited failure against the current source/deployed state; record whether it has already changed.
- [ ] Inventory each actionable design/ask/detection against canonical current tasks and owner receipts. Coordinate existing TG planning debts to completion or supported reassignment to an eligible implementer; preserve TG communication exclusion. Mint only missing implementation promises, keeping original ask references and explicit reasoned declines. Include follow-up disposition for 22:48:06 phaedra autoland strand and 23:19:06 devcd supervisor failure, verifying current recovery before proposing repairs. Hire must not access private job files/accounts; route any job-lane issue to its own owner.
- [ ] Add or strengthen a hermetic regression for the stated failure; see it fail on the broken behavior before applying the bounded repair. For coordination-only work, retain the actual owner receipt and artifact instead of writing a synthetic test.
- [ ] Acceptance: A table covers every cited row with existing/new task ID, owner, exact next action, expected artifact, closure criterion and start receipt or typed block. Periodic witness findings feed a live corrective queue and produce a visible owner action; board-only alerts cannot be counted as completed reconciliation. Never duplicate already settled proposals.
- [ ] Run the focused commands below plus the new regression; record exact outcomes. A nonzero/timeout is an unresolved result, not a PASS.

```bash
rtk proxy mesh-task audit
rtk proxy mesh-promises --check
rtk proxy mesh-promises --balance
```

- [ ] Write /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-07.md; update progress/typed block with exact next action and next update. Coordinate source/deployed verification and landing for code changes.
- [ ] As hire, settle only after acceptance: `MESH_TASK_ACTOR=hire mesh-task done ba260907-07-intake repair /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-07.md "verified outcome with remaining obligations"`.

## 08-charter: Make charter divergence actionable without erasing local overrides

Ledger: `ba260907-08-charter/repair`; owner: hire; priority: P2.

Evidence: haunt destination-divergent repeats from 22:20 through 23:35, often every five minutes. 22:41:27 explicitly identifies preserved local customization with staffing_rc=0. Missing charters were repaired; repeated unchanged divergence is not itself proof of broken restoration.

Files and state: scripts/mesh-charter-watch, tests/test-mesh-charter-watch.sh; charter/haunt.md and ~/.mesh/charter/haunt.md (read/coordinate override, never overwrite blindly).

Dependencies: 09 isolation before running charter tests; no node-local override replacement without coordination.

- [ ] Inspect and reproduce the cited failure against the current source/deployed state; record whether it has already changed.
- [ ] Classify required-input absence separately from an intentional local override. Preserve the override and record an owner-reviewed disposition for the actual difference. Board once on state/content change with a specific corrective task if needed; keep per-run liveness and continuing unresolved status on the reflex's own tape. Verify all roster charters including adint remain available after restoration.
- [ ] Add or strengthen a hermetic regression for the stated failure; see it fail on the broken behavior before applying the bounded repair. For coordination-only work, retain the actual owner receipt and artifact instead of writing a synthetic test.
- [ ] Acceptance: Repeated identical intentional divergence retains truthful per-run records but emits no repeated identical alert; a changed/missing/unreadable required charter emits a new actionable event; live staffing remains readable. Source and deployed script match and exactly one existing cadence stays wired.
- [ ] Run the focused commands below plus the new regression; record exact outcomes. A nonzero/timeout is an unresolved result, not a PASS.

```bash
rtk proxy bash tests/test-mesh-charter-watch.sh
rtk proxy mesh-staffing --json
```

- [ ] Write /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-08.md; update progress/typed block with exact next action and next update. Coordinate source/deployed verification and landing for code changes.
- [ ] As hire, settle only after acceptance: `MESH_TASK_ACTOR=hire mesh-task done ba260907-08-charter repair /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-08.md "verified outcome with remaining obligations"`.

## 09-test-isolation: Prove charter tests cannot write the real board

Ledger: `ba260907-09-test-isolation/repair`; owner: hire; priority: P1.

Evidence: 22:37:09, 22:37:18 and 22:37:52 live board entries name /tmp/tmp.../home fixture destinations as witness. Current source now sets a fixture HOME and chat stub; that may already repair the old leak, so verify rather than assume it is still unfixed.

Files and state: scripts/mesh-charter-watch, tests/test-mesh-charter-watch.sh; scripts/mesh-chat and board archive only for read-only forensic checks.

Dependencies: 01 before code edits; must pass before 08 verification.

- [ ] Inspect and reproduce the cited failure against the current source/deployed state; record whether it has already changed.
- [ ] Reconstruct which source/deployed test invocation emitted fixture rows. Build a hermetic regression around the real wrapper under a cron-like environment and an adversarial PATH, with a canary 'live board' outside the fixture. Ensure all child tools/log paths stay inside the fixture. Preserve historical board rows and mark the three timestamps as test-origin via one correction after proof; never delete the archive.
- [ ] Add or strengthen a hermetic regression for the stated failure; see it fail on the broken behavior before applying the bounded repair. For coordination-only work, retain the actual owner receipt and artifact instead of writing a synthetic test.
- [ ] Acceptance: The historical leaking variant makes the isolation assertion fail; repaired source/deployed wrappers pass and write zero canary live-board or liveness rows. If the code is already repaired, ship only the missing regression/evidence and correction. Run no suspected leaking variant against production tapes.
- [ ] Run the focused commands below plus the new regression; record exact outcomes. A nonzero/timeout is an unresolved result, not a PASS.

```bash
rtk proxy bash tests/test-mesh-charter-watch.sh
```

- [ ] Write /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-09.md; update progress/typed block with exact next action and next update. Coordinate source/deployed verification and landing for code changes.
- [ ] As hire, settle only after acceptance: `MESH_TASK_ACTOR=hire mesh-task done ba260907-09-test-isolation repair /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-09.md "verified outcome with remaining obligations"`.

## 10-evidence: Keep cited verification artifacts available across restart and review

Ledger: `ba260907-10-evidence/repair`; owner: hire; priority: P2.

Evidence: 23:15:51 discover cites /tmp/discover-upower-20260907T231541Z.txt; 23:24:16 health says it has vanished and cannot revalidate bytes. 21:47:13 also cites a /tmp/discover battery artifact. A new measurement does not recover the old bytes.

Files and state: scripts/mesh-task, scripts/mesh-handoff, scripts/mesh-codex-lifecycle; charter/discover.md, charter/health.md; existing durable ~/.mesh/knowledge and repository evidence conventions.

Dependencies: Coordinate artifact schema with 04/05; cited command verifies this audit artifact, implementer must also verify its new durable artifact.

- [ ] Inspect and reproduce the cited failure against the current source/deployed state; record whether it has already changed.
- [ ] Use the existing durable artifact locations for externally cited findings; record hash, size, timestamp and relevant boot/revision before posting. Preserve the evidence reference through handoff. Mark vanished historical artifacts unverifiable and distinguish replacement observations. Avoid retaining credentials, bulk raw private tapes or unnecessary sensor data.
- [ ] Add or strengthen a hermetic regression for the stated failure; see it fail on the broken behavior before applying the bounded repair. For coordination-only work, retain the actual owner receipt and artifact instead of writing a synthetic test.
- [ ] Acceptance: A controlled temporary-workspace cleanup leaves the promoted evidence readable and hash-identical; handoff restoration resolves that same artifact. Missing artifact reports UNKNOWN/unverifiable, never reconstructed PASS. At least one new real discovery/review receipt demonstrates the durable path.
- [ ] Run the focused commands below plus the new regression; record exact outcomes. A nonzero/timeout is an unresolved result, not a PASS.

```bash
rtk proxy sha256sum /home/mesh-home/.mesh/audits/board-20260907T233638Z.log
```

- [ ] Write /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-10.md; update progress/typed block with exact next action and next update. Coordinate source/deployed verification and landing for code changes.
- [ ] As hire, settle only after acceptance: `MESH_TASK_ACTOR=hire mesh-task done ba260907-10-evidence repair /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-10.md "verified outcome with remaining obligations"`.

## 11-empty-pane: Treat empty or timed-out dashboards as observation failures

Ledger: `ba260907-11-empty-pane/repair`; owner: hire; priority: P1.

Evidence: 23:11:40 and 23:24:18 health handoffs repeat mesh-dash --once check timeout at 12s and defer investigation. 23:24:36 sound interprets an empty state stream as no available action. A failed observation cannot establish an idle/healthy state.

Files and state: scripts/mesh-dash, scripts/mesh-pane-consume, scripts/mesh-witness-promises; charter/health.md, charter/sound.md; relevant dashboard producers.

Dependencies: 01 for code changes; health/sound owners supply live verification.

- [ ] Inspect and reproduce the cited failure against the current source/deployed state; record whether it has already changed.
- [ ] Capture return code, elapsed time, stdout/stderr and producer freshness for bounded health/sound reads. Locate the dependency causing empty/time-out behavior and repair it or publish explicit UNKNOWN with an owned retryable task. Keep the top-pane measurement lane algorithmic/read-only for witness; route repair via the board. Suppress repeated no-change LLM wakeups only when observation succeeded.
- [ ] Add or strengthen a hermetic regression for the stated failure; see it fail on the broken behavior before applying the bounded repair. For coordination-only work, retain the actual owner receipt and artifact instead of writing a synthetic test.
- [ ] Acceptance: Empty success, timeout, missing producer and real quiet output are distinct fixture states; a failed read never produces a green idle claim. One bounded live health and sound read produces meaningful output or an explicit typed unresolved block with owner and next update. Verify renderer and consumer wiring, not just unit classifier tests.
- [ ] Run the focused commands below plus the new regression; record exact outcomes. A nonzero/timeout is an unresolved result, not a PASS.

```bash
rtk proxy timeout 15 mesh-dash --once check
rtk proxy timeout 15 mesh-dash --once sound
```

- [ ] Write /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-11.md; update progress/typed block with exact next action and next update. Coordinate source/deployed verification and landing for code changes.
- [ ] As hire, settle only after acceptance: `MESH_TASK_ACTOR=hire mesh-task done ba260907-11-empty-pane repair /home/mesh-home/.mesh/audits/board-20260907T233638Z-result-11.md "verified outcome with remaining obligations"`.
