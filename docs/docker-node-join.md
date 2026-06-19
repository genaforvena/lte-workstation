# Docker Node Join — running a mesh mind in a container

A Docker container is a valid mesh node. The genome is substrate-agnostic: as long as
SSH is reachable and a tmux session exists, it's a node. This guide covers the two main
cases: a **mind node** (Claude or other agent) and a **plain shell node** (compute/relay).

## Why Docker

- Instant disposable minds: `docker run` → mesh node in seconds
- Clean separation: each container is a fresh identity, gets its own Tailscale key
- CI/test: spin up a node, run a reflex, tear down — no permanent host changes

## Tailscale in a container

Tailscale needs either root+`NET_ADMIN`+`NET_RAW` caps, or **userspace networking mode**
(no root, no caps — preferred in constrained environments).

```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y curl tmux git openssh-server
# Tailscale
RUN curl -fsSL https://tailscale.com/install.sh | sh
```

Start options:

```bash
# Option A: privileged (full kernel networking, exit-node capable)
docker run -d --name mesh-node \
  --cap-add NET_ADMIN --cap-add NET_RAW \
  --device /dev/net/tun \
  -e TS_AUTHKEY=tskey-auth-... \
  mesh-image

# Option B: userspace networking (no root caps, not an exit-node, still mesh-reachable)
docker run -d --name mesh-node \
  -e TS_AUTHKEY=tskey-auth-... \
  -e TS_EXTRA_ARGS="--tun=userspace-networking" \
  mesh-image
```

Use a **one-time** Tailscale auth key from the admin console (never reuse keys from logs).
Tag it `tag:lte-node` in the key settings or with
`tailscale up --advertise-tags=tag:lte-node` inside the container after auth.

## Minimal Dockerfile — mind node

```dockerfile
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y curl tmux git openssh-server nodejs npm sudo

# Tailscale
RUN curl -fsSL https://tailscale.com/install.sh | sh

# Claude Code (or swap for another agent)
RUN npm install -g @anthropic-ai/claude-code

# Genome
RUN git clone https://github.com/genaforvena/lte-workstation /root/lte-workstation
RUN cp /root/lte-workstation/scripts/mesh-* /usr/local/bin/ && chmod +x /usr/local/bin/mesh-*

# Entrypoint: auth Tailscale, then run mesh-restore (opens tmux session + chat room)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

```bash
#!/usr/bin/env bash
# entrypoint.sh
set -e
# Start Tailscale daemon
tailscaled --tun=userspace-networking &
sleep 2
tailscale up --authkey="${TS_AUTHKEY}" --advertise-tags=tag:lte-node --hostname="${HOSTNAME}"
# Restore mesh session (tmux + chat + snapshot loop)
# PATH-resolved: the Dockerfile installs tools to /usr/local/bin (on PATH);
# fall back to the repo copy if tools were installed elsewhere.
mesh-restore 2>/dev/null || /root/lte-workstation/scripts/mesh-restore
# Keep container alive via tmux session
exec tmux new-session -A -s "$(hostname)"
```

## Running bootstrap.sh inside a container

`bootstrap.sh` runs as-is once Tailscale is up. It enables Tailscale SSH, tags the node,
and copies mesh tools — the same flow as a bare-metal node:

```bash
docker exec -it mesh-node bash -c "cd /root/lte-workstation && ./bootstrap.sh"
```

## Stateful filtering warning (Docker + Tailscale)

Tailscale itself flags this: Docker's `iptables` rules can interfere with DNS and mesh
connectivity inside containers. Symptoms: container can reach the internet but can't
resolve Tailscale node names.

Fix: add `--dns=100.100.100.100` to `docker run`, or set it in `daemon.json`:

```json
{ "dns": ["100.100.100.100", "8.8.8.8"] }
```

## Substrate rule still applies

A Docker container that offers a route (exit-node, relay) must not carry its own
Tailscale control-plane traffic on that route. Same invariant as a bare-metal node —
`mesh-card --refresh` flags violations.

## Quick-start (userspace, no caps, mind node)

```bash
# Create entrypoint.sh from the example in the "Minimal Dockerfile — mind node" section
cat > entrypoint.sh << 'ENTRYPOINT'
#!/usr/bin/env bash
set -e
tailscaled --tun=userspace-networking &
sleep 2
tailscale up --authkey="${TS_AUTHKEY}" --advertise-tags=tag:lte-node --hostname="${HOSTNAME}"
mesh-restore 2>/dev/null || /root/lte-workstation/scripts/mesh-restore
exec tmux new-session -A -s "$(hostname)"
ENTRYPOINT
chmod +x entrypoint.sh

# Create a Dockerfile from the "Minimal Dockerfile — mind node" section above
cat > Dockerfile.mind << 'DOCKERFILE'
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y curl tmux git openssh-server nodejs npm sudo
RUN curl -fsSL https://tailscale.com/install.sh | sh
RUN npm install -g @anthropic-ai/claude-code
RUN git clone https://github.com/genaforvena/lte-workstation /root/lte-workstation
RUN cp /root/lte-workstation/scripts/mesh-* /usr/local/bin/ && chmod +x /usr/local/bin/mesh-*
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
DOCKERFILE

# Build
docker build -f Dockerfile.mind -t mesh-mind .

# Run (get a fresh one-time key from https://login.tailscale.com/admin/settings/keys)
docker run -d --name my-mesh-mind \
  -e TS_AUTHKEY=tskey-auth-<one-time-key> \
  -e ANTHROPIC_API_KEY=... \
  mesh-mind

# Attach to the node's tmux session
docker exec -it my-mesh-mind tmux new-session -A -s "$(docker exec my-mesh-mind hostname)"
```

The container joins the mesh, its session appears in `tailscale status`, and other nodes
can reach it via `mesh-tell --node user@<ts-ip> <window> <prompt>`.
