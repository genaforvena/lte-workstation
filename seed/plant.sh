#!/bin/sh
# mishe mishe to tauftauf — the seeder.
#
#   sh -c "$(curl -fsSL https://raw.githubusercontent.com/genaforvena/lte-workstation/main/seed/plant.sh)"
#
# Read it first. That is not a formality: pasting a URL into a shell is literally
# "run a stranger's code on my machine", and a seeder that cannot be read before it
# runs has no business asking. So: no obfuscation, no second download inside, no
# sudo of its own accord, and every path it touches outside its own folder is named
# out loud below and again on screen before anything is written.
#
# WHAT IT TOUCHES
#   ~/.mishe/            everything it plants (board, handoff, organs, the `mishe` core)
#   ~/.local/bin/mishe   one symlink, so the core is on PATH
#   a tmux session named after the node
# WHAT IT DOES NOT DO
#   no package install without asking · no cron · no systemd · no network beyond the
#   one download that fetched this file · nothing outside $HOME
#
# The seeder is single-use. It plants, it shows you what it planted, and then it
# deletes itself in front of you.

set -u

MISHE_HOME="${MISHE_HOME:-$HOME/.mishe}"
BIN_DIR="$HOME/.local/bin"
SELF="$0"

# ---------------------------------------------------------------- terminal

if [ -t 1 ]; then TTY_OUT=1; else TTY_OUT=0; fi
if [ -t 0 ]; then TTY_IN=1; else TTY_IN=0; fi

cols() { c=$(tput cols 2>/dev/null); [ -n "${c:-}" ] && [ "$c" -gt 0 ] 2>/dev/null && echo "$c" || echo 80; }
rows() { r=$(tput lines 2>/dev/null); [ -n "${r:-}" ] && [ "$r" -gt 0 ] 2>/dev/null && echo "$r" || echo 24; }
COLS=$(cols); ROWS=$(rows)

esc() { [ "$TTY_OUT" = 1 ] && printf '%b' "$1"; }
dim()  { esc "\033[2m"; }
bold() { esc "\033[1m"; }
off()  { esc "\033[0m"; }
clear_screen() { [ "$TTY_OUT" = 1 ] && printf '\033[2J\033[H'; }
hide_cursor() { esc "\033[?25l"; }
show_cursor() { esc "\033[?25h"; }
pause() { [ "$TTY_OUT" = 1 ] && sleep "$1"; }

trap 'show_cursor; exit 130' INT TERM

# Centre a line in the real terminal width. Never assume 80.
say_centre() {
    text="$1"
    len=$(printf '%s' "$text" | wc -c | tr -d ' ')
    pad=$(( (COLS - len) / 2 )); [ "$pad" -lt 0 ] && pad=0
    printf '%*s%s\n' "$pad" '' "$text"
}

# ---------------------------------------------------------------- the birth

# The mishustik. It is born, it shows you what it knows, it plants, it dies.
# The MESH is not born — it is the thing that was already there and gets a node.
CREATURE_1='   ( .. )   '
CREATURE_2='  ( o.o )   '
CREATURE_3='  ( ^.^ )   '
CREATURE_X='  ( x.x )   '
LEGS='   /|  |\   '
LEGS_DEAD='   \      / '

WORD_LINES="
 _ __ ___ (_)___| |__   ___
| '_ \` _ \\| / __| '_ \\ / _ \\
| | | | | | \\__ \\ | | |  __/
|_| |_| |_|_|___/_| |_|\\___|
"

birth() {
    clear_screen
    hide_cursor
    top=$(( (ROWS - 12) / 2 )); [ "$top" -lt 0 ] && top=0
    i=0; while [ "$i" -lt "$top" ]; do printf '\n'; i=$((i+1)); done

    for frame in "$CREATURE_1" "$CREATURE_2" "$CREATURE_3"; do
        printf '\033[2K'; say_centre "$frame"
        printf '\033[2K'; say_centre "$LEGS"
        pause 0.35
        [ "$TTY_OUT" = 1 ] && printf '\033[2A'
    done
    printf '\033[2B\n'

    dim; say_centre "mishe mishe to tauftauf"; off
    pause 0.5
    # The wordmark arrives a line at a time — the thing writing itself out.
    printf '%s' "$WORD_LINES" | while IFS= read -r line; do
        [ -z "$line" ] && continue
        bold; say_centre "$line"; off
        pause 0.12
    done
    pause 0.4
    dim; say_centre "(Finnegans Wake 3.9 — 'is mise', I am; 'tauftauf', to baptise.)"; off
    dim; say_centre "The mesh is not born here. It has always been running. This is a node joining it."; off
    off
    show_cursor
    printf '\n'
}

