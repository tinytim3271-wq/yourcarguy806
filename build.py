#!/usr/bin/env python3
"""Static site generator for Reliable Automotive Services (yourcarguy806.com).

English lives at /, Spanish at /es/. Content: content_en.py and content_es.py.
Run:  python3 build.py   -> writes the deployable site to ./dist
"""
import html
import json
import os
import shutil
from datetime import date

import content_en as EN
import content_es as ES
from icons_gen import ICONS, LOGO

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
STATIC = os.path.join(ROOT, "static")

SITE = "https://www.yourcarguy806.com"
NAME = "Reliable Automotive Services"
SHORT = "Your Car Guy 806"
CALL_DISPLAY, CALL_E164 = "(806) 451-3520", "+18064513520"
TEXT_DISPLAY, TEXT_E164 = "(806) 776-4460", "+18067764460"
TEL = "tel:" + CALL_E164
SMS = "sms:" + TEXT_E164
TODAY = date.today().isoformat()
LANGS = {"en": EN, "es": ES}


def asset_version(rel):
    """Short content hash so a changed CSS/JS file gets a new URL and is never served stale from cache."""
    import hashlib
    with open(os.path.join(STATIC, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:10]


V_CSS = asset_version("css/site.css")
V_SITE_JS = asset_version("js/site.js")
V_LANG_JS = asset_version("js/lang.js")

esc = html.escape


def call_link():
    return f'<a href="{TEL}">{CALL_DISPLAY}</a>'


def text_link():
    return f'<a href="{SMS}">{TEXT_DISPLAY}</a>'


def fill(s, C=None):
    """Fill phone placeholders in content strings."""
    return s.replace("{call_link}", call_link()).replace("{text_link}", text_link()) \
            .replace("{call}", CALL_DISPLAY).replace("{text}", TEXT_DISPLAY)


# ---------------------------------------------------------------- page ids & paths
def path_for(lang, pid):
    C = LANGS[lang]
    kind = pid[0]
    if kind == "service":
        s = next(x for x in C.SERVICES if x["key"] == pid[1])
        return C.UI["paths"]["services"] + s["slug"] + "/"
    if kind == "area_page":
        a = next(x for x in C.AREAS if x["key"] == pid[1])
        return C.UI["paths"]["area"] + a["slug"] + "/"
    return C.UI["paths"][kind]


def other(lang):
    return "es" if lang == "en" else "en"


# ---------------------------------------------------------------- schema
def business_schema(lang):
    C = LANGS[lang]
    desc = {"en": "Mobile mechanic serving Lubbock County and surrounding West Texas towns. On-site diagnostics, brakes, batteries, starters, alternators, cooling systems, tune-ups, suspension, inspections, and maintenance.",
            "es": "Mecánico a domicilio en el condado de Lubbock y pueblos cercanos del oeste de Texas. Diagnóstico, frenos, baterías, marchas, alternadores, enfriamiento, afinación, suspensión, inspecciones y mantenimiento en el lugar."}[lang]
    other_towns = ["New Deal", "Abernathy", "Ransom Canyon", "Buffalo Springs", "Ropesville", "Smyer", "Levelland", "Lorenzo", "Ralls"]
    return {
        "@context": "https://schema.org", "@type": "AutoRepair", "@id": SITE + "/#business",
        "name": NAME, "alternateName": SHORT, "description": desc,
        "url": SITE + "/", "telephone": CALL_E164,
        "image": SITE + "/og-image.png", "logo": SITE + "/icons/icon-512.png",
        "address": {"@type": "PostalAddress", "addressLocality": "Lubbock", "addressRegion": "TX", "addressCountry": "US"},
        "contactPoint": [
            {"@type": "ContactPoint", "telephone": CALL_E164, "contactType": "customer service", "description": "Phone calls"},
            {"@type": "ContactPoint", "telephone": TEXT_E164, "contactType": "customer service", "description": "Text messages"},
        ],
        "areaServed": [{"@type": "AdministrativeArea", "name": "Lubbock County, Texas"}]
            + [{"@type": "City", "name": a["name"] + ", TX"} for a in C.AREAS]
            + [{"@type": "City", "name": t + ", TX"} for t in other_towns],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": {"en": "Mobile auto repair services", "es": "Servicios de mecánica a domicilio"}[lang],
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": SITE + path_for(lang, ("service", s["key"]))}} for s in C.SERVICES]},
    }


def website_schema(lang):
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
            "name": NAME, "alternateName": SHORT, "inLanguage": ["en-US", "es-US"], "publisher": {"@id": SITE + "/#business"}}


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def crumbs_schema(crumbs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]}


