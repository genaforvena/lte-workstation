#!/usr/bin/env python3
"""Build leakage-safe, metadata-only fixtures for the wake model evaluation.

The default output contains source hashes, counts, time bounds, split cutoffs, and
series definitions. It does not copy chat text or sensor rows into the artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


UTC = timezone.utc
DEFAULT_ROOT = Path("/home/mesh-home/.mesh")
MODEL_CARDS = {
    "timesfm": {
        "id": "google/timesfm-3.0-pytorch",
        "card": "https://huggingface.co/google/timesfm-3.0-pytorch",
        "license": "TimesFM Non-Commercial License v1.0",
        "license_url": "https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE",
    },
    "spark": {
        "id": "XHToken/Spark-X2.5-4B",
        "card": "https://huggingface.co/XHToken/Spark-X2.5-4B",
        "license": "Apache-2.0",
        "license_url": "https://github.com/XHToken/Spark-X2.5/blob/main/LICENSE",
    },
    "minicpm": {
        "id": "openbmb/MiniCPM5-2B",
        "card": "https://huggingface.co/openbmb/MiniCPM5-2B",
        "license": "Apache-2.0",
        "license_url": "https://github.com/OpenBMB/MiniCPM/blob/main/LICENSE",
    },
}


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def file_meta(path: Path) -> dict:
    if not path.exists():
        return {"path": str(path), "present": False, "bytes": 0, "sha256": None}
    return {"path": str(path), "present": True, "bytes": path.stat().st_size, "sha256": sha256(path)}


def sensor_meta(path: Path) -> dict:
    if not path.exists():
        return {**file_meta(path), "rows": 0, "start": None, "end": None, "columns": []}
    lines = path.read_text(errors="replace").splitlines()
    clean_lines = [line.replace("\x00", "") for line in lines]
    header = next((line for line in clean_lines if line and not line.startswith("#")), "")
    columns = header.split("\t") if header else []
    raw_rows = [line for line in clean_lines if line and not line.startswith("#")][1:]
    rows = [line.split("\t") for line in raw_rows if re.match(r"^\d{4}-\d\d-\d\dT", line)]
    timestamps = [parse_ts(row[0]) for row in rows if row and row[0]]
    nul_lines = sum("\x00" in line for line in lines)
    return {**file_meta(path), "rows": len(rows), "start": iso(min(timestamps)) if timestamps else None,
            "end": iso(max(timestamps)) if timestamps else None, "columns": columns,
            "integrity": {"nul_padded_lines": nul_lines, "invalid_record_lines": len(raw_rows) - len(rows)}}


def chat_meta(path: Path, bucket_minutes: int = 60) -> dict:
    if not path.exists():
        return {**file_meta(path), "rows": 0, "start": None, "end": None, "series": {}}
    counts = Counter()
    timestamps = []
    for line in path.read_text(errors="replace").splitlines():
        match = re.match(r"^(\S+)\s+.*?\s::\s+(.*)$", line)
        if not match:
            continue
        timestamp, body = parse_ts(match.group(1)), match.group(2)
        timestamps.append(timestamp)
        bucket = timestamp - timedelta(minutes=timestamp.minute % bucket_minutes,
                                        seconds=timestamp.second, microseconds=timestamp.microsecond)
        counts[(bucket, "all_rows")] += 1
        for label in ("task", "taking", "done", "fyi", "alert", "idle", "dispatch"):
            if f"[{label}]" in body:
                counts[(bucket, label)] += 1
    series = {}
    for _, label in sorted(counts):
        series[label] = sum(value for (__, name), value in counts.items() if name == label)
    return {**file_meta(path), "rows": len(timestamps), "start": iso(min(timestamps)) if timestamps else None,
            "end": iso(max(timestamps)) if timestamps else None, "bucket_minutes": bucket_minutes,
            "series": series}


def split_bounds(start: datetime, end: datetime, horizon_hours: int = 6) -> dict:
    span = (end - start).total_seconds()
    train = start + timedelta(seconds=span * 0.70)
    validation = start + timedelta(seconds=span * 0.85)
    embargo = timedelta(hours=horizon_hours)
    return {
        "method": "chronological-70-15-15-with-embargo",
        "forecast_horizon_hours": horizon_hours,
        "train": {"start": iso(start), "end_exclusive": iso(train - embargo)},
        "validation": {"start": iso(train + embargo), "end_exclusive": iso(validation - embargo)},
        "test": {"start": iso(validation + embargo), "end_exclusive": iso(end + timedelta(seconds=1))},
        "excluded_boundary_windows": [
            {"start": iso(train - embargo), "end": iso(train + embargo)},
            {"start": iso(validation - embargo), "end": iso(validation + embargo)},
        ],
        "fit_rule": "No normalization, threshold, seasonal period, or prompt example may read validation/test rows.",
    }


def build_manifest(root: Path, chat_log: Path, sensor_tape: Path, out: Path) -> dict:
    sensor = sensor_meta(sensor_tape)
    chat = chat_meta(chat_log)
    starts = [parse_ts(value) for value in (sensor.get("start"), chat.get("start")) if value]
    ends = [parse_ts(value) for value in (sensor.get("end"), chat.get("end")) if value]
    start, end = min(starts), max(ends)
    numeric_sources = [
        root / "power.log", root / "wifi-quality.log", root / "wifi-rf.log",
        root / "package-power.log", root / "body-power-readings.log", root / "wifiscan.log",
    ]
    manifest = {
        "schema": "wake-eval-fixtures/v1",
        "created_at": iso(datetime.now(UTC)),
        "repository": "/home/mesh-home/lte-workstation",
        "privacy": {"raw_rows_included": False, "chat_text_included": False,
                     "derived_chat_series": "hourly counts by marker; no message content"},
        "sources": {"sensor_tape": sensor, "chat_log": chat,
                    "numeric_sensor_logs": [file_meta(path) for path in numeric_sources]},
        "series": {
            "sensor_state_one_hot": {"source": str(sensor_tape), "kind": "categorical-to-binary",
                                      "columns": sensor.get("columns", [])[1:], "missing": ["NOLOG", "STALE", "UNKNOWN"]},
            "chat_activity_hourly": {"source": str(chat_log), "kind": "count", "labels": ["all_rows", "task", "taking", "done", "fyi", "alert", "idle", "dispatch"]},
            "numeric_logs": {"kind": "regex-extracted", "candidates": ["power_watts", "wifi_signal_dbm", "wifi_link_percent", "wifi_retry_rate", "wifi_beacon_missed", "package_power_watts"]},
        },
        "splits": split_bounds(start, end),
        "wake_use_cases": [
            {"id": "sensor-change-forecast", "target": "next 1-6 hours of numeric sensor/state-event rates", "action": "advisory only; never actuate or suppress a watchdog"},
            {"id": "board-burst-forecast", "target": "hourly task/done/alert arrival rate", "action": "pre-warm evaluation or raise a review hint; no autonomous dispatch"},
            {"id": "local-mind-triage", "target": "structured classification of a fixed prompt fixture", "action": "offline benchmark only; output must validate against schema"},
        ],
        "baselines": [
            {"id": "persistence", "definition": "y_hat(t+h)=y(t)"},
            {"id": "seasonal-24", "definition": "repeat value from 24 hourly bins earlier when available"},
            {"id": "drift", "definition": "last value plus the most recent train-only first difference"},
        ],
        "resource_budget": {"timesfm": {"ram_gb": 8, "vram_gb": 4, "cold_seconds": 120, "warm_seconds": 30},
                            "local_minds": {"ram_gb": 12, "vram_gb": 8, "cold_seconds": 180, "warm_seconds": 60},
                            "run_limit_minutes": 30, "disk_gb": 12, "network": "model download only; evaluation inputs local"},
        "reproducibility": {"seed": 20260909, "python": "3.11+", "command": f"python3 scripts/wake_eval_fixtures.py --root {root} --out {out}",
                             "result_requirements": ["git revision", "source hashes", "split cutoffs", "model revision", "metrics with denominators", "resource samples", "failure/abstention counts"]},
        "model_cards": MODEL_CARDS,
        "license_constraints": [
            "TimesFM is evaluation/research-only under its non-commercial license; no production, commercial decision-making, distribution, or commercial derivative.",
            "Spark-X2.5-4B and MiniCPM5-2B are Apache-2.0, subject to attribution, NOTICE/license preservation, and ordinary data/privacy obligations.",
            "This fixture artifact contains no model weights and no raw chat text; it does not grant rights beyond the model licenses.",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        sensor = root / "sensor-tape.tsv"
        sensor.write_text("ts\thome_state\twifi\n2026-01-01T00:00:00Z\tQUIET\tUNKNOWN\n2026-01-02T00:00:00Z\tBUSY\tGOOD\n")
        chat = root / "chat.log"
        chat.write_text("2026-01-01T01:00:00Z  a@b  ::  [task] one\n2026-01-02T01:00:00Z  a@b  ::  [done] two\n")
        out = root / "manifest.json"
        result = build_manifest(root, chat, sensor, out)
        assert result["schema"] == "wake-eval-fixtures/v1"
        assert result["sources"]["chat_log"]["series"]["task"] == 1
        assert result["splits"]["method"].startswith("chronological")
        assert result["privacy"]["raw_rows_included"] is False
        assert json.loads(out.read_text())["model_cards"]["timesfm"]["license"]
    print("wake_eval_fixtures: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--chat-log", type=Path)
    parser.add_argument("--sensor-tape", type=Path)
    parser.add_argument("--out", type=Path, default=Path("docs/wake-model-eval-fixtures-20260909.json"))
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.test:
        test()
        return 0
    chat_log = args.chat_log or args.root / "chat.log"
    sensor_tape = args.sensor_tape or args.root / "sensor-tape.tsv"
    manifest = build_manifest(args.root, chat_log, sensor_tape, args.out)
    print(json.dumps({"out": str(args.out), "schema": manifest["schema"],
                      "sensor_rows": manifest["sources"]["sensor_tape"]["rows"],
                      "chat_rows": manifest["sources"]["chat_log"]["rows"],
                      "split": manifest["splits"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
