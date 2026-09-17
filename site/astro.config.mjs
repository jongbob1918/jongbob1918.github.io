import { defineConfig } from 'astro/config';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  site: 'https://jongbob1918.github.io',
  output: 'static',
  outDir: '../dist',
  trailingSlash: 'always',
  redirects: {
    '/notes/category/deep-learning/': '/notes/folder/Deep%20learning/',
    ...Object.fromEntries([1, 2, 3, 4].map(chapter => {
      const slug = `easy-deep-learning-ch0${chapter}`;
      return [`/notes/${slug}/`, `/notes/deep-learning/${slug}/`];
    }))
  },
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [[rehypeKatex, { strict: 'error', throwOnError: true }]]
  }
});
