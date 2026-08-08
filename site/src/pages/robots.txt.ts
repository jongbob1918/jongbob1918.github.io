export const prerender = true;

export function GET({ site }: { site: URL }) {
  const sitemap = new URL('/sitemap.xml', site).toString();

  return new Response(`User-agent: *\nAllow: /\n\nSitemap: ${sitemap}\n`, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  });
}
