import { defineConfig } from 'astro/config';
import remarkMath from 'remark-math';
import remarkBreaks from 'remark-breaks';
import rehypeKatex from 'rehype-katex';
import resolveNoteImages from './src/plugins/resolve-note-images.mjs';

export default defineConfig({
  site: 'https://jongbob1918.github.io',
  output: 'static',
  outDir: '../dist',
  trailingSlash: 'always',
  redirects: {
    '/notes/category/deep-learning/': '/notes/folder/Machine%20Learning%EF%BD%9CDeep%20Learning/',
    '/notes/folder/Deep%20learning/': '/notes/folder/Machine%20Learning%EF%BD%9CDeep%20Learning/',
    ...Object.fromEntries([1, 2, 3, 4].map(chapter => {
      const slug = `easy-deep-learning-ch0${chapter}`;
      return [`/notes/${slug}/`, `/notes/deep-learning/${slug}/`];
    }))
  },
  markdown: {
    remarkPlugins: [remarkMath, remarkBreaks, resolveNoteImages],
    rehypePlugins: [[rehypeKatex, { strict: 'error', throwOnError: true }]]
  }
});
