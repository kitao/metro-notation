import { realpathSync } from 'node:fs';
import { mkdir, mkdtemp, readFile, realpath, rename, rm, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';
import { Marked } from 'marked';
import { defaultTreeAdapter, html, parseFragment, serialize } from 'parse5';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
export const SHEET_IMAGES = ['f2l.png', 'oll-01-30.png', 'oll-31-57.png', 'pll.png'];
// The reviewed PDF and four PNGs in sheets/.
export const SHEETS = ['metro-notation.pdf', ...SHEET_IMAGES];
const WEB_FILES = ['styles.css', 'favicon.svg', 'favicon.png'];
const ROUTE_FILES = ['_headers'];
// Every file the publication is built from, relative to the root.
export const SOURCES = [
  'README.md',
  'web/index.html',
  ...[...WEB_FILES, ...ROUTE_FILES].map((name) => `web/${name}`),
  ...SHEETS.map((name) => `sheets/${name}`),
];
const REPOSITORY = 'https://github.com/kitao/metro-notation/blob/main/';
const JAPANESE = /[\u3040-\u30ff\u3400-\u9fff]/;
// What README markup may contain, element by element: marked's own output plus the badge and
// sheet markup. Scripts, frames, objects, media and forms are absent, so anything else stops
// the build.
const ATTRIBUTES = {
  a: ['href'],
  code: ['class'],
  div: ['class', 'role', 'aria-label'],
  img: ['src', 'alt', 'title', 'width', 'height', 'loading', 'decoding'],
  ol: ['start'],
  td: ['align'],
  th: ['align'],
  ...Object.fromEntries(
    'blockquote br del em h1 h2 h3 h4 h5 h6 hr li p pre span strong table tbody thead tr ul'
      .split(' ')
      .map((name) => [name, []]),
  ),
};
const BADGES = /^https:\/\/(?:img\.shields\.io\/|ko-fi\.com\/img\/)/;

function escapeAttribute(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

// Width and height from the IHDR chunk, which always directly follows the PNG signature.
export function pngSize(png) {
  if (png.toString('latin1', 0, 16) !== '\x89PNG\r\n\x1a\n\x00\x00\x00\x0dIHDR') {
    throw new Error('Expected a PNG image');
  }
  return { width: png.readUInt32BE(16), height: png.readUInt32BE(20) };
}

function* elements(node) {
  for (const child of node.childNodes ?? []) {
    if (child.tagName) yield child;
    yield* elements(child);
  }
}

const textOf = (node) =>
  node.nodeName === '#text' ? node.value : (node.childNodes ?? []).map(textOf).join('');
const attribute = (node, name) => node.attrs.find((item) => item.name === name)?.value;

function setAttribute(node, name, value) {
  node.attrs = [...node.attrs.filter((item) => item.name !== name), { name, value }];
}

// Reserve each PNG's aspect ratio before it loads. Parsed HTML keeps validation consistent
// with how the browser reads attributes, character references and element names.
export function renderReadme(readme, sizes) {
  const markdown = new Marked({
    renderer: {
      link(token) {
        // Relative paths other than the sheets point into the repository on GitHub. Anything
        // else is left for the check below, which refuses all but https and the sheets.
        if (!/^(?:[a-z][a-z\d+.-]*:|[#/]|sheets\/)/i.test(token.href)) {
          token = { ...token, href: REPOSITORY + token.href };
        }
        return `<a href="${escapeAttribute(token.href)}">${this.parser.parseInline(token.tokens)}</a>`;
      },
    },
  });
  const fragment = parseFragment(markdown.parse(readme));
  for (const node of elements(fragment)) {
    // An own property only, so names such as constructor are not taken from Object.prototype.
    const allowed = Object.hasOwn(ATTRIBUTES, node.tagName) ? ATTRIBUTES[node.tagName] : undefined;
    if (!allowed) throw new Error(`README contains a <${node.tagName}> element`);
    for (const { name } of node.attrs) {
      if (!allowed.includes(name))
        throw new Error(`README contains a ${name} attribute on <${node.tagName}>`);
    }
    const href = attribute(node, 'href');
    // The site's headings have no ids, so in-page anchors would lead nowhere.
    if (href !== undefined && !/^(?:https:\/\/|sheets\/)/.test(href))
      throw new Error(`README contains an unexpected link: ${href}`);
    if (node.tagName !== 'img' || BADGES.test(attribute(node, 'src'))) continue;
    // The displayed PNG also opens at full size.
    const sheet = attribute(node, 'src')?.match(/^sheets\/([^/]+)$/)?.[1];
    if (!SHEET_IMAGES.includes(sheet))
      throw new Error(`README contains an unexpected image: ${attribute(node, 'src')}`);
    if (node.parentNode.tagName !== 'a' || attribute(node.parentNode, 'href') !== `sheets/${sheet}`)
      throw new Error('Each sheet image must link to itself');
    const { width, height } = sizes[sheet];
    setAttribute(node, 'width', String(width));
    setAttribute(node, 'height', String(height));
  }
  for (const node of elements(fragment)) {
    if (node.tagName === 'p') {
      if ([...elements(node)].some((child) => child.tagName === 'img'))
        setAttribute(node, 'class', 'sheet-row');
      else if (JAPANESE.test(textOf(node))) setAttribute(node, 'lang', 'ja');
    }
    // Bilingual headings such as "Credits / クレジット" mark their Japanese half.
    const heading = /^h[1-6]$/.test(node.tagName) && textOf(node).match(/^(.*) \/ (.*)$/);
    if (heading && node.childNodes.length === 1 && JAPANESE.test(heading[2])) {
      const span = defaultTreeAdapter.createElement('span', html.NS.HTML, [
        { name: 'lang', value: 'ja' },
      ]);
      defaultTreeAdapter.insertText(span, heading[2]);
      node.childNodes = [];
      defaultTreeAdapter.insertText(node, `${heading[1]} / `);
      defaultTreeAdapter.appendChild(node, span);
    }
  }
  return serialize(fragment);
}

// Only repository files are published. A symlink anywhere in a source path could pull
// in content from elsewhere, so the resolved path must be the path inside the root.
async function readSource(root, path) {
  const file = join(root, path);
  if ((await realpath(file)) !== join(await realpath(root), path)) {
    throw new Error(`Symlinks are not published: ${path}`);
  }
  return readFile(file);
}

// The output is always <root>/dist, so no caller can point the cleanup at other files.
export async function buildSite(root = ROOT) {
  const output = join(root, 'dist');
  const temporary = await mkdtemp(join(root, '.site-'));
  try {
    const site = join(temporary, 'metro-notation');
    await mkdir(join(site, 'sheets'), { recursive: true });
    // Publish the reviewed distribution files, never locally regenerated sheets or source photographs.
    const sizes = {};
    for (const name of SHEETS) {
      const sheet = await readSource(root, `sheets/${name}`);
      await writeFile(join(site, 'sheets', name), sheet);
      if (SHEET_IMAGES.includes(name)) sizes[name] = pngSize(sheet);
    }
    for (const name of WEB_FILES) {
      await writeFile(join(site, name), await readSource(root, `web/${name}`));
    }
    for (const name of ROUTE_FILES) {
      await writeFile(join(temporary, name), await readSource(root, `web/${name}`));
    }
    const readme = (await readSource(root, 'README.md')).toString();
    const template = (await readSource(root, 'web/index.html')).toString();
    // The title and description are the text of the first top-level heading and paragraph,
    // read from their parsed HTML.
    const tokens = new Marked().lexer(readme);
    const plainText = (token) =>
      token && textOf(parseFragment(new Marked().parseInline(token.text)));
    const title = plainText(tokens.find(({ type, depth }) => type === 'heading' && depth === 1));
    const description = plainText(tokens.find(({ type }) => type === 'paragraph'));
    if (!title || !description) throw new Error('README needs a title and description');
    // One pass fills every placeholder, so README text that looks like a placeholder or
    // a "$" replacement pattern stays literal.
    const fill = (html, values) =>
      html.replace(/\{\{(\w+)\}\}/g, (placeholder, name) => {
        if (!Object.hasOwn(values, name)) throw new Error(`Unknown placeholder ${placeholder}`);
        return values[name];
      });
    await writeFile(
      join(site, 'index.html'),
      fill(template, {
        title: escapeAttribute(title),
        description: escapeAttribute(description),
        content: renderReadme(readme, sizes),
      }),
    );
    // rm unlinks a symlinked dist without touching its target.
    await rm(output, { recursive: true, force: true });
    await rename(temporary, output);
  } finally {
    await rm(temporary, { recursive: true, force: true });
  }
  return output;
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    parseArgs({ options: {} });
  } catch (error) {
    console.error(`${error.message}\nUsage: node scripts/build-site.mjs`);
    process.exit(1);
  }
  console.log(`Built ${await buildSite()}/metro-notation/`);
}
