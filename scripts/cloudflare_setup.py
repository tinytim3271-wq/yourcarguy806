#!/usr/bin/env python3
"""Cloudflare setup for www.yourcarguy806.com (Pages project, custom domains, DNS).

  python3 scripts/cloudflare_setup.py ensure-project   # before deploy
  python3 scripts/cloudflare_setup.py attach-domains   # after deploy
  python3 scripts/cloudflare_setup.py verify           # check the live site
  python3 scripts/cloudflare_setup.py bot-fight-off    # keep Bot Fight Mode off

Needs CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID. The token needs
Account > Cloudflare Pages > Edit, Zone > DNS > Edit and Zone > Zone > Read
for yourcarguy806.com.

DNS safety: only A/AAAA/CNAME records on exactly yourcarguy806.com and
www.yourcarguy806.com are ever changed. MX, TXT (SPF/DKIM/DMARC) and every
other name are left alone, so email keeps working.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://api.cloudflare.com/client/v4"
PROJECT = "yourcarguy806"
ZONE = "yourcarguy806.com"
WWW = "www.yourcarguy806.com"
HOSTS = [WWW, ZONE]
PAGES_TARGET = f"{PROJECT}.pages.dev"
# Anything ShopCrank used to bind to this domain. If one is still here, the
# ShopCrank cleanup (PR #199) has not been merged and provisioned yet.
SHOPCRANK_SERVICES = {"shopcrank-api", "mechpro-api", "shopcrank-dispatch"}


class CloudflareError(Exception):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status


class Client:
    def __init__(self, token, opener=None):
        self.token = token
        self.opener = opener or urllib.request.urlopen

    def request(self, method, path, body=None, query=None):
        url = API + path
        if query:
            url += "?" + "&".join(f"{k}={urllib.request.quote(str(v))}" for k, v in query.items())
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": f"Bearer {self.token}", "Content-Type": "application/json",
            "User-Agent": "yourcarguy806-deploy"})
        try:
            with self.opener(req) as resp:
                payload = json.loads(resp.read() or b"{}")
                status = resp.status
        except urllib.error.HTTPError as e:
            status = e.code
            try:
                payload = json.loads(e.read() or b"{}")
            except ValueError:
                payload = {}
        if status >= 400 or payload.get("success") is False:
            msgs = "; ".join(err.get("message", "") for err in payload.get("errors", [])) or f"HTTP {status}"
            raise CloudflareError(f"{method} {path}: {msgs}", status)
        return payload


def ensure_project(cf, account):
    path = f"/accounts/{account}/pages/projects/{PROJECT}"
    try:
        cf.request("GET", path)
        return "exists"
    except CloudflareError as e:
        if e.status != 404:
            raise
    cf.request("POST", f"/accounts/{account}/pages/projects",
               {"name": PROJECT, "production_branch": "main"})
    return "created"


def find_zone(cf, account):
    zones = cf.request("GET", "/zones", query={"name": ZONE, "account.id": account}).get("result") or []
    zone = next((z for z in zones if z.get("name") == ZONE), None)
    if not zone:
        raise CloudflareError(f"Zone {ZONE} was not found on this Cloudflare account (or the token can't read it).")
    return zone["id"]


def shopcrank_leftovers(cf, account, zone_id):
    left = []
    for route in cf.request("GET", f"/zones/{zone_id}/workers/routes").get("result") or []:
        if route.get("script") in SHOPCRANK_SERVICES:
            left.append(f"Worker route {route.get('pattern')} -> {route.get('script')}")
    for dom in cf.request("GET", f"/accounts/{account}/workers/domains").get("result") or []:
        if dom.get("hostname") in HOSTS:
            left.append(f"Worker custom domain {dom.get('hostname')} -> {dom.get('service')}")
    return left


def ensure_dns(cf, zone_id):
    """Point both hostnames at the Pages project with proxied CNAMEs."""
    changes = []
    records = cf.request("GET", f"/zones/{zone_id}/dns_records", query={"per_page": 500}).get("result") or []
    for host in HOSTS:
        mine = [r for r in records if r.get("name") == host and r.get("type") in ("A", "AAAA", "CNAME")]
        good = [r for r in mine if r["type"] == "CNAME" and r.get("content") == PAGES_TARGET and r.get("proxied")]
        for r in mine:
            if r in good[:1]:
                continue
            cf.request("DELETE", f"/zones/{zone_id}/dns_records/{r['id']}")
            changes.append(f"removed {r['type']} {host} -> {r.get('content')}")
        if not good:
            cf.request("POST", f"/zones/{zone_id}/dns_records",
                       {"type": "CNAME", "name": host, "content": PAGES_TARGET, "proxied": True, "ttl": 1,
                        "comment": "Reliable Automotive website (Cloudflare Pages)"})
            changes.append(f"added CNAME {host} -> {PAGES_TARGET}")
    return changes


def attach_domains(cf, account):
    zone_id = find_zone(cf, account)
    left = shopcrank_leftovers(cf, account, zone_id)
    if left:
        raise CloudflareError(
            "ShopCrank still holds this domain:\n  - " + "\n  - ".join(left)
            + "\nMerge ShopCrank PR #199 and let its 'Provision shopcrank.com' workflow finish, then re-run this deploy.")
    path = f"/accounts/{account}/pages/projects/{PROJECT}/domains"
    have = {d.get("name") for d in cf.request("GET", path).get("result") or []}
    added = []
    for host in HOSTS:
        if host not in have:
            cf.request("POST", path, {"name": host})
            added.append(host)
    dns = ensure_dns(cf, zone_id)
    status = {d.get("name"): d.get("status") for d in cf.request("GET", path).get("result") or []}
    return {"added": added, "dns": dns, "status": status}


BOT_PERMISSION_HINT = ("The API token can't change Bot Fight Mode. Edit the token in Cloudflare "
                       "(My Profile > API Tokens) and add Zone > Bot Management > Edit for yourcarguy806.com, "
                       "or turn it off by hand: yourcarguy806.com > Security > Bots > Bot Fight Mode.")


def bot_fight_off(cf, account):
    """Turn off Bot Fight Mode and its JavaScript detections so compliance reviewers and
    other legitimate automated checks can always read the site. Returns a status dict."""
    zone_id = find_zone(cf, account)
    path = f"/zones/{zone_id}/bot_management"
    try:
        current = cf.request("GET", path).get("result") or {}
    except CloudflareError as e:
        if e.status in (401, 403):
            return {"action": "no_permission", "hint": BOT_PERMISSION_HINT}
        raise
    if not current.get("fight_mode") and not current.get("enable_js"):
        return {"action": "already_off"}
    try:
        cf.request("PUT", path, {"fight_mode": False, "enable_js": False})
    except CloudflareError as e:
        if e.status in (401, 403):
            return {"action": "no_permission", "hint": BOT_PERMISSION_HINT, "was": current}
        raise
    after = cf.request("GET", path).get("result") or {}
    if after.get("fight_mode") or after.get("enable_js"):
        raise CloudflareError(f"Bot Fight Mode is still on after the update: {after}")
    return {"action": "turned_off", "was": {k: current.get(k) for k in ("fight_mode", "enable_js")}}


def verify(fetch=None, attempts=30, delay=20):
    fetch = fetch or (lambda url: urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "yourcarguy806-verify"}), timeout=20))
    last = ""
    for _ in range(attempts):
        try:
            with fetch(f"https://{WWW}/") as resp:
                body = resp.read().decode("utf-8", "replace")
                if resp.status == 200 and "Reliable Automotive" in body and "ShopCrank" not in body:
                    return True, "www.yourcarguy806.com is serving the Reliable Automotive site"
                last = f"HTTP {resp.status}, unexpected content"
        except Exception as e:  # DNS/TLS can take a few minutes on first attach
            last = str(e)
        time.sleep(delay)
    return False, f"site not live yet ({last}). Domains can take up to ~15 minutes to activate; re-run verify later."


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else ""
    if cmd == "verify":
        ok, msg = verify()
        print(msg)
        return 0 if ok else 1
    token, account = os.environ.get("CLOUDFLARE_API_TOKEN"), os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    if not token or not account:
        print("Missing CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID (add them as GitHub repo secrets).", file=sys.stderr)
        return 2
    cf = Client(token)
    try:
        if cmd == "ensure-project":
            print(f"Pages project {PROJECT}: {ensure_project(cf, account)}")
        elif cmd == "bot-fight-off":
            r = bot_fight_off(cf, account)
            if r["action"] == "no_permission":
                print(f"::warning title=Bot Fight Mode not changed::{r['hint']}")
            else:
                print(f"Bot Fight Mode: {r['action']}" + (f" (was {r['was']})" if r.get("was") else ""))
        elif cmd == "attach-domains":
            r = attach_domains(cf, account)
            print(f"Custom domains added: {r['added'] or 'none (already attached)'}")
            for line in r["dns"] or ["DNS already correct"]:
                print(f"DNS: {line}")
            print(f"Domain status: {r['status']}")
        else:
            print(__doc__)
            return 1
    except CloudflareError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
