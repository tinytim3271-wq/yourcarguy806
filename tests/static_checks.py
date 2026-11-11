"""Static smoke tests: links, phone targets, SEO tags, hreflang, structured data, sitemap."""
import json, os, sys
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

DIST = os.path.join(os.path.dirname(__file__), "..", "dist")
SITE = "https://www.yourcarguy806.com"
CALL, TEXT = "+18064513520", "+18067764460"
fails = []


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links = []; s.ids = set(); s.h1 = 0; s.title = ""; s.meta = {}; s.canon = None
        s.ld = []; s._in_ld = False; s._in_title = False; s.srcs = []; s.alts = {}; s.lang = None
        s.switch = None; s.form_sms = None; s.select = None
    def handle_starttag(s, t, a):
        a = dict(a)
        if t == "html": s.lang = a.get("lang"); s.dlang = a.get("data-lang")
        if "id" in a: s.ids.add(a["id"])
        if t == "a" and "href" in a: s.links.append(a["href"])
        if t == "a" and "data-set-lang" in a: s.switch = (a["data-set-lang"], a["href"])
        if t == "form" and a.get("id") == "request-form": s.form_sms = a.get("data-sms")
        if t == "select" and a.get("id") == "lang-select": s.select = a
        if t in ("link", "script") and (a.get("href") or a.get("src")) and a.get("rel") not in ("canonical", "alternate"):
            s.srcs.append(a.get("href") or a.get("src"))
        if t == "link" and a.get("rel") == "alternate": s.alts[a["hreflang"]] = a["href"]
        if t == "h1": s.h1 += 1
        if t == "title": s._in_title = True
        if t == "meta": s.meta[a.get("name") or a.get("property")] = a.get("content")
        if t == "link" and a.get("rel") == "canonical": s.canon = a["href"]
        if t == "script" and a.get("type") == "application/ld+json": s._in_ld = True; s.ld.append("")
    def handle_endtag(s, t):
        if t == "title": s._in_title = False
        if t == "script": s._in_ld = False
    def handle_data(s, d):
        if s._in_title: s.title += d
        if s._in_ld: s.ld[-1] += d


pages, raw = {}, {}
for root, _, files in os.walk(DIST):
    for f in files:
        if f.endswith(".html"):
            full = os.path.join(root, f)
            rel = "/" + os.path.relpath(full, DIST).replace("\\", "/")
            url = rel[:-len("index.html")] if rel.endswith("index.html") else rel
            raw[url] = open(full, encoding="utf-8").read()
            p = P(); p.feed(raw[url]); pages[url] = p

def exists(path):
    path = path.split("#")[0].split("?")[0]
    f = os.path.join(DIST, path.lstrip("/"))
    return os.path.isfile(f) or os.path.isfile(os.path.join(f, "index.html"))

