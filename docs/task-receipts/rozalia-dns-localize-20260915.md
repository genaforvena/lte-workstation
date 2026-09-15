# Rozalia DNS-flap localization — missing script built 2026-09-15 (health)

## Forgotten request (quoted)
- 2026-09-15T21:43:53Z Rozalia: "прикол в том, что пока скрипт работает - интернет работает стабильно. видимо, сам факт что идёт какой-то probing нон-стоп - помогает интернету работать стабильно, я хз? давай подумаем как локализовать проблему с DNS, может новый скрипт?"
- 21:44Z mesh promised: "новый скрипт будет параллельно проверять DNS роутера, публичные DNS (1.1.1.1 и 8.8.8.8) по IP и обычный Resolve-DnsName. Тогда увидим, отваливается ли конкретный DNS-сервер или резолюция вообще. Сделаю вариант с логом причины каждого сбоя."
- 2026-09-15T22:37:36Z Rozalia re-asked: "милый мой Меш, давай вернёмся к скрипту который поможет нам определить, почему флакает DNS"
- 22:38Z mesh replied with a placeholder restating the plan but NO script. Promise age at build: ~70 min, one explicit re-ask.
- Source: `~/.mesh/roz-in.log` tail (verified 2026-09-15T22:5xZ).

## Artifact built (this turn, health@mesh-home)
- `scripts/internet-dns-localize.ps1` (worktree, unlanded): 30 min × 15 s samples; per sample: router ping, 1.1.1.1 ping, and FOUR DNS legs (system default, router as -Server, 1.1.1.1, 8.8.8.8) with per-leg failure cause captured; 0=pass/1=fail matching `internet-test-hour.ps1` convention; CSV `dns-localize-<stamp>.csv` on her Desktop.
- Design notes: 15 s interval chosen because 2 s probing masked the fault and 60 s caught DNS=1 once (18:39:36Z `router=0 internet=0 DNS=1` — channel up, resolution down); per-sample multi-resolver split distinguishes "router DNS down" from "all DNS down" from "channel down" in a SINGLE sample, so a masked link still yields a verdict.
- Verification: no pwsh on this node — static review only (param defaults, 9-field `-f` row, empty-Server branch). NOT syntax-proven; tg-roz must relay any error text she returns, and genome should land + gate it.

## Long-standing tasks inventoried (same turn)
- Health ledger slot held: `20260915T200000Z-220000Z/analyze-observation` RUNNING (lease to 23:22Z) — not duplicated.
- Witness flood: ~75 OPEN_UNOWNED `witness-chat-range-review-*`; witness's own serialized cleanup in progress (handoff: 30/86 rejected, 56 remain) — not duplicated.
- Operator TG: quiet 315m, queue=0 — silent operator, not a missed request.

## Root cause (filed separately to genome)
- tg-roz replies are fire-and-forget `mesh-tg-roz` sends with no task-ledger entry: the 21:44Z "Сделаю вариант" promise never became a `[task]`, so `/clear` + handoff ("design or implement the script") carried only a vague next-action and the 22:38Z turn emitted a plan restatement with no artifact. Fix: inbound human promises (operator/Rozalia) enter the promise ledger BEFORE the reply goes out.