# ---------------------------------------------------------------- layout
def header(lang, pid):
    C = LANGS[lang]; U = C.UI; P = U["paths"]
    cur = path_for(lang, pid) if pid else ""
    nav_targets = [P["services"], P["area"], P["about"], P["contact"]]
    links = "".join(
        f'<a href="{u}"{" aria-current=\"page\"" if cur.startswith(u) else ""}>{n}</a>' for n, u in zip(U["nav"], nav_targets))
    o = other(lang); OU = LANGS[o].UI
    alt = path_for(o, pid) if pid else OU["paths"]["home"]
    return f'''<a class="skip" href="#main">{U["skip"]}</a>
<div class="topbar"><div class="wrap"><span class="hide-sm">{U["topbar_left"]}</span>
<span class="topbar-phones"><a href="{TEL}">{ICONS["phone"]}<span class="hide-sm">{U["call"]}&nbsp;</span>{CALL_DISPLAY}</a><span class="sep" aria-hidden="true">&middot;</span><a href="{SMS}">{ICONS["text"]}<span class="hide-sm">{U["text"]}&nbsp;</span>{TEXT_DISPLAY}</a></span></div></div>
<header class="site-header"><div class="wrap">
<a class="brand" href="{P["home"]}" aria-label="{NAME} {U["home_label"]}">{LOGO}<span class="brand-text"><span class="brand-name">Reliable Automotive</span><span class="brand-sub">Your Car Guy &middot; 806</span></span></a>
<div class="header-tools">
<a class="lang-switch" href="{alt}" hreflang="{OU["lang"]}" lang="{o}" data-set-lang="{o}" aria-label="{U["lang_switch_label"]}">{ICONS["globe"]}<span class="ls-full">{OU["name"]}</span><span class="ls-short">{OU["short"]}</span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" data-open="{U["menu"]}" data-close="{U["close"]}">{U["menu"]}</button>
</div>
<nav id="site-nav" class="nav" aria-label="{U["main_nav"]}">{links}<a class="btn btn-red" href="{TEL}">{ICONS["phone"]}{U["call_now"]}</a></nav>
</div></header>'''


def footer(lang, pid):
    C = LANGS[lang]; U = C.UI; P = U["paths"]
    svc = "".join(f'<li><a href="{path_for(lang, ("service", s["key"]))}">{esc(s["name"])}</a></li>' for s in C.SERVICES[:6])
    areas = "".join(f'<li><a href="{path_for(lang, ("area_page", a["key"]))}">{a["name"]}, TX</a></li>' for a in C.AREAS)
    en_path = path_for("en", pid) if pid else "/"
    es_path = path_for("es", pid) if pid else "/es/"
    opts = "".join(f'<option value="{k}"{" selected" if k == lang else ""}>{LANGS[k].UI["name"]}</option>' for k in ("en", "es"))
    return f'''<section class="cta-band"><div class="wrap"><div><h2>{U["cta_h"]}</h2><p>{U["cta_p"]}</p>{sms_note(lang)}</div>
<div class="btn-row" style="margin:0"><a class="btn btn-dark" href="{TEL}">{ICONS["phone"]}{CALL_DISPLAY}</a><a class="btn btn-amber" href="{SMS}">{ICONS["text"]}{U["text"]} {TEXT_DISPLAY}</a></div></div></section>
<footer class="site-footer"><div class="wrap"><div class="grid">
<div><a class="brand" href="{P["home"]}">{LOGO}<span class="brand-text"><span class="brand-name">Reliable Automotive</span><span class="brand-sub">Your Car Guy &middot; 806</span></span></a>
<p>{U["footer_about"]}</p>
<p>{U["call"]}: <a href="{TEL}"><strong>{CALL_DISPLAY}</strong></a><br>{U["text"]}: <a href="{SMS}"><strong>{TEXT_DISPLAY}</strong></a></p>
<div class="lang-setting"><label for="lang-select">{ICONS["globe"]}{U["lang_setting"]}</label>
<select id="lang-select" data-en="{en_path}" data-es="{es_path}">{opts}</select></div></div>
<div><h2>{U["f_services"]}</h2><ul>{svc}<li><a href="{P["services"]}">{U["all_services"]}</a></li></ul></div>
<div><h2>{U["f_area"]}</h2><ul>{areas}<li><a href="{P["area"]}">{U["all_areas"]}</a></li></ul></div>
<div><h2>{U["f_company"]}</h2><ul><li><a href="{P["about"]}">{U["about"]}</a></li><li><a href="{P["contact"]}">{U["contact_req"]}</a></li><li><a href="{TEL}">{U["call"]} {CALL_DISPLAY}</a></li><li><a href="{SMS}">{U["text_us"]}</a></li><li><a href="{P["sms"]}">{U["sms_link"]}</a></li><li><a href="{P["terms"]}">{U["terms"]}</a></li><li><a href="{P["privacy"]}">{U["privacy"]}</a></li></ul></div>
</div>
<div class="footer-bottom"><span>&copy; <span id="year">{date.today().year}</span> {NAME}. Lubbock, Texas.</span><span><a href="{P["terms"]}">{U["terms"]}</a> &middot; <a href="{P["privacy"]}">{U["privacy"]}</a> &middot; <a href="{P["sms"]}">{U["sms_link"]}</a></span></div>
</div></footer>
<nav class="mobile-cta" aria-label="{U["quick"]}"><a class="call" href="{TEL}">{ICONS["phone"]}{U["call"]}</a><a class="text" href="{SMS}">{ICONS["text"]}{U["text"]}</a></nav>'''


