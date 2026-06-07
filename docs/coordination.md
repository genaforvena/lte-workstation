# Substrate changes & multi-agent coordination

The mesh runs **multiple agents at once**, often directed by the same human in
parallel sessions. Stigmergy (independent marks on a shared surface) is safe for a
*commons* — but the network substrate is not a commons. There is exactly **one**
routing table, one default route, one firewall, one SSH path per node. When two
agents mutate that single contended resource without coordinating, they break
connectivity for everything downstream. This happened on 2026-06-07: one agent
applied scoped routing while another re-applied a full-tunnel, and the LAN/login
went down. This doc is the protocol that prevents it.

## What counts as a "substrate change"

Routing (`ip route`, `ip rule`, routing tables), DNS, default route, firewall
(`iptables`/`nft`), WireGuard/`wg-quick`, Tailscale exit-node/advertise, and the
SSH path itself. These are **single-writer, contended, and can sever the path you
are reaching the node through.** Everything else (sensors, compute, reading) is a
commons and needs none of this.

## The single-writer rule

A contended substrate resource has **one owner at a time**. Before you touch it:

1. **Detect other operators.** `ps -u <user> -o pid,tty,etime,args | grep -E 'claude|opencode'`,
   `who`, and read the recent shared trace (`mesh-trace --tail 20`). If another agent
   is active on the same node, assume contention.
2. **Claim ownership on the shared trace.** Write a `mesh-trace` mark naming the
   resource you're taking, the target invariant, and your rollback. This is the
   durable "I changed X at T, here's how to undo it" the postmortem said was always
   missing.
3. **Coordinate through tmux.** All agents run in the one hostname-named session, so
   you can reach any other agent's pane directly and ask it to hold:
   ```bash
   # map agents -> panes
   tmux list-panes -s -t <hostname> -F '#{window_name}.#{pane_index} pane=#{pane_id} tty=#{pane_tty} cmd=#{pane_current_command}'
   ps -o pid,tty,args -p <agent_pids>
   # send a hold/handoff request into the other agent's pane
   tmux send-keys -t <hostname>:<win>.<pane> -l "<coordination message>"
   tmux send-keys -t <hostname>:<win>.<pane> Enter
   ```
   The other agent **acknowledges in the same channel** and states what it has left
   outstanding (its un-rolled-back changes). Now there is a single writer.
4. **Apply under a dead-man's switch** (`mesh-dms`): schedule the rollback *before*
   the change, cancel only after `mesh-health` (and `mesh-card --refresh`) confirm
   the invariant holds. The dead-man gate is the **host-safety** check (host still on
   the clean route); the feature check (consumer egress) is verified separately, with
   no lockout risk. Never reroute the path you are reachable through without one.
5. **Release.** Mark the trace done; the held agent may resume or act as a second
   observer.

## Worked example (2026-06-07)

- IdeaPad-side agent owned the egress fix; a second `claude --resume` on
  default-string had been asked (by the same human) to restore phone/ilya and had
  touched routing.
- The IdeaPad agent wrote a `mesh-trace` ownership mark, then
  `tmux send-keys` into the other agent's pane: *"STOP wg-quick/ip rule/iptables on
  default-string; host stays on the clean route; I own the egress fix."*
- The other agent replied in-pane: *"I'll hold on default-string substrate. You own
  the egress fix,"* and disclosed its outstanding `ip rule 5197` + un-restarted
  `Gtcld.conf` edit.
- Single writer established. No more racing.

## The invariant the substrate must hold

A node that **offers** a route (exit node, VPN egress) must never carry its **own**
control plane (SSH/Tailscale/own egress) on that route. The host stays on the clean
default route; only *forwarded client* traffic rides the offered route, and the
forwarding mark must **exclude LAN/private ranges** (`10/8`, `172.16/12`,
`192.168/16`) and Tailscale CGNAT (`100.64/10`) — otherwise you misroute LAN/login
traffic into the tunnel (the exact bug that broke login on 2026-06-07).

`mesh-card --refresh` checks this invariant automatically and exits non-zero on
violation — run it before and after any substrate change.
