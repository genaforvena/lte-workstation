# Redmi `termux-media-scan` consumer — senses receipt

- Source handoff: `discover` message `cd0a9ac5f3ef89f5`
- Chosen narrow consumer: `scripts/mesh-phone-media-scan`
- Scope: on-demand indexing of one explicitly supplied absolute Redmi media path.

## Design

The wrapper resolves the Redmi address through `mesh-phone-ip`, invokes
`termux-media-scan <quoted-path>` over the existing SSH body lane, and emits the remote result
only when SSH and the command both succeed with non-empty output. A path validation failure is
local `rc=1`. Any transport timeout, no-route, SSH failure, remote failure, or empty result is
`UNKNOWN` with `rc=2`; it is never converted into a successful scan.

This keeps the proven command-level capability narrow and avoids pretending that the 1/3 endpoint
transport sample is universal: `100.103.99.16` timeout and `192.168.8.146` no-route remain
UNKNOWN, while the accepted `192.168.8.203` path is the only path allowed to produce success.

## Test plan and observed result

1. `bash -n scripts/mesh-phone-media-scan` — syntax gate; must pass.
2. `mesh-phone-media-scan --help` — usage/path contract.
3. `mesh-phone-media-scan --test` — dependency gate plus live real-path scan; transport failure
   must return `2` and print `UNKNOWN`, not pass.
4. Inject/stub timeout and no-route SSH outcomes in a temporary HOME/PATH harness; assert both
   return `2`, preserve the reason, and never print a success result.
5. With the accepted Redmi endpoint and a real absolute media path, assert remote
   `Finished scanning 1 file(s)` reaches stdout with `rc=0`.

Observed live check at `2026-09-16`: `mesh-phone-ip` resolved `192.168.8.203`; the wrapper's
real SSH scan returned `rc=255`, emitted `UNKNOWN path=… why=transport-or-remote-failure`, and
returned `rc=2`. This is an honest unavailable result, not a failed capability claim.