def page(lang, pid, title, desc, body, schemas=(), crumbs=None, robots="index,follow"):
    U = LANGS[lang].UI
    path = path_for(lang, pid) if pid else None
    blocks = []
    if pid == ("home",):
        blocks += [business_schema(lang), website_schema(lang)]
    if crumbs:
        blocks.append(crumbs_schema(crumbs))
    blocks.extend(schemas)
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False, separators=(",", ":"))}</script>' for b in blocks)
    og_img = SITE + ("/og-image-es.png" if lang == "es" else "/og-image.png")
    if pid:
        alts = "\n".join(f'<link rel="alternate" hreflang="{LANGS[k].UI["lang"]}" href="{SITE}{path_for(k, pid)}" data-lang="{k}">' for k in ("en", "es"))
        alts += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{path_for("en", pid)}">'
        head_seo = f'<link rel="canonical" href="{SITE}{path}">\n{alts}\n<meta property="og:url" content="{SITE}{path}">'
    else:
        head_seo = ""
    alt_locale = LANGS[other(lang)].UI["og_locale"]
    return f'''<!doctype html>
<html lang="{U["lang"]}" data-lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title, quote=False)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
{head_seo}
<script src="/js/lang.js?v={V_LANG_JS}"></script>
<meta name="theme-color" content="#15171b">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Lubbock">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(U["og_alt"])}">
<meta property="og:locale" content="{U["og_locale"]}">
<meta property="og:locale:alternate" content="{alt_locale}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/anton-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/barlow-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css?v={V_CSS}">
{ld}
</head>
<body>
{header(lang, pid)}
<main id="main">
{body}
</main>
{footer(lang, pid)}
<script src="/js/site.js?v={V_SITE_JS}" defer></script>
</body>
</html>
'''


