import { getCollection } from 'astro:content';
import { categories } from '../data/taxonomy';

export const prerender = true;

const escapeXml = (value: string) => value
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&apos;');

export async function GET({ site }: { site: URL }) {
  const notes = await getCollection('notes', ({ data }) => !data.draft);
  const entries = [
    { path: '/', changefreq: 'monthly', priority: '1.0' },
    { path: '/notes/', changefreq: 'weekly', priority: '0.9' },
    ...categories.map(category => ({
      path: `/notes/category/${category.id}/`,
      changefreq: 'weekly',
      priority: '0.7'
    })),
    ...notes.map(note => ({
      path: `/notes/${note.id}/`,
      lastmod: (note.data.updatedAt ?? note.data.publishedAt).toISOString(),
      changefreq: 'monthly',
      priority: '0.8'
    }))
  ];

  const urls = entries.map(entry => `  <url>\n    <loc>${escapeXml(new URL(entry.path, site).toString())}</loc>${entry.lastmod ? `\n    <lastmod>${entry.lastmod}</lastmod>` : ''}\n    <changefreq>${entry.changefreq}</changefreq>\n    <priority>${entry.priority}</priority>\n  </url>`).join('\n');
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;

  return new Response(body, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' }
  });
}
