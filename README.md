# The Window and the Agent

*On building a workstation that doesn't exist*

Last night I built a working development machine out of things I already owned: a 2011 laptop running an OS three versions out of support, a phone about seven years old, an even older iPhone SE, a Bluetooth keyboard, and a display salvaged from a 2013 Mac. None of these objects is, by current standards, a computer you would choose to work on. Each one, alone, is the kind of thing you are quietly encouraged to replace.

Assembled, they behave like a portable laptop that has never been manufactured. The heavy lifting happens elsewhere — on a VM, and, more importantly, inside a coding agent running on that VM. What I hold in my hands is no longer being asked to compute. It is being asked to show me a screen and take my keystrokes. And at that, a fourteen-year-old laptop is exactly as good as a new one.

I want to argue that this is not a clever hack. It is a small example of a position that two existing communities have each half-discovered, and that neither has yet stated whole.

## Two camps, each half-right

The first camp is permacomputing. Its instinct is ethical and ecological: hardware should last, e-waste is a moral problem, and software ought to respect the machines that already exist rather than conscripting everyone into an upgrade cycle. This is correct and good. But permacomputing's reflex is *local* self-sufficiency. Its ideal is software so lean it runs on the old machine directly, and its suspicion of the cloud runs deep — dependency on a datacenter reads as fragility, as a loss of autonomy. So it sets itself a hard task: heroically optimize software downward until it fits inside weak, old silicon.

The second camp is remote-first computing — thin clients, homelabs, "treat the home server as the computer and the device in your hand as a screen with manners." Its instinct is architectural: put the weight on a capable host, let the endpoint be light. This is also correct. But its motivation is usually convenience, centralization, or raw power. The thin client, in this story, is cheap. It is not *dignified*. Nobody in this camp is moved by the fact that the endpoint was rescued from a drawer. The old phone is incidental; any cheap screen would do.

Each camp holds one of the two pieces. Permacomputing holds the ethics of old hardware. Remote-first holds the architecture that frees it. But put bluntly: permacomputing wants old hardware to stay self-sufficient and pays for it in endless software optimization; remote-first is happy to offload the work but doesn't care whether the endpoint lived a previous life or rolled off a line last week.

## The variable nobody priced in

What changes the equation is the agent.

For decades, "thin client to a powerful machine" meant a remote desktop. You still did the work; the remote box merely lent you its CPU. The endpoint had to render a full graphical environment — windows, compositing, the whole weight of a modern desktop — even though the computation was elsewhere. The screen was thin, but the *interface* was still thick.

A coding agent collapses that. When the thing on the other end is not just horsepower but an *executor*, the endpoint no longer has to present a heavy GUI at all. It has to present a conversation. Text in, text out, a diff, a log, a confirmation. The old phone is not straining to mirror a desktop; it is displaying a dialogue with something that does the work on your behalf.

This is the move neither camp made. Permacomputing said: *software must respect old hardware.* But the deeper implication, once an agent exists, is stronger and stranger: old hardware does not need to carry the software at all. The agent carries it. The hardware becomes a window. And the moment that happens, permacomputing's central burden — the heroic downward optimization — simply dissolves. You no longer need to shrink the software to fit the machine, because the software has left the machine entirely. What stays behind is the lightest possible task, the one task old hardware has always been able to do forever: show text, accept input, hold a network connection.

## Old hardware stops aging

Here is the consequence I find genuinely beautiful.

A display from 2013 does not need to get faster. It renders text exactly as well as a display sold today. A keyboard does not receive updates. A seven-year-old phone can draw a terminal indefinitely; there is no version of "drawing a terminal" that it will fall behind on. The reason old hardware feels obsolete is that we keep asking it to do the one category of thing it cannot keep up with — to *locally* run software that grows heavier every year. Remove that demand, and the obsolescence evaporates. The hardware was never slow at being a window. It was only slow at being a computer, and we have stopped asking it to be one.

So the synthesis is this: old hardware, plus a remote agent, equals a new kind of self-sufficiency — not the local self-sufficiency permacomputing wanted, but something that achieves the same end (long-lived devices, no forced upgrades, dignity for the machine you already have) by an opposite route. Not "make the software small enough to stay home," but "let the work leave, and let the home device be the calm, permanent thing it is good at being."

## A way of seeing

There is a Japanese word, *mitate*, that means something like seeing an ordinary thing as utterly new — not transforming it, but perceiving the form that was already there. The pile of old hardware was always a workstation. Termux, SSH, tmux, an agent — none of it is new. The network was always reliable enough. What was missing was the angle from which the pile resolves into a machine.

This is not a product. It is barely even a configuration. It is a stance: that the device in your hand does not need to be powerful, only present; that power belongs on a host you do not carry; and that the work itself can increasingly be handed to something that does it while you watch. The screen you carry can be any screen you like — including the one you already own and were about to throw away.

