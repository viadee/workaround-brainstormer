// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 5003,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
    },
  },
});