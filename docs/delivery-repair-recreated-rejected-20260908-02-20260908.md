# Delivery repair receipt — recreated-rejected-20260908-02

- **Owner:** hire
- **Task:** `recreated-rejected-20260908-02-corrected/delivery-repair`
- **Checked:** 2026-09-08 (UTC)
- **Target:** `autoland-recreated-rejected-20260908-01/land-unit-5-canary`
- **Target owner:** genome
- **Target description:** land completed `recreated-rejected-20260908-01/unit-5-canary` and verify `docs/ask-answer-funnel-unit-5-canary-registry-20260908.md`.

## Bounded delivery retry

1. `mesh-task check dispatch autoland-recreated-rejected-20260908-01/land-unit-5-canary genome` returned **0**, proving the target was genuinely open and dispatch-eligible at the check.
2. `mesh-task dispatch autoland-recreated-rejected-20260908-01` was then attempted. It returned **2** with `chain ... has no open current step to dispatch`.
3. Immediate live state showed the target **active**, owner `genome`, lease through `2026-09-08T12:28:38Z`.
4. The board records the owner-authored receipt at `2026-09-08T11:58:38Z`: `[taking] autoland-recreated-rejected-20260908-01/land-unit-5-canary`, with `status=claimed`.

This is a reproducible delivery race, not a silent success: the open target became owned between the eligibility check and the retry. The refusal is the safe outcome because a second dispatch would duplicate active work. The target was therefore delivered to its genome owner and started; no historical payload was replayed.

## Verification

```text
mesh-task check dispatch ... genome  -> rc=0
mesh-task dispatch autoland-recreated-rejected-20260908-01 -> rc=2 (no open current step)
mesh-task status autoland-recreated-rejected-20260908-01 -> active; genome; lease=2026-09-08T12:28:38Z
```

The prerequisite receipt remains `/home/mesh-home/lte-workstation/docs/token-usage-source-schema-20260908.md`; this repair receipt is the owner artifact for the replacement delivery attempt.
