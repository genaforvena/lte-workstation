# Repository synchronization audit — 2026-09-07

All discovered repositories were fetched with `git fetch --all --prune` where
the remote completed. Clean behind trees were fast-forwarded:

- `/home/mesh-home/.fzf`: fast-forwarded 66 commits to `origin/master`.
- `/home/mesh-home/.mesh/gigaam-src`: fast-forwarded 2 commits to `origin/main`.
- `/home/mesh-home/prebid-local/prebid-server`: clean and aligned with `origin/master`.

Dirty or locally-ahead trees were preserved without reset, merge, or overwrite.
The tiny-fleet generated adapters and corpora are intentionally uncommitted
artifacts for the completed coordination chain.

Remaining synchronization caveats:

- `/home/mesh-home/src/llama.cpp-prism` was a shallow graft. An unshallow fetch
  succeeded and established a real merge base; the local `prism` branch is
  divergent at `43 ahead / 1123 behind`, requiring an explicit merge/rebase
  decision before changing it.
- `/home/mesh-home/.mesh/knowledge` is locally `ahead 63` of its configured
  `default-string/main`; its SSH fetch hung and was stopped after bounded
  retries. No local content was changed.

No repository was force-reset or discarded. These two caveats are the only
remaining freshness items; all other discovered repositories were fetched and
their local work preserved.
