import { mkdir, readdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { renderProjectDetail } from '../templates/project-detail.mjs';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const dataDirectory = join(root, 'project-data');
const outputDirectory = join(root, 'projects');

await mkdir(outputDirectory, { recursive: true });
const files = (await readdir(dataDirectory)).filter(file => file.endsWith('.mjs')).sort();

for (const file of files) {
  const { default: project } = await import(`${pathToFileURL(join(dataDirectory, file)).href}?v=${Date.now()}`);
  const html = renderProjectDetail(project);
  await writeFile(join(outputDirectory, `${project.slug}.html`), html, 'utf8');
  console.log(`Generated projects/${project.slug}.html`);
}
