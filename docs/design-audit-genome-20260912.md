# Genome audit recheck — 2026-09-12

Claim: `design-spec-task-sweep-20260907/audit-genome`

## Result

The core bootstrap split is still present, but two shipped utilities retain fixed operator
endpoints as runtime defaults. I registered repair work rather than changing code in this audit:

| Finding | Current evidence | Disposition |
|---|---|---|
| Bootstrap peer default | `bootstrap.sh` sets `PEER` from an explicit first argument or `MESH_PEER`; absent both, it stays empty for first-node setup. | Resolved. |
| Node registry split | `nodes.example` documents node-local `~/.mesh/nodes`; `scripts/mesh-patterns.sh` resolves phone entries through `mesh-peer-addr`. | Present; registry examples use documentation CGNAT addresses and placeholders. |
| Historical hardcoded-address and identity findings | Search still returns live addresses, labels, and usernames. `mesh-travels` and the Reticulum proof contain runtime targets; many other hits are test fixtures, network examples, node-class labels, or dated incident evidence. | Reconcile by use, not raw hit count. Two runtime-default repairs opened below. |
| Secret values | Targeted scan for private-key blocks and token-shaped assignments in source found no executable-source hit; the only hit was prose in `docs/devto-redaction-placeholder-key-draft.md`. | No leak found by this bounded scan; this is not a claim that every secret form was exhaustively detected. |
| Docs and operator-specific examples | `docs/reticulum-offgrid-proof.md` deliberately records a specific historical proof, while its runnable script also has current fixed defaults. | Preserve the dated proof as history; remove the runnable defaults. |

## Open repair tasks

- `genome-depersonalization-repair-20260912/mesh-travels-peer-config`: make the peer and remote
  log path configurable; verify with a fixture-level test.
- `genome-depersonalization-repair-20260912/rns-offgrid-peer-network-config`: require a configured
  peer and derive gateway/interface from live routing or require explicit values; test honest missing
  configuration and ensure no fixed endpoint remains.

Plan artifact: `docs/plans/2026-09-12-genome-depersonalization-repair.tsv`. Both rows are open and
owned by `genome` in `mesh-task status genome-depersonalization-repair-20260912`.

## Task dependency follow-up

I attempted `mesh-task wait-for design-spec-task-sweep-20260907 final-design-spec-verification`
against the audit task and both repair tasks. All three attempts exited 2 with `step ... is not the
blocked current step`. The final verification row is later in the sweep and cannot yet accept edges.
When it becomes the blocked current step, add wait-for edges to the two repair task IDs above (and
keep the audit row as a prerequisite if it is not already closed) before allowing final verification
to dispatch.

## Verification

- `mesh-task check dispatch design-spec-task-sweep-20260907/audit-genome tg` exited 0 before claim.
- `MESH_TASK_ACTOR=tg mesh-task take design-spec-task-sweep-20260907 audit-genome` claimed the row.
- `mesh-task status genome-depersonalization-repair-20260912` showed both repair rows open, owned by
  `genome`.
- Targeted source and configuration searches confirmed the defaults and the empty bootstrap peer
  behavior. No runtime tests were needed because this turn made documentation and task-ledger changes
  only.

No runtime code was changed. The two repair tasks and downstream dependency wiring remain open.
