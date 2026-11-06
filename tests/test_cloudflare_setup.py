"""Tests for scripts/cloudflare_setup.py against an in-memory fake Cloudflare API."""
import io
import json
import os
import sys
import unittest
import urllib.error

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import cloudflare_setup as cs  # noqa: E402


class FakeCF:
    """Minimal fake of the Cloudflare endpoints the script uses."""

    def __init__(self, project=False, routes=None, worker_domains=None, dns=None, pages_domains=None):
        self.project = project
        self.routes = routes or []
        self.worker_domains = worker_domains or []
        self.pages_domains = pages_domains or []
        self.dns = dns if dns is not None else []
        self.calls = []
        self.n = 0

    def opener(self, req):
        method, url = req.get_method(), req.full_url
        path = url.split("/client/v4", 1)[1].split("?", 1)[0]
        body = json.loads(req.data) if req.data else None
        self.calls.append((method, path, body))
        status, result = self.route(method, path, body)
        payload = json.dumps({"success": status < 400, "result": result,
                              "errors": [] if status < 400 else [{"message": f"fake {status}"}]}).encode()
        if status >= 400:
            raise urllib.error.HTTPError(url, status, "err", {}, io.BytesIO(payload))
        return _Resp(payload, status)

    def route(self, m, p, b):
        A = "/accounts/acct"
        if p == f"{A}/pages/projects/{cs.PROJECT}" and m == "GET":
            return (200, {"name": cs.PROJECT}) if self.project else (404, None)
        if p == f"{A}/pages/projects" and m == "POST":
            self.project = True
            return 200, b
        if p == "/zones" and m == "GET":
            return 200, [{"id": "z1", "name": cs.ZONE}]
        if p == "/zones/z1/workers/routes":
            return 200, self.routes
        if p == f"{A}/workers/domains":
            return 200, self.worker_domains
        dpath = f"{A}/pages/projects/{cs.PROJECT}/domains"
        if p == dpath and m == "GET":
            return 200, self.pages_domains
        if p == dpath and m == "POST":
            self.pages_domains.append({"name": b["name"], "status": "pending"})
            return 200, self.pages_domains[-1]
        if p == "/zones/z1/dns_records" and m == "GET":
            return 200, self.dns
        if p == "/zones/z1/dns_records" and m == "POST":
            self.n += 1
            rec = {"id": f"new{self.n}", **b}
            self.dns.append(rec)
            return 200, rec
        if p.startswith("/zones/z1/dns_records/") and m == "DELETE":
            rid = p.rsplit("/", 1)[1]
            self.dns = [r for r in self.dns if r["id"] != rid]
            return 200, {"id": rid}
        return 404, None


class _Resp:
    def __init__(self, payload, status):
        self._p, self.status = payload, status

    def read(self):
        return self._p

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


MAIL = [
    {"id": "mx1", "type": "MX", "name": cs.ZONE, "content": "route1.mx.cloudflare.net"},
    {"id": "spf", "type": "TXT", "name": cs.ZONE, "content": "v=spf1 include:_spf.mx.cloudflare.net ~all"},
    {"id": "dkim", "type": "TXT", "name": "cf2024-1._domainkey.yourcarguy806.com", "content": "v=DKIM1; p=abc"},
    {"id": "dmarc", "type": "TXT", "name": "_dmarc.yourcarguy806.com", "content": "v=DMARC1; p=none"},
]
SHOPCRANK_LEFTOVER_A = [
    {"id": "a1", "type": "A", "name": cs.ZONE, "content": "104.21.17.176", "proxied": True},
    {"id": "a2", "type": "A", "name": cs.WWW, "content": "104.21.17.188", "proxied": True},
]


