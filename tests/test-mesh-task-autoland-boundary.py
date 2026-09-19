#!/usr/bin/env python3
import importlib.machinery
import importlib.util
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "mesh-task"


def load_mesh_task():
    sys.path.insert(0, str(ROOT / "scripts"))
    loader = importlib.machinery.SourceFileLoader("mesh_task_boundary", str(SOURCE))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_autoland_requires_settled_source_and_verified_artifact():
    mesh_task = load_mesh_task()
    artifact = ROOT / "scripts" / "mesh-task"
    completed = {
        "id": "source/work",
        "slug": "work",
        "status": "done",
        "artifact": str(artifact),
        "artifact_sha256": "stale-digest",
    }
    data = {"chain": "source", "steps": [completed]}
    canonical = {"data": data}

    mesh_task.latest_chain_record = lambda chain: canonical if chain == "source" else None
    called = []
    mesh_task.mint_autoland_chain = lambda *_args: called.append("mint") or True
    mesh_task.post_autoland_task = lambda *_args: called.append("post") or True

    with tempfile.TemporaryDirectory() as td:
        assert mesh_task.ensure_autoland_task(Path(td) / "source.json", data, completed) is False
    assert called == []


if __name__ == "__main__":
    test_autoland_requires_settled_source_and_verified_artifact()
    print("test-mesh-task-autoland-boundary: PASS")
