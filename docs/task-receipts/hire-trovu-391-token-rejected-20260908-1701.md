# Hire submission credential rejection — 2026-09-08 17:01Z

- Package: unchanged and previously verified `OK`; acceptance remains `ACCEPT` on `trovu/trovu`.
- Supplied token authenticated as the lane identity `ghIsPureTrash` (`GET /user` returned HTTP 200).
- Scope header was broad: it included `repo`, `workflow`, and administrative scopes; it was not the
  required dedicated `public_repo`-only credential.
- Test command: `scripts/mesh-hire-submit --test`.
- Result: rejected by the gate; no comment, fork, push, or PR was attempted.
- Cleanup: the supplied token was removed from `/home/mesh-home/.mesh/secrets/github-hire.env`.
- Funnel position: blocked pending a replacement classic PAT for `ghIsPureTrash` with exactly
  `public_repo`, stored mode `600` as `GH_HIRE_TOKEN` in that file.
