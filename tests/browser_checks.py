"""Browser smoke tests in Chrome: every page (EN + ES) at phone + desktop width under production headers,
plus menu, language switch/setting/persistence, Spanish-browser suggestion, and the request form."""
import http.server, os, re, socketserver, sys, threading, urllib.parse
from playwright.sync_api import sync_playwright

DIST = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))
SHOTS = os.environ.get("SHOTS", "/tmp/shots"); os.makedirs(SHOTS, exist_ok=True)
TEXT = "+18067764460"

HEADERS, cur = {}, None
for line in open(os.path.join(DIST, "_headers")):
    if line.strip() and not line.startswith(" "):
        cur = line.strip(); HEADERS[cur] = {}
    elif line.strip() and cur:
        k, v = line.strip().split(":", 1); HEADERS[cur][k.strip()] = v.strip()


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=DIST, **k)
    def log_message(s, *a): pass
    def end_headers(s):
        for k, v in HEADERS.get("/*", {}).items(): s.send_header(k, v)
        super().end_headers()
    def send_error(s, code, *a, **k):
        if code == 404:  # mimic Cloudflare Pages: nearest 404.html
            nf = "es/404.html" if s.path.startswith("/es/") else "404.html"
            body = open(os.path.join(DIST, nf), "rb").read()
            s.send_response(404); s.send_header("Content-Type", "text/html; charset=utf-8"); s.end_headers(); s.wfile.write(body)
        else:
            super().send_error(code, *a, **k)


srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{port}"

paths = sorted("/" + os.path.relpath(r, DIST).replace("\\", "/").strip(".").strip("/") + "/"
               for r, _, f in os.walk(DIST) if "index.html" in f)
paths = [p.replace("//", "/") for p in paths]

fails = []
def check(cond, msg):
    if not cond: fails.append(msg)

