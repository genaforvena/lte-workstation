# Health dependency disposition — 2026-09-12

- Task: coordination-hledger-plan-20260908/health-dependencies
- Owner: health
- Captured: 2026-09-12T02:53Z
- Source cutoff: mesh-health 02:53:07Z; check dashboard 02:53:47Z; live route probes during 02:42–02:52Z
- Plan: docs/superpowers/plans/2026-09-08-coordination-hledger.md, Task 6

## Doctor process and freshness

At the first process check there was no mesh-doctor invocation. The zero-byte lock file at
~/.mesh/.doctor.lock had mtime 02:23:01Z, but a nonblocking flock probe succeeded, so it was not
held. The check dashboard showed a persisted result from 02:33:16Z, explicitly labelled cached
(5m old at its 02:38:49Z snapshot).

An attempted mesh-doctor --help invoked the full diagnostic because this command has no help
option. That direct run completed with exit 2 and summary 2 FAIL / 33 WARN. It did not refresh
~/.mesh/doctor.log: the file still has mtime 02:33:16Z. At 02:53:47Z the dashboard still showed
the persisted 02:33:16Z result as cached (20m old), with 3 FAIL / 33 WARN, including the two
egress findings and mesh-wifi-quality smoke-test failure. The fresh direct output and persisted
cache disagree by one FAIL; no recovery is claimed from the direct run. After it exited the lock
was free again. Treat the dashboard result as stale cached evidence, not as a current doctor
verdict, until a persisted diagnostic refresh reconciles it.

## Current node and egress evidence

mesh-health completed at 02:53:07Z (rc=0): mesh-home and phaedra passed; GL-MT3000, Redmi 10,
ilya, imozerov-Default-string, imozerov-IdeaPad-3-15IIL05, and rip were offline; imac-rozalia
was skipped as SSH-unreachable. The one-shot check pane at 02:53:47Z reported 10 nodes, two
SSH-reachable, zero LAN-reachable, and eight down; it showed the persisted doctor cache as old.

The current LAN route check is a real FIB finding. enp42s0 owns 100.76.220.69/16, with main-table
default via 100.76.0.1. ip route get 100.76.0.1 selected tailscale0/table 52 instead. The
standalone mesh-card --exit-node-lan probe returned state=swallowed, target 100.76.0.1,
net 100.76.0.0/16, dev tailscale0, table 52. mesh-card --refresh exited 2 with the invariant
violation. The current egress tape at 02:42:01Z showed public egress still OK through route
(US, 38.49.216.141; 1.1.1.1 loss 0%), while its gateway observation reported 100% loss to
100.76.0.1. A separate ping pinned to enp42s0 also received no replies (3/3 lost). This proves
the route selection and a gateway ping failure; it does not prove all LAN traffic fails.

The existing mesh-exit-node-lan-heal --check does not repair this state. It still tests the old
100.74.0.0/16 prefix and refuses it as non-RFC1918; the current interface prefix is 100.76.0.0/16.
The prefix is in the carrier-grade 100.64/10 range also used by Tailscale. No route was changed:
the direct gateway probe failed, the helper's target is stale, and a broader exception needs a
separate routing claim plus peer-route collision checks and independent before/after reachability.
Retry owner: health. Retry when a live local gateway/path is measured and the exception can be
verified without diverting a Tailscale peer; then coordinate the single writer and use mesh-dms.
Impact meanwhile: local-router/LAN reachability is not established; outbound egress through
phaedra works but remains an exit-node dependency/SPOF as the persisted doctor reports.

## Offline and unreachable dependencies

| Peer | Current evidence and expected status | Active obligation, owner, retry | Impact |
|---|---|---|---|
| GL-MT3000 | Offline; Tailscale last-seen 84d, active=True. No live obligation was found by exact host-name search. Treat as an unresolved registered peer, not as healthy. | Health; retry on the next confirmed online observation or if a task names the router. | No remote router management/status path is proven. |
| Redmi 10 | Offline; last-seen 8d, active=True. The 2026-09-12 phone-frontier receipt records SSH 0/3, transport-unreachable, not absent Termux verbs. | Genome owns coordination-hledger-identity-human-20260908/phone-authorized-keys-recheck (open) and coordination-hledger-identity-phone-20260908/phone-authorized-keys-recheck (blocked on operator reachability confirmation). Retry after a confirmed reachable phone endpoint. | Authorized-key repair and SSH-mediated phone/Termux work remain blocked; no new phone capability is proven. |
| ilya | Offline; last-seen 22d, active=True; off-mesh. | Genome owns coordination-hledger-identity-ilya-20260908/ilya-back-online-push-restore-env (blocked). Retry on a confirmed ilya-online event, then push and verify restore.env. | Remote restore configuration cannot be verified or delivered while the host is offline. |
| imac-rozalia | Tailscale says online, but mesh-health skips it because outbound SSH is unreachable. mesh-minds marks it online?*/not reachable for a live probe. who shows an inbound session from 100.121.88.110 since 01:42Z; that proves an incoming session to mesh-home, not the reverse SSH path. | Reuse open health-warning/3df6a8f98b0e495cd109/triage and health-warning/4989e0902917448d4dfa/triage (owner health). Retry outbound SSH from the next stable probe; preserve the direction distinction. | Outbound operations to the Mac are unverified despite its Tailscale presence and inbound session. |
| imozerov-Default-string | Offline; last-seen 59d, active=True; off-mesh. No open coordination task naming this host was found. | Health; retry only on an online event or when a task requires it. | No remote peer capability is currently available; no active coordination task depends on it. |
| imozerov-IdeaPad-3-15IIL05 | Offline; last-seen 12d, active=True; off-mesh. Node context assigns IdeaPad a sensors-only role after mind-home migration. No active coordination task naming it was found. | Health; retry on a confirmed online observation if a sensor obligation needs it. | Sensor availability is not proven; no current coordination dependency was found. |
| rip | Offline; last-seen 8d, active=False; off-mesh. No active coordination task names it. | Health; re-evaluate only if Tailscale registration becomes active or a task needs the peer. | Expected inactive for current coordination; no retry is due now. |

The live health queue also retains open, health-owned recurring triages for egress and the Sep 9
check-stream: health-warning/dd6e6d5f2a315ea2cf80/triage and
health-warning/5a1fd4103ba0b7f8ee4f/triage. They remain linked rather than spawning duplicate
incident rows. No substrate state was edited and no route change was attempted.

## Disposition

The seven peer dependencies now have explicit status, impact, and retry ownership. The doctor
cache is visibly stale and labelled cached; its last persisted result must not be represented as
current. The live route finding is measured but unresolved because the current CGNAT prefix,
stale healer target, and direct gateway non-response leave no verified safe route action in this
read. Existing warning triages remain open for follow-up. The next chain step is witness:
re-read this receipt and the live board, then carry the stale doctor cache and unresolved route
finding as explicit outcomes rather than global health claims.
