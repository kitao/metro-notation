import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';

// Keep the reviewed sheet intact and fit its entire drawing into a social card.
const image = await readFile(new URL('../sheets/pll.png', import.meta.url));
const browser = await chromium.launch();
try {
  const page = await browser.newPage({
    viewport: { width: 1200, height: 630 },
    deviceScaleFactor: 1,
  });
  await page.setContent(`<!doctype html><html lang="en"><meta charset="utf-8">
    <style>
      html, body { margin: 0; width: 1200px; height: 630px; background: white; }
      img { display: block; width: 1200px; height: 630px; object-fit: contain; }
    </style>
    <img alt="The Metro Notation PLL sheet" src="data:image/png;base64,${image.toString('base64')}">`);
  await page.locator('img').evaluate((image) => image.decode());
  const path = fileURLToPath(new URL('../web/og.png', import.meta.url));
  await page.screenshot({ path });
  console.log('Generated web/og.png from sheets/pll.png.');
} finally {
  await browser.close();
}
