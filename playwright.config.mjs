import { defineConfig, devices } from '@playwright/test';

const port = Number(process.env.PLAYWRIGHT_PORT ?? 4179);
if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('Invalid test port.');
const baseURL = `http://127.0.0.1:${port}`;

export default defineConfig({
  testDir: './tests/browser',
  fullyParallel: true,
  // Deployment runs these tests locally, so a stray test.only must fail outside CI too.
  forbidOnly: true,
  reporter: 'list',
  use: {
    baseURL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  // wrangler dev builds dist/ and serves it as Cloudflare would, with _headers.
  webServer: {
    command: `node scripts/wrangler.mjs dev --port ${port}`,
    url: `${baseURL}/metro-notation/`,
    timeout: 120_000,
    // SIGTERM lets Wrangler stop workerd and remove its temporary files.
    gracefulShutdown: { signal: 'SIGTERM', timeout: 10_000 },
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
    // Phone profiles: mobile user agent, touch-only input and high pixel density.
    { name: 'iphone', use: { ...devices['iPhone 17'] } },
    { name: 'android', use: { ...devices['Pixel 9'] } },
  ],
});
