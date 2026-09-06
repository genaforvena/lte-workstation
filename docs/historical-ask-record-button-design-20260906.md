# Historical ask 20260821T004511Z — record-button design

Source: `~/.mesh/voice-in.log`, `2026-08-21T00:45:11Z`.

The ask targets the absent “Granny Keln” application: a phone-accessible record
button, a live recording source, and streaming/control from a phone. No Granny Keln
repository or build target exists in this workspace, so no implementation is claimed.

Implementation contract for the owning repository:

1. expose one explicit `Record` action with visible recording state and stop action;
2. write a non-zero, playable recording artifact and its metadata;
3. expose the control over an authenticated phone session, with an explicit
   disconnect/error state rather than a silent no-op;
4. stream the captured source through the existing mesh audio route; and
5. test the real path end-to-end: button/control event → recording artifact →
   playable stream, including cancellation and reconnect.

This is a design artifact only; the ask remains non-implemented until the target
repository is supplied and the end-to-end test produces its recording artifact.
