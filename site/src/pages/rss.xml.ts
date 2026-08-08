import { getCollection } from 'astro:content';

export const prerender = true;

const escapeXml = (value: string) => value
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&apos;');

export async function GET({ site }: { site: URL }) {
  const notes = (await getCollection('notes', ({ data }) => !data.draft))
    .sort((a, b) => b.data.publishedAt.valueOf() - a.data.publishedAt.valueOf());
  const channelURL = new URL('/notes/', site).toString();
  const items = notes.map(note => {
    const url = new URL(`/notes/${note.id}/`, site).toString();
    return `    <item>\n      <title>${escapeXml(note.data.title)}</title>\n      <link>${escapeXml(url)}</link>\n      <guid isPermaLink="true">${escapeXml(url)}</guid>\n      <description>${escapeXml(note.data.description)}</description>\n      <pubDate>${note.data.publishedAt.toUTCString()}</pubDate>\n    </item>`;
  }).join('\n');
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n  <channel>\n    <title>Jongmyung Kim — Robotics Notes</title>\n    <link>${escapeXml(channelURL)}</link>\n    <description>Robotics software engineering notes by Jongmyung Kim.</description>\n    <language>ko-KR</language>\n${items}\n  </channel>\n</rss>\n`;

  return new Response(body, {
    headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' }
  });
}
