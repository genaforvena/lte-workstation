# Task receipt: age-aware SS connection summary

Task: `vpn-ss-summary-age-aware-20260916/make-ss-summary-age-aware`

## Disposition

Implemented the corrective request from physical `chat.log` line 59666. The VPN
dashboard consumer in `scripts/mesh-dash` now treats `~/.mesh/ss-connections.log`
as a cached observation rather than a live census:

- A readable artifact no older than 30 minutes is rendered with its observation age.
- An artifact older than 30 minutes is rendered `STALE` and explicitly says the
  current SS connection state is `UNKNOWN`; its historical line is retained for
  diagnosis.
- Missing, empty, or unreadable summaries are rendered `UNKNOWN`.

The producer and its schedule were not changed. No routing, DNS, firewall, VPN,
WireGuard, or other substrate state was changed.

## Verification

Independent focused test:

```text
rtk tests/test-mesh-dash-vpn-ss-age.sh
PASS: VPN SS connection summary distinguishes fresh, stale, and missing readings
```

Additional checks:

```text
rtk bash -n scripts/mesh-dash
PASS (exit 0)
rtk git diff --check
PASS (exit 0)
```

The focused test renders the real `vpn` pane against an isolated fixture and
asserts all three states: a two-hour-old summary is `STALE` plus current-state
`UNKNOWN`, a newly touched summary is age-labelled without stale/unknown wording,
and an absent artifact is `UNKNOWN`.

## Artifact hashes

```text
715deecf4ae7291ac5423dfd6331f0eb93a1fa20a32f91ef3edfc4d6413e1a48  scripts/mesh-dash
6bdbcb7c31bbaf071e4908311ef9e341f12d78e068f909703b930442ec2de2b4  tests/test-mesh-dash-vpn-ss-age.sh
```
