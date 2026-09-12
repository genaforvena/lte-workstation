#!/usr/bin/env python3
"""Build deterministic split-disjointness and leakage-control artifacts."""

import argparse
import hashlib
import json
import pathlib
import re
import sys
from datetime import datetime, timezone


AXES = ("repository", "blob_sha256", "time", "prompt_family")
NEAR_DUPLICATE_JACCARD_MIN = 0.75
TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def parse_jsonl(path):
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: malformed JSON ({exc.msg})") from exc
        if not isinstance(row, dict):
            raise ValueError(f"line {line_number}: JSON row must be an object")
        rows.append(row)
    return rows


def normalized_text(value):
    return " ".join(TOKEN_RE.findall(value.lower()))


def token_jaccard(left, right):
    def shingles(value):
        tokens = TOKEN_RE.findall(value.lower())
        if len(tokens) < 3:
            return {" ".join(tokens)} if tokens else set()
        return {" ".join(tokens[index:index + 3]) for index in range(len(tokens) - 2)}

    a, b = shingles(left), shingles(right)
    return len(a & b) / len(a | b) if a | b else 1.0


def time_overlap(train, heldout):
    train_times = [datetime.fromisoformat(row["time"].replace("Z", "+00:00")).astimezone(timezone.utc) for row in train]
    heldout_times = [datetime.fromisoformat(row["time"].replace("Z", "+00:00")).astimezone(timezone.utc) for row in heldout]
    train_max, heldout_min = max(train_times), min(heldout_times)
    if train_max < heldout_min:
        return []
    return [{"train_max": train_max.isoformat().replace("+00:00", "Z"), "heldout_min": heldout_min.isoformat().replace("+00:00", "Z")}]


def split_overlaps(rows):
    train = [row for row in rows if row["split"] == "train"]
    heldout = [row for row in rows if row["split"] == "heldout"]
    overlaps = {}
    for axis in AXES:
        if axis == "time":
            overlaps[axis] = time_overlap(train, heldout)
        else:
            left = {row[axis] for row in train}
            right = {row[axis] for row in heldout}
            overlaps[axis] = sorted(left & right)
    return overlaps


def validate_split_rows(rows):
    if not rows:
        raise ValueError("split fixture is empty")
    required = {"record_id", *AXES, "split", "text"}
    seen = set()
    for index, row in enumerate(rows, 1):
        missing = sorted(required - row.keys())
        if missing:
            raise ValueError(f"split row {index}: missing {', '.join(missing)}")
        if row["split"] not in {"train", "heldout"}:
            raise ValueError(f"split row {index}: unsupported split {row['split']!r}")
        if row["record_id"] in seen:
            raise ValueError(f"duplicate record_id: {row['record_id']}")
        seen.add(row["record_id"])
        if not re.fullmatch(r"[0-9a-f]{64}", row["blob_sha256"]):
            raise ValueError(f"split row {index}: blob_sha256 must be lowercase SHA-256")
        try:
            parsed = datetime.fromisoformat(row["time"].replace("Z", "+00:00"))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"split row {index}: invalid ISO-8601 time") from exc
        if parsed.tzinfo is None:
            raise ValueError(f"split row {index}: time must include a timezone")
        if not isinstance(row["text"], str) or not row["text"].strip():
            raise ValueError(f"split row {index}: text must be non-empty")
    if not any(row["split"] == "train" for row in rows) or not any(row["split"] == "heldout" for row in rows):
        raise ValueError("split fixture must include train and heldout rows")


def duplicate_id_check(rows):
    ids = [row.get("record_id") for row in rows]
    repeated = sorted({record_id for record_id in ids if ids.count(record_id) > 1})
    return {"detected": bool(repeated), "duplicate_record_ids": repeated}


def content_controls(path):
    rows = parse_jsonl(path)
    groups = {}
    for row in rows:
        groups.setdefault(row["pair_id"], []).append(row)
    output = {}
    for pair_id, members in sorted(groups.items()):
        if len(members) != 2 or {row["split"] for row in members} != {"train", "heldout"}:
            raise ValueError(f"content challenge {pair_id}: expected one train and one heldout row")
        a, b = sorted(members, key=lambda row: 0 if row["split"] == "train" else 1)
        exact = sha256(normalized_text(a["text"]).encode()) == sha256(normalized_text(b["text"]).encode())
        similarity = token_jaccard(a["text"], b["text"])
        expected = "exact-copy" if pair_id.startswith("exact-") else "near-duplicate"
        detected = exact if expected == "exact-copy" else (not exact and similarity >= NEAR_DUPLICATE_JACCARD_MIN)
        output[expected] = {
            "pair_id": pair_id,
            "detected": detected,
            "exact_normalized_text_match": exact,
            "token_jaccard": round(similarity, 6),
            "near_duplicate_threshold": NEAR_DUPLICATE_JACCARD_MIN,
            "train_record_id": a["record_id"],
            "heldout_record_id": b["record_id"],
        }
    if set(output) != {"exact-copy", "near-duplicate"}:
        raise ValueError("content challenge must include one exact-copy and one near-duplicate pair")
    return output


