#!/usr/bin/env python3
# orphan-ok: engine behind mesh-hh-drive; never invoked directly, the bash wrapper picks the venv
"""Persistent hh.ru browser driver — one long-lived logged-in page, commands fed through a file.

Why a daemon and not one call per step: hh's flows are many screens deep and every fresh browser
launch pays a 30-40s cold load, so each selector guess would cost minutes. One page stays alive and
answers in a second. The login lives in a storage-state file, so the daemon can die and come back
without re-authenticating.

Invoked by the `mesh-hh-drive` wrapper, which locates the playwright venv. Not run by hand.

Verbs (one per line in the command file):
  goto URL · dump · text SEL · js EXPR · shot NAME · wait MS
  click SEL · clicknth SEL N · clickbtn NAME · clicktext TEXT
  fill SEL TEXT · type SEL TEXT · press KEY · check SEL · select SEL VAL
  mouse X Y · frames · fclick IDX SEL · dismiss · quit

`dismiss` closes hh's profile-completion modal, which silently swallows clicks on the page beneath
it — the single most common reason a hh flow appears to hang while every command reports success.
"""
import json, os, pathlib, shlex, sys, time

MESH = pathlib.Path(os.path.expanduser("~/.mesh"))
STATE = MESH / "browser/hh-state.json"
CMD = MESH / "job/hh-cmd.txt"
LOG = MESH / "job/hh-drive.log"
SHOTS = MESH / "job/shots"
IDLE_LIMIT = int(os.environ.get("HH_IDLE_LIMIT", 45 * 60))

# Verbs whose argument is free text, not a shell-ish selector list. `js`/`text` take the whole
# remainder; `type`/`fill` take "<selector> <text…>" and must not lose the text's punctuation.
RAW_TAIL = {"js", "text", "type", "fill"}

for d in (STATE.parent, CMD.parent, SHOTS):
    d.mkdir(parents=True, exist_ok=True)


def out(*a):
    line = " ".join(str(x) for x in a)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


CONTROLS_JS = """Array.from(document.querySelectorAll('input,button,select,textarea,a[data-qa],[role=button],[role=option],label'))
  .filter(function(e){var r=e.getBoundingClientRect();return r.width>0&&r.height>0})
  .slice(0,80)
  .map(function(e){return e.tagName+'['+(e.type||'')+']'
    +(e.name?' name='+e.name:'')
    +(e.getAttribute('data-qa')?' qa='+e.getAttribute('data-qa'):'')
    +(e.placeholder?' ph='+e.placeholder:'')
    +' :: '+((e.innerText||e.value||'').trim().slice(0,45).replace(/\\n/g,' '))})
  .join('\\n')"""

# hh's "какой формат удобнее / расскажите о себе" wizard renders over the page and eats every click
# beneath it. Closing it is a no-op when it is absent, so it is safe to fire before any interaction.
DISMISS_JS = """(function(){
  var n=0;
  document.querySelectorAll('[data-qa*=close], button[aria-label*=акры], button[aria-label*=lose]')
    .forEach(function(b){var r=b.getBoundingClientRect(); if(r.width>0&&r.height>0){b.click();n++}});
  return n;
})()"""


def dump(pg):
    out("[url]", pg.url)
    try:
        out("[controls]\n" + pg.evaluate(CONTROLS_JS))
    except Exception as e:
        out("[controls] FAIL", type(e).__name__, str(e)[:120])


