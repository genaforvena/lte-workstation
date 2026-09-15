# chat.log no-new-JSON canary — 2026-09-08

Scope: future structured task-state appends only. Historical JSON records remain unchanged.

Implementation:

- New task-state records use deterministic binary property-list data encoded as URL-safe base64 and prefixed `plist64:`.
- Replay accepts both historical JSON and new `plist64:` records.
- Secret screening still runs against an in-memory plaintext representation before append; that representation is never written to `chat.log`.

Verification results are appended below after the live canary.
