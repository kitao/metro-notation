import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { test, expect } from '@playwright/test';
import axe from 'axe-core';
import { SHEET_IMAGES, SHEETS } from '../../scripts/build-site.mjs';

// Badges and fonts load from Shields.io, Ko-fi and Google Fonts; stand-ins keep the tests
// independent of the network, and the fonts fall back to local ones.
const badgeStandIn =
  '<svg xmlns="http://www.w3.org/2000/svg" width="80" height="20"><rect width="80" height="20" fill="#555"/></svg>';

const fontStandIn =
  "@font-face { font-family: 'Noto Sans JP'; src: url(https://fonts.gstatic.com/s/stand-in.woff2) format('woff2'); }";

test.beforeEach(async ({ context }) => {
  await context.route(/^https:\/\/(img\.shields\.io|ko-fi\.com\/img)\//, (route) =>
    route.fulfill({ contentType: 'image/svg+xml', body: badgeStandIn }),
  );
  // The stand-in stylesheet points at fonts.gstatic.com like the real one, so font-src is covered.
  await context.route(/^https:\/\/fonts\.googleapis\.com\//, (route) =>
    route.fulfill({ contentType: 'text/css', body: fontStandIn }),
  );
  await context.route(/^https:\/\/fonts\.gstatic\.com\//, (route) =>
    route.fulfill({ contentType: 'font/woff2', body: '' }),
  );
});

function watchProblems(page) {
  const problems = [];
  page.on('pageerror', (error) => problems.push(error.message));
  page.on('console', (message) => {
    if (message.type() === 'error') problems.push(message.text());
  });
  page.on('response', (response) => {
    if (response.status() >= 400) problems.push(`${response.status()} ${response.url()}`);
  });
  return problems;
}

// The page's Content-Security-Policy blocks injected script tags, so axe runs by evaluation.
async function accessibilityViolations(page) {
  await page.evaluate(axe.source);
  const results = await page.evaluate(() =>
    window.axe.run(document, {
      runOnly: {
        type: 'tag',
        values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice'],
      },
      // The reviewed design tells links apart by color and underlines them on hover, which
      // this rule does not accept for links inside text.
      rules: { 'link-in-text-block': { enabled: false } },
    }),
  );
  return results.violations.map(({ id, nodes }) => ({ id, targets: nodes.map((n) => n.target) }));
}

test('the page shows the README and four whole sheets that open at full size', async ({
  page,
  baseURL,
}) => {
  const problems = watchProblems(page);
  await page.goto('/metro-notation/');
  await expect(page).toHaveTitle('Metro Notation');
  await expect(page.locator('h1')).toHaveText('Metro Notation');
  await expect(page.locator('p[lang="ja"]')).toHaveCount(3);
  await expect(page.locator('a[href="sheets/metro-notation.pdf"]')).toHaveText(
    'metro-notation.pdf',
  );
  expect(
    await page.locator('.badges a').evaluateAll((links) => links.map((link) => link.href)),
  ).toEqual([
    'https://github.com/kitao/metro-notation',
    'https://github.com/sponsors/kitao',
    'https://www.patreon.com/tkitao',
    'https://ko-fi.com/H2H27VDKD',
  ]);
  const images = page.locator('.sheet-row img');
  await expect(images).toHaveCount(4);
  for (const image of await images.all()) await image.evaluate((element) => element.decode());
  const layout = await page.evaluate(() => {
    const main = document.querySelector('main');
    const style = getComputedStyle(main);
    const box = main.getBoundingClientRect();
    return {
      overflow: document.documentElement.scrollWidth > innerWidth,
      pixelRatio: devicePixelRatio,
      content: [
        box.left + parseFloat(style.paddingLeft),
        box.right - parseFloat(style.paddingRight),
      ],
      sheets: [...document.querySelectorAll('.sheet-row img')].map((image) => {
        const rect = image.getBoundingClientRect();
        return {
          href: image.closest('a').href,
          source: image.src,
          natural: [image.naturalWidth, image.naturalHeight],
          declared: [Number(image.getAttribute('width')), Number(image.getAttribute('height'))],
          rect: [rect.left, rect.top, rect.right, rect.bottom],
        };
      }),
    };
  });
  expect(layout.overflow).toBe(false);
  // Each displayed PNG also opens at full size.
  for (const property of ['href', 'source']) {
    expect(layout.sheets.map((sheet) => sheet[property])).toEqual(
      SHEET_IMAGES.map((name) => new URL(`/metro-notation/sheets/${name}`, baseURL).href),
    );
  }
  const [left, right] = layout.content;
  for (const [index, { natural, declared, rect }] of layout.sheets.entries()) {
    // The page reserves the image's real aspect ratio and shows the whole sheet, two per row.
    expect(declared).toEqual(natural);
    const [x1, y1, x2, y2] = rect;
    // The PNG is shown at a reduced size, including on high-density displays.
    expect(natural[0]).toBeGreaterThanOrEqual((x2 - x1) * layout.pixelRatio);
    expect((x2 - x1) / (y2 - y1)).toBeCloseTo(natural[0] / natural[1], 2);
    expect(x1).toBeGreaterThanOrEqual(left - 0.5);
    expect(x2).toBeLessThanOrEqual(right + 0.5);
    expect(x2 - x1).toBeGreaterThan((right - left) * 0.45);
    const neighbor = layout.sheets[index ^ 1].rect;
    expect(y1).toBeCloseTo(neighbor[1], 1);
  }
  expect(layout.sheets[2].rect[1]).toBeGreaterThan(layout.sheets[0].rect[3]);
  expect(problems).toEqual([]);
  // After the page's own checks: axe fetches stylesheets itself, which the page's CSP refuses.
  expect(await accessibilityViolations(page)).toEqual([]);
});

