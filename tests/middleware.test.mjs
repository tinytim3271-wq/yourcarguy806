import test from 'node:test';
import assert from 'node:assert/strict';
import { onRequest } from '../functions/_middleware.js';

const page = () => new Response('<h1>ok</h1>', { status: 200, headers: { 'Content-Type': 'text/html' } });
const ctx = (url) => ({ request: new Request(url), next: async () => page() });

test('bare domain 301s to www, keeping path and query', async () => {
  const r = await onRequest(ctx('https://yourcarguy806.com/es/contacto/?a=1'));
  assert.equal(r.status, 301);
  assert.equal(r.headers.get('location'), 'https://www.yourcarguy806.com/es/contacto/?a=1');
  const http = await onRequest(ctx('http://yourcarguy806.com/'));
  assert.equal(http.headers.get('location'), 'https://www.yourcarguy806.com/');
});

test('www is served as-is and indexable', async () => {
  const r = await onRequest(ctx('https://www.yourcarguy806.com/services/'));
  assert.equal(r.status, 200);
  assert.equal(r.headers.get('x-robots-tag'), null);
  assert.equal(await r.text(), '<h1>ok</h1>');
});

test('pages.dev preview copies are kept out of search results', async () => {
  const r = await onRequest(ctx('https://abc123.yourcarguy806.pages.dev/'));
  assert.equal(r.status, 200);
  assert.equal(r.headers.get('x-robots-tag'), 'noindex');
});