def mutation_controls(rows):
    results = {}
    for axis in AXES:
        mutated = [dict(row) for row in rows]
        train = next(row for row in mutated if row["split"] == "train")
        heldout = next(row for row in mutated if row["split"] == "heldout")
        if axis == "time":
            heldout[axis] = train[axis]
        else:
            heldout[axis] = train[axis]
        overlaps = split_overlaps(mutated)
        results[axis] = {"detected": bool(overlaps[axis]), "overlaps": overlaps[axis]}
    return results


def inspect_fixtures(input_dir):
    files = []
    for path in sorted(item for item in input_dir.rglob("*") if item.is_file()):
        relative = path.relative_to(input_dir).as_posix()
        data = path.read_bytes()
        row = {"path": relative, "sha256": sha256(data), "status": "included", "reason": "valid fixture input"}
        if "generated" in path.relative_to(input_dir).parts or path.name.endswith(".generated"):
            row.update(status="excluded-generated", reason="generated fixture path")
        elif path.suffix == ".jsonl":
            try:
                parsed = parse_jsonl(path)
            except (UnicodeDecodeError, ValueError):
                row.update(status="excluded-malformed-jsonl", reason="invalid JSONL input")
            else:
                duplicate_check = duplicate_id_check(parsed)
                if duplicate_check["detected"]:
                    row.update(status="excluded-duplicate-record-id", reason="duplicate record_id values: " + ", ".join(duplicate_check["duplicate_record_ids"]))
                elif path.name == "leakage-challenges.jsonl":
                    row.update(status="test-only-control", reason="adversarial exact/near-duplicate challenge; never a corpus row")
        files.append(row)
    if not files:
        raise ValueError("fixture input directory contains no files")
    return files


def input_digest(input_dir):
    digest = hashlib.sha256()
    for path in sorted(item for item in input_dir.rglob("*") if item.is_file()):
        relative = path.relative_to(input_dir).as_posix().encode()
        data = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big")); digest.update(relative)
        digest.update(len(data).to_bytes(8, "big")); digest.update(data)
    return digest.hexdigest()


def build_report(input_dir):
    files = inspect_fixtures(input_dir)
    split_rows = parse_jsonl(input_dir / "splits.jsonl")
    validate_split_rows(split_rows)
    overlaps = split_overlaps(split_rows)
    clean = {"disjoint": all(not values for values in overlaps.values()), "overlaps": overlaps,
             "train_count": sum(row["split"] == "train" for row in split_rows),
             "heldout_count": sum(row["split"] == "heldout" for row in split_rows),
             "time_rule": "max(train.time) < min(heldout.time); all timestamps require timezone"}
    mutations = mutation_controls(split_rows)
    duplicate_rows = parse_jsonl(input_dir / "duplicate-records.jsonl")
    mutations["duplicate_record_id"] = duplicate_id_check(duplicate_rows)
    content = content_controls(input_dir / "leakage-challenges.jsonl")
    report = {
        "schema": "tiny-fleet-split-audit/v1",
        "input_sha256": input_digest(input_dir),
        "fixture_files": files,
        "clean_split": clean,
        "mutation_controls": mutations,
        "content_leakage_controls": content,
        "method": {
            "repository_blob_prompt_family": "set intersection between train and heldout must be empty",
            "time": clean["time_rule"],
            "near_duplicate": f"Jaccard similarity of lowercase alphanumeric token 3-gram sets >= {NEAR_DUPLICATE_JACCARD_MIN}; exact normalized text is classified separately",
            "generated_and_malformed": "excluded before split construction and retained with reason and source SHA-256",
            "fixture_provenance": "test fixture only; no corpus redistribution claim",
            "network": "disabled",
        },
    }
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args(argv)
    if not args.input.is_dir():
        parser.error(f"fixture input directory not found: {args.input}")
    report = build_report(args.input)
    if not report["clean_split"]["disjoint"]:
        raise SystemExit("split-audit: baseline fixture leaks across one or more split axes")
    failed = [key for key, value in report["mutation_controls"].items() if not value["detected"]]
    failed.extend(key for key, value in report["content_leakage_controls"].items() if not value["detected"])
    if failed:
        raise SystemExit("split-audit: controls failed to detect: " + ", ".join(failed))
    args.output.mkdir(parents=True, exist_ok=True)
    report_bytes = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    (args.output / "fixture-report.json").write_bytes(report_bytes)
    with (args.output / "fixture-hashes.tsv").open("w", newline="") as handle:
        handle.write("path\tsha256\tstatus\n")
        for row in report["fixture_files"]:
            handle.write(f"{row['path']}\t{row['sha256']}\t{row['status']}\n")
        handle.write(f"fixture-report.json\t{sha256(report_bytes)}\treport\n")
    print(f"split audit report: {args.output / 'fixture-report.json'}")
    print(f"fixture hashes: {args.output / 'fixture-hashes.tsv'}")
    print(f"split axes: repository/blob/time/prompt-family; controls={len(report['mutation_controls']) + len(report['content_leakage_controls'])} detected")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"split-audit: {exc}", file=sys.stderr)
        sys.exit(2)