# ---------------------------------------------------------------- disclosure

disclosure() {
    printf '\n'
    bold; printf '  This seeder will touch exactly these, and nothing else:\n'; off
    printf '    %s\n' "$MISHE_HOME/            the board, the handoff, the organs, the core"
    printf '    %s\n' "$BIN_DIR/mishe        one symlink so the core is on PATH"
    printf '    %s\n' "a tmux session         named after this node"
    printf '\n'
    dim
    printf '  It installs no packages without asking, schedules nothing, needs no sudo\n'
    printf '  of its own accord, and makes no network call beyond the one that fetched it.\n'
    off
    printf '\n'
}

# ---------------------------------------------------------------- asking

ask() {                       # ask "question" "default"
    q="$1"; d="$2"
    if [ "$TTY_IN" != 1 ]; then printf '%s' "$d"; return; fi
    printf '  %s ' "$q" >&2
    [ -n "$d" ] && { dim; printf '[%s] ' "$d" >&2; off; }
    IFS= read -r a < /dev/tty || a=""
    [ -z "$a" ] && a="$d"
    printf '%s' "$a"
}

confirm() {                   # confirm "question"  -> rc 0 = yes
    if [ "$TTY_IN" != 1 ]; then return 1; fi
    printf '  %s [y/N] ' "$1" >&2
    IFS= read -r a < /dev/tty || a=""
    case "$a" in y|Y|yes|YES) return 0 ;; *) return 1 ;; esac
}

# ---------------------------------------------------------------- the core

