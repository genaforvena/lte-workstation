#!/usr/bin/env python3
"""Implementation steps settle only on executables (or plans listing them),
wired to a top pane. Receipts are receipts, not artifacts."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"


def main() -> None:
    workspace = Path(tempfile.mkdtemp(prefix=".test-artifact-kind-", dir=ROOT))
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
            "MESH_TASK_ACTOR": "builder",
            "MESH_TASK_MAX_ACTIVE": "8",
            "TEST_BOARD": str(workspace / "board.log"),
        })

        def run(*args: str, expected: int = 0, actor: str = "builder") -> subprocess.CompletedProcess[str]:
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

        def chain(name: str, owner: str, slug: str, tags: str = "", actor: str = "builder") -> None:
            plan = workspace / f"{name}.tsv"
            prefix = "".join(f"#{line}\n" for line in tags.splitlines() if line)
            plan.write_text(prefix + f"{owner}\t{slug}\tdo the thing\n", encoding="utf-8")
            run("create", name, str(plan), actor=actor)
            run("take", name, slug, actor=actor)

        prose = workspace / "note.md"
        prose.write_text("# notes\n", encoding="utf-8")
        tool = workspace / "fix.sh"
        tool.write_text("#!/bin/sh\necho fixed\n", encoding="utf-8")
        plan_empty = workspace / "empty.tsv"
        plan_empty.write_text("builder\tsome-step\tdo it\n", encoding="utf-8")

        # RED: implement-slug + prose artifact is refused.
        chain("c-impl-prose", "builder", "implement-thing")
        out = run("done", "c-impl-prose", "implement-thing", str(prose), "prose", expected=2)
        assert "cannot settle on prose" in (out.stdout + out.stderr)

        # RED: implement-slug + non-executable script is refused.
        chain("c-impl-noexec", "builder", "fix-thing")
        out = run("done", "c-impl-noexec", "fix-thing", str(tool), "fixed pane:check", expected=2)
        assert "is not executable" in (out.stdout + out.stderr)

        # RED: executable without a named pane is refused (unobserved = waste).
        tool.chmod(0o700)
        chain("c-impl-nopane", "builder", "build-thing")
        out = run("done", "c-impl-nopane", "build-thing", str(tool), "built it", expected=2)
        assert "no observing top pane" in (out.stdout + out.stderr)

        # GREEN: executable + pane settles.
        chain("c-impl-ok", "builder", "wire-thing")
        run("done", "c-impl-ok", "wire-thing", str(tool), "wired, observed pane:check")

        # RED: plan listing no executable is refused.
        chain("c-plan-empty", "builder", "split-thing")
        out = run("done", "c-plan-empty", "split-thing", str(plan_empty),
                  "planned pane:dev", expected=2)
        assert "lists no existing executable" in (out.stdout + out.stderr)

        # GREEN: plan naming an executable settles.
        plan_full = workspace / "full.tsv"
        plan_full.write_text(f"builder\trun-step\trun {tool}\n", encoding="utf-8")
        chain("c-plan-full", "builder", "add-thing")
        run("done", "c-plan-full", "add-thing", str(plan_full), "planned pane:dev")

        # GREEN: receipt-only tag bypasses all three checks.
        chain("c-receipt", "builder", "land-thing", tags="tags=receipt-only")
        run("done", "c-receipt", "land-thing", str(prose), "receipt")

        # GREEN: non-implementation slug keeps prose with no pane needed.
        chain("c-verify", "builder", "verify-thing")
        run("done", "c-verify", "verify-thing", str(prose), "checked")

        # RED: genome owner is an implementation lane even with a neutral slug.
        chain("c-genome", "genome", "review-thing", actor="genome")
        out = run("done", "c-genome", "review-thing", str(prose), "reviewed",
                  expected=2, actor="genome")
        assert "cannot settle on prose" in (out.stdout + out.stderr)
    finally:
        import shutil
        shutil.rmtree(workspace, ignore_errors=True)
    print("PASS: implementation artifacts must be executable (or plans naming them) and pane-wired")


main()
