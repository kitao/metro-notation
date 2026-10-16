import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

export function cloudflare(args, env = process.env, spawn = spawnSync) {
  if (!['deploy', 'dev'].includes(args[0])) {
    throw new Error('Use deploy or dev');
  }
  if (
    ['CLOUDFLARE_API_TOKEN', 'CF_API_TOKEN', 'CLOUDFLARE_API_KEY', 'CF_API_KEY'].some(
      (key) => env[key],
    )
  ) {
    throw new Error('Cloudflare requires OAuth in the OS keychain. Unset API credentials.');
  }
  const wrangler = join(
    dirname(createRequire(import.meta.url).resolve('wrangler/package.json')),
    'bin/wrangler.js',
  );
  const result = spawn(process.execPath, [wrangler, ...args], {
    stdio: 'inherit',
    env: {
      ...env,
      CLOUDFLARE_AUTH_USE_KEYRING: 'true',
      WRANGLER_SEND_METRICS: 'false',
      WRANGLER_LOG_SANITIZE: 'true',
      WRANGLER_WRITE_LOGS: 'false',
    },
  });
  if (result.error) throw result.error;
  return result.status ?? 1;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  try {
    process.exitCode = cloudflare(process.argv.slice(2));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
