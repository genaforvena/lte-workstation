# Connected RFC6598 LAN-prefix guard — 2026-09-14

Task: `exit-node-lan-cgnat-live-repair-20260914/repair-connected-cgnat-guard`.

Changed `scripts/mesh-exit-node-lan-heal` so RFC6598 prefixes pass the shared LAN-prefix gate only
when the exact prefix is a `proto kernel scope link` route in table `main` on an interface that
currently owns the exact address and prefix reported by `mesh-card`. This keeps the shared CGNAT
range from becoming an allowlist: public, unconnected, stale, and non-owned prefixes still fail
loudly. The kernel FIB retains precedence for more-specific routes such as Tailscale peers.

The inline `--test` fixture now covers connected `100.76.0.0/16` acceptance, missing and mismatched
connected routes, an absent reported address, a public prefix, peer-route lookup, idempotent EEXIST,
and dry-run with no route write. `bash -n scripts/mesh-exit-node-lan-heal` and
`scripts/mesh-exit-node-lan-heal --test` both passed. The test was first run before the guard change
and failed because the connected CGNAT prefix was rejected as “not RFC1918”; it passed after the
guard change.

SHA-256 source (also contains the inline test harness):
`b80b07442647cb4807f296ee045ab6d9c153db4a5a952c7785144614af93e9b2`.

SHA-256 T18 test fixture section:
`f885a252482661913cd46703bec783dad2488fa816e5234bc2c42ff6ff75b521`.

Fresh read-only live evidence no longer matches the older task evidence: `enp42s0` owns
`100.74.136.43/16`; table `main` has the exact connected route `100.74.0.0/16 dev enp42s0 proto
kernel scope link`; it has no exact connected route for `100.76.0.0/16`; and `100.76.0.1` still
resolves via `tailscale0` in table 52. `mesh-card --exit-node-lan` reports the live `100.74.0.0/16`
prefix healthy on `enp42s0`. **No real route was written.**

Landed through targeted MeshLand after the source passed its 600-second settle gate. The dry run
selected exactly one path; unrelated candidates were excluded. Commit:
`b0007c3be77115105eae279127b3a04ee39b1682` — `Allow only live connected RFC6598 LAN prefixes`.
`~/.local/bin/mesh-exit-node-lan-heal` has the same SHA-256 as the source, and its deployed
`--test` passed. The subsequent live route application and independent verification were assigned
to separate owners; this implementation turn made no substrate route changes.

## Live route verification — 2026-09-14 06:25–06:30 UTC

Task: `exit-node-lan-cgnat-live-repair-20260914/apply-and-verify-live-cgnat-exclusion`.

At dispatch time, fresh reads derived `enp42s0` address `100.76.34.107/16`, connected route
`100.76.0.0/16`, gateway `100.76.0.1`, and main-table default `via 100.76.0.1 dev enp42s0`.
Table 52 already contained `throw 100.76.0.0/16`, plus its default and peer `/32` routes on
`tailscale0`. The live healer ledger had current stamped `RUN ... lan=ok ... rc=0` rows each minute;
the deployed healer's `--check` said the gateway resolves on `enp42s0` and there was nothing to
apply. The correct route was therefore already present; this window made no routing mutation and
did not arm or cancel a DMS. No other routing owner was held because no write was attempted.

Verification performed:

- `ip -4 route get 100.76.0.1` and `ip -4 route get 100.76.254.254` both returned `dev enp42s0`.
- `ip -4 route get 100.94.116.17` returned `dev tailscale0 table 52`; all table-52 peer `/32`
  entries remained on `tailscale0`.
- `mesh-card --refresh` at 06:28:29Z reported `exit-node-lan: ok`, `invariant-check: OK`, and
  public IP `38.49.216.141`.
- `mesh-health` at 06:27:13Z and 06:30:21Z exited 0 with `PASS` for mesh-home and phaedra; the
  listed long-offline peers remained offline.
- A fresh `curl -fsS https://api.ipify.org` returned `38.49.216.141`; `mesh-ss-test --edge`
  exited 0.
- `mesh-exit-node-lan-heal --test` passed, including the connected-CGNAT acceptance and
  more-specific tailnet-peer precedence fixtures. Source and deployed healer hashes both equal
  `b80b07442647cb4807f296ee045ab6d9c153db4a5a952c7785144614af93e9b2`; the minute reflex is
  present in `~/.mesh/reflexes.cron`.

One follow-up remains for the independent verifier: `mesh-trace` contains a 06:20Z
`[reflex-overwrite]` report calling the healer's content axis frozen, while its stamped run tape
continues to advance and report `lan=ok`. This does not change the verified live FIB result; the
health-owned independent step should resolve whether the freshness warning needs a separate repair.
