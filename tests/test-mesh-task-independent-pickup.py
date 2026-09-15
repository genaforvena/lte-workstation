#!/usr/bin/env python3
"""A blocked chain head must not strand owner-attested independent work."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "scripts" / "mesh-task"
sys.path.insert(0, str(ROOT / "scripts"))
from mesh_task_log import eligibility, replay as replay_task_log  # noqa: E402


def main():
    with tempfile.TemporaryDirectory(prefix="mesh-task-independent-") as tmp:
        root = Path(tmp)
        mesh = root / "mesh"
        mesh.mkdir()
        human_log = root / "human-board.log"
        chat = root / "fake-mesh-chat"
        chat.write_text(
            "#!/usr/bin/env python3\n"
            "import os, sys\n"
            "with open(os.environ['MESH_TASK_CHAT_LOG'], 'a', encoding='utf-8') as f:\n"
            "    f.write(' '.join(sys.argv[1:]) + '\\n')\n"
        )
        chat.chmod(0o755)
        env = dict(os.environ)
        env.update({
            "MESH_DIR": str(mesh),
            "MESH_TASK_DIR": str(mesh / "task-chains"),
            "MESH_TASK_CHAT_CMD": str(chat),
            "MESH_TASK_CHAT_LOG": str(human_log),
            "MESH_TASK_LIVE_OWNERS": "alpha beta",
        })

        def run(owner, *args, expect=0):
            got = subprocess.run([sys.executable, str(TASK), *args], env=dict(env, MESH_TASK_ACTOR=owner),
                                 text=True, capture_output=True)
            if got.returncode != expect:
                raise AssertionError(f"{args}: expected rc={expect}, got {got.returncode}\n"
                                     f"stdout={got.stdout}\nstderr={got.stderr}")
            return got

        plan = root / "plan.tsv"
        plan.write_text("alpha\tinspect\tblocked prerequisite\n"
                        "beta\tverify\tindependent follow-up\n", encoding="utf-8")
        run("alpha", "create", "independent-smoke", str(plan))
        artifact = TASK

        # An ordinary successor remains serial and cannot be dispatched or taken.
        assert run("beta", "check", "dispatch", "independent-smoke/verify", "beta", expect=2)
        run("beta", "take", "independent-smoke", "verify", expect=2)

        run("alpha", "take", "independent-smoke", "inspect")
        run("alpha", "block", "independent-smoke", "inspect", "external-event",
            "prerequisite unavailable", "retry after prerequisite")

        # Only the task's exact owner may attest that bypassing the blocked head is safe.
        run("other", "independent", "independent-smoke", "verify",
            "reviewed as independent", expect=2)
        run("beta", "independent", "independent-smoke", "verify",
            "reviewed as independent")

        records = replay_task_log(mesh / "chat.log")
        assert eligibility(records, "independent-smoke/verify", "dispatch", "beta") == 0
        assert run("beta", "check", "dispatch", "independent-smoke/verify", "beta").returncode == 0
        queued = run("beta", "queue", "--dispatch", "--owner", "beta")
        assert "independent-smoke/verify" in queued.stdout
        audit_ready = run("beta", "audit")
        assert "READY_INDEPENDENT\tbeta\tindependent-smoke/verify" in audit_ready.stdout
        gated = {key: {"revision": value["revision"], "data": value["data"]}
                 for key, value in records.items()}
        gated["independent-smoke"]["data"]["steps"][1]["waiting_for"] = "other-chain/prerequisite"
        assert eligibility(gated, "independent-smoke/verify", "dispatch", "beta") == 2
        state = run("beta", "status", "independent-smoke")
        assert "independent_reason=reviewed as independent" in state.stdout

        run("beta", "take", "independent-smoke", "verify")
        run("beta", "block", "independent-smoke", "verify", "external-event",
            "verification fixture unavailable", "resume after fixture appears")
        side_block = run("beta", "audit")
        assert "BLOCKED\tbeta\tindependent-smoke/verify" in side_block.stdout
        run("beta", "resume", "independent-smoke", "verify", "fixture-ready")
        run("beta", "progress", "independent-smoke", "verify", str(artifact),
            "finish independent check", "2026-09-12T21:00:00Z")
        run("beta", "done", "independent-smoke", "verify", str(artifact), "verified")

        audit = run("beta", "audit")
        assert "BLOCKED\talpha\tindependent-smoke/inspect" in audit.stdout
        assert "DONE\tbeta\tindependent-smoke/verify" in audit.stdout
        blocked_status = run("alpha", "status", "independent-smoke")
        assert "independent-smoke [blocked] (1/2)" in blocked_status.stdout
        assert "independent-smoke/verify [done]" in blocked_status.stdout

        # Once the real prerequisite settles, ordered advancement skips the already-done step.
        run("alpha", "resume", "independent-smoke", "inspect", "prerequisite-ready")
        run("alpha", "done", "independent-smoke", "inspect", str(artifact), "prerequisite complete")
        final = run("alpha", "status", "independent-smoke")
        assert "independent-smoke [complete] (2/2)" in final.stdout
        assert "independent-smoke/verify [done]" in final.stdout

        board = human_log.read_text(encoding="utf-8")
        assert board.count("independent-smoke/verify → owner: beta") == 1
        assert "[taking] independent-smoke/verify" in board


if __name__ == "__main__":
    main()
    print("independent task pickup: ok")
