import { mkdir, readFile, readdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import matter from 'gray-matter';
import { marked } from 'marked';
import { renderProjectDetail } from '../templates/project-detail.mjs';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const dataDirectory = join(root, 'project-data');
const outputDirectory = join(root, 'projects');
const catalogPath = join(root, 'projects.json');

await mkdir(outputDirectory, { recursive: true });
const files = (await readdir(dataDirectory)).filter(file => file.endsWith('.md') && file !== 'README.md').sort();

const slugify = (value, fallback) => {
  const slug = value.normalize('NFKC').toLowerCase()
    .replace(/[^\p{Letter}\p{Number}]+/gu, '-')
    .replace(/^-+|-+$/g, '');
  return slug || fallback;
};

const parseSections = markdown => {
  const headingPattern = /^##\s+(.+?)\s*$/gm;
  const headings = [...markdown.matchAll(headingPattern)];
  const usedIds = new Set();

  return headings.map((heading, index) => {
    const title = heading[1].trim();
    const start = heading.index + heading[0].length;
    const end = headings[index + 1]?.index ?? markdown.length;
    const source = markdown.slice(start, end).trim();
    const baseId = slugify(title, `section-${index + 1}`);
    let id = baseId;
    let suffix = 2;

    while (usedIds.has(id)) id = `${baseId}-${suffix++}`;
    usedIds.add(id);

    return { id, title, body: marked.parse(source, { gfm: true }) };
  });
};

const requiredFields = ['slug', 'shortName', 'group', 'title', 'description', 'team', 'period', 'skills', 'repository', 'overview'];

const validateProject = (project, file) => {
  const missing = requiredFields.filter(field => project[field] === undefined || project[field] === null || project[field] === '');
  if (missing.length) throw new Error(`${file}: missing required fields: ${missing.join(', ')}`);
  if (!Array.isArray(project.skills)) throw new Error(`${file}: skills must be a YAML list`);
  if (!['key', 'side'].includes(project.group)) throw new Error(`${file}: group must be key or side`);
  if (!project.card || typeof project.card !== 'object') throw new Error(`${file}: card settings are required`);
  const missingCardFields = ['image', 'imageAlt', 'titleEn', 'descriptionKo', 'descriptionEn', 'keywords']
    .filter(field => project.card[field] === undefined || project.card[field] === null || project.card[field] === '');
  if (missingCardFields.length) throw new Error(`${file}: missing card fields: ${missingCardFields.join(', ')}`);
  if (!Array.isArray(project.card.keywords)) throw new Error(`${file}: card.keywords must be a YAML list`);
  if (project.card.sequence && !Array.isArray(project.card.sequence)) throw new Error(`${file}: card.sequence must be a YAML list`);
};

const catalog = [];

for (const file of files) {
  const source = await readFile(join(dataDirectory, file), 'utf8');
  const { data, content } = matter(source);
  const project = { ...data, sections: parseSections(content) };
  validateProject(project, file);
  const html = renderProjectDetail(project, file);
  await writeFile(join(outputDirectory, `${project.slug}.html`), html, 'utf8');
  catalog.push({
    slug: project.slug,
    group: project.group,
    order: project.order ?? 999,
    detailUrl: `projects/${project.slug}.html`,
    image: project.card.image,
    imageAlt: project.card.imageAlt,
    imageSequence: project.card.sequence ?? [],
    titleKo: project.title,
    titleEn: project.card.titleEn,
    keywords: project.card.keywords,
    descriptionKo: project.card.descriptionKo,
    descriptionEn: project.card.descriptionEn
  });
  console.log(`Generated projects/${project.slug}.html`);
}

catalog.sort((left, right) => left.order - right.order);
await writeFile(catalogPath, `${JSON.stringify(catalog, null, 2)}\n`, 'utf8');
console.log('Generated projects.json');
