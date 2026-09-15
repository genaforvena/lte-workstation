#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
policy="$root/docs/design-tg-presence-and-ledger-dispatch-20260907.md"

[[ -s "$policy" ]] || {
  echo "policy test: FAIL (missing staffing policy artifact: $policy)" >&2
  exit 1
}

python3 - "$policy" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text()
required = [
    "window", "role", "live", "protected", "open_promises", "open_holds",
    "eligible", "reason", "observed_at", "fails closed", "human-owned",
    "mutation",
]
missing = [word for word in required if word not in text]
if missing:
    raise SystemExit("policy test: FAIL (artifact missing: " + ", ".join(missing) + ")")

# The frozen fixture is deliberately local and deterministic.  It models the
# inputs consumed by the future read-only query without touching live tmux or Ledger.
fixture = [
    {"window": "tg", "role": "communication", "live": True, "protected": False,
     "open_promises": 0, "open_holds": 0, "human_owned": False},
    {"window": "haunt", "role": "research", "live": True, "protected": False,
     "open_promises": 0, "open_holds": 0, "human_owned": False},
    {"window": "genome", "role": "substrate", "live": True, "protected": True,
     "open_promises": 1, "open_holds": 0, "human_owned": False},
    {"window": "witness", "role": "witness", "live": False, "protected": False,
     "open_promises": 0, "open_holds": 0, "human_owned": False},
    {"window": "human", "role": "operator", "live": True, "protected": False,
     "open_promises": 1, "open_holds": 0, "human_owned": True},
]

def classify(row):
    if not row["live"]:
        return False, "not-live"
    if row["window"] in {"tg", "tg-roz"}:
        return False, "communication-window"
    if row["human_owned"]:
        return False, "human-owned"
    if row["protected"]:
        return False, "protected-role-or-substrate"
    if row["open_holds"]:
        return False, "open-hold"
    if row["open_promises"]:
        return False, "already-owned-work"
    return True, "eligible"

verdicts = {row["window"]: classify(row) for row in fixture}
assert [name for name, (ok, _) in verdicts.items() if ok] == ["haunt"], verdicts
assert verdicts["tg"] == (False, "communication-window")

# Mutation arm: making tg look free must not make it a worker.
mutated = next(row for row in fixture if row["window"] == "tg").copy()
mutated.update(role="research", open_promises=0, open_holds=0)
ok, reason = classify(mutated)
assert not ok and reason == "communication-window", (ok, reason)

print("test-mesh-tg-dispatch-policy: PASS (5 fixture rows; only haunt eligible; TG mutation rejected)")
PY
