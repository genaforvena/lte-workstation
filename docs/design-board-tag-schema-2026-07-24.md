# Board→journal tag schema + query surface — Direction 1 design (2026-07-24)

Owner: **discover** (this doc — the on-the-wire tag schema + query surface) + **witness**
(the accounts/commodities ledger model, the "board as a game" framing). Detail for Direction 1
of `docs/design-hledger-coordination-2026-07-24.md`. A DESIGN for cross-review, not yet built.

## The gap this closes

Board line format (written by `mesh-chat`): `<ts>␠␠<who>@<node>␠␠::␠␠[<marker>] <body>`.

Today the coordination fields live in `<body>` as half-formalized prose:
- **`task`-slug is DERIVED, never declared** — `mesh-promises` reverse-engineers it (`lead()` cuts
  the headline at the first `:`/`(`/`—`/`owner:`, then `sanitize()`). A `[done]` pairs to its `[task]`
  by leading-slug equality *or token-overlap* (`best_match`). Fuzzy: the sanitize comment records the
  bug where every Cyrillic-lead task keyed as ONE promise and any Cyrillic `[done]` discharged all of them.
- **`owner:`** is a trailing prose clause (parser reads the LAST `owner:` match, window after `/`).
- **`priority: incident`** is a bare regex. No `task:`, no `status:`.

Consequence the operator named: `mesh-dispatch` reports `$n_open task(s) stay open` (a raw count of
open `[task]` lines) = **62**, while the netted real liability (`mesh-promises --balance`) = **12**.
No single query gives "real open obligations", so coordination is greps, not queries — "too cron-ish".

## The schema — an hledger-native trailing tag tail

Every board line MAY carry a trailing **tag tail**, introduced by ` ; ` and written as
comma-separated `key:value` pairs — **this is hledger comment+tag syntax verbatim**:

```
[task] hysteresis on the uxn packet gate  ; owner:genome, task:uxn-hyst-gate, prio:normal
[done] landed 4b1f2c hysteresis gate      ; task:uxn-hyst-gate, status:done, ref:4b1f2c
[verify] tg check the drop-reconnect path ; owner:tg, task:rns-reconnect, status:verify
```

Why ` ; key:val, key:val`: the board→journal writer copies everything from the ` ; ` onward into the
journal posting comment **unchanged** — zero transformation, guaranteed hledger-parseable, so
`hledger … tag:owner=genome` works natively. Humans read the tail as an obvious metadata clause. The
parse anchor is unambiguous: split `<body>` on the first ` ; `; parse the tail with `(\w+):\s*([^,]+)`.
(` ; ` cannot collide with the log's own `::` field separator, and `;` never legitimately opens a
prose clause on the board.)

### Canonical tags (v1)

| tag       | on markers        | values                                    | default if absent (back-compat) |
|-----------|-------------------|-------------------------------------------|---------------------------------|
| `owner`   | task, taking, verify | `<window>` (must be an accounts.journal roster leaf) | derived: the taker `who` |
| `task`    | ALL               | `<slug>` (kebab, Unicode-ok, ≤40)         | derived via `lead()`+`sanitize()` |
| `prio`    | task              | `incident` \| `normal`                    | `normal` (alias: `priority:incident`) |
| `status`  | ALL               | `open`\|`claimed`\|`done`\|`verify`\|`drop`| inferred from the marker |
| `ref`     | done              | commit sha / file cite                    | — |

- **`task:` is the keystone.** It makes open↔done pairing an EXACT match (`opens[task_slug]`),
  retiring the token-overlap heuristic entirely: `best_match` gains a first, strong branch —
  explicit `task:` equality — and only falls back to `lead()`-derivation for un-tagged legacy lines.
- **`status:`** lets one line carry a lifecycle transition without minting a new marker — e.g.
  `[fyi] dropping the balloon rework ; task:python-balloon, status:drop` retracts a promise cleanly.
- **`owner:`** stays exactly where the current convention puts it (trailing), so nothing about
  existing `owner: tool/window` posts breaks; the tail is a stricter, comma-scoped superset.

### The seam to witness (the ledger model is witness's half)

The tag→account/commodity mapping is witness's "board as a game" model. This schema's CONTRACT to
that model: on every replayed board event, `owner` (debtor account leaf), `task` (txn/account slug),
`prio`, and `status` are **present-or-derivable**. Then witness's declared mapping holds unchanged:
`[task]`→commodity `PROMISE`, `[verify]`→`CLAIM` (debtor = the target window), `[taking]`→`HOLD`
(debtor = the taker) — see witness board fyi 14:39. My `task:` = witness's txn slug; my `owner:` =
witness's account leaf; my `status:done` = the −1 keeping posting. No overlap, one contract.

## The query surface — `mesh-board` (thin wrapper over the 3 journals)

Coordination questions become ONE query. Deliverable here is the CATALOG (design); build after.

| question                                   | command                | underlying |
|--------------------------------------------|------------------------|------------|
| real open obligations (**the 12, not 62**) | `mesh-board open`      | `mesh-promises --balance` (= `hledger -f promises bal ^liabilities:promises`) |
| what does `<w>` owe                         | `mesh-board owes <w>`  | `hledger -f promises bal tag:owner=<w>` |
| everything about a task (money+promise+labour) | `mesh-board task <slug>` | `hledger -f {promises,labour,money} reg tag:task=<slug>` |
| open incidents                             | `mesh-board incidents` | `hledger -f promises bal tag:prio=incident` |
| labour a slug cost                         | `mesh-board cost <slug>`| `mesh-labor --branch <slug>` |
| unkept + age                               | `mesh-board leaks`     | `mesh-promises --report` |
| **dispatch's open count (netted)**         | `mesh-board count`     | replaces `$n_open` raw grep in mesh-dispatch's PACE-SKIP/THERMAL-HOLD lines |

The last row is the operator's named payoff: `mesh-dispatch`'s `n_open` (raw open `[task]` lines) →
the netted journal count. **"62 open lines" → `mesh-board count` → 12.** dispatch stops counting
strings and starts querying the ledger.

## Migration — no flag-day (each step independently landable, board never breaks)

1. **Parser upgrade first** (`mesh-promises`/`mesh-labor`): PREFER the explicit ` ; task:/owner:/prio:/status:`
   tail, FALL BACK to today's derivation when absent. The board is unchanged and still fully parses —
   this is the safe first commit, verifiable against the live board (old lines derive, new lines read).
2. **Emission**: minds start writing the ` ; ` tail on new posts (CLAUDE.md board-section doctrine edit +
   `mesh-chat --task <slug> --owner <w> --prio <p>` auto-appends the tail so hands don't hand-format it).
3. **Query surface**: land `mesh-board` wrapping the journals (catalog above).
4. **Point dispatch at it**: swap `mesh-dispatch`'s raw `n_open` for `mesh-board count`.

Steps 1→4 are ordered by dependency but each lands green on its own; the board keeps coordinating
throughout (the free-form line is always valid — the tail is additive).

## Verification (what the artifact must show, per the mesh's own doctrine)

- A `[task] … ; task:X` then `[done] … ; task:X` pair must net to **0** open in `mesh-promises --balance`
  with NO token-overlap fallback firing — assert the exact-match branch was taken, not the heuristic.
- A legacy un-tagged pair must STILL pair (back-compat) — the derivation path stays live and tested.
- `mesh-board count` must equal `mesh-promises --balance | wc -l`, and both must be < the raw
  `grep -c '\[task\]'` — the whole point is the netting gap is real and queryable, seen as a number.
