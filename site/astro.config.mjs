import { defineConfig } from 'astro/config';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  site: 'https://jongbob1918.github.io',
  output: 'static',
  outDir: '../dist',
  trailingSlash: 'always',
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [[rehypeKatex, { strict: 'error', throwOnError: true }]]
  }
});