class SetupTests(unittest.TestCase):
    def client(self, fake):
        return cs.Client("tok", opener=fake.opener)

    def test_creates_missing_project_once(self):
        fake = FakeCF(project=False)
        self.assertEqual(cs.ensure_project(self.client(fake), "acct"), "created")
        self.assertEqual(cs.ensure_project(self.client(fake), "acct"), "exists")
        posts = [c for c in fake.calls if c[0] == "POST"]
        self.assertEqual(posts, [("POST", "/accounts/acct/pages/projects", {"name": "yourcarguy806", "production_branch": "main"})])

    def test_refuses_while_shopcrank_still_holds_the_domain(self):
        fake = FakeCF(project=True, routes=[{"id": "r", "pattern": "www.yourcarguy806.com/*", "script": "shopcrank-api"}],
                      dns=MAIL + SHOPCRANK_LEFTOVER_A)
        with self.assertRaises(cs.CloudflareError) as ctx:
            cs.attach_domains(self.client(fake), "acct")
        self.assertIn("PR #199", str(ctx.exception))
        # Nothing was changed.
        self.assertFalse([c for c in fake.calls if c[0] != "GET"])

    def test_refuses_while_a_worker_custom_domain_holds_www(self):
        fake = FakeCF(project=True, worker_domains=[{"hostname": cs.WWW, "service": "mechpro-api"}])
        with self.assertRaises(cs.CloudflareError):
            cs.attach_domains(self.client(fake), "acct")

    def test_attaches_domains_and_replaces_only_website_records_keeping_email(self):
        other = {"id": "o1", "type": "A", "name": "shop.yourcarguy806.com", "content": "1.2.3.4"}
        unrelated_route = {"id": "r", "pattern": "www.yourcarguy806.com/blog/*", "script": "someone-else"}
        fake = FakeCF(project=True, routes=[unrelated_route], dns=MAIL + SHOPCRANK_LEFTOVER_A + [other])
        result = cs.attach_domains(self.client(fake), "acct")
        self.assertEqual(result["added"], [cs.WWW, cs.ZONE])
        names = {r["id"] for r in fake.dns}
        for keep in ("mx1", "spf", "dkim", "dmarc", "o1"):
            self.assertIn(keep, names, f"{keep} must not be touched")
        self.assertNotIn("a1", names)
        self.assertNotIn("a2", names)
        cnames = sorted((r["name"], r["content"], r["proxied"]) for r in fake.dns if r["type"] == "CNAME")
        self.assertEqual(cnames, [(cs.WWW, "yourcarguy806.pages.dev", True), (cs.ZONE, "yourcarguy806.pages.dev", True)])
        deleted = [c[1].rsplit("/", 1)[1] for c in fake.calls if c[0] == "DELETE"]
        self.assertEqual(sorted(deleted), ["a1", "a2"])

    def test_second_run_changes_nothing(self):
        fake = FakeCF(project=True, dns=MAIL + SHOPCRANK_LEFTOVER_A)
        cs.attach_domains(self.client(fake), "acct")
        before = len([c for c in fake.calls if c[0] != "GET"])
        again = cs.attach_domains(self.client(fake), "acct")
        after = len([c for c in fake.calls if c[0] != "GET"])
        self.assertEqual(before, after)
        self.assertEqual(again["added"], [])
        self.assertEqual(again["dns"], [])

    def test_verify_requires_the_business_site_not_shopcrank(self):
        def fake_fetch(body, status=200):
            return lambda url: _Resp(body.encode(), status)
        ok, _ = cs.verify(fetch=fake_fetch("<title>Mobile Mechanic | Reliable Automotive Services</title>"), attempts=1, delay=0)
        self.assertTrue(ok)
        ok, _ = cs.verify(fetch=fake_fetch("<title>ShopCrank | Dispatch</title>"), attempts=1, delay=0)
        self.assertFalse(ok)

    def test_missing_secrets_exit_with_a_clear_message(self):
        env = dict(os.environ)
        os.environ.pop("CLOUDFLARE_API_TOKEN", None)
        os.environ.pop("CLOUDFLARE_ACCOUNT_ID", None)
        try:
            self.assertEqual(cs.main(["attach-domains"]), 2)
        finally:
            os.environ.clear()
            os.environ.update(env)


if __name__ == "__main__":
    unittest.main()
