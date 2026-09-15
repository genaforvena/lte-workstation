# Root repository secondary mesh remote — 2026-09-12

Task: `repo-sync-followups-20260912/refresh-root-mesh-remote` (owner `genome`).

The task was still `open` in `mesh-task status repo-sync-followups-20260912` before it was
claimed. Its premise remained current: the checkout has 925 porcelain paths, and the task's
earlier count of 806 was only a prior snapshot. No dirty path was changed during this check.

## Remote role and current evidence

`scripts/mesh-genome-sync` identifies the local bare anchor (`$HOME/genome-mirror.git` by default)
as the durability leg and explicitly calls the `mesh`, `phaedra`, and `ideapad` peer mirrors
best-effort. The tool iterates an explicit peer list, classifies unreachable peers separately, and
does not make the `mesh` peer a required mirror for a successful local anchor.

- `origin` is `https://github.com/genaforvena/lte-workstation`; a bounded 30-second fetch of
  `origin main` succeeded. `HEAD` and `origin/main` are both
  `56950d10edeb7ddef245830b6b691d9a900e859c` (0 ahead / 0 behind).
- The configured `mesh` fetch URL is `imozerov@100.125.157.75:genome-mirror.git`. Tailscale reports
  `imozerov-Default-string` at `100.125.157.75` offline. A bounded 22-second fetch with 5-second
  SSH connect timeout failed with `Connection timed out` before Git protocol/authentication; a
  separate bounded 12-second SSH probe failed identically.
- The failed fetch left `refs/remotes/mesh/main` unchanged at
  `211f45878d0bc7ea9ffdb64fe91dc159fb07ab6a` (last commit shown as 2026-07-07). The cached graph
  is 3,074 commits ahead from local `main` to `mesh/main`, with no mesh-only commits; this is stale
  cache evidence, not a fresh comparison.
- The local bare anchor's `refs/heads/main` equals `HEAD` at
  `56950d10edeb7ddef245830b6b691d9a900e859c`.

## Disposition

The task was correctly scoped and is complete as a bounded freshness diagnosis. The `mesh` peer is
an optional best-effort mirror, not the durability anchor; the local anchor and GitHub `origin`
are current at `HEAD`. The `mesh` peer's freshness remains unknown until its node returns online.
No push, merge, rebase, checkout mutation, or dirty-path edit was made. Retry the bounded fetch
when `imozerov-Default-string` is online, then recalculate the graph comparison.
