#!/usr/bin/env python3
import importlib.machinery
import importlib.util
import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "job" / "mesh-job-apply"
loader = importlib.machinery.SourceFileLoader("mesh_job_apply", str(SOURCE))
spec = importlib.util.spec_from_loader("mesh_job_apply", loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)


def test_tg_summary_excludes_needs_human_and_machine_skips():
    results = [
        ({"employer": "Confirmed Co", "title": "Team Lead"}, "sent", ""),
        ({"employer": "Question Co", "title": "Engineering Manager"},
         "needs-human", "question is not in the fact bank"),
        ({"employer": "No Fit Co", "title": "CTO"}, "dropped", "no approved letter blocks"),
    ]

    text = mod.tg_summary(results, {"Confirmed Co"})

    assert "Confirmed Co" in text
    assert "Question Co" not in text
    assert "No Fit Co" not in text


def test_tg_summary_is_empty_when_no_application_was_confirmed():
    results = [
        ({"employer": "Question Co", "title": "Engineering Manager"},
         "needs-human", "question is not in the fact bank"),
    ]

    assert mod.tg_summary(results, set()) == ""


if __name__ == "__main__":
    test_tg_summary_excludes_needs_human_and_machine_skips()
    test_tg_summary_is_empty_when_no_application_was_confirmed()
    print("test-job-apply-tg-policy: PASS")
