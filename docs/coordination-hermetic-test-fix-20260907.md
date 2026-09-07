# Coordination test isolation fix — 2026-09-07

## Fixed

`scripts/mesh-mind-control --test` now creates and exports a private
`MESH_MC_CHATLOG` under its fenced test directory. Its ACK-pruning path also
reads `${MESH_MC_CHATLOG:-$HOME/.mesh/chat.log}` instead of unconditionally
reading the live board. This prevents a real `[taking]` from another task from
turning an unrelated picker fixture into an owner hold.

## Evidence

- Before the fix, the bounded ownership suite observed the live
  `mood-lora-bench` claim and emitted false `remote-phaedra`/hold failures.
- After the fix, the live board no longer enters the test fixture. `bash -n
  scripts/mesh-mind-control` passes.
- The full `mesh-mind-control --test` still exceeds a 15-second diagnostic
  bound in a later dispatch fixture. `strace` shows the timed process waiting
  after spawning a child that never reaches `execve`; this remains unresolved
  and is not claimed green.

## Other open coordination obligations

- `vpn` is held with repeated owner-authored stale/declined closures and current
  tunnel-pass evidence; no VPN actuation is authorized here.
- `witness-vpn` remains a distinct historical promise after a partial keyed
  discharge; it needs exact obligation-level closure or an explicit hold.
- `mood-lora-bench` is now durably `RUNNING` under genome with a valid lease;
  its artifact and verification are still pending.
