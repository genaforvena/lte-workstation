#!/usr/bin/env python3
"""The witness sees both missing and stale observation, without replaying the ledger."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
    mesh = Path(td)
    (mesh / "chat.log").write_text("")
    (mesh / "operator-intake").mkdir()
    status = mesh / "operator-intake/status.json"
    for stamp, expected in [(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "GAPS"),
                            ("2000-01-01T00:00:00Z", "STALE")]:
        status.write_text(json.dumps(dict(run=stamp, health="GAPS", missing=2)))
        result = subprocess.run([str(ROOT / "scripts/mesh-dash"), "--once", "witness"],
                                env=dict(os.environ, MESH_DIR=td, MESH_REPO=str(ROOT)),
                                text=True, capture_output=True, timeout=20)
        assert f"intake={expected} gaps=2" in result.stdout, result.stdout
    status.unlink()
    result = subprocess.run([str(ROOT / "scripts/mesh-dash"), "--once", "witness"],
                            env=dict(os.environ, MESH_DIR=td, MESH_REPO=str(ROOT)),
                            text=True, capture_output=True, timeout=20)
    assert "intake=UNKNOWN" in result.stdout, result.stdout
print("PASS: witness pane exposes intake gaps, stale observer and missing status")
