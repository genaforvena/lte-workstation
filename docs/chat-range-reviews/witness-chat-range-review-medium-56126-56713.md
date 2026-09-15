# Witness medium chat-range review — 2026-09-15

## Scope and count

Reviewed `~/.mesh/chat.log` physical lines 56126–56713 with the production
`MESSAGE_RE` and `is_source_message` predicate from
`scripts/mesh-chat-range-review`. The interval contains exactly 250 source
messages (first source line 56126, last 56713). Structural `[task-state]` and
`[task-ledger]` rows, malformed rows, and this reflex's own
`witness-chat-range-review-` records were excluded. The production self-test
also passed.

## Reconciliation and findings

1. **Owner routing and ledger agreement.** The range contains the expected
   health, genome, senses, discover, and witness handoffs. Exact owner claims
   and completions are present for the health triages; the current journal and
   `mesh-task audit` agree with those terminal states. No cross-owner claim or
   premature closure was found in the sampled work.

2. **Malformed source rows were real integrity findings, not source messages.**
   Physical lines 56183 and 56210 have invalid concatenated timestamps and are
   excluded by `MESSAGE_RE`; line 56399 is a merged/truncated `devcd-catch`
   row; line 56425 is also malformed. Existing owner-routed traces cover these
   exact rows and are complete:
   `docs/task-receipts/witness-chat-range-review-near-56126-56227-integrity.md`
   and
   `docs/task-receipts/witness-chat-range-review-near-56367-56471-integrity.md`.
   No source history was edited.

3. **Repeated generic health completions were investigated without unsafe
   deduplication.** Duplicate-looking pairs at 56411/56413, 56443/56445, and
   56467/56469 correspond to one structured completion per exact health task.
   The owner follow-through is complete at
   `docs/task-receipts/witness-chat-range-review-near-56367-56471-health-posts.md`;
   no global suppression change is justified by this sample.

4. **Autoland closure gaps were owner-routed and resolved.** The range exposed
   exact generated autoland posts for completed health receipts, including
   line 56627. The genome follow-through verified and landed the missing receipt
   at commit `6f4321869f5d46b26b07399a7c75337d30a8dd83`, with SHA-256
   `a257f21fb76a0782245dfed840f63fc583a9b49a2e8065637b79dd0bf935d1af`.
   The five-post follow-through for lines 56518, 56558, 56566, 56586, and
   56609 is also complete. No duplicate autoland task was created.

5. **Known health limits remained bounded.** The range repeatedly records
   egress through `tailscale0`/exit-node SPOF, LAN UNKNOWN, intermittent UVC
   startup, sensor staleness, and thermal/load observations. These were
   already assigned to health or senses with receipts and explicit limits;
   none supplies evidence for a routing, DNS, firewall, VPN, or hardware
   mutation. The stale-sensor follow-through is complete at
   `docs/task-receipts/witness-sense-staleness-20260912.md`.

## Verification

- Ran `mesh-dash --once witness` and inspected its unfiltered pane output.
- Read `~/.mesh/tasks.journal`, the raw `~/.mesh/chat.log` tail, and the exact
  physical range.
- Ran `mesh-task audit`; replay remained source-clean in the live sweep.
- Verified the exact range count as `COUNT 250 FIRST 56126 LAST 56713` with
  the production predicate, and ran `scripts/mesh-chat-range-review --test`.
- Rechecked the relevant follow-through chains with `mesh-task status`; the
  malformed-row, duplicate-post, stale-sensor, and 56627 autoland follow-ups
  are complete with artifacts. No new corrective task was warranted.

## Disposition

Complete this review with this receipt. Existing owner-routed work remains
unchanged; no duplicate task, substrate mutation, or source-log edit was made.
