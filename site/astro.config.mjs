import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://jongbob1918.github.io',
  output: 'static',
  outDir: '../dist',
  trailingSlash: 'always'
});
