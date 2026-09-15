# Redmi Termux frontier follow-up — 2026-09-14

Task: `discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier`

## Ledger check and repair

The restored discover handoff named an ongoing Redmi residual-Termux sweep, with durable
knowledge/verification artifacts and board entries. A search of `~/.mesh/task-chains` and
`~/.mesh/ledger` found no matching structured task chain. The prior work is therefore evidenced
but not represented as a promise-ledger task. I did not fabricate a historical task row or claim
the old work was ledgered before execution. I created this keyed follow-up before retrying the
frontier; its live attempt is now tracked by the task chain above.

The missing prior entry is a workflow/admission gap: the charter's repeated frontier retries were
handled as separate idle/FYI turns, even though the same unresolved work crossed turns. The shared
rule in `memory/multi-step-work-enters-the-promise-ledger-before-execution.md` now requires a chain
for cross-turn work. The bounded continuation below follows that rule; no runtime behavior was
changed here.

## Prior evidence

- `~/.mesh/knowledge/frontier-dry-phone-termux-uncatalogued-20260912.md` records the three
  candidate verbs and no command-level sample because all documented SSH paths timed out.
- `docs/task-receipts/health-verify-discover-termux-20260913.md` independently verifies the
  knowledge artifact and reports the Redmi peer offline at that capture.
- The 2026-09-14 handoff says `termux-saf-ls` is prior art and no command sample was obtained.

## Fresh bounded attempt

At 2026-09-14 09:24 UTC, I ran `termux-saf-ls` once via SSH port 8022 against each documented
Redmi endpoint, using `u0_a380` and a 4-second connection timeout:

| Endpoint | Result |
|---|---|
| `100.103.99.16:8022` | timed out, SSH exit 255 |
| `192.168.8.203:8022` | timed out, SSH exit 255 |
| `192.168.8.146:8022` | timed out, SSH exit 255 |

No Termux command ran, so this attempt has no command sample and proves no new capability. This is
path-specific reachability evidence at the capture time, not evidence that the verbs are absent.

## Result and retry condition

The follow-up task remains open and is blocked on a Redmi `:8022` endpoint becoming reachable.
Retry only after a reachability/state change, then run the remaining candidate commands on the first
responsive endpoint and validate real returned values. Do not repeat these same probes without new
evidence.

## Blocker diagnosis — 2026-09-14 09:54 UTC

The unblock resolver inspected the live paths before considering another SSH attempt:

- `tailscale status --json` reports Redmi 10 `online=false`, peer `100.103.99.16`, last seen
  `2026-09-03T09:53:36.1Z`.
- `ip neigh show` has no entry for either documented LAN address, `192.168.8.146` or
  `192.168.8.203`.
- `ip route get 192.168.8.203` uses `via 100.76.0.1 dev enp42s0 src 100.76.53.53`; this node
  currently has no route to that Redmi LAN.
- `adb devices -l` lists only the attached Note 3 (`4d00553d61ab90b7`), not the Redmi. The local
  node configuration records the Redmi's wireless ADB as unpaired.

These observations show no changed reachability evidence since the 09:24 UTC bounded SSH sweep, so
I did not repeat the three timeouts. There is no mesh-owned transport path to start Redmi Tailscale
or Termux sshd from this node. The prerequisite is external: the phone owner must bring the Redmi
online, reconnect its Tailscale app or LAN, and start Termux sshd. Keep the parent step blocked on
`event:first-successful-redmi-ssh-port-8022-probe`; once any documented endpoint succeeds, resume
the candidate command sweep. No capability or new Termux sample is claimed.

Verification at 09:54 UTC: fresh Tailscale peer status, LAN neighbor table, route lookup, and ADB
device list were read. The prior three SSH timeouts remain the latest endpoint probes.

Verification: task chain `discover-redmi-termux-frontier-followup-20260914` was created before the
retry and the step was taken; the three live SSH attempts all returned exit 255 with connection
timeouts.