def crumb_html(lang, crumbs):
    items = []
    for i, (n, u) in enumerate(crumbs):
        items.append(f'<li><span aria-current="page">{esc(n)}</span></li>' if i == len(crumbs) - 1 else f'<li><a href="{u}">{esc(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="{LANGS[lang].UI["crumb_label"]}"><ol>{"".join(items)}</ol></nav>'


def page_hero(lang, crumbs, h1, lead, eyebrow, req=None):
    U = LANGS[lang].UI
    req = req or U["paths"]["contact"]
    return f'''<section class="hero page-hero"><div class="wrap">{crumb_html(lang, crumbs)}
<p class="eyebrow">{eyebrow}</p><h1>{esc(h1)}</h1><p class="lead">{esc(lead)}</p>
<div class="btn-row"><a class="btn btn-red" href="{TEL}">{ICONS["phone"]}{U["call"]} {CALL_DISPLAY}</a><a class="btn btn-ghost" href="{req}">{ICONS["text"]}{U["request_service"]}</a></div>
</div></section><div class="stripe" role="none"></div>'''


def faq_html(faqs):
    return '<div class="faq">' + "".join(
        f'<details><summary>{esc(q)}</summary><div><p>{esc(a)}</p></div></details>' for q, a in faqs) + "</div>"


def sms_note(lang):
    U = LANGS[lang].UI
    return f'<p class="sms-note">{U["sms_short"]} <a href="{U["paths"]["sms"]}">{U["sms_details"]}</a></p>'


def callbox(lang):
    U = LANGS[lang].UI
    return f'''<div class="callbox"><h2>{U["quote_h"]}</h2><p>{U["quote_p"]}</p>
<a class="big-phone" href="{TEL}">{CALL_DISPLAY}</a>
<a class="btn btn-red" href="{TEL}">{ICONS["phone"]}{U["call_now"]}</a><a class="btn btn-amber" href="{SMS}">{ICONS["text"]}{U["send_text"]}</a>
<p class="text-line">{U["texts_to"]} <a href="{SMS}">{TEXT_DISPLAY}</a></p>{sms_note(lang)}</div>'''


def service_card(lang, s):
    U = LANGS[lang].UI
    return f'''<a class="card" href="{path_for(lang, ("service", s["key"]))}"><span class="icon">{ICONS[s["icon"]]}</span><h3>{esc(s["name"])}</h3><p>{esc(s["short"])}</p><span class="more">{U["learn_more"]} &rarr;</span></a>'''


OTHER_TOWNS = ["New Deal", "Abernathy", "Ransom Canyon", "Buffalo Springs", "Ropesville", "Smyer", "Levelland", "Lorenzo", "Ralls"]


def area_pills(lang):
    C = LANGS[lang]
    linked = "".join(f'<li><a href="{path_for(lang, ("area_page", a["key"]))}">{a["name"]}</a></li>' for a in C.AREAS)
    plain = "".join(f'<li><span>{t}</span></li>' for t in OTHER_TOWNS)
    return f'<ul class="area-list">{linked}{plain}</ul>'


def aside(lang, inner):
    return f'<aside class="sidebar" aria-label="{LANGS[lang].UI["aside_label"]}">{inner}</aside>'


# ---------------------------------------------------------------- pages
def home(lang):
    C = LANGS[lang]; U = C.UI; H = C.HOME
    cards = "".join(service_card(lang, s) for s in C.SERVICES)
    steps = "".join(f'<div class="step"><h3>{h}</h3><p>{p}</p></div>' for h, p in H["steps"])
    checks = "".join(f"<li>{c}</li>" for c in H["checks"])
    why = "".join(f"<p>{esc(p)}</p>" for p in H["why_p"])
    body = f'''<section class="hero"><div class="wrap">
<div><p class="eyebrow">{H["eyebrow"]}</p>
<h1>{H["h1a"]} <span>{H["h1b"]}</span></h1>
<p class="lead">{esc(H["lead"])}</p>
<div class="btn-row"><a class="btn btn-red" href="{TEL}">{ICONS["phone"]}{U["call"]} {CALL_DISPLAY}</a><a class="btn btn-ghost" href="{U["paths"]["contact"]}">{ICONS["text"]}{U["request_service"]}</a></div></div>
<aside class="hero-badge" aria-label="{H["badge_h"]}"><h2>{H["badge_h"]}</h2>
<a class="big-phone" href="{TEL}">{CALL_DISPLAY}</a>
<ul class="checks">{checks}</ul>
<a class="btn btn-amber" style="width:100%" href="{SMS}">{ICONS["text"]}{H["text_btn"]}</a>
<p class="text-line">{U["texts_to"]} <a href="{SMS}">{TEXT_DISPLAY}</a></p>{sms_note(lang)}</aside>
</div></section><div class="stripe" role="none"></div>

<section><div class="wrap"><div class="section-head"><p class="eyebrow">{H["svc_eyebrow"]}</p><h2>{H["svc_h"]}</h2>
<p>{esc(H["svc_p"])}</p></div>
<div class="grid grid-3">{cards}</div></div></section>

<section class="section-dark"><div class="wrap"><div class="section-head"><p class="eyebrow">{H["how_eyebrow"]}</p><h2>{H["how_h"]}</h2></div>
<div class="grid grid-3 steps">{steps}</div></div></section>

<section class="section-cream"><div class="wrap two-col">
<div class="prose"><p class="eyebrow">{H["why_eyebrow"]}</p><h2>{H["why_h"]}</h2>
{why}
<h3>{H["serving_h"]}</h3>{area_pills(lang)}
<p style="margin-top:1em"><a href="{U["paths"]["area"]}">{H["see_area"]} &rarr;</a></p></div>
{aside(lang, callbox(lang))}</div></section>

<section><div class="wrap"><div class="section-head"><p class="eyebrow">{H["faq_eyebrow"]}</p><h2>{H["faq_h"]}</h2></div>{faq_html(C.HOME_FAQ)}</div></section>'''
    return page(lang, ("home",), H["title"], H["desc"], body, schemas=[faq_schema(C.HOME_FAQ)])


def services_index(lang):
    C = LANGS[lang]; U = C.UI; S = C.SERVICES_PAGE
    crumbs = [(U["crumb_home"], U["paths"]["home"]), (S["eyebrow"], U["paths"]["services"])]
    cards = "".join(service_card(lang, s) for s in C.SERVICES)
    body = page_hero(lang, crumbs, S["h1"], S["lead"], S["eyebrow"]) + f'''
<section><div class="wrap"><div class="grid grid-3">{cards}</div>
<div class="prose" style="margin-top:48px"><h2>{S["more_h"]}</h2><p>{S["more_p"].replace("{call}", call_link()).replace("{text}", text_link())}</p></div></div></section>'''
    return page(lang, ("services",), S["title"], S["desc"], body, crumbs=crumbs)


def service_page(lang, s):
    C = LANGS[lang]; U = C.UI; T = C.SERVICE_TPL
    pid = ("service", s["key"]); path = path_for(lang, pid)
    crumbs = [(U["crumb_home"], U["paths"]["home"]), (U["nav"][0], U["paths"]["services"]), (s["name"], path)]
    covers = "".join(f"<li>{esc(c)}</li>" for c in s["covers"])
    sections = "".join(f"<h2>{esc(h)}</h2><p>{esc(p)}</p>" for h, p in s["body"])
    others = "".join(f'<li><a href="{path_for(lang, ("service", o["key"]))}">{esc(o["name"])}</a></li>' for o in C.SERVICES if o["key"] != s["key"])
    area_links = ", ".join(f'<a href="{path_for(lang, ("area_page", a["key"]))}">{a["name"]}</a>' for a in C.AREAS)
    svc_name = s["name"].lower() if lang == "en" else s["name"][0].lower() + s["name"][1:]
    where = T["where_p"].replace("{svc}", esc(svc_name)).replace("{areas}", area_links).replace("{call}", call_link())
    schema = {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"],
              "url": SITE + path, "description": s["desc"], "provider": {"@id": SITE + "/#business"},
              "areaServed": [{"@type": "AdministrativeArea", "name": "Lubbock County, Texas"}], "inLanguage": U["lang"]}
    body = page_hero(lang, crumbs, s["h1"], s["intro"], U["mobile_service"]) + f'''
<section><div class="wrap two-col"><div class="prose">
<h2>{T["included"]}</h2><ul class="checks">{covers}</ul>
{sections}
<h2>{T["where"]}</h2><p>{where}</p>
<h2>{T["faq"]}</h2>{faq_html(s["faq"])}
</div>{aside(lang, callbox(lang) + f'<div class="linkbox"><h2>{U["other_services"]}</h2><ul>{others}</ul></div>')}</div></section>'''
    return page(lang, pid, s["title"], s["desc"], body, schemas=[schema, faq_schema(s["faq"])], crumbs=crumbs)


def area_index(lang):
    C = LANGS[lang]; U = C.UI; A = C.AREA_PAGE
    crumbs = [(U["crumb_home"], U["paths"]["home"]), (U["nav"][1], U["paths"]["area"])]
    cards = "".join(f'''<a class="card" href="{path_for(lang, ("area_page", a["key"]))}"><span class="icon">{ICONS["pin"]}</span><h3>{a["name"]}, TX</h3><p>{esc(a["intro"][:140].rsplit(" ", 1)[0])}&hellip;</p><span class="more">{A["card_more"].replace("{town}", a["name"])} &rarr;</span></a>''' for a in C.AREAS)
    towns = ", ".join(OTHER_TOWNS[:-1]) + f" {A['and']} " + OTHER_TOWNS[-1]
    body = page_hero(lang, crumbs, A["h1"], A["lead"], A["eyebrow"]) + f'''
<section><div class="wrap"><div class="grid grid-3">{cards}</div>
<div class="prose" style="margin-top:48px"><h2>{A["also_h"]}</h2>
<p>{A["also_p"].replace("{towns}", towns).replace("{call}", call_link())}</p>
{area_pills(lang)}</div></div></section>'''
    return page(lang, ("area",), A["title"], A["desc"], body, crumbs=crumbs)


def area_page(lang, a):
    C = LANGS[lang]; U = C.UI; T = C.AREA_TPL
    pid = ("area_page", a["key"]); path = path_for(lang, pid)
    t = lambda s: s.replace("{town}", a["name"])
    crumbs = [(U["crumb_home"], U["paths"]["home"]), (U["nav"][1], U["paths"]["area"]), (a["name"], path)]
    svc = "".join(f'<li><a href="{path_for(lang, ("service", s["key"]))}">{esc(s["name"])}</a> &mdash; {esc(s["short"])}</li>' for s in C.SERVICES)
    near = "".join(f'<li><a href="{path_for(lang, ("area_page", n))}">{next(x["name"] for x in C.AREAS if x["key"] == n)}, TX</a></li>' for n in a["nearby"])
    faqs = [(t(q), fill(t(ans))) for q, ans in T["faq"]]
    schema = {"@context": "https://schema.org", "@type": "Service", "name": t(T["schema_name"]),
              "serviceType": "Mobile auto repair", "url": SITE + path, "provider": {"@id": SITE + "/#business"},
              "areaServed": {"@type": "City", "name": a["name"] + ", TX"}, "inLanguage": U["lang"]}
    body = page_hero(lang, crumbs, a["h1"], a["intro"], f"{a['name']}, Texas") + f'''
<section><div class="wrap two-col"><div class="prose">
<h2>{t(T["h_repair"])}</h2><p>{esc(a["local"])}</p>
<h2>{t(T["h_services"])}</h2><ul>{svc}</ul>
<h2>{t(T["h_faq"])}</h2>{faq_html(faqs)}
</div>{aside(lang, callbox(lang) + f'<div class="linkbox"><h2>{U["nearby"]}</h2><ul>{near}<li><a href="{U["paths"]["area"]}">{U["full_area"]}</a></li></ul></div>')}</div></section>'''
    return page(lang, pid, a["title"], a["desc"], body, schemas=[schema, faq_schema(faqs)], crumbs=crumbs)


def about(lang):
    C = LANGS[lang]; U = C.UI; A = C.ABOUT
    crumbs = [(U["crumb_home"], U["paths"]["home"]), (A["eyebrow"], U["paths"]["about"])]
    body = page_hero(lang, crumbs, A["h1"], A["lead"], A["eyebrow"]) + f'''
<section><div class="wrap two-col"><div class="prose">{fill(A["html"])}</div>{aside(lang, callbox(lang))}</div></section>'''
    return page(lang, ("about",), A["title"], A["desc"], body, crumbs=crumbs)


def contact(lang):
    C = LANGS[lang]; U = C.UI; K = C.CONTACT; J = C.FORM_JS
    crumbs = [(U["crumb_home"], U["paths"]["home"]), (K["eyebrow"], U["paths"]["contact"])]
    opts = "".join(f"<option>{esc(s['name'])}</option>" for s in C.SERVICES)
    data = " ".join(f'data-{k.replace("_", "-")}="{esc(v)}"' for k, v in J.items())
    hint = K["hint"].replace("{text}", f"<strong>{TEXT_DISPLAY}</strong>").replace("{call}", call_link())
    body = page_hero(lang, crumbs, K["h1"], K["lead"], K["eyebrow"], req="#request-form") + f'''
<section><div class="wrap two-col">
<form id="request-form" class="form" novalidate aria-describedby="form-hint" data-sms="{TEXT_E164}" {data}>
<h2 style="font-size:1.8rem;margin:0">{K["form_h"]}</h2>
<p id="form-hint" class="hint">{hint}</p>
<div class="row"><div><label for="f-name">{K["name"]} *</label><input id="f-name" type="text" name="name" autocomplete="name" required></div>
<div><label for="f-phone">{K["phone"]} *</label><input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="(806) 555-0123"></div></div>
<div class="row"><div><label for="f-vehicle">{K["vehicle"]} *</label><input id="f-vehicle" type="text" name="vehicle" required placeholder="{K["vehicle_ph"]}"></div>
<div><label for="f-service">{K["service"]}</label><select id="f-service" name="service"><option value="">{K["not_sure"]}</option>{opts}</select></div></div>
<div class="row"><div><label for="f-location">{K["location"]} *</label><input id="f-location" type="text" name="location" required placeholder="{K["location_ph"]}"></div>
<div><label for="f-when">{K["when"]}</label><input id="f-when" type="text" name="when" placeholder="{K["when_ph"]}"></div></div>
<div><label for="f-details">{K["details"]}</label><textarea id="f-details" name="details" rows="5" placeholder="{K["details_ph"]}"></textarea></div>
<div class="consent"><input id="f-consent" type="checkbox" name="consent" value="yes">
<label for="f-consent">{K["sms_consent"]} <a href="{U["paths"]["sms"]}">{U["sms_details"]}</a> &middot; <a href="{U["paths"]["privacy"]}">{U["privacy"]}</a> &middot; <a href="{U["paths"]["terms"]}">{U["terms"]}</a></label></div>
<p class="error" role="alert" aria-live="polite"></p>
<div class="actions"><button class="btn btn-red" type="submit">{ICONS["text"]}{K["submit"]}</button><button id="copy-request" class="btn btn-dark" type="button">{K["copy"]}</button></div>
</form>
{aside(lang, callbox(lang) + f'<div class="linkbox"><h2>{K["area_h"]}</h2><p>{K["area_p"]} <a href="{U["paths"]["area"]}">{K["area_link"]}</a>.</p></div>')}
</div></section>'''
    return page(lang, ("contact",), K["title"], K["desc"], body, crumbs=crumbs)


def legal_page(lang, kind, D):
    C = LANGS[lang]; U = C.UI
    pid = (kind,); path = path_for(lang, pid)
    crumbs = [(U["crumb_home"], U["paths"]["home"]), (D["h1"], path)]
    toc = "".join(f'<li><a href="#s{i+1}">{esc(h)}</a></li>' for i, (h, _) in enumerate(D["sections"]))
    secs = "".join(f'<h2 id="s{i+1}">{i+1}. {esc(h)}</h2>{fill(b)}' for i, (h, b) in enumerate(D["sections"]))
    body = f'''<section class="hero page-hero"><div class="wrap">{crumb_html(lang, crumbs)}<p class="eyebrow">{U["legal"]}</p><h1>{esc(D["h1"])}</h1><p class="lead">{esc(D["lead"])}</p><p>{U["effective"]} {C.EFFECTIVE}</p></div></section><div class="stripe" role="none"></div>
<section><div class="wrap two-col"><div class="prose">{secs}</div>
{aside(lang, f'<div class="linkbox"><h2>{U["on_page"]}</h2><ul>{toc}</ul></div>' + callbox(lang))}</div></section>'''
    return page(lang, pid, D["title"], D["desc"], body, crumbs=crumbs)


def sms_page(lang):
    C = LANGS[lang]; U = C.UI; D = C.SMS_PAGE
    pid = ("sms",); path = path_for(lang, pid)
    crumbs = [(U["crumb_home"], U["paths"]["home"]), (D["eyebrow"], path)]
    secs = "".join(f'<h2 id="s{i+1}">{esc(h)}</h2>{fill(b)}' for i, (h, b) in enumerate(D["sections"]))
    body = f'''<section class="hero page-hero"><div class="wrap">{crumb_html(lang, crumbs)}<p class="eyebrow">{D["eyebrow"]}</p><h1>{esc(D["h1"]).replace(TEXT_DISPLAY, f'<span class="nowrap">{TEXT_DISPLAY}</span>')}</h1><p class="lead">{esc(D["lead"])}</p>
<div class="btn-row"><a class="btn btn-amber" href="{SMS}">{ICONS["text"]}{D["cta_btn"]}</a><a class="btn btn-ghost" href="{U["paths"]["contact"]}#request-form">{D["form_btn"]}</a></div>
<p class="sms-note hero-note">{U["sms_short"]}</p></div></section><div class="stripe" role="none"></div>
<section><div class="wrap two-col"><div class="prose">
<div class="consent-box" id="consent"><h2>{D["consent_h"]}</h2><p>{esc(D["consent"])}</p>
<p><a class="btn btn-red" href="{SMS}">{ICONS["text"]}{D["cta_btn"]}</a></p></div>
<h2>{D["cta_h"]}</h2><p>{esc(D["cta_p"])}</p>
{secs}<p><a href="{U["paths"]["sms_evidence"]}">{LANGS[lang].SMS_EVIDENCE["eyebrow"]} &rarr;</a></p></div>
{aside(lang, callbox(lang))}</div></section>'''
    schema = {"@context": "https://schema.org", "@type": "WebPage", "name": D["title"], "url": SITE + path,
              "inLanguage": U["lang"], "about": {"@id": SITE + "/#business"}}
    return page(lang, pid, D["title"], D["desc"], body, schemas=[schema], crumbs=crumbs)


def evidence_image(lang, key):
    """Screenshot captured by scripts/capture_sms_evidence.py; returns (src, width, height) or None."""
    rel = f"sms-evidence/{key}-{lang}.webp"
    path = os.path.join(STATIC, rel)
    if not os.path.exists(path):
        return None
    from PIL import Image
    with Image.open(path) as im:
        w, h = im.size
    return "/" + rel + "?v=" + asset_version(rel), w, h


def sms_evidence_page(lang):
    C = LANGS[lang]; U = C.UI; D = C.SMS_EVIDENCE
    pid = ("sms_evidence",); path = path_for(lang, pid)
    crumbs = [(U["crumb_home"], U["paths"]["home"]), (U["sms_link"], U["paths"]["sms"]), (D["eyebrow"], path)]
    steps = []
    for title, key, text, alt in D["steps"]:
        img = evidence_image(lang, key)
        fig = (f'<figure class="evidence"><img src="{img[0]}" width="{img[1]}" height="{img[2]}" alt="{esc(alt)}" loading="lazy">'
               f'<figcaption>{esc(alt)}</figcaption></figure>') if img else ""
        steps.append(f'<h2>{esc(title)}</h2><p>{fill(text)}</p>{fig}')
    body = f'''<section class="hero page-hero"><div class="wrap">{crumb_html(lang, crumbs)}<p class="eyebrow">{D["eyebrow"]}</p><h1>{esc(D["h1"])}</h1><p class="lead">{esc(D["lead"])}</p>
<div class="btn-row"><a class="btn btn-amber" href="{SMS}">{ICONS["text"]}{C.SMS_PAGE["cta_btn"]}</a></div></div></section><div class="stripe" role="none"></div>
<section><div class="wrap two-col"><div class="prose">
<h2>{D["summary_h"]}</h2>{fill(D["summary"])}
<div class="consent-box"><h2>{D["disclosure_h"]}</h2><p>{esc(C.SMS_PAGE["consent"])}</p><p class="small">{U["sms_short"]}</p></div>
{"".join(steps)}
<h2>{D["links_h"]}</h2>{D["links"]}
</div>{aside(lang, callbox(lang))}</div></section>'''
    return page(lang, pid, D["title"], D["desc"], body, crumbs=crumbs)


def not_found(lang):
    C = LANGS[lang]; U = C.UI; N = C.NOT_FOUND
    body = f'''<section class="hero page-hero"><div class="wrap"><p class="eyebrow">{N["eyebrow"]}</p><h1>{N["h1"]}</h1>
<p class="lead">{N["lead"]}</p>
<div class="btn-row"><a class="btn btn-red" href="{U["paths"]["home"]}">{N["home"]}</a><a class="btn btn-ghost" href="{TEL}">{ICONS["phone"]}{U["call"]} {CALL_DISPLAY}</a></div></div></section><div class="stripe" role="none"></div>
<section><div class="wrap"><h2>{N["popular"]}</h2><div class="grid grid-3">{"".join(service_card(lang, s) for s in C.SERVICES[:3])}</div></div></section>'''
    return page(lang, None, N["title"], N["desc"], body, robots="noindex,follow")


# ---------------------------------------------------------------- assets
def write(rel, content, mode="w"):
    p = os.path.join(DIST, rel.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, mode, **({"encoding": "utf-8"} if "b" not in mode else {})) as f:
        f.write(content)


def make_images():
    from PIL import Image, ImageDraw, ImageFont

    def font(size):
        for cand in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
            if os.path.exists(cand):
                return ImageFont.truetype(cand, size)
        return ImageFont.load_default()
    anton_ttf = os.path.join(ROOT, "assets", "Anton-Regular.ttf")

    def display(size):
        return ImageFont.truetype(anton_ttf, size) if os.path.exists(anton_ttf) else font(size)

    def badge(size):
        im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(im); s = size / 64
        d.ellipse([2 * s, 2 * s, 62 * s, 62 * s], fill="#c8202f", outline="#f2a516", width=max(1, int(3 * s)))
        d.ellipse([10 * s, 10 * s, 54 * s, 54 * s], fill="#15171b")
        d.line([(22 * s, 43 * s), (37 * s, 28 * s)], fill="#f2a516", width=max(2, int(6 * s)))
        d.ellipse([33 * s, 17 * s, 47 * s, 31 * s], fill="#f2a516")
        d.polygon([(41 * s, 16 * s), (48 * s, 23 * s), (44 * s, 25 * s), (39 * s, 20 * s)], fill="#15171b")
        return im

    os.makedirs(os.path.join(DIST, "icons"), exist_ok=True)
    for sz, name in [(180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")]:
        bg = Image.new("RGBA", (sz, sz), "#15171b")
        b = badge(int(sz * 0.86))
        bg.alpha_composite(b, ((sz - b.width) // 2, (sz - b.height) // 2))
        bg.convert("RGB").save(os.path.join(DIST, "icons", name), optimize=True)
    badge(64).save(os.path.join(DIST, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

    for fname, tag, call_lbl, text_lbl in [("og-image.png", "MOBILE MECHANIC · LUBBOCK COUNTY, TX", "CALL", "TEXT"),
                                            ("og-image-es.png", "MECÁNICO A DOMICILIO · CONDADO DE LUBBOCK", "LLAME", "MENSAJE")]:
        W, H = 1200, 630
        og = Image.new("RGB", (W, H), "#15171b")
        d = ImageDraw.Draw(og)
        for x in range(-H, W + H, 44):
            d.polygon([(x, H - 26), (x + 22, H - 26), (x + 48, H), (x + 26, H)], fill="#f2a516")
        d.rectangle([0, 0, W, 14], fill="#c8202f")
        b = badge(250)
        og.paste(b, (70, 150), b)
        d.text((360, 120), "RELIABLE AUTOMOTIVE", font=display(78), fill="#f4ecdc")
        d.text((360, 212), "SERVICES", font=display(78), fill="#f4ecdc")
        d.text((364, 318), tag, font=font(28), fill="#f2a516")
        d.text((360, 372), f"{call_lbl} {CALL_DISPLAY}", font=display(64), fill="#ffffff")
        d.text((360, 452), f"{text_lbl} {TEXT_DISPLAY}", font=display(48), fill="#f2a516")
        d.text((364, 530), "yourcarguy806.com", font=font(26), fill="#cfc6b4")
        og.save(os.path.join(DIST, fname), optimize=True)


def all_pages():
    """Yield (pid, {lang: html})."""
    out = []
    for lang in ("en", "es"):
        C = LANGS[lang]
        out += [(lang, ("home",), home(lang)), (lang, ("services",), services_index(lang)), (lang, ("area",), area_index(lang)),
                (lang, ("about",), about(lang)), (lang, ("contact",), contact(lang)),
                (lang, ("terms",), legal_page(lang, "terms", C.TERMS)), (lang, ("privacy",), legal_page(lang, "privacy", C.PRIVACY)), (lang, ("sms",), sms_page(lang)),
                (lang, ("sms_evidence",), sms_evidence_page(lang))]
        out += [(lang, ("service", s["key"]), service_page(lang, s)) for s in C.SERVICES]
        out += [(lang, ("area_page", a["key"]), area_page(lang, a)) for a in C.AREAS]
    return out


def main():
    # sanity: both languages define the same services/areas
    assert [s["key"] for s in EN.SERVICES] == [s["key"] for s in ES.SERVICES], "service keys differ"
    assert [a["key"] for a in EN.AREAS] == [a["key"] for a in ES.AREAS], "area keys differ"
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(STATIC, DIST)

    pages = all_pages()
    for lang, pid, content in pages:
        write(path_for(lang, pid) + "index.html", content)
    write("404.html", not_found("en"))
    write("es/404.html", not_found("es"))

    write("icons/icon.svg", LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    make_images()

    # sitemap with hreflang alternates
    urls = []
    for lang, pid, _ in pages:
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[k].UI["lang"]}" href="{SITE}{path_for(k, pid)}"/>' for k in ("en", "es"))
        alt += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{path_for("en", pid)}"/>'
        prio = "1.0" if pid == ("home",) else ("0.8" if pid[0] in ("service", "area_page") else "0.7")
        urls.append(f"<url><loc>{SITE}{path_for(lang, pid)}</loc><lastmod>{TODAY}</lastmod><priority>{prio}</priority>{alt}</url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": NAME, "short_name": "Your Car Guy", "start_url": "/", "display": "standalone",
        "background_color": "#15171b", "theme_color": "#15171b",
        "icons": [{"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))
    write("llms.txt", f"# {NAME}\n\n> Mobile mechanic (\"Your Car Guy 806\") serving Lubbock, Lubbock County, and surrounding West Texas towns. Call {CALL_DISPLAY}. Text {TEXT_DISPLAY}. Site available in English and Spanish ({SITE}/es/).\n\n## Services\n"
          + "".join(f"- [{s['name']}]({SITE}{path_for('en', ('service', s['key']))}): {s['short']}\n" for s in EN.SERVICES)
          + "\n## Service area\n" + "".join(f"- [{a['name']}, TX]({SITE}{path_for('en', ('area_page', a['key']))})\n" for a in EN.AREAS)
          + "".join(f"- {t}, TX\n" for t in OTHER_TOWNS))
    write("_headers", """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src 'self'; connect-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'

/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/icons/*
  Cache-Control: public, max-age=604800
/css/*
  Cache-Control: public, max-age=3600
/js/*
  Cache-Control: public, max-age=3600
""")
    write("_redirects", """/home / 301
/index.html / 301
/services.html /services/ 301
/contact.html /contact/ 301
/about.html /about/ 301
/areas /service-area/ 301
/service-areas /service-area/ 301
/privacy-policy /privacy/ 200
/privacy-policy/ /privacy/ 200
/privacy.html /privacy/ 200
/terms-of-service /terms/ 200
/terms-of-service/ /terms/ 200
/terms-and-conditions /terms/ 200
/terms-and-conditions/ /terms/ 200
/terms.html /terms/ 200
/sms-terms /sms/ 200
/sms-terms/ /sms/ 200
/sms-consent /sms/ 200
/text /sms/ 200
/text-us /sms/ 200
/sms-consent-evidence /sms-opt-in/ 200
/sms-consent-evidence/ /sms-opt-in/ 200
/opt-in /sms-opt-in/ 200
/espanol /es/ 301
/spanish /es/ 301
/es/services /es/servicios/ 301
/es/contact /es/contacto/ 301
""")
    print(f"Built {len(pages)} pages (+2 404s) into {DIST}")


if __name__ == "__main__":
    main()
