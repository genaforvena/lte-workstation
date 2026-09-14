#!/usr/bin/env python3
"""Keep the generated prerequisite-recovery contract complete and concise."""
import importlib.machinery
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
loader = importlib.machinery.SourceFileLoader("mesh_task", str(ROOT / "scripts/mesh-task"))
mesh_task = loader.load_module()


def test_prerequisite_recovery_contract_preserves_rules_with_less_boilerplate():
    description = mesh_task.autonomous_task_description("Do the work")
    for obligation in (
        "before rejecting, inspect repo, ledger, and live mesh",
        "reuse an exact active prerequisite task or create/link one",
        "mesh-owned work and evidence-based decisions/registrations without waiting",
        "parent queued/typed-blocked until gate passes",
        "substitute honestly or record exact event/retry condition",
        "Reject only invalid, duplicate, out-of-scope, or unsafe work with evidence",
    ):
        assert obligation in description
    assert len(description) <= len("Do the work") + 450


if __name__ == "__main__":
    test_prerequisite_recovery_contract_preserves_rules_with_less_boilerplate()
    print("prerequisite-contract: ok")
