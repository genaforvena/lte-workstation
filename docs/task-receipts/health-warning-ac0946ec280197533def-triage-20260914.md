# Triage retired route marker and known reachability limits

At 2026-09-14T19:16Z, triaged
`health-warning/ac0946ec280197533def/triage`, from the 2026-09-12T00:01:34Z
roll-call FYI.

The embedded `route:no | PROPOSE none (retired 2026-09-07T08:59:10Z)` is historical
status, not a live route proposal. Earlier health receipts
`task-receipts/health-warning-3ea960d7c6438f1a59e7-triage-20260912.md` and
`task-receipts/health-warning-5e43a109a54314e62d9c-triage-20260912.md` document
the known exit-node/LAN visibility conditions and why that marker must not be
revived. No routing, VPN, firewall or DNS state was changed.

Fresh `mesh-health` reports mesh-home, Phaedra, and iMac reachable; several other
peers remain offline. The one-shot check pane reports current egress probe `OK`
with zero loss but keeps the configured exit-node path and its topology risk
visible. A bounded read-only `ssh -o BatchMode=yes -o ConnectTimeout=5
imac-rozalia true` probe exits 255 with `Host key verification failed`, so SSH
authentication is still unverified; this does not establish a password/key
rejection, and no host-key/configuration change is justified by this triage.

Result: the retired route proposal remains closed; egress currently works through
the configured path, while independent exit-node resilience, LAN visibility and
trusted SSH identity remain known limits. Keep those limits explicit and retry
SSH only after the host key is independently verified or a trusted identity
change is supplied. No duplicate route task or substrate action is warranted.
