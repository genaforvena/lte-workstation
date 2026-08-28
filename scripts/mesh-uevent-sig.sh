#!/usr/bin/env bash
# mesh-uevent-sig.sh — THE ONE PLACE that says which synthetic uevents on this mesh are OURS.
# orphan-ok: sourced library, never executed. Its launchers are the tools that source it —
#   mesh-devcd-catch (signs its receive-leg probe) and mesh-udev-stream (classifies the tape's
#   synth column, and signs its own hwmon probe). Verify by grep: `grep -l mesh-uevent-sig.sh
#   scripts/mesh-*` must name both; if it names neither, this file is a genuine orphan.
#
#   . "${MESH_UEVENT_SIG_LIB:-$HOME/.local/bin/mesh-uevent-sig.sh}" 2>/dev/null || \
#     . "$(dirname "$0")/mesh-uevent-sig.sh" 2>/dev/null || true
#
#   mesh_uevent_sig_uuid  <tool>            # the fixed uuid that tool signs with (rc 1: unregistered)
#   mesh_uevent_sig_class <raw>             # classify a tape's raw synth field -> one WORD on stdout
#   mesh_uevent_trigger_signed <tool> <sudo> <devdir>...   # fire a SIGNED synthetic uevent
#
# WHY THIS FILE EXISTS. A probe that proves a listener is alive has to MINT the very signal the
# node's device-churn detectors read, and nothing in between said the enumeration was ours:
# mesh-devcd-catch fires `udevadm trigger --action=change --subsystem-match=mem` as its receive-leg
# probe, that mints 8 uevents on /dev/{full,kmsg,mem,null,port,random,urandom,zero}, and
# mesh-device-churn reads /sys/kernel/uevent_seqnum and reports CHURN. Attributing one such burst
# cost 35 hours. CLAUDE.md already carries the rule — sign the event at the SOURCE, in a field the
# kernel prints, never fingerprint it by device set or burst size, because a size band is a proxy
# for identity and its failure direction is SILENCE.
#
# THE FIELD IS SYNTH_UUID AND IT IS THREE-VALUED (all three measured live on mesh-home,
# udevadm 255, 2026-08-28, off `udevadm monitor --udev --property`):
#
#   property absent      -> a KERNEL-originated uevent. Driven with a real loop-device attach:
#                           3 events on /devices/virtual/block/loop0 carried no SYNTH_UUID at all.
#   SYNTH_UUID=0         -> SYNTHETIC BUT UNSIGNED. The kernel's kobject_synth_uevent() stamps the
#                           literal `SYNTH_UUID=0` when something writes a bare action word to a
#                           sysfs `uevent` file — which is exactly what a plain `udevadm trigger`
#                           does. 8 such events per mem-subsystem trigger.
#   SYNTH_UUID=<uuid>    -> SIGNED, and the signer chose the value.
#
# THE TRAP THE OBVIOUS FIX WALKS INTO: `udevadm trigger --uuid` TAKES NO ARGUMENT. On udevadm 255
# it MINTS a fresh random uuid PER DEVICE and prints them to stdout (measured: one 8-device mem
# trigger printed 8 distinct uuids). So it cannot carry a known identity, and routing those printed
# uuids to the reader would mean a sidecar file the reader must open, freshly, on every burst — a
# crash between the trigger and the sidecar write loses the attribution for exactly the events it
# was minted to explain.
#
# So we write the uuid ourselves, straight into the device's `uevent` file — `printf 'change <uuid>'`
# — which is the same syscall udevadm makes, minus the discarded identity. The kernel's
# kobject_action_args() only requires uuid_is_valid(): 8-4-4-4-12 hex with dashes. It does NOT
# require randomness, so a CONSTANT is legal and a constant is what makes attribution possible.
#
# THE NAMESPACE IS LOAD-BEARING, NOT DECORATION. Every mesh uuid starts `6d657368` — "mesh" in hex
# ASCII. That prefix, not the per-tool table below, is what answers "was this ours": a tool added
# next year that signs with the namespace and never touches this table still reads as OURS
# (`ours:unregistered`), instead of being misfiled as a stranger's. The table only refines ours into
# WHICH tool. A registry that must be edited in lockstep to stay correct is a constant that outlives
# its reader; this one degrades to a coarser true answer instead of a confident wrong one.
#
# WHAT MUST NEVER HAPPEN: an unsigned or kernel event being swallowed by this exemption. The day a
# real device enumerates is the day the tape must still say so, loudly. mesh_uevent_sig_class maps
# EVERY non-ours value to its own word and never to `ours`, and a tape row written before this
# column existed classifies `unknown` — never `kernel`, which would silently backdate the field.

