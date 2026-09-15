# `mesh-selfcare` smoke failure triage — 2026-09-13

Task: `mesh-doctor-selfcare-triage-20260913/triage-mesh-selfcare-smoke-failure`
Owner: `health`

## Finding

The health pane at 2026-09-13 21:39:09Z showed the cached doctor result from
21:31:41Z: FAIL=3, WARN=33, including `smoke-test FAIL (real): mesh-selfcare`.
The focused test did fail live at 21:40:16–21:40:25Z with exit 1:

```text
smoke-test: FAIL (loop fixture flipped STATEF but posted nothing)
```

The failure was a race in the smoke fixture, not a failure to post during an
ordinary live cycle. `report_on_change` writes `.selfcare-state` before invoking
`mesh-chat`. The fixture watched only for the state-file change, then immediately
sent TERM to its loop process group and checked the chat stub's log. The xtrace
at `/tmp/health-selfcare-xtrace.log` (mtime 21:40:47Z, exit 1) shows that order:
the loop fixture observes DOWN, `_fx_reap` sends TERM, and only then does the
parent assert the post log. The test could therefore interrupt the child in the
small interval between those two observable effects.

## Change and verification

Adjusted the fixture in `scripts/mesh-selfcare` to wait for both the DOWN state
and the `connectivity changed` chat record before terminating the loop. The
failure assertion now names both expected effects. The installed command at
`/home/mesh-home/.local/bin/mesh-selfcare` is a symlink to this source file; both
paths had the same SHA-256 after the change:
`d9d075357e220070af736f368fc54a248aa5ac95ed2051898e269ea9d230d161`.

| UTC | Command | Exit | Result |
|---|---|---:|---|
| 21:40:16–21:40:25 | `timeout -k 5 150 mesh-selfcare --test` | 1 | Reproduced the false failure above. |
| 21:40:47 (trace mtime) | `bash -x /home/mesh-home/.local/bin/mesh-selfcare --test` | 1 | Confirmed state detection, immediate group reap, then missing-post assertion. |
| 21:42:09–21:42:33 | `./scripts/mesh-selfcare --test` | 0 | `smoke-test: ok` after fixture correction. |
| 21:42:40–21:43:05 | `timeout -k 5 150 mesh-selfcare --test` | 0 | Active command path passed. |
| 21:43:40–21:44:08 | `./scripts/mesh-selfcare --test` | 0 | Repeat passed. |
| 21:44:08–21:44:32 | `./scripts/mesh-selfcare --test` | 0 | Repeat passed. |
| 21:45:22–21:45:47 | `./scripts/mesh-selfcare --test` | 0 | Final verification passed; `git diff --check` also exited 0. |

Conclusion: the reported real smoke failure was reproducible before the fixture
change and cleared in five consecutive focused runs afterward. No routes,
services, or other substrate state were changed. The pane's doctor summary was
cached at 21:31:41Z; its next doctor refresh will provide the corresponding
fleet health confirmation.
