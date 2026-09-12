# Genome health finding: separate SSH authentication refusal from reachability

The health receipt for `imac-rozalia` records a successful Tailscale ping and ICMP ping followed
by `Permission denied (publickey,password,keyboard-interactive)` from SSH. The health output still
called this `SSH unreachable`, conflating an answering SSH endpoint that refuses credentials with
a transport timeout. The repeated chronic warning is therefore not evidence that the peer is
network-offline; host-side SSH access remains an operator issue.

`scripts/mesh-health` now preserves successful remote probe output and classifies failed SSH
diagnostics. A `Permission denied` diagnostic renders `SKIP … SSH authentication refused` for both
Linux and Android probes. Other nonzero SSH invocations remain `SKIP … SSH unreachable`, and the
probe remains `SKIP` because it could not measure remote internet access. No peer configuration,
credential, route, or network state was changed.

Evidence from `docs/task-receipts/health-warning-45982f4b489126abc294-triage-20260911.md`
(SHA-256 `986fc22067f0d16f3d23e44fbf625e94f7674d2bbe1b710387149461554573d1`), measured
2026-09-11T23:44Z: Tailscale reported `Online=true` and `Active=true`; Tailscale ping and ICMP each
replied 3/3 times; SSH returned 255 with `Permission denied (publickey,password,keyboard-interactive)`.
The later
`health-warning/4989e0902917448d4dfa/triage` dispatch repeats the same `100.121.88.110 — SSH
unreachable` text as a chronic roll-up.

Verification performed:

- `scripts/mesh-health --test` — PASS; its fixture distinguishes permission refusal from connection
  timeout using the production SSH classifier and both Linux/Android render paths.
- `tests/test-mesh-health-ssh-auth-classification.sh` — PASS.
- `bash -n scripts/mesh-health` — PASS.

The new wording improves diagnosis; it does not resolve the iMac's SSH access or infer remote
internet health without a successful login.
