#!/usr/bin/env python3
"""Role-specific projection of full mesh-dash source frames into live-pane budgets."""
from __future__ import annotations

import collections
import os
import re
import sys


role = sys.argv[1] if len(sys.argv) > 1 else ""
mesh = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/.mesh")
lines = sys.stdin.read().splitlines()
if not lines:
    raise SystemExit(0)

prefix = lines[:2]
body = lines[2:]
out: list[str] = list(prefix)


def push(*items: str) -> None:
    for item in items:
        if item and item not in out:
            out.append(item)


try:
    pane_rows = int(os.environ.get("MESH_DASH_PANE_ROWS", "0"))
    pane_cols = int(os.environ.get("MESH_DASH_PANE_COLS", "0"))
except ValueError:
    pane_rows = pane_cols = 0

if role == "check" and 0 < pane_rows <= 11 and pane_cols >= 80:
    def first_line(source: list[str], predicate) -> str:
        return next((line for line in source if predicate(line)), "")

    def section(marker: str) -> list[str]:
        start = next((i for i, line in enumerate(body) if line.startswith(marker)), -1)
        if start < 0:
            return []
        end = next((i for i in range(start + 1, len(body)) if body[i].startswith("-- ")), len(body))
        return body[start:end]

    goal = re.search(r"goal-source=(\S+)", lines[0])
    stamp = re.search(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", lines[1] if len(lines) > 1 else "")
    out[:] = [f"goal-source={goal.group(1) if goal else 'UNKNOWN'} · check={stamp.group(0) if stamp else 'UNKNOWN'}"]

    self_line = first_line(body, lambda line: line.lstrip().startswith("self:"))
    liveness_line = first_line(body, lambda line: line.startswith("egress "))
    self_state = re.search(r"self:\s*([A-Z]+)", self_line, re.I)
    egress = re.search(r"egress\s+(\S+)", liveness_line, re.I)
    supervised = re.search(r"supervised\s+(\d+UP/\d+DOWN)", liveness_line, re.I)
    organs_live = re.search(r"organs\s+(\d+LIVE/\d+DARK)", liveness_line, re.I)
    push(
        f"self={self_state.group(1).upper() if self_state else 'UNKNOWN'}"
        f" · egress={egress.group(1) if egress else 'UNKNOWN'}"
        f" · supervised={supervised.group(1) if supervised else 'UNKNOWN'}"
        f" · organs={organs_live.group(1) if organs_live else 'UNKNOWN'}"
    )

    fleet = first_line(body, lambda line: line.startswith("-- FLEET"))
    fleet_section = section("-- FLEET")
    fleet_state = re.search(r"\b(LIVE|UNKNOWN|STALE|FAIL|DEGRADED|PASS|OK)\b", fleet, re.I)
    nodes = first_line(fleet_section[1:], lambda line: re.match(r"\s*\d+\s+nodes:", line) is not None)
    node_summary = re.search(r"(\d+\s+nodes:\s*[^|]+)", nodes)
    path_state = re.search(r"\bPATH:\s*([A-Z]+)", nodes, re.I)
    fleet_parts = [f"-- FLEET {fleet_state.group(1).upper() if fleet_state else 'UNKNOWN'}"]
    if node_summary:
        fleet_parts.append(node_summary.group(1).strip())
    if path_state:
        fleet_parts.append(f"PATH: {path_state.group(1).upper()}")
    push(" · ".join(fleet_parts))

    doctor_section = section("-- DOCTOR")
    doctor_header = doctor_section[0] if doctor_section else ""
    doctor_state = re.search(r"\b(PASS|FAIL|UNKNOWN|STALE|DEGRADED|OK)\b", doctor_header, re.I)
    doctor_age = re.search(r"cached\s+([^)]+)", doctor_header, re.I)
    doctor_deferred = any("full doctor remains deferred" in line.lower() for line in doctor_section)
    doctor_parts = [f"-- DOCTOR {doctor_state.group(1).upper() if doctor_state else 'UNKNOWN'}"]
    if doctor_age:
        doctor_parts.append(f"cached={doctor_age.group(1).strip()}")
    if doctor_deferred:
        doctor_parts.append("full doctor deferred")
    push(" · ".join(doctor_parts))

    cpu_line = first_line(body, lambda line: "load-audit(" in line)
    gpu_line = first_line(body, lambda line: line.strip().startswith("GPU ") and not line.strip().startswith("GPU decoder"))
    cpu_state = re.search(r"\bCPU=([A-Z0-9_-]+)", cpu_line, re.I)
    gpu_state = re.search(r"\bGPU\s+([A-Z0-9_-]+)", gpu_line, re.I)
    gpu_age = re.search(r"\(([^)]+)\)", gpu_line)
    gpu_metrics = [match.group(0) for pattern in (r"\bvram=\S+", r"\butil=\S+", r"\btemp=\S+") if (match := re.search(pattern, gpu_line, re.I))]
    gpu_parts = [f"-- CPU/GPU CPU={cpu_state.group(1).upper() if cpu_state else 'UNKNOWN'}"]
    gpu_parts.append(f"GPU={gpu_state.group(1).upper() if gpu_state else 'UNKNOWN'}{f'/{gpu_age.group(1)}' if gpu_age else ''}")
    gpu_parts.extend(gpu_metrics)
    push(" ".join(gpu_parts))

    organ_section = section("-- organs")
    organ_header = organ_section[0] if organ_section else ""
    organ_counts = first_line(organ_section[1:], lambda line: re.match(r"\s*\d+\s+states:", line) is not None)
    counts = re.search(r"(\d+)\s+states:\s*(\d+)\s+alarm.*?·\s*(\d+)\s+stale.*?·\s*(\d+)\s+quiet", organ_counts, re.I)
    organ_state = "LIVE" if "all LIVE" in organ_header else "UNKNOWN"
    if counts:
        push(f"-- organs {organs_live.group(1) if organs_live else organ_state} · {counts.group(1)} states · {counts.group(2)} alarm · {counts.group(3)} stale · {counts.group(4)} quiet")
    else:
        push(f"-- organs {organs_live.group(1) if organs_live else organ_state}")

    autopoiesis = first_line(body, lambda line: line.startswith("-- autopoiesis"))
    reflex = re.search(r"reflexes=([A-Z]+)", autopoiesis, re.I)
    vitality = re.search(r"vitality=([A-Z]+)", autopoiesis, re.I)
    feed = re.search(r"\bfeed\s+(\S+)", autopoiesis, re.I)
    evolve = re.search(r"\bevolve\s+(\S+)", autopoiesis, re.I)
    streams = re.search(r"\bstreams\s+(\S+)", autopoiesis, re.I)
    if autopoiesis:
        push(
            f"-- autopoiesis reflexes={reflex.group(1).upper() if reflex else 'UNKNOWN'}"
            f" vitality={vitality.group(1).upper() if vitality else 'UNKNOWN'}"
            f" feed={feed.group(1) if feed else 'UNKNOWN'}"
            f" evolve={evolve.group(1) if evolve else 'UNKNOWN'}"
            f" streams={streams.group(1) if streams else 'UNKNOWN'}"
        )
    else:
        push("-- autopoiesis UNKNOWN")

    push("  omitted: node/VPN/doctor/organ details; full=mesh-dash --once check")
    print("\n".join(out))
    raise SystemExit(0)




def span(start: str, end: str | None = None, source: list[str] | None = None) -> tuple[int, int]:
    data = body if source is None else source
    first = next((i for i, line in enumerate(data) if start in line), -1)
    if first < 0:
        return -1, -1
    if end:
        last = next((i for i in range(first + 1, len(data)) if end in data[i]), len(data))
    else:
        last = next((i for i in range(first + 1, len(data)) if data[i].startswith("-- ") or data[i].startswith("=== ")), len(data))
    return first, last




def age(path: str) -> str:
    try:
        seconds = max(0, int(__import__("time").time() - os.path.getmtime(path)))
    except OSError:
        return "UNKNOWN (artifact absent)"
    if seconds < 3600:
        return f"{seconds // 60}m"
    if seconds < 86400:
        return f"{seconds // 3600}h"
    return f"{seconds // 86400}d"


def omitted(text: str) -> str:
    return f"  omitted from live pane: {text}; full frame=mesh-dash --once {role}"

def compact_cross(line: str) -> str:
    match = re.match(r"\s*cross-val \(([^)]+)\):\s*(.*)", line)
    if not match:
        return line
    label, payload = match.groups()
    states = re.search(r"\b(PASS|INCOMPLETE|UNREACHABLE|UNKNOWN|STALE|DEGRADED|OK)\b", payload, re.I)
    state = states.group(1).upper() if states else "UNKNOWN"
    age_ttl = re.search(r"last written (\d+)s ago \(TTL (\d+)s\)", payload, re.I)
    if age_ttl:
        reason = f"evidence age={age_ttl.group(1)}s > TTL={age_ttl.group(2)}s"
    elif state == "INCOMPLETE":
        reason = "peer OFFLINE; no live second vantage; map invalid" if "OFFLINE" in payload else "second vantage incomplete"
    elif state in ("PASS", "OK"):
        stamp = re.search(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", payload)
        reason = f"observed_at={stamp.group(0)}" if stamp else "producer result present"
    else:
        reason = re.sub(r"\s+", " ", payload).strip().split(" — ", 1)[0][:96]
    return f"  cross-val ({label}): {state} · {reason}"


def compact_reflex(line: str) -> str:
    if not line.lstrip().startswith("reflex-health:"):
        return line
    status = re.search(r"reflex-health:\s*([A-Z]+)", line, re.I)
    fresh = re.search(r"(\d+)\s+per-run reflex\(es\) fresh|per-run fresh=(\d+)", line, re.I)
    cohort = re.search(r"cohort[= ]+(\d+/\d+ held while \d+ moved)", line, re.I)
    frozen = re.findall(r"([a-z0-9-]+):(\d+)s", line, re.I)
    if not fresh and not frozen:
        return line
    pieces = [f"reflex-health: {status.group(1).upper() if status else 'UNKNOWN'}"]
    pieces.append(f"per-run fresh={(fresh.group(1) or fresh.group(2)) if fresh else 'UNKNOWN'}")
    pieces.append(f"cohort={cohort.group(1) if cohort else 'UNKNOWN'}")
    if frozen:
        oldest = max(frozen, key=lambda item: int(item[1]))
        pieces.append(f"overwrite-only frozen={len(frozen)}; oldest={oldest[0]}:{oldest[1]}s")
    else:
        pieces.append("overwrite-only frozen=none reported")
    return "  " + " · ".join(pieces)


def compact_mobile_link(line: str) -> str:
    if not line.startswith("  MOBILE-LINK:"):
        return line
    parts = line.split(" · ")
    out = []
    for part in parts:
        label = re.match(r"\s*(?:MOBILE-LINK:\s*)?([A-Za-z-]+)\b", part)
        if not label:
            out.append(part.strip())
            continue
        name = label.group(1)
        state_match = re.search(rf"\b{re.escape(name)}=([A-Z]+)\b", part, re.I)
        if not state_match:
            state_match = re.search(r"\bstatus=([A-Z]+)\b", part, re.I)
        if not state_match:
            state_match = re.search(rf"\b{re.escape(name)}\s+([A-Z]+)\b", part, re.I)
        state = state_match.group(1).upper() if state_match else "UNKNOWN"
        fields = dict(re.findall(r"([A-Za-z][A-Za-z0-9_-]*)=([^|·\s]+)", part))
        freshness = re.search(r"freshness=([A-Z]+)|\((fresh|recent|aging|stale|unknown)\)", part, re.I)
        suffix = next((group for group in freshness.groups() if group), "UNKNOWN").upper() if freshness else "UNKNOWN"
        keys = {
            "connectivity": ("active_default", "validated", "cell", "idle_s"),
            "netpolicy": ("metered_policy_rows", "warning_bytes", "limit_bytes"),
            "gfxinfo": ("age_s",),
            "traffic": ("age_s",),
        }.get(name, ())
        selected = [f"{key}={fields[key]}" for key in keys if key in fields]
        out.append(f"{name}={state}" + (" " + " ".join(selected) if selected else "") + f" {suffix}")
    return "  MOBILE-LINK: " + " · ".join(out)


def compact_note3(line: str) -> str:
    if not line.startswith("  NOTE3:"):
        return line
    parts = line.split(" · ")
    out = []
    for part in parts:
        if "netstats status=" in part:
            status = re.search(r"netstats status=([A-Z]+)", part)
            age_s = re.search(r"age_s=(\d+)", part)
            iface = re.search(r"iface=([^\s|]+)", part)
            stale = "STALE" if re.search(r"\(stale\)", part, re.I) else "UNKNOWN"
            out.append("netstats " + (status.group(1) if status else "UNKNOWN") +
                       f" age_s={age_s.group(1) if age_s else 'UNKNOWN'}" +
                       f" iface={iface.group(1) if iface else 'UNKNOWN'} freshness={stale}")
        else:
            compacted = part.strip()
            compacted = re.sub(r"\s+hal_tick_ns=\d+", "", compacted)
            compacted = compacted.replace("craft-light", "light").replace("climate in_hpa=", "climate hPa=")
            compacted = compacted.replace("d_hpa=", "d=").replace("out_c=", "out=")
            compacted = re.sub(r"\bgravity gx=", "gravity x=", compacted)
            compacted = re.sub(r"\bgy=", "y=", compacted)
            compacted = re.sub(r"\bgz=", "z=", compacted)
            compacted = compacted.replace("(malformed battery state)", "(malformed)")
            compacted = compacted.replace("(fresh)", "FRESH").replace("(on-demand)", "on-demand")
            compacted = compacted.replace("cam last frame idle", "cam=IDLE")
            out.append(compacted)
    return "  " + " · ".join(out)


if role == "minds":
    a, b = span("-- live state per mind")
    if a >= 0:
        push(body[a])
        groups: dict[str, list[str]] = collections.defaultdict(list)
        for line in body[a + 1:b]:
            match = re.match(r"\s*([a-zA-Z0-9-]+):\s+([A-Z][A-Z-]*)", line)
            if match:
                groups[match.group(2)].append(match.group(1))
        for status in sorted(groups):
            push(f"  {status}: {', '.join(groups[status])}")
        cache = os.path.join(mesh, ".mind-state-watch.cache")
        push(f"  source={cache} age={age(cache)}")
    else:
        push("-- live state per mind UNKNOWN (source section absent)")
    a, b = span("-- allocation:")
    if a >= 0:
        alloc_rows = body[a:b]
        push(body[a])
        push(*(line + " · freshness UNKNOWN (dispatch source TTL absent)" if "gate: dispatch" in line else line for line in alloc_rows[1:] if re.search(r"open|unclaimed|idle hands|UNKNOWN|gate: dispatch", line, re.I)))
        if not any("gate: dispatch" in line for line in alloc_rows):
            push("  gate: dispatch UNKNOWN (source row absent)")
    else:
        push("-- allocation UNKNOWN (dispatch gate and queue state absent)")
    for marker, rules in (
        ("-- division of labour:", re.compile(r"intended J=|realized J=|no owner-assigned|UNKNOWN|UNENGAGED|elastic:", re.I)),
        ("-- spend:", re.compile(r"^\s*(?:PAID|FREE|->)|UNKNOWN|total", re.I)),
        ("-- budget:", re.compile(r"paid|cap|ceiling|unset|UNKNOWN", re.I)),
    ):
        a, b = span(marker)
        if a >= 0:
            push(body[a])
            selected = [line for line in body[a + 1:b] if rules.search(line)]
            push(*selected)
            if not selected:
                push(f"  {marker[3:-1]} UNKNOWN (source rows absent)")
            if marker == "-- division of labour:" and not any("realized J=" in line for line in selected):
                push("  realized allocation: UNKNOWN (no realized J row)")
        else:
            push(f"{marker} UNKNOWN (source section absent)")
    push(omitted("prompt/spinner/model/workdir tails, raw task titles, quota detail, operator-hands, context-pressure and mesh-wide capability census (source: mind-state cache, mesh-dispatch, mesh-quota, mesh-operator-hands, mesh-ctx-pressure, mesh-minds)"))

elif role == "genome":
    commit_count = 0
    in_commits = False
    for line in body:
        if line.startswith("-- recent commits"):
            in_commits = True
            continue
        if in_commits:
            if line.startswith("-- "):
                in_commits = False
            elif line.strip():
                commit_count += 1
                continue
        push(line)
    if commit_count:
        push(f"  recent commit history: {commit_count} rows omitted; source=git log --oneline -5")

elif role == "senses":
    # The sense map is a capability inventory, not a stream of independent measurements. Keep every
    # node/capability and cross-check class, but group repeated roster rows so cached sensor readings fit.
    map_a = next((i for i, line in enumerate(body) if line.startswith("# harvest:")), -1)
    map_b = next((i + 1 for i, line in enumerate(body[map_a + 1:], map_a + 1) if line.lstrip().startswith("(cached ")), -1) if map_a >= 0 else -1
    if map_a >= 0 and map_b > map_a:
        map_lines = body[map_a:map_b]
        devices: dict[str, list[str]] = collections.defaultdict(list)
        active: list[str] = []
        passive: list[str] = []
        mode = ""
        for line in map_lines:
            if line.startswith("-- DEVICES"):
                mode = "devices"
                continue
            if line.startswith("-- ACTIVE"):
                mode = "active"
                continue
            if line.startswith("-- PASSIVE"):
                mode = "passive"
                continue
            if line.startswith("-- "):
                mode = ""
                continue
            if mode == "devices" and line.strip():
                match = re.match(r"\s*(.+?)\s+(online|offline)\s+(.*)$", line, re.I)
                if match:
                    name, state, detail = match.group(1), match.group(2).lower(), match.group(3)
                    devices[state].append(f"{name} {detail}".strip())
                else:
                    devices["UNKNOWN"].append(line.strip())
            elif mode == "active" and line.strip():
                active.append(line.strip().split(" — ", 1)[0])
            elif mode == "passive" and line.strip() and not line.lstrip().startswith("("):
                passive.append(line.strip().split(" — ", 1)[0])
        push(map_lines[0])
        push("-- DEVICES (all nodes; capabilities retained) --")
        if devices:
            for state in sorted(devices):
                push(f"  {state}: " + " | ".join(devices[state]))
        else:
            push("  device capability census: UNKNOWN (no cached devices)")
        if active:
            push("  active cross-checks: " + " | ".join(active))
        else:
            push("  active cross-checks: UNKNOWN (no cached declaration)")
        if passive:
            push("  passive cross-checks: " + " | ".join(passive))
        else:
            push("  passive cross-checks: UNKNOWN (no cached declaration)")
        push(map_lines[-1])
    elif map_a >= 0:
        push("  mesh-sense-map: UNKNOWN (cached output incomplete)")
    else:
        push("  mesh-sense-map: UNKNOWN (source section absent)")

    for line in body:
        if line.startswith("  cross-val ("):
            push(compact_cross(line))
        elif line.startswith("  NOTE3:"):
            push(compact_note3(line))
        elif line.startswith("  MOBILE-LINK:"):
            push(compact_mobile_link(line))
        elif line.startswith("-- LIVE READINGS"):
            gate = next((item.strip() for item in body if item.startswith("  producer gate:")), "")
            push(f"{line} · {gate}" if gate else line)
        elif line.startswith("  producer gate:"):
            continue
        elif line.startswith("  NIC tx FIFO:") or line.startswith("  GPU decoder:"):
            push(line)
    if not any(line.startswith("  cross-val (") for line in body):
        push("  cross-val UNKNOWN (source section absent)")
    if not any(line.startswith("-- LIVE READINGS") for line in body):
        push("-- LIVE READINGS UNKNOWN (source section absent)")
    # Preserve every sensor value while grouping adjacent non-critical inventory fields.
    a, b = span("=== mesh sensorium")
    synthetic_header = a < 0
    if synthetic_header:
        a = next((i for i, line in enumerate(body) if line.startswith(("BODY ", "ROOM ", "PRESENCE ", "HOUSEHOLD ", "SITUATION ", "COORDINATION ", "NODE ", "CPU ", "LIVE-ONLY "))), -1)
    if a >= 0:
        b = next((i for i in range(a + 1, len(body)) if body[i].startswith("  GPU decoder:")), len(body))
        sensor_rows = body[a:b]
        if synthetic_header:
            push("=== mesh sensorium (source=mesh-sensorium --cached) ===")
        else:
            push(sensor_rows[0])
        grouped: dict[str, list[str]] = collections.defaultdict(list)
        order = ["BODY", "ROOM", "PRESENCE", "SITUATION", "NODE", "LIVE-ONLY"]
        values = sensor_rows if synthetic_header else sensor_rows[1:]
        for line in values:
            label = line.split(None, 1)[0] if line.strip() else ""
            if label == "ROOM":
                compacted = line.strip()
                compacted = re.sub(r"room=PRESENT\(blind:([^)]+)\) \(([^)]+)\)", r"room=PRESENT/BLIND(\1)/\2", compacted)
                compacted = re.sub(r"ambient=([^| ]+)\|dwell_s=(\d+)\|changes_24h=(\d+)\|fixture=([^ ]+) \(([^)]+)\)", r"ambient=\1 dwell=\2s changes=\3 fixture=\4/\5", compacted)
                grouped["ROOM"].append(compacted)
            elif label == "HOUSEHOLD":
                grouped["PRESENCE"].append(line.strip())
            elif label == "COORDINATION":
                grouped["SITUATION"].append(line.strip())
            elif label == "CPU":
                grouped["NODE"].append(line.strip())
            elif label in order:
                grouped[label].append(line.strip())
        for label in order:
            if grouped[label]:
                push("  " + " · ".join(grouped[label]))
    else:
        push("=== mesh sensorium UNKNOWN (source section absent)")
    a, b = span("-- attended-ness", "-- sense-reflex liveness")
    if a >= 0:
        values = [line.strip() for line in body[a + 1:b] if line.strip()]
        push("-- attendance (stale sessions excluded): " + " · ".join(values) if values else "-- attendance UNKNOWN (source rows absent)")
    else:
        push("-- attendance UNKNOWN (source section absent)")
    a, b = span("-- sense-reflex liveness", "-- recent sense work")
    if a >= 0:
        reflex = [compact_reflex(line).strip() for line in body[a + 1:b] if line.strip()]
        push("-- sense-reflex: " + " · ".join(reflex) if reflex else "-- sense-reflex UNKNOWN (source rows absent)")
    else:
        push("-- sense-reflex UNKNOWN (source section absent)")
    a, b = span("-- recent sense work", "-- sense-evolve")
    if a >= 0:
        recent = [line.strip() for line in body[a + 1:b] if line.strip()]
        push("-- recent sense work: " + recent[-1] if recent else "-- recent sense work UNKNOWN (source rows absent)")
    else:
        push("-- recent sense work UNKNOWN (source section absent)")
    a, b = span("-- sense-evolve", "-- frontier:")
    if a >= 0:
        values = [line.strip() for line in body[a + 1:b] if line.strip()]
        push("-- sense-evolve: " + " · ".join(values) if values else "-- sense-evolve UNKNOWN (source row absent)")
    else:
        push("-- sense-evolve UNKNOWN (source section absent)")
    a, b = span("-- frontier:")
    if a >= 0:
        push(*body[a:b])
    else:
        push("-- frontier UNKNOWN (source section absent)")
    push(omitted("raw device prose, mobile fields, cross-val rationale, reflex frozen ages and older board rows; source=sense-map/sensorium/reflex artifacts/chat.log"))

elif role == "check":
    # Preserve health verdicts while bounding member lists and secondary process detail.
    keep = ("-- FLEET", "-- DOCTOR", "-- VPN", "-- CPU/GPU load", "-- organs", "-- supervised loops DOWN", "-- autopoiesis")
    current = ""
    vpn_omitted = 0
    organ_detail_count = 0
    organ_omitted = 0
    for line in body:
        if line.startswith("-- "):
            if current == "-- VPN" and vpn_omitted:
                push(f"  {vpn_omitted} VPN detail rows omitted; full client roster and cache age are in the vpn pane")
                vpn_omitted = 0
            if current == "-- organs" and organ_omitted:
                push(f"  {organ_omitted} alarm/stale details omitted; {'one named row retained' if organ_detail_count else 'no named detail row present in source'}")
            current = next((marker for marker in keep if line.startswith(marker)), "")
            if current:
                push(line)
            continue
        if current == "-- VPN":
            if re.search(r"friends@phaedra|clients:|egress now:|egress 24h:|UNKNOWN|UNAVAILABLE|STALE", line, re.I):
                push(line)
            else:
                vpn_omitted += 1
        elif current == "-- organs":
            if line.lstrip().startswith("✗"):
                organ_detail_count += 1
                if organ_detail_count == 1:
                    push(line)
                else:
                    organ_omitted += 1
            else:
                match = re.search(r"\+(\d+) more alarm/stale not shown", line)
                if match:
                    organ_omitted += int(match.group(1))
                else:
                    push(line)
        elif current == "-- CPU/GPU load" and line.lstrip().startswith("top:"):
            continue
        elif current:
            push(line)
        elif re.search(r"^\s*(?:self:|egress |vitals:|[0-9]+ states:|supervised [0-9]+UP|accounting:|mishe gates:|health mind|pane coverage)", line, re.I):
            push(line)
    if current == "-- VPN" and vpn_omitted:
        push(f"  {vpn_omitted} VPN detail rows omitted; full client roster and cache age are in the vpn pane")
    if current == "-- organs" and organ_omitted:
        push(f"  {organ_omitted} alarm/stale details omitted; {'one named row retained' if organ_detail_count else 'no named detail row present in source'}")
    for marker in keep:
        present = any(line.startswith(marker) for line in body)
        if marker == "-- supervised loops DOWN":
            present = present or any(re.search(r"\bsupervised \d+UP/\d+DOWN\b", line, re.I) for line in body)
        if not present:
            push(f"{marker} UNKNOWN (source section absent)")
    push(omitted("state-wall members, extra VPN details, extra organ alarms and top-process detail; source=mesh-dash --once check; retained: egress, FLEET, DOCTOR, vitals, CPU/GPU, organ counts, mishe gates and UNKNOWN"))

elif role == "vpn":
    a, b = span("-- MY EGRESS", "-- CONNECTED MACHINES")
    if a >= 0:
        push(*body[a:b])
    else:
        push("-- MY EGRESS UNKNOWN (source section absent)")
    a, b = span("-- CONNECTED MACHINES", "-- SERVER health")
    peers: list[str] = []
    offline: list[str] = []
    summary_seen = False
    source_unknown = False
    if a >= 0:
        push(body[a])
        push("  source=tailscale status --json; freshness=live at frame render")
        for line in body[a + 1:b]:
            if "ONLINE (" in line and "OFFLINE (" in line:
                summary_seen = True
                push(line)
            elif "unreadable" in line.lower() or "unavailable" in line.lower():
                source_unknown = True
                push(line)
            elif line.strip() and not line.startswith("-- "):
                parts = line.split()
                if "lastseen" in line:
                    offline.append(f"{parts[0]} lastseen {parts[parts.index('lastseen') + 1] if len(parts) > parts.index('lastseen') + 1 else 'UNKNOWN'}")
                else:
                    name = parts[0] if parts else "UNKNOWN"
                    conn = next((p for p in parts if p == "direct" or p == "relay"), "")
                    path = " ".join(parts[parts.index(conn):parts.index(conn) + 2]) if conn else "path UNKNOWN"
                    peers.append(f"{name}({path})")
        if not summary_seen and not source_unknown:
            push("  Tailscale peer census: UNKNOWN (roster summary absent)")
        if peers:
            push("  online peers: " + ", ".join(peers))
        if offline:
            push("  offline peers: " + ", ".join(offline))
    else:
        push("-- CONNECTED MACHINES UNKNOWN (source section absent; Tailscale freshness UNKNOWN)")
    for start, end in (
        ("-- SERVER health", "-- TUNNEL end-to-end"),
        ("-- TUNNEL end-to-end", "-- VPN USERS"),
    ):
        a, b = span(start, end)
        if a >= 0:
            section = body[a:b]
            if start == "-- SERVER health":
                rows = [line.strip() for line in section[1:] if line.strip()]
                state = re.search(r"\b(PASS|OK|HEALTHY|DEGRADED|DOWN|UNKNOWN)\b", " ".join(rows), re.I)
                logged = re.search(r"\(logged ([^)]+)\)", " ".join(rows), re.I)
                if rows:
                    push(f"-- SERVER health state={state.group(1).upper() if state else 'UNKNOWN'} · logged {logged.group(1) if logged else 'UNKNOWN'}")
                    push(*section[1:])
                else:
                    push("-- SERVER health UNKNOWN (source status row absent)")
            else:
                push(*section)
        else:
            push(f"{start} UNKNOWN (source section absent)")
    a, b = span("-- VPN USERS", "-- SS escalation gate")
    if a >= 0:
        users = body[a:b]
        push(users[0])
        kept = [item for item in users[1:] if re.search(r"ss-connections|enrichment cache|0 clients|client cache|WireGuard:|WG by name|^\s+ON:|^\s+off:|BREACH|UNKNOWN|STALE", item, re.I)]
        push(*kept)
        if not kept:
            push("  UNKNOWN (VPN client/connection summary absent)")
    else:
        push("-- VPN USERS UNKNOWN (client/connection source section absent)")
    a, b = span("-- SS escalation gate", "-- verdict CHANGES")
    if a >= 0:
        push(*body[a:b])
    else:
        push("-- SS escalation gate UNKNOWN (source section absent)")
    a, b = span("-- verdict CHANGES", "-- mind here")
    if a >= 0:
        changes = [line for line in body[a:b] if line.strip()]
        push(changes[0] if changes else body[a])
        if len(changes) > 1:
            push(changes[-1])
            push(f"  {len(changes) - 2} older verdict rows omitted; source={mesh}/chat.log")
    else:
        push("-- verdict CHANGES UNKNOWN (source section absent)")
    push(omitted("Tailscale IP/OS/traffic details, per-client geography, old verdict history and explanatory prose; names, online/offline path/age, own egress, server, tunnel, SS set, client-cache age and named WireGuard state retained"))

elif role == "job":
    # This pane is operational state, not the private fact base or a second hiring lane.
    for line in body:
        if line.startswith("mission:"):
            push(line)
        elif line.startswith("-- pipeline by state --"):
            push(line)
        elif line.startswith("-- pipeline EMPTY"):
            push(line)
        elif line.startswith("-- newest 8"):
            push("-- newest 3 tracked roles (date | company | role | state) --")
        elif line.startswith("-- awaiting reply"):
            push(line)
        elif line.startswith("-- CV items still awaiting") or line.startswith("-- ВХОДЯЩИЕ") or line.startswith("-- РАЗБОР НЕПОЛОН") or line.startswith("-- ВХОДЯЩИЕ БЕЗ ОТВЕТА"):
            push(line)
        elif line.startswith("-- HARD RULES"):
            push("-- HARD RULES: Note 3 first; LinkedIn take-only (no apply/login); employer's own site; unsourced facts/fields block; this lane owns applications and the operator attends interviews; full rule source: mesh-dash --once job --")
        elif line.startswith("-- HIS SPINE"):
            push("-- private CV facts omitted; source=~/.mesh/job/cv-source-2026-08-14.md; read before writing or making claims --")
        elif line.startswith("-- WHY HE LEFT"):
            push("-- private departure framing omitted; source=~/.mesh/job/departure-framing.md --")
        elif line.startswith("-- his answers so far"):
            push("-- private answer artifacts omitted; source=~/.mesh/job/ --")
        elif "разрядить:" in line:
            push(line)
    # Newest role rows are a changing list; keep the latest three, but name the remainder.
    if not any(line.startswith("mission:") for line in body):
        push("mission: UNKNOWN (source field absent)")
    a, b = span("-- newest 8")
    if a >= 0:
        rows = [line for line in body[a + 1:b] if line.strip()]
        push(*rows[:3])
        if len(rows) > 3:
            push(f"  {len(rows) - 3} older role rows omitted; source={mesh}/job-board.tsv")
    else:
        push("-- tracked roles UNKNOWN (source section absent)")
    a, b = span("-- awaiting reply")
    if a >= 0:
        rows = [line for line in body[a + 1:b] if line.strip()]
        if rows:
            push(rows[0])
            if len(rows) > 1:
                push(f"  {len(rows) - 1} more unanswered rows omitted; oldest first; source={mesh}/job-board.tsv")
    else:
        push("-- awaiting reply UNKNOWN (source section absent)")
    a, b = span("-- pipeline by state")
    states = []
    if a >= 0:
        states = [line.strip() for line in body[a + 1:b] if line.strip()]
        if states:
            push("  pipeline: " + " · ".join(states))
        elif not any(line.startswith("-- pipeline EMPTY") for line in body):
            push("  pipeline: UNKNOWN (source rows absent)")
    elif not any(line.startswith("-- pipeline EMPTY") for line in body):
        push("  pipeline: UNKNOWN (source section absent)")
    sent = re.search(r"\bsent\s+(\d+)\b", " ".join(states), re.I)
    push(f"sent {sent.group(1)} · freshness UNKNOWN (source has no declared age threshold)" if sent else "sent UNKNOWN (pipeline source field absent)")
    if not any(line.startswith(("-- CV items still awaiting", "-- ВХОДЯЩИЕ", "-- РАЗБОР НЕПОЛОН", "-- ВХОДЯЩИЕ БЕЗ ОТВЕТА")) for line in body):
        push("-- intake completeness UNKNOWN (source section absent)")
    if not any("разрядить:" in line or re.search(r"машинн\w*\s+ног", line, re.I) for line in body):
        push("machine-leg coverage: UNKNOWN (source field absent)")
    push(omitted("private CV/departure details, older pipeline rows, answer filenames and board traffic; sources=~/.mesh/job/cv-source-2026-08-14.md, departure-framing.md, job-board.tsv, chat.log; role counts, sent/oldest, intake completeness, UNKNOWN and machine-leg coverage retained"))
elif role == "sound":
    # Keep live producer leases and corpus coverage, but replace the unbounded claim/history tables by
    # verdicts and current-state summaries. Any non-HOLDS claim stays named in the live pane.
    a, b = span("-- CLAIMS:")
    if a >= 0:
        claims = body[a:b]
        push(claims[0])
        source_row = next((line.strip() for line in claims[1:] if line.strip().startswith("source:")), "")
        if source_row:
            rows = re.search(r"\((\d+) rows, mtime[ =]([^)]*)\)", source_row)
            push(f"  claims source=records.log rows={rows.group(1)} mtime={rows.group(2)} · ROM=series-stats.rom" if rows else "  claims source: UNKNOWN (timestamped source row unreadable)")
        else:
            push("  claims source: UNKNOWN (timestamped source row absent)")
        measurable = next((line.strip() for line in claims if line.strip().startswith("measurable rows:")), "")
        if measurable:
            push("  " + re.sub(r"^measurable rows:\s*", "measurable=", measurable))
        unknown_counts = [(name, count) for name, count in re.findall(r"unknown\[([^\]]+)\]:\s*(\d+)", "\n".join(claims), re.I)]
        total_unknown = re.search(r"unknown\(degenerate fbeats<=1\)=(\d+)", "\n".join(claims), re.I)
        if unknown_counts or total_unknown:
            detail = ",".join(f"{name}={count}" for name, count in unknown_counts) or "per-organ=UNKNOWN"
            push(f"  sub-window unknown={total_unknown.group(1) if total_unknown else 'UNKNOWN'} (degenerate fbeats<=1): {detail}")
        gate = next((line.strip() for line in claims if line.strip().startswith("claim-gate:")), "")
        push("  " + gate if gate else "  claim-gate: UNKNOWN (source gate row absent)")
        summary = next((line for line in claims if line.strip().startswith("***")), "")
        counts = re.search(r"(\d+) standing claim\(s\).*?(\d+) UNDECIDABLE", summary, re.I)
        if counts:
            push(f"  claim summary: {counts.group(1)} REFUTED/DRIFT/MIXTURE; {counts.group(2)} UNDECIDABLE (CI spans zero)")
        named: list[tuple[str, list[str]]] = []
        current_name = ""
        current_verdicts: list[str] = []
        for line in claims[1:]:
            stripped = line.strip()
            header = re.match(r"(claim \d+ — .+)$", stripped)
            if header:
                if current_name:
                    named.append((current_name, current_verdicts))
                current_name = header.group(1)
                current_verdicts = []
                continue
            verdict = re.match(r"=>\s*(HOLDS|DRIFT|REFUTED|MIXTURE|INDISTINGUISHABLE|UNKNOWN|UNDECIDABLE|DIAGNOSTIC)\b", stripped)
            if verdict and current_name:
                current_verdicts.append(verdict.group(1))
        if current_name:
            named.append((current_name, current_verdicts))
        for name, verdicts in named:
            non_holds = collections.Counter(value for value in verdicts if value != "HOLDS")
            if non_holds:
                claim_id = re.match(r"claim \d+", name)
                quoted = re.search(r'"([^"]+)"', name)
                label = f"{claim_id.group(0)} “{quoted.group(1)}”" if claim_id and quoted else (claim_id.group(0) if claim_id else "claim UNKNOWN")
                states = ", ".join(f"{value}×{non_holds[value]}" if non_holds[value] > 1 else value for value in sorted(non_holds))
                push(f"  {label} => {states}")
            elif not verdicts:
                push(f"  {name.split(' — ', 1)[0]} => UNKNOWN (verdict row absent)")
    else:
        push("  claim-gate: UNKNOWN (CLAIMS section absent)")
    # Keep the source sections that carry current health, corpus, and held-experiment state.
    headers = (
        "-- LEASES",
        "-- SOURCES",
        "-- RECORDS",
        "-- INBOX",
        "-- RENDERS",
        "-- SOUNDSCAPES",
        "-- EXPERIMENTS",
    )
    older_records = 0
    older_renders = 0
    for marker in headers:
        a, b = span(marker)
        if a < 0:
            continue
        rows = body[a:b]
        if marker.startswith("-- LEASES"):
            leases = []
            for line in rows[1:]:
                match = re.match(r"\s*([A-Za-z0-9_-]+)\s+(fresh|recent|stale|held|booting|down|idle|unknown)\s+(.*)", line, re.I)
                if match:
                    producer, state, detail = match.groups()
                    leases.append(f"{producer}={state.upper()} ({detail.split(' — ', 1)[0]})")
                elif line.strip():
                    leases.append("UNKNOWN (source lease row unreadable)")
            push(rows[0], "  leases: " + " · ".join(leases) if leases else "  leases UNKNOWN (source rows absent)")
        elif marker.startswith("-- SOURCES"):
            source_states = []
            for part in " | ".join(line.strip() for line in rows[1:] if line.strip()).split(" | "):
                match = re.match(r"(\w+)\s+(\S+)\s+ago\s+(\d+) in corpus(?:\s+·\s+(\d+) ground in-window\(~4h\))?", part)
                if match:
                    organ, age_text, count, ground = match.groups()
                    source_states.append(f"{organ}={age_text}/{count}/{ground if ground else 'UNKNOWN'}")
                elif "no record in the corpus" in part:
                    source_states.append("voice=never/no-record")
            push(rows[0], "  organs: " + (", ".join(source_states) if source_states else "UNKNOWN (source rows absent)"))
        elif marker.startswith("-- RECORDS"):
            push(rows[0])
            measurements = [line.strip() for line in rows[1:] if re.match(r"\s*\d{4}-\d\d-\d\dT", line)]
            if measurements:
                latest = measurements[-1]
                fields = re.search(r"(\d{4}-\d\d-\d\dT\d\d:\d\dZ)\s+(\S+)\s+\S+\s+dur=([\d.]+)\s+win=([\d.]+)\s+cov=([\d.]+)\s+score=([\d.]+)\s+beats=(\d+).*->\s*(\w+)$", latest)
                push(f"  latest record: {fields.group(1)} {fields.group(2)} score={fields.group(6)} beats={fields.group(7)} dur={fields.group(3)}s win={fields.group(4)}s cov={fields.group(5)} → {fields.group(8)}" if fields else "  latest record UNKNOWN (source row unreadable)")
                if len(measurements) > 1:
                    older_records = len(measurements) - 1
            else:
                push("  latest record UNKNOWN (no timestamped row)")
        elif marker.startswith("-- INBOX"):
            inbox_rows = [line.strip() for line in rows[1:] if line.strip()]
            push(rows[0], inbox_rows[0] if inbox_rows else "  inbox state UNKNOWN (source rows absent)")
        elif marker.startswith("-- RENDERS"):
            push(rows[0])
            values = [line for line in rows[1:] if line.strip()]
            renders = [line.strip() for line in values if re.match(r"\s*\d{4}-\d\d-\d\dT", line)]
            meta = [line.strip() for line in values if re.search(r"novelty|UNKNOWN|STALE|FAIL|SOURCE-STARVED", line, re.I)]
            if renders:
                latest = renders[-1]
                fields = re.search(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)\s+amc l\s+(\d+) w\s+(\d+) ss\s+([\d.]+) s\s+([\d.]+) c\s+([^\s]+).*?src=([^\s]+).*?mode\s+([^\s]+).*?cov\s+([\d.]+|na|UNKNOWN)", latest, re.I)
                push(f"  latest render: {fields.group(1)} src={fields.group(7)} · amc l{fields.group(2)} w{fields.group(3)} ss{fields.group(4)} s{fields.group(5)} c{fields.group(6)} · mode={fields.group(8)} cov={fields.group(9)}" if fields else "  latest render UNKNOWN (source row unreadable)")
                if len(renders) > 1:
                    older_renders = len(renders) - 1
            else:
                push("  UNKNOWN (no timestamped render rows)")
            push(*[line for line in meta if line.startswith("novelty") or re.search(r"UNKNOWN|STALE|FAIL|SOURCE-STARVED", line, re.I)][-2:])
        elif marker.startswith("-- SOUNDSCAPES"):
            push(rows[0])
            values = [line.strip() for line in rows[1:] if line.strip()]
            if values:
                push(values[-1])
            else:
                push("  last soundscape result UNKNOWN (source row absent)")
        else:
            push(*rows)
    if older_records or older_renders:
        push(f"  older record/render rows omitted: {older_records}/{older_renders}; source=mesh records/log")
    for marker in headers:
        if span(marker)[0] < 0:
            push(f"{marker} UNKNOWN (source section absent)")
    if span("-- REPO:")[0] >= 0:
        push("  repository branch/dirty detail omitted; source=grainneukeln repo")
    # Keep diversity even when it is UNKNOWN; do not let an absent producer masquerade as silence.
    diversity = [line for line in body if line.lstrip().startswith("diversity:") or "MONOTONE" in line or "TIMEOUT" in line and "mesh-room-music" in line]
    push(*diversity)
    if not any(line.lstrip().startswith("diversity:") for line in body):
        push("diversity: UNKNOWN (source result absent)")
    push(omitted("frontier prose, per-client/source details, historical notable/repository rows, older record/render/soundscape history and recipes; source=mesh records/log and sound-experiments.md"))

elif role == "wake":
    # The source already bounds scored rungs, replicate families and adapters, and names each remainder.
    if any(line.startswith("lane:") for line in body):
        push(*(line for line in body if line.startswith("lane:")))
    else:
        push("lane: UNKNOWN (run identity field absent)")
    for marker in ("-- RUN IN FLIGHT", "-- no lane run", "-- producer gate:", "-- repo:"):
        a, b = span(marker)
        if a >= 0:
            push(*body[a:b])
        elif marker == "-- producer gate:":
            push("-- producer gate: UNKNOWN (source section absent)")
        elif marker == "-- repo:":
            push("-- repo: UNKNOWN (GPU/run-state source absent)")
    if not any(line.startswith("-- RUN IN FLIGHT") or line.startswith("-- no lane run") for line in body):
        push("-- RUN IN FLIGHT UNKNOWN (no run/no-lane status section)")
    a, b = span("SCORED RUNGS", "TRAINED ADAPTERS")
    if a >= 0:
        scored = body[a:b]
        push(scored[0] + " · aggregate freshness threshold UNKNOWN (per-rung ages shown)")
        push(*scored[1:])
    else:
        push("SCORED RUNGS UNKNOWN (source section absent)")
    a, b = span("TRAINED ADAPTERS")
    if a >= 0:
        push(body[a])
        adapter_rows = [line for line in body[a + 1:b] if re.search(r"VAL LOSS IS.*ANTI-SELECTOR|recently between replicates|no trainlog\.json|showing the|n_train=|UNREADABLE|adapter|trainlog|UNKNOWN|STALE|PASS|FAIL|age=", line, re.I)]
        warning_rows = [line for line in adapter_rows if re.search(r"VAL LOSS IS.*ANTI-SELECTOR|recently between replicates|no trainlog\.json|UNREADABLE|UNKNOWN|STALE|PASS|FAIL", line, re.I) and "n_train=" not in line]
        train_rows = [line for line in adapter_rows if "n_train=" in line]
        total_match = next((re.search(r"of (\d+) adapters", line, re.I) for line in adapter_rows if "showing the" in line.lower()), None)
        seed_note = any("NOTE: before 2026-08-18" in line for line in body[a + 1:b])
        push(*warning_rows)
        if total_match and total_match.group(1):
            total = int(total_match.group(1))
            push(f"  latest trained adapter of {total}; {max(0, total - 1)} older adapters omitted; source=~/finnegans-fake/wake/fold-lora-*/trainlog.json")
        if train_rows:
            push(train_rows[-1])
        else:
            push("  UNKNOWN (adapter/trainlog status rows absent)")
        if seed_note:
            push("  seed note: before 2026-08-18, the seed chose rows but not torch RNG; older adapters are not replicates—check ages.")
    else:
        push("TRAINED ADAPTERS UNKNOWN (source section absent)")
    if not any("power-off age" in line.lower() for line in body):
        push("GPU power-off age: UNKNOWN (this renderer has no power-off-age source; idle utilization is not power-off evidence)")
    push(omitted("older adapter logs and board history; source=~/finnegans-fake/wake/fold-lora-*/trainlog.json and ~/.mesh/chat.log; scored-run remainder, paired uncertainty, adapter/trainlog state, run/GPU state and UNKNOWN power-off age retained"))

else:
    # Genome's role name is already its pane name; check maps to health above.
    push(*body)

# De-duplicate while preserving semantic order, and do not create a blank frame if a source vanished.
seen: set[str] = set()
for line in out:
    if line not in seen:
        print(line)
        seen.add(line)