titles, descs = {}, {}
n_tel = n_sms = 0
for url, p in pages.items():
    for href in p.links + p.srcs:
        if href.startswith("tel:"):
            n_tel += 1
            if href != "tel:" + CALL: fails.append(f"{url}: tel link to wrong number {href}")
            continue
        if href.startswith("sms:"):
            n_sms += 1
            if href != "sms:" + TEXT: fails.append(f"{url}: sms link to wrong number {href}")
            continue
        if href.startswith(("mailto:", "http")):
            continue
        if href.startswith("#"):
            if href[1:] not in p.ids: fails.append(f"{url}: missing anchor {href}")
            continue
        if not exists(href): fails.append(f"{url}: broken link {href}")
    is_es = url.startswith("/es/")
    want_lang = "es-US" if is_es else "en-US"
    if p.lang != want_lang: fails.append(f"{url}: html lang {p.lang}")
    if url.endswith("404.html"):
        if "noindex" not in (p.meta.get("robots") or ""): fails.append(f"{url}: 404 should be noindex")
        continue
    if p.h1 != 1: fails.append(f"{url}: {p.h1} h1 tags")
    t, d = p.title.strip(), p.meta.get("description", "")
    if not 25 <= len(t) <= 65: fails.append(f"{url}: title length {len(t)}: {t}")
    if not 110 <= len(d) <= 165: fails.append(f"{url}: description length {len(d)}: {d}")
    if t in titles: fails.append(f"{url}: duplicate title with {titles[t]}")
    if d in descs: fails.append(f"{url}: duplicate description with {descs[d]}")
    titles[t] = url; descs[d] = url
    if p.canon != SITE + url: fails.append(f"{url}: canonical {p.canon}")
    og = SITE + ("/og-image-es.png" if is_es else "/og-image.png")
    if p.meta.get("og:image") != og: fails.append(f"{url}: og:image")
    if "(806) 451-3520" not in raw[url] or "(806) 776-4460" not in raw[url]:
        fails.append(f"{url}: both phone numbers should appear")
    # hreflang
    if set(p.alts) != {"en-US", "es-US", "x-default"}: fails.append(f"{url}: hreflang set {set(p.alts)}")
    else:
        self_tag = "es-US" if is_es else "en-US"; other_tag = "en-US" if is_es else "es-US"
        if p.alts[self_tag] != SITE + url: fails.append(f"{url}: hreflang self mismatch")
        other_url = p.alts[other_tag][len(SITE):]
        if other_url not in pages: fails.append(f"{url}: hreflang target missing {other_url}")
        elif pages[other_url].alts.get(self_tag) != SITE + url: fails.append(f"{url}: hreflang not reciprocal with {other_url}")
        if not p.switch or p.switch[1] != other_url: fails.append(f"{url}: language switch points to {p.switch}, expected {other_url}")
        if not p.select or p.select.get("data-en") != (other_url if is_es else url) or p.select.get("data-es") != (url if is_es else other_url):
            fails.append(f"{url}: language setting select wrong {p.select}")
        if p.alts["x-default"] != p.alts["en-US"]: fails.append(f"{url}: x-default should be English")
    for blob in p.ld:
        try:
            j = json.loads(blob)
            if j.get("@context") != "https://schema.org": fails.append(f"{url}: ld context")
        except Exception as e:
            fails.append(f"{url}: invalid JSON-LD {e}")
    if not p.ld: fails.append(f"{url}: no structured data")
    terms = "/es/terminos/" if is_es else "/terms/"; priv = "/es/privacidad/" if is_es else "/privacy/"
    if terms not in p.links or priv not in p.links: fails.append(f"{url}: missing terms/privacy link")

for home in ("/", "/es/"):
    types = [json.loads(b)["@type"] for b in pages[home].ld]
    for need in ("AutoRepair", "WebSite", "FAQPage"):
        if need not in types: fails.append(f"{home} missing {need} schema")
    biz = json.loads(pages[home].ld[0])
    if biz.get("telephone") != CALL: fails.append(f"{home} schema telephone wrong")
    if TEXT not in json.dumps(biz): fails.append(f"{home} schema missing text line")

for c in ("/contact/", "/es/contacto/"):
    if pages[c].form_sms != TEXT: fails.append(f"{c}: form texts {pages[c].form_sms}, expected {TEXT}")

# ---- SMS registration (A2P / toll-free) evidence
def text_of(url):
    import re as _re
    return _re.sub(r"\s+", " ", _re.sub(r"<[^>]+>", " ", raw[url]))
for sms_url, contact_url, privacy_url, terms_url, words in [
        ("/sms/", "/contact/", "/privacy/", "/terms/",
         ["Message frequency varies", "data rates may apply", "Reply STOP", "HELP", "not a condition of purchase", "(806) 776-4460"]),
        ("/es/mensajes-de-texto/", "/es/contacto/", "/es/privacidad/", "/es/terminos/",
         ["frecuencia de los mensajes varía", "cargos por mensajes y datos", "STOP", "HELP", "no es condición de compra", "(806) 776-4460"])]:
    for url in (sms_url, contact_url):
        t = text_of(url)
        for w in words:
            if w not in t: fails.append(f"{url}: SMS disclosure missing {w!r}")
    if 'id="f-consent" type="checkbox" name="consent" value="yes" required' not in raw[contact_url]:
        fails.append(f"{contact_url}: required SMS consent checkbox missing")
    if f'href="{sms_url}"' not in raw[privacy_url] or f'href="{sms_url}"' not in raw[terms_url]:
        fails.append(f"{privacy_url}/{terms_url}: must link the SMS page")
    tt = text_of(terms_url)
    for w in ("STOP", "HELP", "(806) 776-4460"):
        if w not in tt: fails.append(f"{terms_url}: SMS terms missing {w!r}")