with sync_playwright() as pw:
    chrome = os.environ.get("CHROME_PATH", "/usr/bin/google-chrome")
    browser = pw.chromium.launch(executable_path=chrome if os.path.exists(chrome) else None, args=["--no-sandbox"])

    # ---- every page, both viewports
    for vw, vh, label in [(360, 740, "phone-small"), (390, 844, "phone"), (1280, 900, "desktop")]:
        ctx = browser.new_context(viewport={"width": vw, "height": vh}, locale="en-US")
        page = ctx.new_page(); errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        for p in paths:
            errors.clear()
            r = page.goto(BASE + p, wait_until="networkidle")
            check(r.status == 200, f"[{label}] {p}: HTTP {r.status}")
            check(page.url == BASE + p, f"[{label}] {p}: unexpectedly redirected to {page.url}")
            check(not errors, f"[{label}] {p}: console errors {errors}")
            ov = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(ov <= 0, f"[{label}] {p}: horizontal overflow {ov}px")
            check(page.evaluate("document.fonts.check('16px Anton') && document.fonts.check('16px Barlow')"), f"[{label}] {p}: fonts not loaded")
            phone = label.startswith("phone")
            check(page.is_visible(".mobile-cta") == phone, f"[{label}] {p}: mobile call bar visibility")
            check(page.is_visible(".lang-switch"), f"[{label}] {p}: language switch not visible")
            small = page.evaluate("[...document.querySelectorAll('.btn,.mobile-cta a,.lang-switch,.nav-toggle')].filter(e=>e.offsetParent&&e.getBoundingClientRect().height<44).length")
            check(not small, f"[{label}] {p}: {small} tap targets under 44px")
            # header must not wrap/overlap: brand, switch and toggle on one row
            if phone:
                rows = page.evaluate("""(()=>{const b=document.querySelector('.site-header .brand').getBoundingClientRect(),
                    t=document.querySelector('.header-tools').getBoundingClientRect(); return [b.top,t.top,b.right,t.left]})()""")
                check(rows[3] >= rows[2] - 1, f"[{label}] {p}: header brand overlaps language/menu controls {rows}")
        if label != "phone-small":
            for name, p in [("home", "/"), ("es-home", "/es/"), ("es-contact", "/es/contacto/"), ("es-terms", "/es/terminos/"), ("es-privacy", "/es/privacidad/")]:
                page.goto(BASE + p, wait_until="networkidle")
                page.screenshot(path=f"{SHOTS}/{name}-{label}.png", full_page=False)
        ctx.close()

    # ---- menu labels in both languages (phone)
    for lang_path, open_lbl, close_lbl in [("/", "Menu", "Close"), ("/es/", "Menú", "Cerrar")]:
        ctx = browser.new_context(viewport={"width": 390, "height": 844}); page = ctx.new_page()
        page.goto(BASE + lang_path, wait_until="networkidle")
        check(page.text_content(".nav-toggle").strip() == open_lbl, f"{lang_path}: toggle label {page.inner_text('.nav-toggle')!r}")
        page.click(".nav-toggle")
        check(page.is_visible("#site-nav"), f"{lang_path}: menu did not open")
        check(page.text_content(".nav-toggle").strip() == close_lbl, f"{lang_path}: close label wrong")
        if lang_path == "/es/": page.screenshot(path=f"{SHOTS}/es-menu-open-phone.png")
        page.keyboard.press("Escape")
        check(not page.is_visible("#site-nav"), f"{lang_path}: Escape did not close menu")
        ctx.close()

    # ---- language switch, persistence, and setting
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, locale="en-US"); page = ctx.new_page()
    page.goto(BASE + "/services/brake-repair/", wait_until="networkidle")
    check(page.locator(".lang-suggest").count() == 0, "suggestion bar shown to English browser")
    page.click(".lang-switch"); page.wait_for_load_state("networkidle")
    check(page.url == BASE + "/es/servicios/reparacion-de-frenos/", f"switch went to {page.url}")
    check(page.evaluate("localStorage.getItem('ras-lang')") == "es", "switch did not save Spanish preference")
    # preference remembered: English URLs now open Spanish
    page.goto(BASE + "/contact/", wait_until="networkidle")
    check(page.url == BASE + "/es/contacto/", f"saved Spanish pref did not redirect /contact/ (got {page.url})")
    page.goto(BASE + "/", wait_until="networkidle")
    check(page.url == BASE + "/es/", f"saved Spanish pref did not redirect home (got {page.url})")
    # footer setting back to English
    page.goto(BASE + "/es/terminos/", wait_until="networkidle")
    page.select_option("#lang-select", "en"); page.wait_for_load_state("networkidle"); page.wait_for_timeout(300)
    check(page.url == BASE + "/terms/", f"setting to English went to {page.url}")
    check(page.evaluate("localStorage.getItem('ras-lang')") == "en", "setting did not save English")
    page.goto(BASE + "/es/privacidad/", wait_until="networkidle")
    check(page.url == BASE + "/privacy/", f"saved English pref did not redirect Spanish page (got {page.url})")
    # switch link back to Spanish overrides the English pref
    page.click(".lang-switch"); page.wait_for_load_state("networkidle")
    check(page.url == BASE + "/es/privacidad/", f"switch back to Spanish went to {page.url}")
    check(page.evaluate("document.documentElement.lang") == "es-US", "Spanish page lang attr")
    ctx.close()

    # ---- Spanish-language browser, no saved choice: suggestion bar, never auto-redirect
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, locale="es-MX"); page = ctx.new_page()
    page.goto(BASE + "/services/", wait_until="networkidle")
    check(page.url == BASE + "/services/", "Spanish browser was auto-redirected (should only be offered)")
    check(page.is_visible(".lang-suggest"), "suggestion bar not shown to Spanish browser")
    page.screenshot(path=f"{SHOTS}/suggest-bar-phone.png")
    page.click(".lang-suggest .lang-dismiss")
    check(not page.is_visible(".lang-suggest"), "Keep English did not dismiss bar")
    page.reload(wait_until="networkidle")
    check(page.locator(".lang-suggest").count() == 0, "bar came back after Keep English")
    page.evaluate("localStorage.clear()"); page.reload(wait_until="networkidle")
    page.click(".lang-suggest a"); page.wait_for_load_state("networkidle")
    check(page.url == BASE + "/es/servicios/", f"suggest link went to {page.url}")
    ctx.close()

    # ---- request form in both languages: validation, copy, and SMS target
    for path, label_name, missing_word, lang_line in [("/contact/", "Name: ", "your name", None),
                                                      ("/es/contacto/", "Nombre: ", "su nombre", "Idioma preferido: Español")]:
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, permissions=["clipboard-read", "clipboard-write"])
        page = ctx.new_page(); seen = []
        page.on("request", lambda r: seen.append(r.url)); page.on("framenavigated", lambda f: seen.append(f.url))
        page.goto(BASE + path, wait_until="networkidle")
        page.click("button[type=submit]")
        check(missing_word in page.inner_text(".error"), f"{path}: empty-form message {page.inner_text('.error')!r}")
        page.fill("#f-name", "Test Customer"); page.fill("#f-phone", "806-555")
        page.click("button[type=submit]")
        check("10" in page.inner_text(".error"), f"{path}: short phone not rejected")
        page.fill("#f-phone", "(806) 555-0123"); page.fill("#f-vehicle", "2016 Chevy Silverado")
        page.select_option("#f-service", index=2); page.fill("#f-location", "82nd & Slide")
        page.fill("#f-details", "Grinding when stopping & pulls left")
        page.click("#copy-request")
        clip = page.evaluate("navigator.clipboard.readText()")
        check(label_name + "Test Customer" in clip and "82nd & Slide" in clip, f"{path}: copied text wrong {clip!r}")
        if lang_line: check(lang_line in clip, f"{path}: Spanish preference line missing")
        check("776-4460" in page.inner_text(".error"), f"{path}: copy confirmation should name the text line")
        page.evaluate("document.getElementById('request-form').requestSubmit()"); page.wait_for_timeout(500)
        m = re.search(r"sms:(\+\d+)\?&body=(\S+)", " ".join(seen))
        if not m: fails.append(f"{path}: submit did not open an sms: link")
        else:
            check(m.group(1) == TEXT, f"{path}: form texts {m.group(1)}, expected {TEXT}")
            body = urllib.parse.unquote(m.group(2))
            check("2016 Chevy Silverado" in body and "Grinding when stopping & pulls left" in body, f"{path}: sms body {body!r}")
            check("Text consent" not in body and "Consentimiento para mensajes" not in body, f"{path}: consent line sent without the box checked: {body!r}")
        # The optional consent box: unchecked by default, and checking it adds the consent line.
        check(not page.is_checked("#f-sms-consent"), f"{path}: consent box starts checked")
        check(page.get_attribute("#f-sms-consent", "required") is None, f"{path}: consent box must not be required")
        # Center it first: on phones the fixed Call/Text bar covers the bottom of the screen.
        page.evaluate("document.getElementById('f-sms-consent').scrollIntoView({block: 'center'})")
        page.check("#f-sms-consent"); seen.clear()
        page.evaluate("document.getElementById('request-form').requestSubmit()"); page.wait_for_timeout(500)
        m = re.search(r"sms:(\+\d+)\?&body=(\S+)", " ".join(seen))
        consent_word = "Consentimiento para mensajes: Sí" if lang_line else "Text consent: Yes"
        check(bool(m) and consent_word in urllib.parse.unquote(m.group(2)), f"{path}: checked box did not add the consent line")
        ctx.close()

    # ---- 404s
    ctx = browser.new_context(); page = ctx.new_page()
    r = page.goto(BASE + "/no-such-page/"); check(r.status == 404 and "This Page Broke Down" in page.content(), "English 404")
    r = page.goto(BASE + "/es/no-existe/"); check(r.status == 404 and "Esta página se descompuso" in page.content(), "Spanish 404")
    ctx.close()
    browser.close()

srv.shutdown()
print(f"Browser-tested {len(paths)} pages x 3 viewports + language, menu, form, and 404 flows")
if fails:
    print("FAIL"); [print(" -", f) for f in fails]; sys.exit(1)
print("PASS: browser checks")
