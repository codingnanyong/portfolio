import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  base: './',
  server: {
    proxy: {
      '/openapi.json': { target: 'http://localhost:30001', changeOrigin: true },
      '/api': { target: 'http://localhost:30001', changeOrigin: true },
    },
  },
});
