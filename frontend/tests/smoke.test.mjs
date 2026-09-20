import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'

const readProjectFile = (path) => readFile(new URL(`../${path}`, import.meta.url), 'utf8')

test('the application shell exposes the required accessible landmarks', async () => {
  const html = await readProjectFile('index.html')
  assert.match(html, /<main[\s>]/)
  assert.match(html, /role="tablist"/)
  assert.match(html, /aria-live="polite"/)
})

test('the client calls every supported backend route through the configured API base URL', async () => {
  const app = await readProjectFile('public/static/app.js')
  for (const route of [
    '/api/intake',
    '/api/rights',
    '/api/documents/generate',
    '/api/documents/download-pdf',
    '/api/compliance/verify-citations',
  ]) {
    assert.match(app, new RegExp(`apiUrl\\('${route.replaceAll('/', '\\/')}\\'\\)`))
  }
})