test('security headers apply and the pages run without CSP violations', async ({ page }) => {
  await page.addInitScript(() => {
    window.violations = [];
    document.addEventListener('securitypolicyviolation', (event) =>
      window.violations.push(`${event.violatedDirective} ${event.blockedURI}`),
    );
  });
  for (const path of ['/metro-notation/']) {
    const headers = (await page.goto(path)).headers();
    expect(headers['x-content-type-options'], path).toBe('nosniff');
    expect(headers['referrer-policy'], path).toBe('strict-origin-when-cross-origin');
    const policy = Object.fromEntries(
      headers['content-security-policy'].split(';').map((directive) => {
        const [name, ...values] = directive.trim().split(/\s+/);
        return [name, values];
      }),
    );
    expect(policy['default-src'], path).toEqual(["'none'"]);
    // Local runs neither inject the analytics script nor frame the page, so check these by value.
    expect(policy['script-src'], path).toContain('https://static.cloudflareinsights.com');
    expect(policy['connect-src'], path).toContain('https://cloudflareinsights.com');
    for (const name of ['base-uri', 'form-action', 'frame-ancestors'])
      expect(policy[name], `${path} ${name}`).toEqual(["'none'"]);
    await expect
      .poll(() => page.evaluate(() => [...document.images].every((image) => image.complete)))
      .toBe(true);
    await page.evaluate(() => document.fonts.ready);
    expect(await page.evaluate(() => window.violations), path).toEqual([]);
  }
});

test('links are underlined on hover', async ({ page }) => {
  await page.goto('/metro-notation/');
  const link = page.locator('a[href="sheets/metro-notation.pdf"]');
  const decoration = () => link.evaluate((element) => getComputedStyle(element).textDecorationLine);
  expect(await decoration()).toBe('none');
  await link.hover();
  expect(await decoration()).toBe('underline');
});

test('keyboard focus shows an outline', async ({ page, browserName }) => {
  await page.goto('/metro-notation/');
  // WebKit moves focus to links only with Alt+Tab, as in Safari's default settings.
  await page.keyboard.press(browserName === 'webkit' ? 'Alt+Tab' : 'Tab');
  const focused = page.locator(':focus');
  await expect(focused).toHaveAttribute('href', 'https://github.com/kitao/metro-notation');
  expect(await focused.evaluate((element) => getComputedStyle(element).outlineStyle)).toBe('solid');
});

test('Cloudflare redirects the slashless URL, serves the reviewed sheets and 404s elsewhere', async ({
  request,
  baseURL,
}, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium', 'Server responses do not depend on the browser.');
  // wrangler dev serves every path, so this checks the Static Assets redirect, not route matching.
  const redirect = await request.get('/metro-notation?from=test', { maxRedirects: 0 });
  expect(redirect.status()).toBe(307);
  expect(new URL(redirect.headers().location, baseURL).href).toBe(
    new URL('/metro-notation/?from=test', baseURL).href,
  );
  // Every response on the routes, including the redirect and 404s, carries the headers.
  const headers = {
    'x-content-type-options': 'nosniff',
    'referrer-policy': 'strict-origin-when-cross-origin',
    'content-security-policy': expect.stringContaining("default-src 'none'"),
  };
  expect(redirect.headers()).toMatchObject(headers);
  expect((await request.get('/metro-notation/')).headers()).toMatchObject(headers);
  const digest = (bytes) => createHash('sha256').update(bytes).digest('hex');
  for (const name of SHEETS) {
    const response = await request.get(`/metro-notation/sheets/${name}`);
    expect(response.status()).toBe(200);
    expect(response.headers()['content-type']).toBe(
      name.endsWith('.pdf') ? 'application/pdf' : 'image/png',
    );
    expect(digest(await response.body())).toBe(
      digest(await readFile(new URL(`../../sheets/${name}`, import.meta.url))),
    );
    // The browsers' image and PDF viewers style themselves, which the page policy would block.
    expect(response.headers()['x-content-type-options']).toBe('nosniff');
    expect(response.headers()).not.toHaveProperty('content-security-policy');
  }
  for (const path of [
    '/metro-notation/missing',
    '/metro-notation/no/such/page/',
    '/metro-notationx',
    '/metro-notation.pdf',
  ]) {
    const response = await request.get(path);
    expect(response.status(), path).toBe(404);
    expect(response.headers(), path).toMatchObject(headers);
  }
});
