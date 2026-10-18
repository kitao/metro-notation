import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { experimental_readRawConfig } from 'wrangler';
import { SOURCES } from '../scripts/build-site.mjs';

const read = (path) => readFile(new URL(`../${path}`, import.meta.url), 'utf8');

test('the Worker serves only the built site under kitao.dev/metro-notation, rebuilt by Wrangler', () => {
  // Wrangler's own reader parses the file as Wrangler does, including comments.
  const { rawConfig: config } = experimental_readRawConfig({
    config: fileURLToPath(new URL('../wrangler.jsonc', import.meta.url)),
  });
  const { $schema, compatibility_date: compatibilityDate, build, ...deployment } = config;
  assert.equal($schema, './node_modules/wrangler/config-schema.json');
  assert.match(compatibilityDate, /^\d{4}-\d{2}-\d{2}$/);
  // An exact match also rejects additions such as "main", which would run Worker code.
  assert.deepEqual(deployment, {
    name: 'metro-notation',
    workers_dev: false,
    preview_urls: false,
    routes: [{ pattern: 'kitao.dev/metro-notation*', zone_name: 'kitao.dev' }],
    assets: { directory: './dist' },
  });
  assert.equal(build.command, 'node scripts/build-site.mjs');
  // wrangler dev rebuilds when any published source changes; dist/ itself is never watched.
  for (const source of SOURCES)
    assert.ok(
      build.watch_dir.some((watched) => source === watched || source.startsWith(`${watched}/`)),
      source,
    );
  assert.ok(!build.watch_dir.some((watched) => /^(?:\.\/)?dist(?:\/|$)/.test(watched)));
});

test('Python and Node pin the same Playwright release, so one browser install serves both', async () => {
  const { devDependencies } = JSON.parse(await read('package.json'));
  const python = (await read('pyproject.toml')).match(/"playwright==([^"]+)"/)?.[1];
  assert.equal(python, devDependencies['@playwright/test']);
});