write_core() {
    mkdir -p "$MISHE_HOME/organs" "$MISHE_HOME/handoff" "$BIN_DIR" || return 1
    : > "$MISHE_HOME/board" 2>/dev/null || true
    cat > "$MISHE_HOME/mishe" <<'__CORE__'
#!/bin/sh
# mishe — the whole core. Five habits, no organs.
#
#   mishe board [line]        read the board, or write one line to it
#   mishe claims              open claims: posted, never settled
#   mishe handoff <text>      write the work-state that survives a /clear
#   mishe restore             print it back
#   mishe organ <name> <cmd>  register a command whose OUTPUT is the data pane
#   mishe dash                the data pane: every organ, refreshed
#   mishe test                does the planting hold?
#
# A claim on the board must settle. [task]/[taking]/[verify] open one; [done]
# closes it. An open claim nobody closed is a promise that never resolved, and
# `mishe claims` is the only reason it cannot age quietly where nobody looks.
set -u
H="${MISHE_HOME:-$HOME/.mishe}"
BOARD="$H/board"; ORGANS="$H/organs"; HAND="$H/handoff"
WHO="${MISHE_WHO:-$(id -un)@$(hostname 2>/dev/null || echo node)}"
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
mkdir -p "$H" "$ORGANS" "$HAND" 2>/dev/null; [ -f "$BOARD" ] || : > "$BOARD"

slug() { printf '%s' "$1" | sed -n 's/^\[[a-z]*\][[:space:]]*\([A-Za-z0-9._-]\{1,\}\).*/\1/p'; }

cmd_board() {
    if [ $# -eq 0 ]; then tail -n 40 "$BOARD"; return 0; fi
    printf '%s  %s  ::  %s\n' "$(now)" "$WHO" "$*" >> "$BOARD"
    tail -n 1 "$BOARD"
}
cmd_claims() {
    open=""
    while IFS= read -r line; do
        case "$line" in
            *"[task]"*|*"[taking]"*|*"[verify]"*) s=$(slug "${line#*:: }"); [ -n "$s" ] && open="$open $s" ;;
            *"[done]"*) s=$(slug "${line#*:: }"); [ -n "$s" ] && open=$(printf '%s' "$open" | tr ' ' '\n' | grep -vx "$s" | tr '\n' ' ') ;;
        esac
    done < "$BOARD"
    set -- $open
    [ $# -eq 0 ] && { echo "no open claims"; return 0; }
    echo "open claims (posted, never settled):"
    for s in "$@"; do printf '  %s\n' "$s"; done
}
cmd_handoff() {
    [ $# -eq 0 ] && { echo "usage: mishe handoff <what was done + what is next + which files>" >&2; return 2; }
    f="$HAND/$(id -un).md"
    { printf '# handoff written %s by %s\n\n' "$(now)" "$WHO"; printf '%s\n' "$*"; } > "$f"
    cmd_board "[handoff] $*" >/dev/null
    echo "$f"
}
cmd_restore() {
    f="$HAND/$(id -un).md"
    [ -f "$f" ] || { echo "(no handoff yet)"; return 0; }
    cat "$f"
}
cmd_organ() {
    [ $# -lt 2 ] && { ls -1 "$ORGANS" 2>/dev/null; return 0; }
    name="$1"; shift
    printf '%s\n' "$*" > "$ORGANS/$name"
    echo "organ '$name' registered: $*"
}
cmd_dash() {
    for o in "$ORGANS"/*; do
        [ -e "$o" ] || { echo "no organs yet — mishe organ <name> '<command>'"; return 0; }
        n=$(basename "$o"); c=$(cat "$o")
        printf '\033[1m== %s\033[0m  \033[2m%s\033[0m\n' "$n" "$c"
        out=$(sh -c "$c" 2>&1)
        if [ -z "$out" ]; then
            # An organ that produces nothing is NOT an organ that is fine. Say so,
            # because a silent pane and a dead pane look identical.
            printf '  \033[2m(no output — this organ produced nothing)\033[0m\n'
        else
            printf '%s\n' "$out" | sed 's/^/  /'
        fi
    done
}
cmd_watch() { while :; do clear; date -u +%H:%M:%SZ; echo; cmd_dash; sleep "${MISHE_REFRESH:-20}"; done; }
cmd_test() {
    rc=0
    for p in "$H" "$ORGANS" "$HAND" "$BOARD"; do
        [ -e "$p" ] || { echo "MISSING $p"; rc=1; }
    done
    t=$(now)
    cmd_board "[task] selftest-$t a claim that must settle" >/dev/null
    cmd_claims | grep -q "selftest-$t" || { echo "FAIL: an open claim did not show as open"; rc=1; }
    cmd_board "[done] selftest-$t settled" >/dev/null
    cmd_claims | grep -q "selftest-$t" && { echo "FAIL: a settled claim still shows as open"; rc=1; }
    cmd_handoff "selftest $t" >/dev/null
    cmd_restore | grep -q "$t" || { echo "FAIL: the handoff did not come back"; rc=1; }
    [ "$rc" = 0 ] && echo "ok — board settles claims, handoff survives, paths exist"
    return $rc
}
c="${1:-board}"; [ $# -gt 0 ] && shift
case "$c" in
    board) cmd_board "$@" ;;   claims) cmd_claims ;;
    handoff) cmd_handoff "$@" ;; restore) cmd_restore ;;
    organ) cmd_organ "$@" ;;   dash) cmd_dash ;;  watch) cmd_watch ;;
    test) cmd_test ;;
    *) echo "mishe: board | claims | handoff | restore | organ | dash | watch | test" >&2; exit 2 ;;
esac
__CORE__
    chmod +x "$MISHE_HOME/mishe"
    ln -sf "$MISHE_HOME/mishe" "$BIN_DIR/mishe"
}

# ---------------------------------------------------------------- agents

find_agent() {
    for a in claude codex opencode; do
        command -v "$a" >/dev/null 2>&1 && { echo "$a"; return 0; }
    done
    return 1
}

# ---------------------------------------------------------------- main

main() {
    birth
    disclosure

    if [ "$TTY_IN" != 1 ]; then
        printf '  '; bold; printf 'Not a terminal.'; off
        printf ' Piping this into sh gives it no way to ask you anything.\n'
        printf '  Run it so it keeps your terminal:\n\n'
        printf '    sh -c "$(curl -fsSL <url>)"\n\n'
        printf '  Nothing was written.\n'
        exit 1
    fi

    NODE=$(ask "What should this node be called?" "$(hostname 2>/dev/null || echo node)")
    printf '\n'

    printf '  planting… '
    write_core || { printf 'failed\n'; exit 1; }
    printf 'done\n'
    "$MISHE_HOME/mishe" board "[fyi] node $NODE planted by the seeder" >/dev/null

    printf '  self-test: '
    if MISHE_HOME="$MISHE_HOME" "$MISHE_HOME/mishe" test; then :; else
        printf '  the planting did not hold — leaving it in place so you can look\n'; exit 1
    fi

    # ---- tmux: the shared surface. Planted in front of you, not behind you.
    if command -v tmux >/dev/null 2>&1; then
        HAVE_TMUX=1
    else
        printf '\n'
        printf '  tmux is not installed. It is the one thing the mesh cannot do without:\n'
        printf '  it is the surface a person looks INTO and interferes with, and the\n'
        printf '  scrollback is the node%s memory.\n' "'s"
        if confirm "Install tmux now? (I will show you the exact command first)"; then
            HAVE_TMUX=0
            for m in "apt-get install -y tmux" "dnf install -y tmux" "pacman -S --noconfirm tmux" "brew install tmux"; do
                mgr=${m%% *}
                command -v "$mgr" >/dev/null 2>&1 || continue
                if [ "$mgr" = brew ]; then cmd="$m"; else cmd="sudo $m"; fi
                printf '\n    %s\n\n' "$cmd"
                if confirm "Run that?"; then sh -c "$cmd" && HAVE_TMUX=1; fi
                break
            done
        else
            HAVE_TMUX=0
        fi
    fi

    AGENT=$(find_agent) || AGENT=""
    if [ -z "$AGENT" ]; then
        printf '\n  No agent found on PATH (looked for claude, codex, opencode).\n'
        printf '  The node is planted and usable by hand; add an agent later and re-run\n'
        printf '  the last step with:  mishe organ mind %s\n' "'<your agent command>'"
    fi

    # ---- the first organ, so the data pane is never empty on arrival
    "$MISHE_HOME/mishe" organ node "uptime; echo; df -h \"\$HOME\" | tail -1" >/dev/null

    printf '\n'
    bold; say_centre "planted"; off
    printf '\n'
    printf '  %s\n' "$MISHE_HOME"
    ls -1 "$MISHE_HOME" | sed 's/^/    /'
    printf '\n'

    # ---- and the seeder dies, in front of you
    printf '  '; dim; printf 'the seeder is single-use. deleting it:'; off; printf '\n'
    if [ -f "$SELF" ] && [ "$SELF" != "sh" ] && [ "$SELF" != "-" ]; then
        printf '    rm %s\n' "$SELF"
        rm -f "$SELF" 2>/dev/null
        if [ -f "$SELF" ]; then printf '    (could not — delete it yourself)\n'
        else printf '    gone: %s\n' "$(ls "$SELF" 2>&1)"; fi
    else
        printf '    it was never on disk — it ran from the pipe and is gone with the shell\n'
    fi
    printf '\n'
    say_centre "( x.x )"
    dim; say_centre "mishustik is dead. the node is $NODE."; off
    printf '\n'

    if [ "${HAVE_TMUX:-0}" = 1 ]; then
        printf '  Opening the node. Top pane is what it sees, bottom is where you and it think.\n'
        printf '  Detach with ctrl-b d; come back with:  tmux attach -t %s\n\n' "$NODE"
        pause 1.5
        tmux new-session -d -s "$NODE" 2>/dev/null
        tmux send-keys -t "$NODE" "MISHE_HOME='$MISHE_HOME' '$MISHE_HOME/mishe' watch" C-m 2>/dev/null
        tmux split-window -v -t "$NODE" 2>/dev/null
        tmux resize-pane -t "$NODE".0 -y 12 2>/dev/null
        if [ -n "$AGENT" ]; then
            tmux send-keys -t "$NODE" "$AGENT" C-m 2>/dev/null
        fi
        exec tmux attach -t "$NODE"
    else
        printf '  No tmux, so no shared surface yet. Everything else is planted:\n'
        printf '    mishe board "[task] the first thing I want"\n'
        printf '    mishe claims\n'
        printf '    mishe dash\n'
    fi
}

main "$@"
