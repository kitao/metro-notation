import assert from 'node:assert/strict';
import { cp, mkdtemp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { buildSite, renderReadme, SHEETS } from '../scripts/build-site.mjs';
import { cloudflare } from '../scripts/cloudflare.mjs';

const ROOT = fileURLToPath(new URL('../', import.meta.url));

test('publication contains only the page, style, favicons, and unchanged reviewed sheets', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'metro-site-test-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  for (const name of ['README.md', 'web', 'sheets']) {
    await cp(join(ROOT, name), join(root, name), { recursive: true });
  }
  await mkdir(join(root, 'dist'), { recursive: true });
  await writeFile(join(root, 'dist', 'old-private-file'), 'do not publish');
  const output = await buildSite(root);
  assert.deepEqual((await readdir(output)).sort(), ['404.html', '_headers', 'metro-notation']);
  const site = join(output, 'metro-notation');
  assert.deepEqual((await readdir(site)).sort(), [
    'favicon.png',
    'favicon.svg',
    'index.html',
    'sheets',
    'styles.css',
  ]);
  assert.deepEqual((await readdir(join(site, 'sheets'))).sort(), [...SHEETS].sort());
  for (const name of SHEETS) {
    assert.deepEqual(
      await readFile(join(site, 'sheets', name)),
      await readFile(join(ROOT, 'sheets', name)),
    );
  }
  const html = await readFile(join(site, 'index.html'), 'utf8');
  assert.equal((html.match(/class="badges"/g) || []).length, 1);
  assert.equal((html.match(/alt="GitHub stars"/g) || []).length, 1);
  assert.equal((html.match(/alt="GitHub Sponsors"/g) || []).length, 1);
  assert.equal((html.match(/alt="Patreon"/g) || []).length, 1);
  assert.equal((html.match(/alt="Support me on Ko-fi"/g) || []).length, 1);
  assert.match(
    html,
    /name="description" content="Metro Notation represents Rubik's Cube algorithms as metro-style diagrams\. Their shapes help you remember the moves\."/,
  );
  assert.equal((html.match(/class="sheet-row"/g) || []).length, 2);
  assert.equal((html.match(/<a href="sheets\/[^"]+"><img/g) || []).length, 4);
  assert.match(html, /<p lang="ja">/);
  assert.doesNotMatch(html, /\{\{|<script|width="49%"/);
  for (const match of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    const link = match[1];
    if (/^(?:https?:|data:)/.test(link)) continue;
    // Shared fonts are served by kitao-dev, outside this publication's assets.
    if (link === '/assets/fonts/noto-sans-jp.css') continue;
    await readFile(join(site, link.replace(/^\/metro-notation\//, '')));
  }
  assert.match(html, /href="https:\/\/github.com\/kitao\/metro-notation\/blob\/main\/LICENSE"/);
  assert.match(
    html,
    /href="https:\/\/github.com\/kitao\/metro-notation\/blob\/main\/src\/metronotation\/assets\/fonts\/README.md"/,
  );
  // A failed rebuild must leave the previous reviewed publication available.
  await rm(join(root, 'sheets', SHEETS[0]));
  await assert.rejects(buildSite(root));
  assert.equal(await readFile(join(site, 'index.html'), 'utf8'), html);
});

test('README text remains the page source and unexpected images stop the build', () => {
  const rendered = renderReadme('# Metro Notation\n\nUpdated **description**.\n\n説明です。\n');
  assert.match(rendered, /Updated <strong>description<\/strong>\./);
  assert.match(rendered, /<p lang="ja">説明です。<\/p>/);
  assert.throws(
    () => renderReadme('<img src="algorithms/photos/private.png">'),
    /unexpected sheet/,
  );
  assert.throws(
    () =>
      renderReadme(
        '<img data-src="https://img.shields.io/badge/ok" src="algorithms/photos/private.png">',
      ),
    /unexpected sheet/,
  );
});

test('Cloudflare rejects credential overrides and always requires OS keychain storage', () => {
  for (const key of ['CLOUDFLARE_API_TOKEN', 'CF_API_TOKEN', 'CLOUDFLARE_API_KEY', 'CF_API_KEY']) {
    assert.throws(
      () =>
        cloudflare(['deploy'], { [key]: 'synthetic-test-value' }, () => {
          assert.fail('Credentials must be rejected before invoking Wrangler');
        }),
      /OS keychain/,
    );
  }
  const status = cloudflare(
    ['deploy', '--dry-run'],
    { CLOUDFLARE_AUTH_USE_KEYRING: 'false' },
    (command, args, options) => {
      assert.equal(command, process.execPath);
      assert.deepEqual(args.slice(1), ['deploy', '--dry-run']);
      assert.equal(options.env.CLOUDFLARE_AUTH_USE_KEYRING, 'true');
      assert.equal(options.env.WRANGLER_SEND_METRICS, 'false');
      assert.equal(options.env.WRANGLER_LOG_SANITIZE, 'true');
      assert.equal(options.env.WRANGLER_WRITE_LOGS, 'false');
      return { status: 7 };
    },
  );
  assert.equal(status, 7);
});
