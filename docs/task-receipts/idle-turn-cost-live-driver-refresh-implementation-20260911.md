# Live consumer driver refresh implementation — 2026-09-11

Task: `idle-turn-cost-live-driver-refresh-20260911/wire-version-aware-consumer-refresh`

## Result

`mesh-consume-all` now derives the wanted identity from the deployed
`mesh-pane-consume` executable with `sha256sum`. It stamps that SHA in
`MESH_PANE_CONSUME_LOADED_SHA` before `exec`, and compares it with each live
driver's `/proc/$pid/environ`. A missing or different SHA is stale even when
interval and delivery argv match. The supervisor also removes stale and
duplicate drivers, retaining exactly one current process per live channel.

The pane script contains no static version marker. Existing interval and
`--deliver` routing parsing is unchanged, and the refresh path does not issue
`--kick`; each replacement therefore relies only on the driver's existing
startup contract.

## Red-first evidence

Before the implementation, the newly added same-argv/different-loaded-marker
regression failed:

```text
smoke-test: FAIL (loaded version drift not STALE)
TEST_RC=1
```

After implementation, the coverage passed for same SHA → `OK`, different SHA
→ `STALE`, missing SHA → `STALE`, plus a source assertion that spawn wiring
stamps the SHA and derives it with `sha256sum`.

## Deployment and live evidence

`mesh-sync-tools --apply` returned 0. The single deployed supervisor was run
once after deployment; its log records all 15 Sep 9 processes as SHA/argv
stale and starts their replacements. The post-refresh process audit found one
driver for each configured channel, all with start times between
`2026-09-11T14:57:28Z` and `2026-09-11T14:57:30Z`, loaded SHA
`44a44dd490c31a44dda3bed0ca681d61be638f26a222b063a33778647dd20c3a`, and
the preserved intervals:

```text
genome 60  tg 60  senses 60  health 60  pub 60  discover 60
sound 7200  vpn 3600  witness 60  tg-roz 60  job 60  adint 60
hire 60  haunt 60  wake 60
```

No duplicate remained, and no supervisor kick was sent.

## Verification

- `bash -n scripts/mesh-consume-all scripts/mesh-pane-consume` — pass.
- `bash scripts/mesh-consume-all --test` — pass, including SHA drift and
  spawn-wiring regressions.
- `bash scripts/mesh-pane-consume --test` — pass.
- `mesh-sync-tools --apply` — pass.
- Live `/proc/$pid/environ` + argv audit — 15/15 current SHA, exactly one per
  configured channel, intervals preserved.
