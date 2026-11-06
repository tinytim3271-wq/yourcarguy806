# yourcarguy806.com — Reliable Automotive Services

A static website (no server, no database) built for Cloudflare Pages.

- `content_en.py` / `content_es.py` — all English and Spanish wording (services, towns, FAQs, Terms, Privacy). Edit both when you change content; the build stops if they don't list the same services and towns.
- `build.py` — generates every page in both languages (English at `/`, Spanish at `/es/`). Phone numbers are set at the top: calls go to (806) 686-0709, texts and the contact form go to (806) 776-4460.
- `static/` — CSS, JavaScript, and self-hosted fonts.
- `dist/` — the finished website. **This is the folder you upload to Cloudflare.**
- `tests/` — smoke tests (`python3 tests/static_checks.py`, `python3 tests/browser_checks.py`).

## Publishing (automatic)
Every push to `main` builds the site, runs all the tests, and publishes to Cloudflare Pages through `.github/workflows/deploy.yml`:
1. Builds both languages and runs the static checks, HTML validation, deploy-script tests, and Chrome browser tests. Nothing publishes if any test fails.
2. Creates the `yourcarguy806` Pages project if it doesn't exist, then deploys `dist/`.
3. Attaches `www.yourcarguy806.com` and `yourcarguy806.com`, and points both at Pages with proxied CNAME records. Only A/AAAA/CNAME records on exactly those two names are ever changed. **Email records (MX, SPF, DKIM, DMARC) are never touched.**
4. Checks that the live site is the Reliable Automotive site.

The bare domain redirects to www through `functions/_middleware.js`, and preview copies on `*.pages.dev` are hidden from Google.

**One-time setup:** add these repository secrets under GitHub → Settings → Secrets and variables → Actions:
- `CLOUDFLARE_ACCOUNT_ID`: shown on the right side of the Cloudflare dashboard home page.
- `CLOUDFLARE_API_TOKEN`: create it at Cloudflare → My Profile → API Tokens → Create Token → Custom token, with these permissions:
  - Account › Cloudflare Pages › Edit
  - Zone › DNS › Edit (zone: yourcarguy806.com)
  - Zone › Zone › Read (zone: yourcarguy806.com)

If ShopCrank still holds the domain, the deploy stops with a message to merge ShopCrank PR #199 first. Nothing is changed in that case.

To re-run a deploy: GitHub → Actions → "Build, test & deploy yourcarguy806.com" → Run workflow.

## After it's live: SEO steps that matter most

1. **Google Business Profile** (business.google.com). This is the biggest factor for "mechanic near me" searches. Set it up as a *service-area business* (hide the street address, list Lubbock County towns), category **Mobile mechanic** plus **Auto repair shop**, phone (806) 686-0709, website https://www.yourcarguy806.com. Ask happy customers for Google reviews.
2. **Google Search Console** (search.google.com/search-console): add a *Domain* property for yourcarguy806.com. Cloudflare can add the verification DNS record automatically. Then submit `https://www.yourcarguy806.com/sitemap.xml`.
3. **Bing Webmaster Tools**: import from Search Console in one click.
4. Use the exact same business name, phone, and website on Facebook, Yelp, Nextdoor, and Apple Business Connect. Consistent listings help local ranking.
5. Add real job photos over time. Original photos of your truck and work help both trust and rankings.

## Language setting
- Every page has an English/Español switch in the header, plus a "Language / Idioma" setting in the footer. The visitor's choice is remembered in their browser, so the site keeps opening in that language.
- Visitors whose phone or browser is set to Spanish get a one-time prompt offering the Spanish site. Nobody is redirected automatically, so Google indexes both languages.
- Each English page is linked to its Spanish twin (hreflang), so Google shows Spanish speakers the Spanish page.

## Things to confirm or edit
- The service list: delete anything you don't do on site, and add anything missing.
- Business hours aren't listed anywhere yet. Add them once they're set (and to the Google Business Profile).
- The contact form and every "Text" button open a pre-filled **text message** to (806) 776-4460. Calls go to (806) 686-0709.
- The Spanish site says the *website* is in Spanish. It doesn't promise Spanish over the phone. If you or a tech speak Spanish, say so in the "¿Hablan español?" FAQ in content_es.py.
- Terms of Service and Privacy Policy (English and Spanish, with the English version controlling) are solid starting points, not legal advice. Have them reviewed if you want certainty, especially the warranty and liability sections.
