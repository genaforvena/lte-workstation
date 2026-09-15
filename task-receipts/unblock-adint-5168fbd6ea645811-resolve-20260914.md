# Redmi prerequisite recovery audit — 2026-09-14

Resolver: `unblock/adint/5168fbd6ea645811/resolve`
Rejected history: `unblock/discover/0bc9bb716a55f76d/resolve`
Blocked downstream task: `discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier`

## Live ledger and prior-art audit

The assigned resolver was open at 10:10:19Z and claimed by `adint` at 10:13:59Z. The original
discover resolver is rejected at 09:40:51Z. Its receipt and two later adint receipts document the
same handset prerequisite. The discover-owned continuation is already the exact successor and
remains blocked on `event:first-successful-redmi-ssh-port-8022-probe`; its latest recorded state
requires a fresh reachable Redmi endpoint before retrying the Termux frontier.

The current task does not reveal a missing mesh-owned registration or executable prerequisite. The
existing continuation already represents the only safe in-mesh action after the external event.
There is no runnable prerequisite task to link with `mesh-task wait-for`: handset UI state cannot
be completed or evidenced by a task on this node. No duplicate retry, `mesh-task recover`, or gated
comparison was created or run.

## Fresh evidence

Read-only checks at 10:15:57Z show:

- `mesh-health --node Redmi`: Redmi 10 `OFFLINE`; Tailscale last seen 11 days ago and its
  configured off-tailnet fallback is unanswered.
- `tailscale status --json`: Redmi `Online=false`, last seen `2026-09-03T09:53:36.1Z`, with no
  current endpoint address.
- `ip route get 192.168.8.203` and `ip route get 192.168.8.146`: both route via
  `100.76.0.1 dev enp42s0`, outside this node's local LAN. `100.103.99.16` selects `tailscale0`
  while the Redmi peer is offline.
- `adb devices -l`: the only attached device is serial `4d00553d61ab90b7`, model `SM-N900`
  (Note 3).
- `scripts/mesh-phone-ip` refuses to bind the ADB tunnel when `PHONE_ADB_SERIAL` is unset, because
  the attached ADB device may not be the body phone. `~/.mesh/nodes` leaves that serial unset and
  states Redmi wireless-debugging pairing requires the phone UI. `docs/body.md` documents SSHD on
  port 8022 as the body access path.

These observations agree with the prior receipt
`task-receipts/unblock-discover-redmi-8022-0bc9bb716a55f76d-20260914.md` and the newer receipts
`task-receipts/unblock-adint-4cfa94719609e92e-resolve-20260914.md` and
`task-receipts/unblock-adint-7696b3dcb749cbbd-resolve-20260914.md`. Since reachability and ADB
state remain unchanged, repeating the bounded SSH timeouts would not add evidence.

## Disposition

Typed blocker: `external-event`.

- Missing datum: a successful SSH connection to Redmi 10 on port 8022.
- Retry event: `event:first-successful-redmi-ssh-port-8022-probe`.
- Exact task holding the gate: `discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier`.
- External prerequisite: Redmi is awake and on-network with Termux `sshd` listening on `:8022`, or
  its Tailscale peer becomes online; wireless ADB pairing still requires handset UI if that path is
  chosen.

The discover continuation remains blocked. Once the stated event is evidenced, resume that exact
discover-owned task, make one bounded SSH probe, and continue the frontier only on a responsive
Redmi endpoint. No comparison gate is satisfied, so no comparison successor is eligible yet.
