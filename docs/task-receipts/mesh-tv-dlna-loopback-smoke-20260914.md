# mesh-tv-dlna loopback smoke diagnosis — 2026-09-14

Task: `chat-review-mesh-tv-dlna-loopback-smoke-20260914/diagnose-local-origin-timeout`.

## Finding

The proxy-bypass smoke arm timed out because it tested a same-host TCP connection to the node's
current LAN-source address, `100.74.169.95`. That address is inside `100.64.0.0/10`, which the live
Tailscale input chain drops when a packet arrives on an interface other than `tailscale0`. The local
route for `100.74.169.95` resolves to `lo`, so a connection from the test process back to its own
server matches that anti-spoof rule. The origin server never receives the request. This is a host
firewall-policy interaction in the test fixture, not evidence that `http_open()` sent the request
through a proxy or that HTTP access to a different LAN host times out.

The task's earlier description named `100.76.75.116`; at investigation time the default route had
changed to `via 100.74.0.1 dev enp42s0 src 100.74.169.95`, with `100.74.169.95/16` assigned to
`enp42s0`. `ip route get 100.74.169.95` returned `local ... dev lo`. The live `ts-input` chain
accepted `100.81.222.19` on `lo`, then dropped `100.64.0.0/10` sources arriving off `tailscale0`.

Before the change, `python3 scripts/mesh-tv-dlna --test` reproduced:

```text
smoke-test: FAIL (http_open raised while bypassing: <urlopen error timed out>)
```

A minimal `HTTPServer` reproduction bound to `100.74.169.95` also timed out through both urllib's
direct opener and a raw TCP connection, while the same fixture on `127.0.0.1` returned `origin`.
No routes, firewall rules, VPN settings, or TV state were changed.

## Change and verification

Commit `8852eadf` (`mesh-land: update scripts/mesh-tv-dlna: Isolate proxy-bypass tests from Tailscale CGNAT self-connection drops`)
changes only the smoke-test fixture. It now serves the origin on `127.0.0.2` as `lan-origin.test`,
with a scoped resolver mapping for that test hostname. The configured default opener returns the
proxy's `PROXIED` response, while `http_open()` returns `origin`; this keeps the control arm
discriminating without relying on the node's LAN address or firewall policy. The source and deployed
`~/.local/bin/mesh-tv-dlna` hashes match at
`d5be63b1a90c0d24936d101ff62cb44a09f0b2c48c7ec5edf22b65d6570e01ce`.

`python3 -m py_compile scripts/mesh-tv-dlna` and `git diff --check -- scripts/mesh-tv-dlna` passed.
The updated source test and deployed `mesh-tv-dlna --test` both passed the HTTP proxy-bypass arm and
then exited `2` at the separate SSDP check. Its evidence says multicast is `state=swallowed`, with
`dev=tailscale0` and `lan_dev=enp42s0`; the TV was not queried or changed. `mesh-tv --test` forwarded
that downstream result and exited `0`.

The remaining limitation is explicit: this node cannot currently verify renderer discovery because
its SSDP path is swallowed. The HTTP self-test now isolates proxy selection from that multicast
limitation and from Tailscale's same-host CGNAT-source filter.