# The mesh namespace prefix. `6d657368` = "mesh" in hex ASCII.
MESH_UEVENT_SIG_NS="${MESH_UEVENT_SIG_NS:-6d657368}"

# The registry. Fourth group `8000` and the version nibble `4` keep these well-formed v4-shaped
# uuids; the last group spells the tool in hex ASCII so a raw tape row is readable by eye.
mesh_uevent_sig_uuid(){   # $1 = tool name -> uuid on stdout, rc 1 if unregistered
  case "${1:-}" in
    mesh-devcd-catch) printf '%s-0001-4000-8000-64657663645f\n' "$MESH_UEVENT_SIG_NS" ;;  # "devcd_"
    mesh-udev-stream) printf '%s-0002-4000-8000-756465767374\n' "$MESH_UEVENT_SIG_NS" ;;  # "udevst"
    *) return 1 ;;
  esac
}

# Reverse lookup, table first then namespace. Returns rc 1 for anything that is not ours.
mesh_uevent_sig_name(){   # $1 = uuid -> tool name (or `unregistered`) on stdout
  local u="${1:-}" t
  for t in mesh-devcd-catch mesh-udev-stream; do
    [ "$u" = "$(mesh_uevent_sig_uuid "$t")" ] && { printf '%s\n' "$t"; return 0; }
  done
  case "$u" in "$MESH_UEVENT_SIG_NS"-*) printf 'unregistered\n'; return 0;; esac
  return 1
}

# THE CLASSIFIER. One word per world, and the four worlds answer different questions — a caller that
# folds them back together has undone the whole point.
#   kernel      a real device did something
#   ours:<tool> one of our own probes, and we can name which
#   unsigned    synthetic, but nobody signed it: NOT exempt, someone must go look
#   foreign     signed by something that is not us: NOT exempt either
#   unknown     the tape row predates this column: absence of evidence, never `kernel`
mesh_uevent_sig_class(){   # $1 = the raw synth field as recorded on the tape
  local raw="${1:-}" n
  case "$raw" in
    ''|na)  printf 'unknown\n' ;;
    -)      printf 'kernel\n' ;;
    0)      printf 'unsigned\n' ;;
    *)      if n="$(mesh_uevent_sig_name "$raw")"; then printf 'ours:%s\n' "$n"; else printf 'foreign\n'; fi ;;
  esac
}

# Fire a signed synthetic `change` on each named device directory. Writes `change <uuid>` to
# <devdir>/uevent, which is what udevadm trigger does except that the identity survives.
# $1 tool · $2 sudo command (may be empty for an already-root caller) · $3.. device directories.
# rc 0 if at least one write landed, 1 if none did — a probe that could not fire must never read
# like a probe that fired and found nothing.
mesh_uevent_trigger_signed(){
  local tool="${1:-}" sudo_cmd="${2:-}" uuid d ok=0
  shift 2 2>/dev/null || return 1
  uuid="$(mesh_uevent_sig_uuid "$tool")" || return 1
  for d in "$@"; do
    [ -e "$d/uevent" ] || continue
    if [ -n "$sudo_cmd" ]; then
      printf 'change %s\n' "$uuid" | $sudo_cmd tee "$d/uevent" >/dev/null 2>&1 && ok=$((ok+1))
    else
      printf 'change %s\n' "$uuid" > "$d/uevent" 2>/dev/null && ok=$((ok+1))
    fi
  done
  [ "$ok" -gt 0 ]
}
