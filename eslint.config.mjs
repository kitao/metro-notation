import { fileURLToPath } from 'node:url';
import js from '@eslint/js';
import globals from 'globals';
import { defineConfig, includeIgnoreFile } from 'eslint/config';

export default defineConfig([
  // Builds, Wrangler bundles and the virtual environment hold JavaScript that is not ours.
  includeIgnoreFile(fileURLToPath(new URL('.gitignore', import.meta.url))),
  js.configs.recommended,
  {
    files: ['**/*.mjs'],
    languageOptions: { globals: globals.node },
  },
  {
    files: ['tests/browser/**/*.mjs'],
    languageOptions: { globals: globals.browser },
  },
  {
    rules: {
      eqeqeq: 'error',
      'no-var': 'error',
      'prefer-const': 'error',
    },
  },
]);
