# Health-warning triage: `health-warning/73b7e12d6aecec088434`

- Checked: `2026-09-11T23:57Z`
- Owner: `health` on `mesh-home`
- Task: `health-warning/73b7e12d6aecec088434/triage`
- Source warning: `2026-09-10T04:33:41Z`, chronic signature `35f22fafd26a`, repeated `100.121.88.110 — SSH unreachable`.

## Verdict

This is the known imac-rozalia SSH access failure recurring under the same
chronic signature. Recent evidence shows Tailscale transport can be healthy
while SSH authentication is refused, so the watchdog's “unreachable” wording
does not establish a current network outage. The live pane again classifies
imac-rozalia as down, but also reports high local load and unreliable
reachability probes. No safe local network or substrate change follows from
that mixed evidence; SSH credential or service repair remains with the iMac
owner.

## Evidence

- `mesh-dash --once check` at `2026-09-11T23:57Z`: fleet sample lists
  `imac-rozalia` among peers down and explicitly warns that local load makes
  reachability probes unreliable.
- The health receipt for the same host at `23:54Z`
  (`health-warning-6bb2518841e91cf12b61-triage-20260911.md`) records the peer
  active/direct at `5.227.25.156:55351`, a successful direct Tailscale ping,
  and SSH ending with `Permission denied
  (publickey,password,keyboard-interactive)`.
- That recent transport/authentication evidence narrows the known blind spot to
  SSH access. This pass did not repeat host probes because the live pane marks
  them unreliable and the focused evidence is only three minutes old.
