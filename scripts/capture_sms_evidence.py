#!/usr/bin/env python3
"""Capture the SMS opt-in screenshots shown on /sms-opt-in/ from the built site.

  python3 build.py && python3 scripts/capture_sms_evidence.py && python3 build.py

Writes static/sms-evidence/<key>-<lang>.webp. Re-run whenever the text
buttons, disclosures, or request form change, so the evidence stays accurate.
"""
import functools
import http.server
import io
import os
import socketserver
import threading

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
OUT = os.path.join(ROOT, "static", "sms-evidence")
PATHS = {"en": {"home": "/", "sms": "/sms/", "contact": "/contact/"},
         "es": {"home": "/es/", "sms": "/es/mensajes-de-texto/", "contact": "/es/contacto/"}}


def save(png, name, max_width=1100):
    im = Image.open(io.BytesIO(png)).convert("RGB")
    if im.width > max_width:
        im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, name), "WEBP", quality=82, method=6)
    print("wrote", name, im.size)


def main():
    os.makedirs(OUT, exist_ok=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(Quiet, directory=DIST)
    srv = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    chrome = os.environ.get("CHROME_PATH", "/usr/bin/google-chrome")
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=chrome if os.path.exists(chrome) else None, args=["--no-sandbox"])
        for lang, P in PATHS.items():
            desk = b.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=2)
            pg = desk.new_page()
            pg.goto(base + P["home"], wait_until="networkidle")
            save(pg.locator(".hero-badge").screenshot(), f"home-text-cta-{lang}.webp", 900)
            pg.goto(base + P["sms"], wait_until="networkidle")
            save(pg.locator(".consent-box").screenshot(), f"sms-consent-box-{lang}.webp")
            pg.goto(base + P["contact"], wait_until="networkidle")
            box = pg.locator(".consent").bounding_box()
            act = pg.locator("#request-form .actions").bounding_box()
            pad = 16
            clip = {"x": box["x"] - pad, "y": box["y"] - pad, "width": box["width"] + 2 * pad,
                    "height": act["y"] + act["height"] - box["y"] + 2 * pad}
            save(pg.screenshot(clip=clip, full_page=True), f"form-consent-{lang}.webp")
            desk.close()
            phone = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
            pg = phone.new_page()
            pg.goto(base + P["sms"], wait_until="networkidle")
            save(pg.screenshot(), f"sms-phone-{lang}.webp", 600)
            phone.close()
        b.close()
    srv.shutdown()


if __name__ == "__main__":
    main()
