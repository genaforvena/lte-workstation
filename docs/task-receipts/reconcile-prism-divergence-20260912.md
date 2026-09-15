# Prism divergence review — 2026-09-12

## Snapshot checked

- Checkout: `/home/mesh-home/src/llama.cpp-prism`, branch `prism` at `79697f23a2c8f3aa2ccb2fd7406095a8dbfbb454` (`perf(ggml-cpu): enable Q2_0 fast path on AVX-VNNI CPUs (#72)`).
- Worktree: clean (`git status --porcelain=v1` empty); repository is not shallow.
- Compared with cached `origin/prism` at `d8f26eec76da6d09bb708bcba51ef64b8cd868a3` (`cuda: keep the PTX L2 prefetch hints off HIP and MUSA (#168)`), the merge base is `8a963fc10ee005b3f425d14bcd427eef5c57f157` (`convert : fix conversion for Mistral-Medium-3.5-128B (#24268)`).
- `rev-list --left-right --count prism...origin/prism`: **43 / 1,131**.
- `origin/prism` reflog says its last update was a successful `fetch --all --prune` at **2026-09-12 04:03:38 UTC**. This review ran at about 16:40 UTC. The inventory therefore describes that cached snapshot; no new fetch was run because updating remote-tracking refs would violate the task's “do not modify refs” boundary. Verify freshness with the operator before acting on either direction.

## Commit inventory

The complete unique-commit inventory (full SHA, date, author, subject; one row per commit) is in [reconcile-prism-divergence-commits-20260912.tsv](reconcile-prism-divergence-commits-20260912.tsv): 43 local-only rows and 1,131 cached-upstream-only rows.

Local-only history is predominantly Prism feature work: Q1_0/Q2_0 quantization and CPU/ARM/Metal/CUDA/Vulkan kernels; Hopper WGMMA; KV-cache mean-centering and calibration; DSpark speculative decoding and conversion; Metal GDN/ring decode; plus release/CI and focused test follow-ups. It spans 2026-04-17 through 2026-07-17. The 43 commits include three merge commits (PRs #52, #56 and #63).

Cached upstream-only history spans 2026-06 through 2026-09 (300 commits in June, 371 in July, 440 in August, 18 in September). Its cumulative tree delta from the merge base touches 2,049 files: 346,998 insertions and 95,667 deletions. The local cumulative delta touches 117 files: 11,965 insertions and 265 deletions. Upstream has continued broad core, backend, build/CI, and UI development during the divergence; this is not a small maintenance-only gap.

`git cherry -v origin/prism prism` reports eight local commits with patch-equivalent changes already represented upstream, 32 non-equivalent non-merge local commits, and three local merge commits. The equivalent local commits are:

- `ac71e9f8fd912196dff1039c5b6200f501881546` — Add release-prism workflow
- `5f334715677dfcb26973e8ba1959861136995a54` — release-prism: install spirv-headers for ubuntu-arm64 vulkan build
- `6700b536ff953400eb530a739b4a904ecab44f12` — CI OpenMP redist DLL lookup
- `0ad1dab7b392cd27439176b8907ebb4b13f5ebb4` — disable LLAMA_BUILD_APP in iOS Xcode build
- `a18e55e493a213773be3180348d59d31f19a6065` — self-generated KV mean-center calibration corpus helper
- `f28050ecfcc26011775f1ea213d74e3e3fda5b79` — calibration helper review follow-up
- `a5527fc87ed907f9901d130d3d16e1723f4aca6c` — hybrid-model KV mean-centering and calibration guard
- `62061f91088281e65071cc38c5f69ee95c39f14e` — include speculative-simple in release archives

## Decision brief

No refs were modified. Do not merge or rebase until the operator chooses a direction and confirms whether to refresh `origin/prism` first.

- **Rebase** would put the local work on top of the much newer upstream line and can omit patch-equivalent changes, but the three merge commits require an explicit topology choice (`--rebase-merges` or flattening). The 32 non-equivalent commits span large, heavily evolved subsystems, so conflict resolution and behavioral validation are likely substantial.
- **Merge** would preserve the existing local commit IDs and merge topology and record the divergence in a merge commit, but it retains duplicate ancestry for the eight patch-equivalent changes and can still require broad conflict resolution across the 117 locally changed files.

Before either operation, refresh/freeze the target snapshot by operator choice, inspect the exact local diff and overlap, and run an isolated trial on a disposable worktree or temporary branch. Compare resulting trees and tests before landing anything. This review did not attempt that trial because the requested direction is still unchosen.

## Verification

Read-only checks: clean status, non-shallow repository, merge-base lookup, ahead/behind count, local/upstream commit logs, patch-equivalence classification, remote-tracking reflog freshness, and range diff statistics. No build or tests were run; no source changes, fetch, checkout, or ref updates were made.
