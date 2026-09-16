#!/usr/bin/env python3
"""Real restore output supplies workflow pointers for each chartered window."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
    for charter in sorted((ROOT / "charter").glob("*.md")):
        env = dict(os.environ, MESH_DIR=td, MESH_GENOME=str(ROOT),
                   MESH_HANDOFF_TEST_WINDOW=charter.stem)
        result = subprocess.run(["bash", str(ROOT / "scripts/mesh-handoff"), "--restore"],
                                env=env, text=True, capture_output=True)
        assert result.returncode == 0, result.stderr
        context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
        assert f"Charter for the `{charter.stem}` window" in context
        assert "Mesh operating contract — every engine, every mind" in context
        assert "`mesh:3`" in context
        assert "Standing autonomy orders" in context
        assert "An idea does not wait for a go" in context
        assert "living procedures, not set in stone" in context
        assert "adapt and improve" in context
        for skill in ("mesh-window-turn", "mesh-audit", "mesh-unblock", "mesh-operator-followthrough", "mesh-task-recovery", "mesh-invariants"):
            path = ROOT / ".agents/skills" / skill / "SKILL.md"
            assert str(path) in context, (charter.stem, skill)
            assert path.is_file()
    # A node-local charter remains authoritative while workflows stay discoverable.
    local = Path(td) / "charter"
    local.mkdir()
    (local / "job.md").write_text("LOCAL JOB DUTIES\n")
    result = subprocess.run(["bash", str(ROOT / "scripts/mesh-handoff"), "--restore"],
                            env=dict(env, MESH_HANDOFF_TEST_WINDOW="job"), text=True, capture_output=True)
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "LOCAL JOB DUTIES" in context
    assert "mesh-operator-followthrough/SKILL.md" in context
    assert "Prefer subagents by default" in context
    # A partial deployment must report the missing workflow files.
    missing_genome = Path(td) / "genome"
    result = subprocess.run(["bash", str(ROOT / "scripts/mesh-handoff"), "--restore"],
                            env=dict(env, MESH_HANDOFF_TEST_WINDOW="job", MESH_GENOME=str(missing_genome)),
                            text=True, capture_output=True)
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "workflow UNAVAILABLE" in context
print("PASS: every genome charter restores workflow pointers and local overrides retain precedence")
