# Zero trust at the capability router: request checks do not revoke sessions

## Review

The latest successful `mesh-study` brief on zero trust (2026-09-11) surfaced an urgent-care
architecture article. The transferable mechanism is the distinction in NIST SP 800-207 between a
policy decision and a policy enforcement point (PEP): the PEP enables, monitors, and eventually
terminates access, and receives policy updates from the decision side. NIST's implementation guide
also describes real-time risk assessment as part of establishing and maintaining access. See
[NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) and
[NIST SP 1800-35, Volume A](https://pages.nist.gov/zero-trust-architecture/VolumeA/ExecutiveSummary.html).

The mesh capability router already has a per-invocation enforcement point: `scripts/mesh-organ`
reads the capability's current `# cap-allow:` list immediately before executing it and denies an
unlisted caller with exit 3. Its local self-test covers allowed, denied, and unrestricted calls.
The unembodied boundary is session maintenance: once an allowed long-running capability starts,
changing its allow-list does not terminate that process. This is distinct from the useful, already
implemented request-time authorization, so the policy should not be described as revoking active
work.

## Applied probe

Ran the actual `scripts/mesh-organ` router against an isolated temporary capability directory and
disabled only its route log. Request one was authorized as `discover`; its child began and slept.
While it was active, atomically replaced its allow-list with `health`. Request two, from the same
`discover` caller, was denied with exit 3 and named the new allow-list. The original child remained
alive and completed. The child artifact was exactly:

```text
started
finished
```

This verifies that authorization is re-read for each new request, while revocation does not reach
an already-running child. The probe used temporary files only and made no live-policy changes. It
was a behavioral probe, not a change to the router or a claim that the mesh needs session-kill
semantics for every organ.

## Design implication

If a future long-running capability requires immediate revocation, that capability needs an
explicit session contract and an enforcement mechanism that can observe policy changes and stop its
own work. A generic router-wide kill path should be considered only with a concrete organ and
operator requirement; the present evidence establishes the boundary, not the need for that broader
actuator.

## Current organ check (2026-09-12 12:31Z)

The live manifest exposed capabilities on mesh-home and phaedra; the other declared hosts were
offline or unreachable during this check. Neither reachable node had executable files in
`~/.mesh/caps` carrying a `# cap-allow:` policy. Direct `mesh-organ --scope` checks reported
`cap-allow=<unrestricted>` for `dlna-tv@mesh-home` and `dlna-tv@phaedra`, and for the local
camera, mic, UVC-metadata, display-link, and TV capabilities. There is therefore no active scoped
policy whose revocation can currently be claimed to terminate an organ session.

One concrete persistent process does exist: `mesh-organ dlna-tv` resolves to `mesh-tv-dlna`, which
starts a detached Range HTTP server on port 8099 (`start_new_session=True`, `serve_forever()`) and
reuses it to preserve playback across video switches. The router's wait-and-record wrapper cannot
own or terminate that detached child. The tool's `stop` verb sends a DLNA playback command; it is not
a server-session revocation contract. No such server process was running during this check.
`mesh-uvc-metadata`, by contrast, performs bounded retries and exits after one capture.

Decision: `mesh-tv-dlna` is the concrete candidate if its capability is later given a restrictive
allow-list or an operator states that policy changes must end active playback. Neither condition is
present now: its live scope is unrestricted and no immediate-revocation requirement was found. I did
not add a generic router kill path or alter playback. If that policy is introduced, define the TV
organ's own session identity/owner, policy re-read boundary, and stop behavior for the detached
server and active streams before calling it revocation.

## Feed status

`mesh-study` was attempted on 2026-09-12, but its pulls failed with `OAuth session expired and
could not be refreshed` (including the 12:05Z genetic-algorithm and chaos-engineering pulls). This
review used the newest successful zero-trust brief in `~/.mesh/study.log`.