for url, phrase in [("/privacy/", "No mobile information will be shared with third parties or affiliates for marketing or promotional purposes."),
                    ("/sms/", "No mobile information will be shared with third parties or affiliates for marketing or promotional purposes."),
                    ("/es/privacidad/", "No se compartirá información móvil con terceros ni afiliados para fines de mercadotecnia o promoción.")]:
    if phrase not in text_of(url): fails.append(f"{url}: carrier non-sharing clause missing")
for url in pages:
    if url.endswith("404.html"): continue
    if 'class="sms-note"' not in raw[url]: fails.append(f"{url}: no SMS disclosure next to Text buttons")
redirects = open(os.path.join(DIST, "_redirects")).read()
for alias in ("/privacy-policy /privacy/ 200", "/terms-of-service /terms/ 200", "/sms-terms /sms/ 200"):
    if alias not in redirects: fails.append(f"_redirects missing alias {alias}")

# ---- CSS/JS links carry a content hash so edge and browser caches never serve stale files
import hashlib, re as _re2
for asset in ("css/site.css", "js/site.js", "js/lang.js"):
    want = hashlib.sha256(open(os.path.join(DIST, asset), "rb").read()).hexdigest()[:10]
    for url in pages:
        found = _re2.findall(r'/' + _re2.escape(asset) + r'(\?v=[0-9a-f]+)?"', raw[url])
        if found and found != ["?v=" + want] * len(found):
            fails.append(f"{url}: {asset} link not versioned with current hash ({found})")

# ---- SMS opt-in evidence page: every step has its screenshot, and the SMS page links to it
for url, lang in (("/sms-opt-in/", "en"), ("/es/evidencia-sms/", "es")):
    if url not in pages:
        fails.append(f"missing evidence page {url}"); continue
    for key in ("home-text-cta", "sms-consent-box", "form-consent", "sms-phone"):
        rel = f"sms-evidence/{key}-{lang}.webp"
        if not os.path.isfile(os.path.join(DIST, rel)): fails.append(f"{url}: screenshot {rel} not built")
        elif f'src="/{rel}?v=' not in raw[url]: fails.append(f"{url}: screenshot {rel} not shown")
    if "(806) 776-4460" not in text_of(url): fails.append(f"{url}: text number missing")
for sms_url, ev in (("/sms/", "/sms-opt-in/"), ("/es/mensajes-de-texto/", "/es/evidencia-sms/")):
    if f'href="{ev}"' not in raw[sms_url]: fails.append(f"{sms_url}: does not link {ev}")

ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
locs = {l.text for l in ET.parse(os.path.join(DIST, "sitemap.xml")).getroot().findall("s:url/s:loc", ns)}
expected = {SITE + u for u in pages if not u.endswith("404.html")}
if locs != expected: fails.append(f"sitemap mismatch: missing {expected - locs}, extra {locs - expected}")
if "Sitemap: " + SITE + "/sitemap.xml" not in open(os.path.join(DIST, "robots.txt")).read(): fails.append("robots missing sitemap")

en = [u for u in pages if not u.startswith("/es/") and not u.endswith("404.html")]
es = [u for u in pages if u.startswith("/es/") and not u.endswith("404.html")]
print(f"Checked {len(pages)} pages ({len(en)} English, {len(es)} Spanish), {sum(len(p.links) for p in pages.values())} links, "
      f"{n_tel} call links, {n_sms} text links, {sum(len(p.ld) for p in pages.values())} JSON-LD blocks")
if len(en) != len(es): fails.append("English and Spanish page counts differ")
if fails:
    print("FAIL"); [print(" -", f) for f in fails]; sys.exit(1)
print("PASS: static checks")
