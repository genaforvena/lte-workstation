# Human-readable task ledger contract

Date: 2026-09-08  
Chain: `human-readable-task-ledger-20260908`  
Scope: future authoritative writes only; historical `chat.log` bytes are immutable.

## Decision

Use a new `[task-ledger]` marker with a flat, labelled snapshot. Keep snapshots rather than deriving
state from conversational `[task]`, `[taking]`, and `[done]` receipts: those messages predate the
ledger, can be quoted in prose, and do not carry every future step or every state field. A dedicated
human-readable snapshot preserves atomic replay, revision conflict detection, and recovery while
making the board line directly inspectable.

This is a ledger evolution, not an autopoiesis product. It changes the substrate that autopoiesis
uses; therefore it is an explicit three-step task chain with a separate implementation owner and
witness verification dependency.

## Wire grammar

One physical UTF-8 line:

```text
<timestamp>  <author>  ::  [task-ledger] v1 r=<revision> | <path>=<typed-value> | <path>=<typed-value> ...
```

Examples (abridged only in this document; production snapshots contain every leaf):

```text
[task-ledger] v1 r=1 | /chain=s:demo | /created=s:2026-09-08T10:00:00Z | /current=i:0 | /status=s:open | /steps/0/id=s:demo/build | /steps/0/owner=s:genome | /steps/0/status=s:open | /steps/0/description=s:Build the readable writer
[task-ledger] v1 r=2 | /chain=s:demo | /current=i:0 | /status=s:active | /steps/0/status=s:active | /steps/0/started=s:2026-09-08T10:01:00Z
[task-ledger] v1 r=3 | /chain=s:demo | /current=i:0 | /status=s:blocked | /steps/0/status=s:blocked | /steps/0/blocker_type=s:dependency | /steps/0/needs=s:review artifact
[task-ledger] v1 r=4 | /chain=s:demo | /current=i:0 | /status=s:complete | /steps/0/status=s:done | /steps/0/artifact=s:/tmp/demo.md
[task-ledger] v1 r=4 | /chain=s:demo | /current=i:0 | /status=s:rejected | /steps/0/status=s:rejected | /steps/0/rejected_reason=s:Superseded by demo-v2
```

`path` is a JSON-Pointer-shaped location. Dictionary keys escape `~` as `~0` and `/` as `~1`;
list members use zero-based decimal indexes. Fields are emitted in deterministic dictionary-key order
and list order. The root is reconstructed from paths; duplicate paths, sparse lists, a scalar/list
shape conflict, or an absent root is malformed.

Typed values are intentionally small and readable:

- `s:<text>` string
- `i:<decimal>` integer (booleans are not integers)
- `b:true` or `b:false` boolean
- `n:null` null

String text stays literal UTF-8, including spaces. Only bytes that can break the one-line grammar are
percent escaped: `%` → `%25`, `|` → `%7C`, LF → `%0A`, CR → `%0D`, and other ASCII controls as
uppercase `%HH`. Decoding rejects malformed percent escapes and invalid typed values. This is not a
JSON object and contains no opaque whole-record encoding.

## Ordering and compatibility

- New writes append `[task-ledger]` only. They never append `[task-state]`, `{...}`, or `plist64:`.
- Replay recognizes historical `[task-state]` JSON and plist64 records plus new `[task-ledger]` v1.
- Both formats enter the same validated `{schema, revision, data}` representation.
- Revisions remain per-chain positive integers. Duplicate identical revisions are harmless;
  conflicting duplicates, gaps, and incomplete physical lines fail replay.
- `mesh-chat` scrubs the fully readable line before append. Any scrub mutation rejects the transition.
- The writer appends and fsyncs `chat.log` before replacing disposable JSON caches.

## Required acceptance evidence

1. A test is observed failing while the writer still emits plist64.
2. Unit coverage includes Unicode, spaces, `%`, `|`, LF/CR, null/bool/int, malformed escapes,
   mixed legacy/new history, duplicate delivery, conflict, gap, and truncation.
3. Source-coverage and task lifecycle tests pass.
4. A live canary records the pre-append byte offset, creates/takes/settles a chain, and preserves the
   exact appended suffix as an artifact.
5. That suffix contains readable `[task-ledger]` records and no future `[task-state]`, JSON snapshot,
   or `plist64:` record.
6. `mesh-task replay --json`, `mesh-task audit`, and `mesh-dash --once witness` all consume the mixed
   immutable history and show the canary correctly.
