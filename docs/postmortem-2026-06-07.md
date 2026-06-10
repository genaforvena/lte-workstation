# Postmortem: VPN routing outage — 2026-06-05–07

**Symptom**: "internet was down from the router to all machines" after agents fulfilled the request
"route all traffic on my phone through a machine with a VPN."

**Duration**: ~2 days (2026-06-05 to 2026-06-07).

---

## What happened

Three routing changes were layered on `default-string` and the LAN router by agents acting on a
single-node VPN request:

1. `default-string` was made a **Tailscale exit node** (`--advertise-exit-node`), and other nodes
   were pointed at it (`--exit-node=100.125.157.75`).
2. A **full-tunnel commercial WireGuard** (`dlmrgf`, `AllowedIPs=0.0.0.0/0`, endpoint
   `194.147.115.17:12331`) was brought up on `default-string`, with IP forwarding on.
3. A **`wgclient` WireGuard interface on the OpenWRT router** itself was added, routing the
   entire LAN through the VPN.

Net effect: every node's internet — and the whole LAN's — funnelled through one foreign VPN
endpoint. When the endpoint flapped, the internet was gone for everyone.

Degradation persisted after the event: IdeaPad latency to 1.1.1.1 was ~390 ms; IdeaPad had
100% packet loss via exit-node due to missing MASQUERADE for dlmrgf.

---

## Root causes

**1. Global scope, not local** — the user wanted one VM routed. The agents advertised an exit
node for everyone, full-tunnelled the shared host, and added a `wgclient` to the **router** (the
whole LAN). Blast radius far exceeded the request.

**2. Involuntary coupling** — other nodes and every device behind the router inherited a route
they never opted into.

**3. Control plane tied to data plane** — `dlmrgf` with `AllowedIPs=0.0.0.0/0` captured all of
`default-string`'s own traffic, including SSH and Tailscale. When the VPN endpoint died, the
host became unreachable.

**4. No before/after verification** — "VPN is up" (interface exists) was the only artifact.
"Every node still reaches 1.1.1.1" was never checked.

**5. No durable trace** — the next agent had to reconstruct the whole change forensically from
`journald` + session `.jsonl`. `mesh-trace` existed but was not used for substrate changes.

---

## What was NOT wrong

The feature itself is legitimate: the IdeaPad VM egressing through `default-string`'s VPN is a
valid personal operator arrangement. The problem was *how* the coupling was built, not that the
coupling exists.

---

## Fixes applied

- `dlmrgf` config: `Table = off` — wg-quick no longer hijacks the default route; the host's own
  SSH/Tailscale uses `wlp2s0` always.
- PostUp policy routing: only exit-node forwarded traffic (from tailscale0, destined outside
  Tailscale subnet) is routed through dlmrgf, with MASQUERADE.
- Router `wgclient`: **to be removed** — needs router login (todo, flagged).
- `mesh-health` script: before/after artifact for future substrate changes.
- `mesh-dms` script: dead-man's switch wrapper for substrate changes.
- CLAUDE.md: substrate doctrine, kernel doctrine, tmux convention, no central registry.
- `vpn-hub.service` retired: central WG registry replaced by Tailscale + local traces.

---

## Doctrine updates

See CLAUDE.md § "Substrate changes — mandatory protocol" and § "The kernel".

---

## Lessons (summary)

1. **Scope must match the request.** One VM → touch one VM.
2. **Control plane ≠ data plane.** The host's management path must never depend on the VPN.
3. **Verification extends to regressions.** Check every node's internet before and after.
4. **Emergence works for commons; not for exclusive resources.** The routing table is not
   `mesh-trace`. Concurrent substrate mutations without coordination are dangerous.
5. **The easy path wins under pressure.** Secrets/passwords pasted into prompts instead of going
   through age+SOPS. Wiring ideals into the easy path is the real fix.
