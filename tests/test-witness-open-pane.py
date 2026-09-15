"""Exercise the real renderer against an isolated coordination summary."""
import os
from pathlib import Path
import runpy
import tempfile
from unittest.mock import patch

repo = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"HOME": directory}):
    mesh = Path(directory) / ".mesh"
    mesh.mkdir()
    (mesh / "witness.log").write_text("2026-09-08T03:00:00Z senses=UNKNOWN\n")
    summary = mesh / "tasks.journal"
    content = ("timestamp=2026-09-08T03:00:00Z\n"
               "DONE\tjob\tchain/completed-only\tartifact=/proof\n"
               "RUNNING\tjob\tchain/current\tlease=future\n"
               "BLOCKED\tvpn\tchain/verification\tblocker_type=dependency\tretry=waiting-for-input\n"
               "QUEUED\tjob\tchain/next\tcurrent=chain/current\n")
    summary.write_text(content)
    module = runpy.run_path(str(repo / "scripts/mesh-witness"), run_name="witness_test")
    render = module["render_pane"]
    render.__globals__["_labour_tree"] = lambda: "fixture labour"
    pane = render(embed=True)
    assert "completed-only" not in pane, "completed task still shown in pane"
    for task in ("chain/current", "chain/verification", "chain/next"):
        assert task in pane, f"unfinished task hidden: {task}"
    assert "BLOCKED\tvpn\tchain/verification\tblocker_type=dependency\tretry=waiting-for-input" in pane
    assert summary.read_text() == content, "renderer changed audit history"
print("witness open pane: PASS")
