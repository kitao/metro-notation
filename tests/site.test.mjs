import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import {
  cp,
  lstat,
  mkdir,
  mkdtemp,
  readdir,
  readFile,
  rename,
  rm,
  symlink,
  writeFile,
} from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import {
  buildSite,
  pngSize,
  renderReadme,
  SHEET_IMAGES,
  SHEETS,
  SOURCES,
} from '../scripts/build-site.mjs';

const ROOT = fileURLToPath(new URL('../', import.meta.url));

// Each test builds a disposable copy, so the repository's dist/ is never written to.
async function withRoot(run) {
  const temporary = await mkdtemp(join(tmpdir(), 'metro-site-test-'));
  try {
    const root = join(temporary, 'root');
    for (const name of ['README.md', 'web', 'sheets']) {
      await cp(join(ROOT, name), join(root, name), { recursive: true });
    }
    await run(root, temporary);
  } finally {
    await rm(temporary, { recursive: true, force: true });
  }
}

const listFiles = async (directory) =>
  (await readdir(directory, { recursive: true, withFileTypes: true }))
    .filter((entry) => !entry.isDirectory())
    .map((entry) => join(entry.parentPath, entry.name).slice(directory.length + 1))
    .sort();

test('publication contains only the pages, headers, style, favicons, preview and unchanged reviewed sheets', async () => {
  await withRoot(async (root) => {
    await mkdir(join(root, 'dist'));
    await writeFile(join(root, 'dist', 'old-private-file'), 'do not publish');
    await writeFile(join(root, 'web', '.DS_Store'), 'local metadata');
    const output = await buildSite(root);
    assert.deepEqual(
      await listFiles(output),
      [
        '_headers',
        ...['favicon.png', 'favicon.svg', 'index.html', 'styles.css', 'og.png'].map((name) =>
          join('metro-notation', name),
        ),
        ...SHEETS.map((name) => join('metro-notation', 'sheets', name)),
      ].sort(),
    );
    const site = join(output, 'metro-notation');
    for (const name of SHEETS) {
      assert.deepEqual(
        await readFile(join(site, 'sheets', name)),
        await readFile(join(ROOT, 'sheets', name)),
      );
    }
    const html = await readFile(join(site, 'index.html'), 'utf8');
    for (const alt of ['GitHub stars', 'GitHub Sponsors', 'Patreon', 'Support me on Ko-fi']) {
      assert.equal(html.split(`alt="${alt}"`).length, 2, alt);
    }
    assert.match(
      html,
      /name="description" content="Metro Notation represents Rubik's Cube algorithms as metro-style diagrams\. Their shapes help you remember the moves\."/,
    );
    assert.equal(html.match(/class="sheet-row"/g).length, 2);
    // Each displayed PNG links to itself and reserves its real aspect ratio.
    const images = [...html.matchAll(/<a href="sheets\/([^"]+)"><img ([^>]+)>/g)];
    assert.deepEqual(
      images.map(([, name]) => name),
      SHEET_IMAGES,
    );
    for (const [, name, attributes] of images) {
      assert.match(attributes, new RegExp(`^src="sheets/${name}"`));
      const { width, height } = pngSize(await readFile(join(ROOT, 'sheets', name)));
      assert.match(attributes, new RegExp(` width="${width}" height="${height}"$`));
    }
    assert.equal(html.match(/<p lang="ja">/g).length, 3);
    assert.doesNotMatch(html, /\{\{|<script|%"/);
    for (const [, link] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
      if (/^https?:/.test(link)) continue;
      await readFile(join(site, link.replace(/^\/metro-notation\//, '')));
    }
    // The social card uses a published PNG with matching dimensions.
    const meta = (property) =>
      html.match(new RegExp(`<meta property="og:${property}" content="([^"]+)"`))[1];
    const image = new URL(meta('image'));
    assert.equal(image.origin, new URL(meta('url')).origin);
    const preview = await readFile(join(site, image.pathname.replace(/^\/metro-notation\//, '')));
    assert.deepEqual(pngSize(preview), {
      width: Number(meta('image:width')),
      height: Number(meta('image:height')),
    });
    for (const path of ['LICENSE', 'src/metronotation/assets/fonts/README.md']) {
      assert.match(
        html,
        new RegExp(`href="https://github.com/kitao/metro-notation/blob/main/${path}"`),
      );
    }
    // The headers are published as written.
    for (const name of ['_headers']) {
      assert.deepEqual(await readFile(join(output, name)), await readFile(join(ROOT, 'web', name)));
    }
    // A failed rebuild must leave the previous reviewed publication available.
    await rm(join(root, 'sheets', SHEETS[0]));
    await assert.rejects(buildSite(root));
    assert.deepEqual(
      (await readdir(root)).filter((name) => name.startsWith('.site-')),
      [],
    );
    assert.equal(await readFile(join(site, 'index.html'), 'utf8'), html);
  });
});

test('SOURCES lists every file the publication is built from', async (t) => {
  // config.test.mjs checks that wrangler dev watches these files, so none may be missing.
  const root = await mkdtemp(join(tmpdir(), 'metro-sources-test-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  for (const file of SOURCES) {
    await mkdir(dirname(join(root, file)), { recursive: true });
    await cp(join(ROOT, file), join(root, file));
  }
  await buildSite(root);
});

test('README text stays literal and escaped in the title, description, links and body', async () => {
  await withRoot(async (root) => {
    const readme = await readFile(join(root, 'README.md'), 'utf8');
    const first = readme.match(/^\*\*Metro Notation\*\*.*$/m)[0];
    // Replacer functions keep the "$" patterns of these test strings literal as well.
    const edited = readme
      .replace('# Metro Notation', () => `# Metro "$&" & $' {{content}}`)
      .replace(first, () => `Lead $& and $' with "quotes" & a < b > c.`);
    await writeFile(
      join(root, 'README.md'),
      `${edited}\nSee [notes](docs/x?a=1&b=2) for $& and $'.\n`,
    );
    const html = await readFile(join(await buildSite(root), 'metro-notation/index.html'), 'utf8');
    assert.match(html, /<title>Metro &quot;\$&amp;&quot; &amp; \$' \{\{content\}\}<\/title>/);
    assert.match(
      html,
      /<meta name="description" content="Lead \$&amp; and \$' with &quot;quotes&quot; &amp; a &lt; b &gt; c\." \/>/,
    );
    assert.match(
      html,
      /<a href="https:\/\/github.com\/kitao\/metro-notation\/blob\/main\/docs\/x\?a=1&amp;b=2">notes<\/a> for \$&amp; and \$'\./,
    );
    assert.equal(html.match(/<main>/g).length, 1);
    assert.doesNotMatch(html, /<main>\{\{content\}\}/);
  });
});

test('an unknown placeholder in the page template stops the build', async () => {
  await withRoot(async (root) => {
    const template = await readFile(join(root, 'web/index.html'), 'utf8');
    await writeFile(join(root, 'web/index.html'), template.replace('</main>', '{{footer}}</main>'));
    await assert.rejects(buildSite(root), /Unknown placeholder \{\{footer\}\}/);
  });
});

test('the title and description are the first heading and paragraph as plain text', async () => {
  await withRoot(async (root) => {
    const readme = await readFile(join(root, 'README.md'), 'utf8');
    const first = readme.match(/^\*\*Metro Notation\*\*.*$/m)[0];
    await writeFile(
      join(root, 'README.md'),
      readme
        .replace('# Metro Notation', '# Metro `Notation` &amp; *more*')
        .replace(
          first,
          '**Metro** uses [routes](docs/design.md), *shapes*, `R U` &amp; <a href="https://example.com/?a>b">"more"</a>.',
        ),
    );
    const html = await readFile(join(await buildSite(root), 'metro-notation/index.html'), 'utf8');
    assert.match(html, /<title>Metro Notation &amp; more<\/title>/);
    assert.match(
      html,
      /<meta name="description" content="Metro uses routes, shapes, R U &amp; &quot;more&quot;\." \/>/,
    );
  });
});

test('README markup is rendered and unexpected images stop the build', () => {
  const rendered = renderReadme('# Metro Notation\n\nUpdated **description**.\n\n説明です。\n', {});
  assert.match(rendered, /Updated <strong>description<\/strong>\./);
  assert.match(rendered, /<p lang="ja">説明です。<\/p>/);
  assert.equal(
    renderReadme('## Notes / メモ\n\n## Input / Output\n', {}),
    '<h2>Notes / <span lang="ja">メモ</span></h2>\n<h2>Input / Output</h2>\n',
  );
  const sizes = { 'pll.png': { width: 30, height: 20 } };
  const sized = renderReadme(
    '<p><a href="sheets/pll.png"><img src="sheets/pll.png" alt="PLL" width="49%" /></a></p>',
    sizes,
  );
  assert.equal(
    sized,
    '<p class="sheet-row"><a href="sheets/pll.png"><img src="sheets/pll.png" alt="PLL" width="30" height="20"></a></p>',
  );
  for (const markup of [
    '<img src="algorithms/photos/private.png">',
    '<img data-src="https://img.shields.io/badge/ok" src="algorithms/photos/private.png">',
    '<img src="sheets/metro-notation.pdf">',
    '<script>alert(1)</script>',
    '<iframe src="https://example.invalid/"></iframe>',
    '<p><img src="https://img.shields.io/badge/ok" onerror="alert(1)"></p>',
    '<a href="javascript:alert(1)">badge</a>',
    "<a href=' JavaScript:alert(1)'>badge</a>",
    '<img src="https://img.shields.io/badge/ok" onload=alert(1)>',
    // Spellings that only a real HTML parser reads as the browser does.
    '<div><img/onerror=alert(1) src="https://img.shields.io/x"></div>',
    '<img src="https://img.shields.io/x" onload=&#97;lert(1)>',
    'Text <a href="java&#115;cript:alert(1)">x</a> more',
    `<img alt=' src="https://img.shields.io/x"' src="https://tracker.example/p.png">`,
    '<img src="https://img.shields.io/x" srcset="https://tracker.example/p.png 1x">',
    'Text <IMG SRC="https://tracker.example/p.png" alt="x"> more',
    // Element names that only Object.prototype defines.
    '<constructor>x</constructor>',
    '<constructor id=a>x</constructor>',
    // Links the site cannot follow: anchors without heading ids and other schemes.
    '[Credits](#credits)',
    '[Mail](mailto:someone@example.com)',
    '[Plain](http://example.com/)',
    '[Root](/LICENSE)',
  ]) {
    assert.throws(() => renderReadme(markup, sizes), /README contains/, markup);
  }
  // Text and code that only mention them stay allowed, as marked escapes them.
  assert.match(
    renderReadme('Write `<script>`, onerror="x", only=1 or href="javascript:x" as text.\n', {}),
    /Write <code>&lt;script&gt;<\/code>, onerror="x", only=1/,
  );
  for (const image of [
    '<img src="sheets/pll.png">',
    '<a href="sheets/f2l.png"><img src="sheets/pll.png"></a>',
  ]) {
    assert.throws(() => renderReadme(image, sizes), /must link to itself/, image);
  }
});

test('PNG sizes come from the image header', async () => {
  assert.deepEqual(pngSize(await readFile(join(ROOT, 'web/favicon.png'))), {
    width: 32,
    height: 32,
  });
  assert.throws(() => pngSize(Buffer.from('<svg></svg>')), /Expected a PNG/);
});

test('sources reached through symlinks are refused, so only repository files are published', async () => {
  await withRoot(async (root, temporary) => {
    const outside = join(temporary, 'outside');
    await mkdir(outside);
    for (const path of [
      'sheets/f2l.png',
      'web/styles.css',
      'web/index.html',
      'README.md',
      'sheets',
      'web',
    ]) {
      // The linked content is valid, so only the symlink check can stop the build.
      const moved = join(outside, path.replaceAll('/', '-'));
      await rename(join(root, path), moved);
      await symlink(moved, join(root, path));
      await assert.rejects(buildSite(root), /Symlinks are not published/, path);
      await rm(join(root, path));
      await rename(moved, join(root, path));
    }
    await assert.rejects(lstat(join(root, 'dist')), { code: 'ENOENT' });
    // A symlink above the root is not part of the repository and is allowed.
    await symlink(root, join(temporary, 'root-link'));
    await buildSite(join(temporary, 'root-link'));
    assert.equal((await lstat(join(root, 'dist'))).isDirectory(), true);
  });
});

test('a symlinked dist is replaced without touching its target', async () => {
  await withRoot(async (root, temporary) => {
    const elsewhere = join(temporary, 'elsewhere');
    await mkdir(elsewhere);
    await writeFile(join(elsewhere, 'keep.txt'), 'Keep');
    await symlink(elsewhere, join(root, 'dist'), 'junction');
    await buildSite(root);
    assert.equal((await lstat(join(root, 'dist'))).isDirectory(), true);
    assert.deepEqual(await readdir(elsewhere), ['keep.txt']);
  });
});

test('the build script runs when started through a symlinked path', async (t) => {
  const temporary = await mkdtemp(join(tmpdir(), 'metro-link-test-'));
  t.after(() => rm(temporary, { recursive: true, force: true }));
  await symlink(fileURLToPath(new URL('../scripts', import.meta.url)), join(temporary, 'scripts'));
  // An unknown option stops the script with an error before it builds anything.
  const result = spawnSync(
    process.execPath,
    [join(temporary, 'scripts', 'build-site.mjs'), '--unknown'],
    { encoding: 'utf8' },
  );
  assert.equal(result.status, 1);
  assert.match(result.stderr, /Unknown option '--unknown'/);
});
