#!/usr/bin/env python3
"""Tagged audits cannot settle until every finding has a ledger disposition."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"


def main() -> None:
    workspace = Path(tempfile.mkdtemp(prefix=".test-audit-followthrough-", dir=ROOT))
    try:
        mesh = workspace / "mesh"
        writer = workspace / "writer"
        writer.write_text("#!/bin/sh\nprintf '%s\\n' \"$1\" >>\"$TEST_BOARD\"\n", encoding="utf-8")
        writer.chmod(0o700)
        env = dict(os.environ)
        env.update({
            "MESH_DIR": str(mesh),
            "MESH_TASK_DIR": str(mesh / "chains"),
            "MESH_TASK_CHAT_CMD": str(writer),
            "MESH_TASK_HANDOFF_CMD": "/bin/true",
            "MESH_TASK_ACTOR": "auditor",
            "MESH_TASK_MAX_ACTIVE": "8",
            "TEST_BOARD": str(workspace / "board.log"),
        })

        def run(*args: str, expected: int = 0, actor: str = "auditor") -> subprocess.CompletedProcess[str]:
            result = subprocess.run(
                [sys.executable, str(TASK), *args],
                env=dict(env, MESH_TASK_ACTOR=actor),
                text=True,
                capture_output=True,
                check=False,
            )
            assert result.returncode == expected, (
                f"{args!r}: expected rc={expected}, got {result.returncode}\n"
                f"stdout={result.stdout}\nstderr={result.stderr}"
            )
            return result

        def plan(name: str, tagged: bool = True, owner: str = "auditor") -> Path:
            path = workspace / f"{name}.tsv"
            prefix = "#tags=audit-followthrough\n" if tagged else ""
            path.write_text(prefix + f"{owner}\treview\treview evidence and disposition findings\n", encoding="utf-8")
            return path

        def artifact(name: str) -> Path:
            path = workspace / f"{name}.md"
            path.write_text(f"# {name}\n", encoding="utf-8")
            return path

        def manifest(path: Path, findings: list[dict]) -> None:
            Path(str(path) + ".findings.json").write_text(
                json.dumps({"version": 1, "findings": findings}) + "\n",
                encoding="utf-8",
            )

        audit_artifact = artifact("audit")
        run("create", "tagged-audit", str(plan("tagged-audit")))
        dispatch_text = (workspace / "board.log").read_text(encoding="utf-8")
        assert "finding manifest" in dispatch_text and "cannot reject" in dispatch_text
        run("take", "tagged-audit", "review")
        missing = run("done", "tagged-audit", "review", str(audit_artifact), expected=2)
        assert "finding manifest" in missing.stderr
        state = json.loads((mesh / "chains" / "tagged-audit.json").read_text(encoding="utf-8"))
        assert state["status"] == "active"

        manifest(audit_artifact, [{
            "id": "missing-task",
            "actionable": True,
            "task": "corrective/fix",
            "owner": "fixer",
        }])
        absent = run("done", "tagged-audit", "review", str(audit_artifact), expected=2)
        assert "does not exist" in absent.stderr

        run("create", "corrective", str(plan("corrective", tagged=False, owner="fixer")))
        manifest(audit_artifact, [{
            "id": "wrong-owner",
            "actionable": True,
            "task": "corrective/review",
            "owner": "someone-else",
        }])
        wrong = run("done", "tagged-audit", "review", str(audit_artifact), expected=2)
        assert "owner mismatch" in wrong.stderr

        manifest(audit_artifact, [{
            "id": "routed-finding",
            "actionable": True,
            "task": "corrective/review",
            "owner": "fixer",
        }])
        run("done", "tagged-audit", "review", str(audit_artifact), "all findings routed")

        no_action_artifact = artifact("no-action")
        run("create", "no-action-audit", str(plan("no-action-audit")))
        run("take", "no-action-audit", "review")
        manifest(no_action_artifact, [{
            "id": "checked-cleanly",
            "actionable": False,
            "reason": "the measured state already satisfies the acceptance condition",
        }])
        run("done", "no-action-audit", "review", str(no_action_artifact), "no corrective work")

        run("create", "reject-audit", str(plan("reject-audit")))
        run("take", "reject-audit", "review")
        bypass = run("reject", "reject-audit", "review", "nothing to do", expected=2)
        assert "cannot be rejected" in bypass.stderr

        ordinary_artifact = artifact("ordinary")
        run("create", "ordinary", str(plan("ordinary", tagged=False)))
        run("take", "ordinary", "review")
        run("done", "ordinary", "review", str(ordinary_artifact), "ordinary completion unchanged")
        print("PASS: tagged audits require verified finding-to-ledger dispositions; rejection cannot bypass")
    finally:
        shutil.rmtree(workspace)


if __name__ == "__main__":
    main()
