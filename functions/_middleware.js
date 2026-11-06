// Cloudflare Pages middleware for yourcarguy806.com.
// - Sends the bare domain to www so search engines see one site.
// - Keeps preview copies on *.pages.dev out of search results.
const CANONICAL_HOST = 'www.yourcarguy806.com';
const APEX_HOST = 'yourcarguy806.com';

export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.hostname === APEX_HOST) {
    url.hostname = CANONICAL_HOST;
    url.protocol = 'https:';
    return new Response(null, { status: 301, headers: { Location: url.toString() } });
  }
  const response = await context.next();
  if (url.hostname.endsWith('.pages.dev')) {
    const copy = new Response(response.body, response);
    copy.headers.set('X-Robots-Tag', 'noindex');
    return copy;
  }
  return response;
}
