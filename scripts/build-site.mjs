import { cp, mkdir, readFile, rename, rm, mkdtemp, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Marked } from 'marked';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
export const SHEETS = [
  'metro-notation.pdf',
  'f2l.png',
  'oll-01-30.png',
  'oll-31-57.png',
  'pll.png',
];
const REPOSITORY = 'https://github.com/kitao/metro-notation/blob/main/';

function escapeAttribute(value) {
  return value.replaceAll('&', '&amp;').replaceAll('"', '&quot;').replaceAll('<', '&lt;');
}

export function renderReadme(readme) {
  const markdown = new Marked({
    renderer: {
      link(token) {
        if (!/^(?:https?:|#|sheets\/)/.test(token.href)) {
          token = { ...token, href: REPOSITORY + token.href };
        }
        return `<a href="${escapeAttribute(token.href)}">${this.parser.parseInline(token.tokens)}</a>`;
      },
    },
  });
  return markdown
    .parse(readme)
    .replace(/<img\b[^>]*>/g, (image) => {
      const source = image.match(/src="sheets\/([^"]+)"/);
      if (!source || !SHEETS.includes(source[1]) || !source[1].endsWith('.png')) {
        throw new Error('README contains an unexpected sheet image');
      }
      return `<a href="sheets/${source[1]}">${image.replace(/ width="[^"]*"/, '')}</a>`;
    })
    .replace(/<p>([^]*?)<\/p>/g, (paragraph, content) => {
      if (content.includes('<img ')) return `<p class="sheet-row">${content}</p>`;
      if (/[\u3040-\u30ff\u3400-\u9fff]/.test(content)) return `<p lang="ja">${content}</p>`;
      return paragraph;
    });
}

export async function buildSite(root = ROOT, { preview = false } = {}) {
  const output = join(root, 'dist');
  const temporary = await mkdtemp(join(root, '.site-'));
  try {
    const site = join(temporary, 'metro-notation');
    await mkdir(join(site, 'sheets'), { recursive: true });
    const readme = await readFile(join(root, 'README.md'), 'utf8');
    const template = await readFile(join(root, 'web/index.html'), 'utf8');
    const title = readme.match(/^# (.+)$/m)?.[1];
    const description = readme.split('\n\n')[1]?.replaceAll('**', '');
    if (!title || !description) throw new Error('README needs a title and description');
    const page = (content, pageTitle = title) =>
      template
        .replace('{{title}}', escapeAttribute(pageTitle))
        .replace('{{description}}', escapeAttribute(description))
        .replace('{{content}}', content);
    const badges = await readFile(join(root, 'web/badges.html'), 'utf8');
    const home = renderReadme(readme).replace('</h1>', () => `</h1>\n${badges}`);
    await writeFile(join(site, 'index.html'), page(home));
    await writeFile(
      join(temporary, '404.html'),
      page(
        '<h1>Page not found</h1>\n<p><a href="/metro-notation/">Metro Notation</a></p>',
        'Page not found · Metro Notation',
      ),
    );
    for (const name of ['styles.css', 'favicon.svg', 'favicon.png']) {
      await cp(join(root, 'web', name), join(site, name));
    }
    // Publish the reviewed distribution files, never locally regenerated sheets or source photographs.
    for (const name of SHEETS) {
      await cp(join(root, 'sheets', name), join(site, 'sheets', name));
    }
    await writeFile(
      join(temporary, '_headers'),
      '/metro-notation/*\n' +
        '  X-Content-Type-Options: nosniff\n' +
        '  Referrer-Policy: strict-origin-when-cross-origin\n' +
        '  Cache-Control: public, max-age=0, must-revalidate\n',
    );
    if (preview) {
      // The root Worker owns shared fonts in production. Only local preview
      // needs a copy, so its same-origin font requests work without CORS.
      await cp(join(root, '../kitao-dev/assets/fonts'), join(temporary, 'assets/fonts'), {
        recursive: true,
      });
    }
    await rm(output, { recursive: true, force: true });
    await rename(temporary, output);
  } finally {
    await rm(temporary, { recursive: true, force: true });
  }
  return output;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  console.log(
    `Built ${await buildSite(ROOT, { preview: process.argv.includes('--preview') })}/metro-notation/`,
  );
}
