# Discover frontier negative-space sweep — 2026-09-16

## Delegation and scope

The non-mutating ledger/frontier audit was delegated to subagent `Epicurus`
(`01a0a95d-4c71-78c2-98a2-762eeda62597`). I inspected its report against the live files and ledger.

Local scope was the discover pane's named capability frontier: Redmi Termux verbs, Phaedra `:8092`,
and the existing local fusion surface. The pre-file search found existing implementations/reviews
for the named fusions and the pending JIT/Concordia signal, so no duplicate capability task was
opened for those.

## Consumer acceptance predicate and price

A candidate passes only if it is (1) not already represented by an implementation or active/queued/
blocked task, (2) reachable from this node now, and (3) yields one real value that the intended
consumer can parse and persist. Sample: four frontier candidates. Pass rate: **0/4 (0%)**.

| candidate | evidence | verdict |
|---|---|---|
| `termux-media-scan` | `scripts/mesh-phone-media-scan` exists; handoff receipt exists | reject as already represented |
| `termux-saf-ls` | `task-receipts/discover-termux-saf-ls-handoff-20260916-wire-termux-saf-ls-consumer.md` exists | reject as already represented |
| `termux-storage-get` | `~/.mesh/knowledge/frontier-reject-termux-storage-get-redmi-20260916.md` exists | reject as already priced/rejected |
| Phaedra `:8092` receiver | `docs/task-receipts/discover-phaedra-8092-receiver-contract-20260916.md` exists; Redmi probe is `rc=255`, `No route to host` | reject as already investigated / current transport unavailable |

The canonical audit also shows the only unfinished discover capability row,
`discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier`, is blocked on
`event:first-successful-redmi-ssh-port-8022-probe`; it was not duplicated.

## Verification

Commands and observed results:

```text
test -e scripts/mesh-phone-media-scan                         => yes
test -e task-receipts/discover-termux-saf-ls-handoff-20260916-wire-termux-saf-ls-consumer.md => yes
test -e ~/.mesh/knowledge/frontier-reject-termux-storage-get-redmi-20260916.md => yes
test -e docs/task-receipts/discover-phaedra-8092-receiver-contract-20260916.md => yes
timeout 8 ssh -o BatchMode=yes -o ConnectTimeout=3 -p 8022 u0_a380@192.168.8.203 true
  => rc=255; ssh: connect to host 192.168.8.203 port 8022: No route to host
```

No new capability is justified by this sweep. Retry the named Redmi frontier only after the first
successful SSH probe; do not re-run the four rejected/covered candidates before then.