The good computer doesn't have to travel with you. Increasingly, it doesn't even have to be operated by you. It only has to be reachable. And almost anything, it turns out, is enough to reach it.

---

## How to build it

What follows is how the setup described above actually works — the practical infrastructure behind the idea.

![lte-workstation: phone terminal + Telegram bot notifications](screenshot.svg)

### What you get

- **Permanent mosh connection** via Tailscale — stable IP, survives switching networks mid-session
- **SSH fallback** via ngrok — dynamic public URL, auto-notified via Telegram bot
- **Auto-notifications** — Telegram message with connection commands whenever your machine comes online
- **Auto-start on reboot** — everything comes back up without manual action
- **Optional: MTProto Telegram proxy** — for regions where Telegram is blocked (Russia, Iran, etc.)
- **Phone as a sensor node** — SSH from the VM back into the phone; access mic, camera, location, battery via termux-api

### Prerequisites

You need these installed on your Linux machine before running setup:

| Tool | Purpose | Install |
|------|---------|---------|
| [Docker](https://docs.docker.com/engine/install/) | Runs MTG proxy container | distro packages |
| [ngrok](https://ngrok.com/download) | SSH tunnel with public URL | download binary → `~/.local/bin/ngrok` |
| [bore](https://github.com/ekzhang/bore) | TCP tunnel for proxy relay | `cargo install bore-cli` |
| [mosh](https://mosh.org) | Resilient SSH alternative | `sudo apt install mosh` |
| [Tailscale](https://tailscale.com/download) | Permanent private IP | package + `sudo tailscale up` |

You also need:
- A **Telegram bot token** — create one via [@BotFather](https://t.me/BotFather) → `/newbot`
- Your **Telegram chat ID** — message [@userinfobot](https://t.me/userinfobot)
- An **ngrok account** (free) — get your auth token at [dashboard.ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)

### Setup

```bash
git clone https://github.com/genaforvena/lte-workstation
cd lte-workstation
./setup.sh
```

The script checks prerequisites, asks for your tokens, generates config, installs scripts, and enables systemd services. Run it once.

Your credentials are saved to `~/.config/remote-access/env` (chmod 600, never committed to git).

### How it works

```
Phone (Termux + mosh)  ──── Tailscale WireGuard ──── Linux VM
                                                           │
                                                    ngrok TCP tunnel
                                                    → public SSH URL
                                                           │
                                                  bore.pub TCP tunnel
                                                    → MTG proxy (optional)
                                                    → Telegram servers
```

On boot:
1. `ngrok.service` opens a TCP tunnel to port 22 and sends you a Telegram message with the SSH command and your permanent mosh address
2. `bore-mtg.service` (if enabled) sends two Telegram proxy buttons: one via your Tailscale IP (permanent, works on LTE where bore.pub may be blocked) and one via bore.pub (fallback)

The bore.pub port changes on restart — that's expected. The bot always sends the fresh link. **Use the Tailscale link on LTE.**

### Phone setup (Termux)

```bash
pkg update && pkg install termux-services mosh openssh termux-api
```

Connect to the VM:

```bash
mosh your-user@your-tailscale-ip
```

Get your Tailscale IP from the Telegram notification or by running `tailscale ip -4` on the VM.

> **Tip:** pair a Bluetooth keyboard with your phone. A $15–20 keyboard transforms the experience — you get proper modifier keys, Tab, arrow keys, and no on-screen keyboard eating half your screen.

Start the SSH server so the VM can reach back into the phone:

```bash
sshd
```

To prevent Android from killing the Termux process during long sessions:

```bash
termux-wake-lock   # run this in Termux before long operations
```

Also disable battery optimization: **Settings → Apps → Termux → Battery → Unrestricted**. On Xiaomi/Redmi, also enable **Autostart** for Termux in Settings → Apps.

### Phone as a sensor node

Once `sshd` is running on the phone and both devices are on Tailscale, the VM can SSH *into* the phone. This turns the phone into a sensor node — the VM can access the phone's hardware remotely.

```bash
# From the VM
ssh -p 8022 u0_a386@<phone-tailscale-ip>
```

With [termux-api](https://wiki.termux.com/wiki/Termux:API) installed (`pkg install termux-api`), and the **Termux:API companion app** from F-Droid:

```bash
# Check battery
ssh -p 8022 u0_a386@<phone-ip> "termux-battery-status"

# Get location
ssh -p 8022 u0_a386@<phone-ip> "termux-location -p network"

# Record audio (grant Microphone permission first; run termux-setup-storage for storage access)
ssh -p 8022 u0_a386@<phone-ip> "termux-wake-lock; termux-microphone-record -l 10"
# wait for isRecording: false before copying
ssh -p 8022 u0_a386@<phone-ip> "termux-microphone-record -i"
scp -P 8022 u0_a386@<phone-ip>:storage/shared/TermuxAudioRecording_*.m4a ./
```

> **Permissions required:** Microphone → Settings → Apps → Termux → Permissions → Microphone. Storage → run `termux-setup-storage` in Termux and approve the dialog.

> **Camera capture** (`termux-camera-photo`) requires the Termux:API companion app from F-Droid. Camera info and battery status work without it.

For scripted access without interactive password prompts, use `SSH_ASKPASS`:

```bash
cat > /tmp/askpass.sh << 'EOF'
#!/bin/bash
printf 'your-termux-password'
EOF
chmod +x /tmp/askpass.sh
SSH_ASKPASS=/tmp/askpass.sh SSH_ASKPASS_REQUIRE=force \
  ssh -p 8022 -o PasswordAuthentication=yes -o PreferredAuthentications=password \
  u0_a386@<phone-ip> "termux-battery-status"
```

### MTProto proxy (censored regions)

If Telegram is blocked on your LTE network, the optional proxy routes your Telegram traffic through this machine and out via your network's exit point. Setup prompts you for an SNI domain (fake-TLS camouflage) — pick a domain that's commonly accessed on your network:

- Russia: `yandex.ru`
- Iran: pick any unblocked local domain
- Other: `google.com`, `apple.com`, or any HTTPS site that isn't blocked

The proxy secret is embedded in the Telegram "Add Proxy" button the bot sends you.

#### Sharing with others

`proxy-bot.service` runs an access-control bot on the same Telegram bot token. To share your proxy:

1. Send friends your bot link: `https://t.me/yourbotname`
2. They tap `/start` — you receive a notification with their Telegram handle and **Approve / Deny** buttons
3. Tap **Approve** — the bot sends them the proxy link automatically

**Owner commands** (send these to your bot):

| Command | What it does |
|---------|-------------|
| `/list` | Show all users and their status (approved / pending / denied) |
| `/revoke @username` | Cut off someone's access |

When the bore.pub port changes (service restart), all approved users are automatically sent the updated link — no manual re-sharing needed.

> **Note:** the bot needs `python3` and `python-telegram-bot==20.*` installed in `~/.local/venv/proxy-bot/`. The setup script handles this. Approved users receive the bore.pub link (publicly accessible); your personal Tailscale link is sent only to you.

### Terminal stack

Connectivity gets you in. The tools make it feel like a real workstation. This is what works well over mosh on a phone screen:

| Tool | What it does | Install |
|------|-------------|---------|
| [Helix](https://helix-editor.com) | Modal editor with LSP built-in, no plugin manager needed | `sudo apt install helix` or [binary](https://github.com/helix-editor/helix/releases) |
| [lazygit](https://github.com/jesseduffield/lazygit) | Terminal git UI, everything on one screen | `sudo apt install lazygit` |
| [zoxide](https://github.com/ajeetdsouza/zoxide) | Smarter `cd` — jump to any directory by partial name | `sudo apt install zoxide` |
| [yazi](https://github.com/sxyazi/yazi) | Terminal file manager, opens files in Helix | [binary releases](https://github.com/sxyazi/yazi/releases) |
| [fzf](https://github.com/junegunn/fzf) | Fuzzy finder for history, files, processes | `sudo apt install fzf` |
| [starship](https://starship.rs) | Cross-shell prompt, shows git state and context | `curl -sS https://starship.rs/install.sh \| sh` |

These tools are optimized for terminal use with no mouse — which is exactly what you have on a phone. Helix in particular is worth learning: it's modal like Vim but with LSP, tree-sitter, and multi-cursor built in, so you don't need to configure plugins to get a full IDE experience.

For yazi + zoxide integration (so directories you navigate to in yazi are learned by `z`), and Helix as yazi's default opener, see [genaforvena/dotfiles](https://github.com/genaforvena/dotfiles).

## Files

```
scripts/
  ngrok-notify.sh      # sends Telegram message with SSH/mosh commands on ngrok start
  bore-mtg.sh          # bore tunnel + proxy notifications + notifies approved users on port change
  proxy-bot.py         # access-control bot: approve/deny proxy requests from Telegram
  ngrok.service        # systemd user service
  bore-mtg.service     # systemd user service
  proxy-bot.service    # systemd user service
setup.sh               # one-time interactive setup
```

## Maintenance

**Rotate tokens:** edit `~/.config/remote-access/env`, then `systemctl --user restart ngrok.service bore-mtg.service`.

**Regenerate MTG secret** (e.g. to change SNI domain):
```bash
docker run --rm ghcr.io/9seconds/mtg:2 generate-secret --hex yandex.ru
# update MTG_SECRET in ~/.config/remote-access/env and ~/.config/mtg/config.toml
docker restart mtg
systemctl --user restart bore-mtg.service
```

**Check service status:**
```bash
systemctl --user status ngrok.service bore-mtg.service proxy-bot.service
journalctl --user -u proxy-bot.service -f
```
