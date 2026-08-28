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
  mouse X Y · frames · fclick IDX SEL · dismiss · upload SEL PATH · settext SEL PATH
  fillenv SEL KEY (value from env or ~/.mesh/job/.creds.env — never logged) · quit

`dismiss` closes hh's profile-completion modal, which silently swallows clicks on the page beneath
it — the single most common reason a hh flow appears to hang while every command reports success.

`upload` is what makes this driver usable for ATS forms (Greenhouse/Ashby/Lever), where the resume
is a file input rather than a text field — a drag-drop widget still carries a real <input type=file>
underneath, so the selector to hand it is that input, not the visible dropzone.

HH_PROFILE names the instance: a second driver (say the webmail one) gets its own state, command
file, log and shots so its cookies never land in hh's session. Default profile = `hh`.
"""
import json, os, pathlib, shlex, sys, time

MESH = pathlib.Path(os.path.expanduser("~/.mesh"))
PROFILE = os.environ.get("HH_PROFILE", "hh")
STATE = pathlib.Path(os.environ.get("HH_STATE", MESH / f"browser/{PROFILE}-state.json"))
CMD = pathlib.Path(os.environ.get("HH_CMD", MESH / f"job/{PROFILE}-cmd.txt"))
LOG = pathlib.Path(os.environ.get("HH_LOG", MESH / f"job/{PROFILE}-drive.log"))
SHOTS = MESH / "job/shots"
HOME_URL = os.environ.get("HH_HOME", "https://hh.ru/")
IDLE_LIMIT = int(os.environ.get("HH_IDLE_LIMIT", 45 * 60))
# THE IDLE PAGE IS NOT A FREE PAGE. This daemon exists so the login page stays warm, but the page
# it stays warm ON is whatever the last command left it on — and hh's SPAs (negotiations, the chat
# list) keep animating forever. Measured 2026-08-21 (health@): the renderer held ~0.7 of a core
# CONTINUOUSLY between commands, 14.6 CPU-hours over 20h16m, uncorrelated with the drive's output.
# So park on about:blank once the command file has been quiet, and re-goto the parked URL when the
# next command arrives: the cold-load cost this daemon avoids is the BROWSER LAUNCH, not a goto.
# HH_PARK_AFTER=0 disables parking. Note what parking COSTS — a re-goto restores the URL, never the
# page's in-memory state — so it must be long enough that no flow can straddle it (steps in
# mesh-job-apply land seconds apart), and both edges are logged so a lost half-filled form is
# readable in the log rather than a mystery.
PARK_AFTER = int(os.environ.get("HH_PARK_AFTER", 180))
PARK_URL = "about:blank"

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
    +' :: '+((e.type==='password'||/pass|pwd/i.test(e.name||e.id||''))
        ? '<'+(e.value||'').length+' chars hidden>'
        : (e.innerText||e.value||'').trim().slice(0,45).replace(/\\n/g,' '))})
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
        # HH_HEADLESS=0 launches the FULL chromium instead of chrome-headless-shell, which needs a
        # display — the bash wrapper supplies one via xvfb-run. This is not a cosmetic knob: an ATS
        # anti-spam gate reads the browser, not the IP. Measured 2026-08-16 on Ashby, five attempts:
        # fal and Braintrust answered "flagged as possible spam" from BOTH this node's exits (privoxy
        # 38.49.216.141 and the direct 77.246.104.228, each confirmed inside the browser via ipify,
        # not in a shell), while Prime Intellect had accepted an identical submission through the
        # first of those exits 25 minutes earlier. Same IP, opposite verdicts — so the IP was never
        # the variable, and the page's own advice ("turn off your VPN or proxy") points at the wrong
        # thing. What differs is the fingerprint: headless-shell is the most detectable chromium
        # build there is, and these forms carry an empty g-recaptcha-response.
        # HH_PROXY routes this browser out a vantage the node's default route does not have.
        # Needed since 2026-08-20: hh.ru blackholed the tailscale exit node's IP (TCP 443 to
        # 94.124.200.0 never answers from 38.49.216.141, measured from this node AND from the
        # exit node itself), while the node's own uplink gets 302 -> nn.hh.ru, 200. chromium
        # cannot bind an interface, so the vantage arrives as a socks proxy
        # (`mesh-vantage-socks`, whose sockets are SO_BINDTODEVICE-bound to that uplink).
        launch = {"headless": os.environ.get("HH_HEADLESS", "1") != "0"}
        if os.environ.get("HH_PROXY"):
            launch["proxy"] = {"server": os.environ["HH_PROXY"]}
        b = p.chromium.launch(**launch)
        ctx = b.new_context(storage_state=str(STATE), locale="ru-RU",
                            timezone_id="Europe/Moscow",
                            user_agent=("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"))
        pg = ctx.new_page()
        pg.goto(HOME_URL, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(4000)
        out("[ready]")
        dump(pg)

        seen, last = 0, time.time()
        parked = None
        park_skipped = False
        while time.time() - last < IDLE_LIMIT:
            lines = CMD.read_text(encoding="utf-8").splitlines()
            if len(lines) <= seen:
                if (PARK_AFTER and parked is None and time.time() - last > PARK_AFTER
                        and pg.url != PARK_URL):
                    want = pg.url
                    # NEVER PARK A URL WE CANNOT NAVIGATE BACK TO. A failed goto leaves the page on
                    # chrome-error://chromewebdata/, and Page.goto of a chrome-error URL is
                    # unconditionally ERR_ABORTED — so parking one converts a transient blip into a
                    # driver that refuses every later verb. The gate is an ALLOWLIST of the schemes
                    # this driver legitimately sits on: an unlisted scheme costs the CPU the parker
                    # exists to save, and says so, which is the loud direction. The other direction
                    # (park it, wedge, and name the wrong subject) is the failure this replaced.
                    if not want.startswith(("http://", "https://", "file://")):
                        if not park_skipped:
                            out("[park-SKIP]", want, "(not a URL we could un-park to)")
                            park_skipped = True
                        time.sleep(2)
                        continue
                    try:
                        pg.goto(PARK_URL, wait_until="domcontentloaded", timeout=15000)
                        parked = want
                        park_skipped = False
                        out("[park]", want)
                    except Exception as e:
                        # A park that fails must not be remembered as done: the page is still on
                        # the live URL, so the next command must NOT re-goto anything.
                        out("[park-FAIL]", type(e).__name__, str(e)[:200])
                time.sleep(2)
                continue
            for step in lines[seen:]:
                seen += 1
                step = step.strip()
                if not step:
                    continue
                last = time.time()
                park_skipped = False   # a new episode must re-announce; a latched flag goes quiet
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
                    if parked is not None:
                        # goto replaces the destination anyway and quit is leaving; everything else
                        # assumes the page it was left on, so restore it first.
                        if verb not in ("goto", "quit"):
                            try:
                                pg.goto(parked, wait_until="domcontentloaded", timeout=60000)
                                pg.wait_for_timeout(3500)
                                out("[unpark]", parked)
                            except Exception as e:
                                # An un-park that fails must be spent, not RETRIED FOREVER. Left
                                # set, `parked` makes every later shot/js/click re-attempt the same
                                # dead navigation, so one bad URL wedges the driver until some lane
                                # happens to send a `goto` (the one verb that skips this branch) —
                                # and each failure names the verb, never the parked URL that is
                                # actually refusing. Clearing it costs the page position, which the
                                # caller can restore; keeping it costs every command after.
                                out("[unpark-FAIL]", parked, type(e).__name__, str(e)[:160])
                                # The failed navigation leaves the page mid-flight on an error
                                # document, so the verb that triggered this un-park dies with
                                # "Execution context was destroyed" — a message about a race, not
                                # about the dead URL named on the line above. Land on about:blank
                                # so that verb runs against a live context and anything it reports
                                # after this is its own failure.
                                try:
                                    pg.goto(PARK_URL, wait_until="domcontentloaded", timeout=15000)
                                except Exception:
                                    pass
                        parked = None
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
                    elif verb == "fillenv":
                        # A password must never reach the command file, the log, or a pane. The
                        # caller names a KEY; the value is looked up in the environment, then in
                        # ~/.mesh/job/.creds.env, and only its LENGTH is ever printed.
                        val = os.environ.get(rest[1])
                        if val is None:
                            cf = MESH / "job/.creds.env"
                            if cf.exists():
                                for ln in cf.read_text(encoding="utf-8").splitlines():
                                    ln = ln.strip()
                                    if ln.startswith("#") or "=" not in ln:
                                        continue
                                    k, v = ln.split("=", 1)
                                    if k.strip() == rest[1]:
                                        val = v.strip().strip('"').strip("'")
                                        break
                        if not val:
                            out("[FAIL] fillenv: no value for", rest[1])
                        else:
                            pg.fill(rest[0], val, timeout=20000)
                            pg.wait_for_timeout(800)
                            out("[fillenv]", rest[1], f"({len(val)} chars) ->", rest[0])
                    elif verb == "settext":
                        # A cover letter is multi-line and the command file is line-based, so the
                        # text comes from a FILE — the same file that gets archived as the audit
                        # copy of what was sent, which is why this reads it rather than taking it
                        # inline: one artifact, no chance of the archive and the form diverging.
                        pth = pathlib.Path(os.path.expanduser(" ".join(rest[1:])))
                        if not pth.is_file() or pth.stat().st_size == 0:
                            out("[FAIL] settext: no such file (or empty):", pth)
                        else:
                            body = pth.read_text(encoding="utf-8")
                            pg.fill(rest[0], body, timeout=20000)
                            pg.wait_for_timeout(1200)
                            out("[settext]", pth, len(body), "chars ->", rest[0])
                    elif verb == "upload":
                        # Assert the file EXISTS before handing it over: playwright accepts a
                        # missing path against some inputs and the form then submits with no
                        # resume, which reads downstream as a successful application.
                        pth = pathlib.Path(os.path.expanduser(" ".join(rest[1:])))
                        if not pth.is_file() or pth.stat().st_size == 0:
                            out("[FAIL] upload: no such file (or empty):", pth)
                        else:
                            pg.set_input_files(rest[0], str(pth), timeout=20000)
                            pg.wait_for_timeout(2500)
                            out("[upload]", pth, pth.stat().st_size, "bytes ->", rest[0])
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
