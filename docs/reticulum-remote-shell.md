# Reticulum remote shell — the "not-ssh" channel

**Operator ask (2026-07-24):** ssh lags from ilya/rip — want a more stable non-ssh remote channel
over Reticulum. Delivered: `mesh-rns-sh`, an ssh-free remote shell/exec over an RNS Link.

## Why it's more stable than ssh here

- **It rides the LAN directly.** ilya dials mesh-home's rnsd at `192.168.8.225:4242` (on-link /24),
  so the RNS traffic goes straight over the wifi L2 — **it never touches the laggy tailscale/egress
  path** that ssh was crawling through. (mesh-home egress is ~350KB/s and the sole wifi path deauths
  ~every 14 min — ssh sessions die on it; an RNS Link does not depend on it.)
- **An RNS Link resumes; a TCP ssh session dies.** Reticulum re-establishes across brief drops and
  path changes instead of dropping you to a dead prompt.
- **Transport-agnostic.** The same shell carries onto LoRa/RNode radio later with no change.

## Use it

From any node on the RNS network (mesh-home, ilya):

```bash
mesh-rns-sh ilya                 # interactive shell on ilya          (rnsh)
mesh-rns-sh ilya uptime          # run one command on ilya, print out (rnx)
mesh-rns-sh ilya 'bash -c "df -h; free -m"'   # shell command (quote the whole thing)
mesh-rns-sh mesh-home            # interactive shell on mesh-home (from another node)
mesh-rns-sh --list               # show known nodes + their dest hashes
mesh-rns-sh --serve              # (re)start THIS node's listeners — idempotent, kept up by cron/reflex
```

A connect shows a brief spinner (`Path requested → Establishing link → Command delivered`) — that is
the Link coming up, like watching ssh connect; the output follows it.

## How it's wired

- **Transport:** `rnsd` on each node (mesh-home = `mesh-reticulum.service`, a transport node on
  `0.0.0.0:4242` + wifi AutoInterface; ilya joins via a `TCPClientInterface` to the LAN IP). Bring a
  peer's rnsd up with `~/.mesh/rns-up.sh`.
- **Listeners:** `rnx -l` (one-shot exec) + `rnsh -l` (interactive shell), started by
  `mesh-rns-sh --serve`, kept alive by the shim's `# reflex-cadence: */5 --serve` on mesh-home and a
  `*/5` crontab entry on ilya.
- **Auth (identity-based, fail-safe):** listeners run `-a <hash>` per line of `~/.mesh/rns-allowed`
  (trusted client identity hashes). `--serve` **REFUSES to start with an empty allowlist** — a
  no-`-a` listener is an open shell to the whole RNS net. Add a new client's identity hash to
  `~/.mesh/rns-allowed` on every node to let it connect.
- **Registry:** `~/.mesh/rns-nodes` maps `<node> <rnsh_hash> <rnx_hash>` (runtime state, per node).

## Verify (`--test`)

`mesh-rns-sh --test`: asserts the fail-safe refusal, the allowlist→`-a` flag mapping, and a **live
E2E rnx round-trip** through this node's own listener (a nonce must come back — a broken channel
FAILs, an absent rnsd is honest exit 2).

## Not yet: rip + radio

`rip` isn't on the LAN (tailscale peer `100.116.125.102`), so its RNS link would go over tailscale-TCP
— more *resilient* than ssh (Link resume) but the same underlying path, not the LAN bypass ilya gets.
Setup = RNS venv + `rns-up.sh` join + `mesh-rns-sh --serve` on rip, then add it to `~/.mesh/rns-nodes`
+ its client identity to `~/.mesh/rns-allowed`. The RF lane (RNode/LoRa, `reticulum-radio-lane.md`) is
the true-independent transport.

## Files
- `scripts/reticulum/mesh-rns-sh.sh` — the tool  ·  `scripts/mesh-rns-sh` — deploy shim
- `~/.mesh/{rns-nodes,rns-allowed,rns-exec.id}` — registry / allowlist / exec identity (per node)
- `~/.mesh/rns-up.sh` — bring a node's rnsd up and join the network
