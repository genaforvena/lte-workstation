#!/usr/bin/env python3
import importlib.machinery
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
loader = importlib.machinery.SourceFileLoader("mesh_task", str(ROOT / "scripts/mesh-task"))
spec = importlib.util.spec_from_loader("mesh_task", loader)
mesh_task = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mesh_task)


def test_common_experiment_labels_receive_parameter_contract():
    for label in ("benchmark", "ablation", "replication"):
        description = mesh_task.autonomous_task_description(f"Run a {label} and compare configurations")
        assert "machine-owned parameter selection" in description
        assert "corpus/dataset manifests" in description
        assert "cross-validation folds/repeats" in description
        assert "not applicable" in description


if __name__ == "__main__":
    test_common_experiment_labels_receive_parameter_contract()
    print("autonomy-detection: ok")
