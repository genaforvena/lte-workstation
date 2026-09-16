# Health-warning triage — `health-warning/d9d8d788fd60d433ae15`

Checked 2026-09-16 05:49–05:54 UTC on `mesh-home`.

## Finding

The source warning at `/home/mesh-home/.mesh/chat.log:71958` is a terminal
delivery failure emitted at `2026-09-16T05:13:19Z`:

```text
[@wake] [delivery-failed] target:wake window:5965118 count:1
msg:b4b66228d30587e3 attempts:b4b66228d30587e3=0
reason:b4b66228d30587e3=age-expiry age-limit:900s
```

The delivery log independently records the failure at
`/home/mesh-home/.mesh/chat-deliver.log:2623` with age 909 seconds and zero
attempts. The canonical delivery ledger at
`/home/mesh-home/.mesh/chat-deliver-ledger.json:14209` records the same message,
sender/target, `status=failed`, `terminal_reason=age-expiry`, and
`failure_emitted=true`.

Nearby messages were delivered before and after this event, so this evidence
does not identify a durable node or substrate fault. The local
`mesh-operator-intake.path` unit is absent from this node, while the dashboard
warning is cached fleet state; no restart or routing, DNS, firewall, VPN, or
Tailscale change is warranted from this warning.

## Disposition

**Known delivery-edge age-expiry; no repair warranted from this evidence.**
The implementation at `scripts/mesh-chat-deliver:107-132` classifies the
observed age threshold as `age-expiry` and persists terminal state. A future
warning with a non-updating delivery log or ledger would be a separate,
actionable liveness issue.

## Verification and delegation

Personally inspected the source chat line, canonical task JSON,
`chat-deliver.log`, delivery ledger entry, implementation branch, and the
owner ledger line. `mesh-chat-deliver --test` passed its stable-ID,
terminal-control, and bounded-ledger smoke test. The one-shot dashboard also
showed the warning plus cached `mesh-operator-intake.path` failure; those are
recorded as separate live follow-ups, not silently marked fixed.

Delegated a read-only audit to `health-warning-d9d8-audit`; I personally
inspected its returned references and then independently inspected the cited
files and lines. The worker did not claim tasks, post board messages, or edit
files. Ownership, receipt writing, board voice, substrate boundaries, and
final ledger verification remained local.
