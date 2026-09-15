# Health warning triage: repeated egress, LAN, and microphone delta

Task: `health-warning/38bacb4a2ec1b8b3b041/triage`

The 18:15Z warning repeats the two egress findings and LAN UNKNOWN, with a transient peer-path
delta and a mic-default warning. Current read-only checks at 13:49Z show:

- The one-shot check pane reports supervised egress on `tailscale0` (`4UP/0DOWN`), a current
  egress probe `OK loss=0%`, 0/439 bad in its 24-hour counter, and an exit-node dependency.
  `tailscale status` shows `phaedra` active as the exit node over a direct path. This confirms
  reachability while retaining the known single-exit SPOF.
- The `imac-rozalia` path is time-varying: the current Tailscale status shows it idle; a concurrent
  path-watch FYI at 13:49:01Z reported direct-to-relay fallback for that peer. The warning's
  relay observation cannot be called fixed from one sample.
- `mesh-lan-presence --nodes` exits 1/UNKNOWN: no local address in `192.168.8.0/24`, no ARP view
  of that segment, and no known host answered ICMP. Router-down is not established.
- The physical default route uses `enp42s0`, but a targeted `ip route get 100.76.0.1` resolves via
  `tailscale0 table 52`; `ip rule` confirms table 52 is selected before the main table. The default
  route alone is not evidence that the pane's Tailscale egress label is wrong. This confirms the
  correction recorded in the previous task's addendum.
- `pactl get-default-source` names the USB2.0 Camera microphone. `pactl list short sources` shows
  that source present in PipeWire; `arecord -l` shows no free subdevice, and `fuser` reports an
  active `arecord` owner on `/dev/snd/pcmC2D0c`. I did not contend with it by starting another
  capture. This establishes the selected source and current device use, not that the doctor's
  mic-default warning is cleared or that the recorder caused it.
- The pane's doctor summary remains cached from 13:35:58Z. The earlier live sweep printed known
  egress FAILs and the mic-default WARN but did not complete; its totals are not a fresh result.

Verdict: current egress probe passes, but the intentional exit-node SPOF remains. LAN is still
unobservable from this host and the iMac relay observation is transient. The selected microphone
source exists but its hardware is currently owned by an `arecord` process, so microphone
availability has not been independently tested. No routing, VPN, DNS, firewall, or audio setting
was changed.

Verification: `mesh-dash --once check` at 13:49Z; `tailscale status`; `mesh-lan-presence --nodes`
(exit 1/UNKNOWN); `ip route get 100.76.0.1`; `ip rule`; `pactl get-default-source`; `pactl list
short sources`; `arecord -l`; and `fuser -v /dev/snd/*`. No fresh completed `mesh-doctor` total
is claimed.
