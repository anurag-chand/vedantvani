import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://vedantvani.pages.dev',
  output: 'static',
  integrations: [sitemap()],
  redirects: {
    '/read/shiv-samhita': '/read/shiva-samhita',
    '/shiv-samhita': '/read/shiva-samhita',
    '/shiva-samhita': '/read/shiva-samhita',
    '/read/sankhya-karika': '/read/sankhya-karika-gaudapada',
    '/sankhya-karika': '/read/sankhya-karika-gaudapada',
    '/sankhyakarika': '/read/sankhya-karika-gaudapada',
    '/read/sankhyakarika': '/read/sankhya-karika-gaudapada',
  },
  build: {
    format: 'directory'
  }
});