def run():
    from playwright.sync_api import sync_playwright

    if not STATE.exists():
        STATE.write_text('{"cookies":[],"origins":[]}', encoding="utf-8")
    CMD.write_text("", encoding="utf-8")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(storage_state=str(STATE), locale="ru-RU",
                            timezone_id="Europe/Moscow",
                            user_agent=("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"))
        pg = ctx.new_page()
        pg.goto("https://hh.ru/", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(4000)
        out("[ready]")
        dump(pg)

        seen, last = 0, time.time()
        while time.time() - last < IDLE_LIMIT:
            lines = CMD.read_text(encoding="utf-8").splitlines()
            if len(lines) <= seen:
                time.sleep(2)
                continue
            for step in lines[seen:]:
                seen += 1
                step = step.strip()
                if not step:
                    continue
                last = time.time()
                out(f"\n>>> {step}")
                try:
                    # shlex eats quotes and apostrophes, which is right for `click a.b` and fatal
                    # for `js ...'selector'...` or a letter containing wrapper'ов. Verbs whose
                    # payload is free text take the raw remainder; only selector verbs get shlex.
                    head = step.split(None, 1)
                    verb = head[0]
                    raw = head[1] if len(head) > 1 else ""
                    if verb in RAW_TAIL:
                        rest = ([raw] if raw else []) if verb in ("js", "text") else raw.split(None, 1)
                    else:
                        parts = shlex.split(step)
                        verb, rest = parts[0], parts[1:]
                    if verb == "quit":
                        ctx.storage_state(path=str(STATE))
                        b.close()
                        out("[quit]")
                        return 0
                    elif verb == "dump":
                        dump(pg)
                    elif verb == "goto":
                        pg.goto(rest[0], wait_until="domcontentloaded", timeout=60000)
                        pg.wait_for_timeout(3500)
                        out("[url]", pg.url)
                    elif verb == "dismiss":
                        out("[dismiss] closed", pg.evaluate(DISMISS_JS))
                        pg.wait_for_timeout(1200)
                    elif verb == "js":
                        r = pg.evaluate(" ".join(rest))
                        out("[js]", json.dumps(r, ensure_ascii=False) if not isinstance(r, str) else r)
                    elif verb == "click":
                        pg.click(rest[0], timeout=15000)
                        pg.wait_for_timeout(2500)
                    elif verb == "clickbtn":
                        pg.get_by_role("button", name=" ".join(rest)).first.click(timeout=15000)
                        pg.wait_for_timeout(2500)
                    elif verb == "clicktext":
                        pg.get_by_text(" ".join(rest), exact=False).first.click(timeout=15000)
                        pg.wait_for_timeout(2500)
                    elif verb == "clicknth":
                        pg.locator(rest[0]).nth(int(rest[1])).click(timeout=15000)
                        pg.wait_for_timeout(2500)
                    elif verb == "fill":
                        pg.fill(rest[0], " ".join(rest[1:]), timeout=15000)
                        pg.wait_for_timeout(1000)
                    elif verb == "type":
                        pg.type(rest[0], " ".join(rest[1:]), delay=45, timeout=20000)
                        pg.wait_for_timeout(1200)
                    elif verb == "press":
                        (pg.press(rest[0], rest[1], timeout=15000) if len(rest) > 1
                         else pg.keyboard.press(rest[0]))
                        pg.wait_for_timeout(1200)
                    elif verb == "check":
                        pg.check(rest[0], timeout=15000)
                    elif verb == "select":
                        pg.select_option(rest[0], rest[1], timeout=15000)
                    elif verb == "mouse":
                        pg.mouse.move(int(rest[0]), int(rest[1]))
                        pg.wait_for_timeout(250)
                        pg.mouse.click(int(rest[0]), int(rest[1]))
                        pg.wait_for_timeout(2500)
                    elif verb == "frames":
                        out("[frames] " + "\n".join(f"{i}: {fr.url[:120]}"
                                                   for i, fr in enumerate(pg.frames)))
                    elif verb == "fclick":
                        pg.frames[int(rest[0])].click(" ".join(rest[1:]), timeout=15000)
                        pg.wait_for_timeout(2500)
                    elif verb == "wait":
                        pg.wait_for_timeout(int(rest[0]))
                    elif verb == "text":
                        out("[text]", pg.inner_text(rest[0] if rest else "body")[:4000])
                    elif verb == "shot":
                        pth = SHOTS / f"{rest[0]}.png"
                        pg.screenshot(path=str(pth), full_page=False)
                        out("[shot]", pth)
                    else:
                        out("[?] unknown verb", verb)
                except Exception as e:
                    out("[FAIL]", type(e).__name__, str(e)[:300])
                try:
                    ctx.storage_state(path=str(STATE))
                    os.chmod(STATE, 0o600)
                except Exception:
                    pass
        out("[idle-exit]")
        ctx.storage_state(path=str(STATE))
        b.close()
    return 0


if __name__ == "__main__":
    sys.exit(run())
