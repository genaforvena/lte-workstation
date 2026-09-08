"""Promise-family age may signal attention but must not remove an open obligation."""
import os
import subprocess
import tempfile
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    mesh = root / "mesh"
    mesh.mkdir()
    (mesh / "chat.log").write_text(
        "2020-01-01T00:00:00Z genome@n :: [task] old-open-task: explicit closure required owner:genome\n"
    )
    env = dict(os.environ, HOME=str(root), MESH_DIR=str(mesh), MESH_CHAT_LOG=str(mesh / "chat.log"),
               MESH_PROMISES_DIR=str(mesh / "promises"), MESH_PROMISE_ROSTER="genome",
               MESH_ASK_VOICE_IN=str(mesh / "no-voice"), MESH_ASK_TG_SENT=str(mesh / "no-tg"))
    result = subprocess.run(["bash", str(repo / "scripts/mesh-promises"), "--json"], env=env,
                            text=True, capture_output=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert '"retired": 0' in result.stdout, result.stdout
    assert 'old-open-task' in result.stdout, result.stdout
print("PASS: age never retires an open promise by default")
