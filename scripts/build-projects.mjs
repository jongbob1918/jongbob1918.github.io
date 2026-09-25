import { mkdir, readFile, readdir, writeFile, unlink } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import matter from 'gray-matter';
import { marked } from 'marked';
import { renderProjectDetail } from '../templates/project-detail.mjs';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const dataDirectory = join(root, 'project-data');
const englishDataDirectory = join(dataDirectory, 'en');
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

    return { id, title, body: marked.parse(source, { gfm: true, breaks: true }) };
  });
};

// Validate all inputs before replacing any generated files.
const identifier = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const requireText = (value, field, file) => {
  if (typeof value !== 'string' || !value.trim()) throw new Error(`${file}: ${field} must be a nonempty string`);
};
const optionalText = (value, field, file) => {
  if (value !== undefined && typeof value !== 'string') throw new Error(`${file}: ${field} must be a string`);
};
const validateOrder = (value, field, file) => {
  if (!Number.isInteger(value) || value < 1) throw new Error(`${file}: ${field} must be a positive integer`);
};
const validateSkills = (value, field, file) => {
  if (value !== undefined && (!Array.isArray(value) || value.some(skill => typeof skill !== 'string' || !skill.trim()))) {
    throw new Error(`${file}: ${field} must be a list of nonempty strings`);
  }
};
const categories = JSON.parse(await readFile(join(dataDirectory, 'categories.json'), 'utf8'));
if (!Array.isArray(categories)) throw new Error('categories.json: expected a list');
const categoryIds = new Set();
for (const category of categories) {
  if (!identifier.test(category.id ?? '') || categoryIds.has(category.id)) throw new Error(`categories.json: invalid or duplicate id ${category.id}`);
  if (category.id === 'key') throw new Error('categories.json: key is reserved for the Projects section');
  categoryIds.add(category.id);
  for (const field of ['titleKo', 'titleEn']) requireText(category[field], field, category.id);
  validateOrder(category.priority, 'priority', category.id);
  if (!['main', 'compact'].includes(category.layout)) throw new Error(`${category.id}: layout must be main or compact`);
  for (const field of ['color', 'darkColor']) {
    if (category[field] !== undefined && !/^#[0-9a-f]{6}$/i.test(category[field])) throw new Error(`${category.id}: ${field} must be a six-digit hex color`);
  }
}
categories.sort((a, b) => a.priority - b.priority || a.id.localeCompare(b.id, 'en'));
const categoryRank = new Map(categories.map((category, index) => [category.id, index]));
const catalog = [];
const generatedPages = new Map();
const slugs = new Set();

for (const file of files) {
  const { data, content } = matter(await readFile(join(dataDirectory, file), 'utf8'));
  if (!identifier.test(data.slug ?? '') || slugs.has(data.slug)) throw new Error(`${file}: invalid or duplicate slug ${data.slug}`);
  slugs.add(data.slug);
  if (!categoryIds.has(data.category)) throw new Error(`${file}: unknown category ${data.category}; register it in categories.json`);
  validateOrder(data.order ?? 999, 'order', file);
  if (data.detail !== undefined && typeof data.detail !== 'boolean') throw new Error(`${file}: detail must be true or false`);
  const englishFile = `en/${data.slug}.md`;
  const { data: englishData, content: englishContent } = matter(await readFile(join(englishDataDirectory, `${data.slug}.md`), 'utf8'));
  if (englishData.slug !== data.slug) throw new Error(`${englishFile}: slug must match ${data.slug}`);
  for (const [localized, name] of [[data, file], [englishData, englishFile]]) {
    requireText(localized.title, 'title', name);
    for (const field of ['description', 'period', 'team', 'role', 'context', 'introduction', 'overview', 'shortName', 'repository']) optionalText(localized[field], field, name);
  }
  validateSkills(data.skills, 'skills', file);
  const card = data.card ?? {};
  if (typeof card !== 'object' || Array.isArray(card)) throw new Error(`${file}: card must be an object`);
  validateSkills(card.skills, 'card.skills', file);
  for (const field of ['image', 'imageAlt']) optionalText(card[field], `card.${field}`, file);
  if (card.image) requireText(card.imageAlt, 'card.imageAlt', file);
  if (card.imageFit !== undefined && !['cover', 'contain'].includes(card.imageFit)) throw new Error(`${file}: card.imageFit must be cover or contain`);
  if (card.sequence !== undefined && !Array.isArray(card.sequence)) throw new Error(`${file}: card.sequence must be a list`);
  for (const item of card.sequence ?? []) {
    requireText(item.src, 'card.sequence.src', file);
    requireText(item.alt, 'card.sequence.alt', file);
    if (!Number.isFinite(item.duration) || item.duration <= 0) throw new Error(`${file}: sequence duration must be positive`);
  }
  const defaults = { description: '', period: '', team: '', role: '', overview: '', skills: [], repository: '' };
  const project = { ...defaults, ...data, shortName: data.shortName || data.title, sections: parseSections(content) };
  const englishProject = { ...defaults, ...englishData, sections: parseSections(englishContent) };
  const hasDetail = data.detail !== false;
  if (hasDetail) generatedPages.set(`${project.slug}.html`, renderProjectDetail(project, { ko: project, en: englishProject }, file));
  catalog.push({
    slug: project.slug,
    category: project.category,
    order: project.order ?? 999,
    detailUrl: hasDetail ? `projects/${project.slug}.html` : null,
    image: card.image ?? '',
    imageAlt: card.imageAlt ?? '',
    imageFit: card.imageFit ?? 'cover',
    imageSequence: card.sequence ?? [],
    titleKo: project.title,
    titleEn: englishProject.title,
    overviewKo: project.description,
    overviewEn: englishProject.description,
    periodKo: project.period,
    periodEn: englishProject.period,
    teamKo: project.team,
    teamEn: englishProject.team,
    contributionKo: project.role,
    contributionEn: englishProject.role,
    keywords: card.skills ?? project.skills,
  });
}
catalog.sort((a, b) => categoryRank.get(a.category) - categoryRank.get(b.category) || a.order - b.order || a.slug.localeCompare(b.slug, 'en'));
for (const [file, html] of generatedPages) {
  await writeFile(join(outputDirectory, file), html, 'utf8');
  console.log(`Generated projects/${file}`);
}
// Only remove obsolete pages bearing our generator signature; leave hand-written files alone.
for (const file of await readdir(outputDirectory)) {
  if (!file.endsWith('.html') || generatedPages.has(file)) continue;
  const path = join(outputDirectory, file);
  const html = await readFile(path, 'utf8');
  if (/^<!doctype html>\n<!-- Generated from project-data\/[^\n]+ by templates\/project-detail\.mjs\. -->/.test(html)) await unlink(path);
}
await writeFile(catalogPath, `${JSON.stringify({ version: 1, categories, projects: catalog }, null, 2)}\n`, 'utf8');
console.log('Generated projects.json');
