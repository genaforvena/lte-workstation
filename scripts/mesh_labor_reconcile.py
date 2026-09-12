#!/usr/bin/env python3
"""Reconcile mesh-labor source TURN rows against the exact journal feed windows."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path
import re
import sys


def instant(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_source(path: Path):
    rows = []
    with path.open(errors="replace") as stream:
        for number, line in enumerate(stream, 1):
            fields = line.split()
            if len(fields) < 6 or fields[1] != "turn":
                continue
            try:
                stamp = instant(fields[0])
            except ValueError:
                print(f"source: invalid TURN timestamp at line {number}: {fields[0]}", file=sys.stderr)
                raise
            task = next((field[5:] for field in fields[6:] if field.startswith("task:")), "-")
            rows.append((stamp, fields[4], fields[2], task))
    return rows


def journal_files(directory: Path):
    return sorted(directory.glob("[0-9][0-9][0-9][0-9].journal"))


def load_journal(directory: Path):
    # hledger has already checked syntax and parity. Parse the source dimensions needed for independent
    # completeness validation: (feed interval, provider, owner-window, explicit task ID).
    groups = Counter()
    intervals = set()
    journal_total = 0
    task_totals = Counter()
    transaction = re.compile(r"(?m)(?=^\d{4}-\d\d-\d\d\s+\*)")
    window_re = re.compile(r"(?:^|\s)window:([^.]*)\.\.([^\s;]+)")
    task_re = re.compile(r"^\d{4}-\d\d-\d\d\s+\*\s+labour feed task:([^\s;]+)", re.M)
    posting_re = re.compile(
        r"^\s+expenses:labour:([^:\s]+):([^\s]+)\s+([0-9,]+)\s+TURN\s*$", re.M
    )
    for path in journal_files(directory):
        content = path.read_text(errors="replace")
        for block in transaction.split(content):
            if not block.strip():
                continue
            window = window_re.search(block)
            postings = list(posting_re.finditer(block))
            if not window:
                if postings:
                    raise ValueError(f"unwindowed labour posting in {path}")
                continue
            start, end = instant(window.group(1)), instant(window.group(2))
            if start >= end:
                raise ValueError(f"invalid feed window in {path}: {window.group(0)}")
            intervals.add((start, end))
            task_match = task_re.search(block)
            task = task_match.group(1) if task_match else "-"
            for posting in postings:
                provider, owner_window, amount = posting.groups()
                count = int(amount.replace(",", ""))
                groups[(start, end, provider, owner_window.strip(), task)] += count
                journal_total += count
                if task != "-":
                    task_totals[task] += count
    return intervals, groups, journal_total, task_totals


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: mesh_labor_reconcile.py <spend.log> <labour-dir>", file=sys.stderr)
        return 2
    source_path, directory = Path(sys.argv[1]), Path(sys.argv[2])
    if not source_path.is_file():
        print(f"reconciliation: UNKNOWN — source missing: {source_path}")
        return 2
    rows = load_source(source_path)
    intervals, journal_groups, journal_total, journal_tasks = load_journal(directory)
    watermark_path = directory / ".watermark"
    watermark = instant(watermark_path.read_text().strip()) if watermark_path.exists() else None
    if intervals:
        first_start = min(start for start, _ in intervals)
        last_end = max(end for _, end in intervals)
    else:
        first_start = last_end = None

    expected = Counter()
    hits = Counter()
    explicit_source = Counter()
    for index, (stamp, provider, owner_window, task) in enumerate(rows):
        if task != "-":
            explicit_source[task] += 1
        for start, end in intervals:
            if start < stamp <= end:
                expected[(start, end, provider, owner_window, task)] += 1
                hits[index] += 1

    mismatches = []
    all_groups = set(expected) | set(journal_groups)
    for key in sorted(all_groups, key=lambda item: tuple(str(x) for x in item)):
        source_count, booked_count = expected[key], journal_groups[key]
        if source_count != booked_count:
            start, end, provider, owner_window, task = key
            mismatches.append((start, end, provider, owner_window, task, source_count, booked_count))

    pre_inception = pending = uncovered_source = duplicate_coverage = 0
    for index, (stamp, _, _, _) in enumerate(rows):
        if hits[index] > 1:
            duplicate_coverage += 1
        elif hits[index] == 1:
            continue
        elif first_start is not None and stamp <= first_start:
            pre_inception += 1
        elif watermark is not None and stamp > watermark:
            pending += 1
        elif watermark is None:
            uncovered_source += 1
        else:
            # Includes a delayed completion appended after its timestamp has passed the watermark.
            uncovered_source += 1

    duplicate_feed_turns = sum(max(0, journal_groups[key] - expected[key]) for key in all_groups)
    missing_feed_turns = sum(max(0, expected[key] - journal_groups[key]) for key in all_groups)
    unexplained_groups = len(mismatches) + uncovered_source

    task_source_total = sum(explicit_source.values())
    untagged = len(rows) - task_source_total
    coverage = 100.0 * task_source_total / len(rows) if rows else 0.0
    print(
        "source_cutoff=%s watermark=%s"
        % (max((row[0] for row in rows), default="n/a"), watermark.isoformat() if watermark else "none")
    )
    print(
        "source TURN=%d journal TURN=%d difference=%+d feed_windows=%d"
        % (len(rows), journal_total, len(rows) - journal_total, len(intervals))
    )
    print(
        "partition: pre_inception=%d not_yet_fed=%d documented_corrections=0 duplicate_feed_turns=%d missing_feed_turns=%d interval_overlap_rows=%d unexplained_groups=%d"
        % (pre_inception, pending, duplicate_feed_turns, missing_feed_turns, duplicate_coverage, unexplained_groups)
    )
    print(
        "task_attribution: explicit=%d/%d (%.1f%%) untagged_unknown=%d task_ids=%d journal_explicit=%d"
        % (task_source_total, len(rows), coverage, untagged, len(explicit_source), sum(journal_tasks.values()))
    )
    print("window_task_groups: %d mismatched=%d" % (len(all_groups), len(mismatches)))
    for start, end, provider, owner_window, task, source_count, booked_count in mismatches[:20]:
        print(
            "  mismatch window:%s..%s %s/%s task:%s source=%d journal=%d"
            % (start.isoformat(), end.isoformat(), provider, owner_window, task, source_count, booked_count)
        )
    if len(mismatches) > 20:
        print("  ... %d additional mismatched groups" % (len(mismatches) - 20))

    if duplicate_coverage or unexplained_groups or mismatches:
        print("source reconciliation: FAIL (missing, duplicate, delayed, or over-booked source rows)")
        return 1
    print("source reconciliation: OK (all booked windows and explicit task tags match source)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        print(f"source reconciliation: UNKNOWN — {error}", file=sys.stderr)
        raise SystemExit(2)
