import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const notesDirectory = join(root, 'site/src/content/notes');
const imagesDirectory = join(root, 'site/public/images/notes');
const imageExtensions = /\.(?:avif|gif|jpe?g|png|svg|webp)$/i;
const errors = [];
const usedImages = new Set();

function filesIn(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? filesIn(path) : [path];
  });
}

for (const note of filesIn(notesDirectory).filter(path => path.endsWith('.md'))) {
  const source = readFileSync(note, 'utf8');
  const references = [
    ...source.matchAll(/<img\b[^>]*\bsrc=["']([^"']+)["'][^>]*>/gi),
    ...source.matchAll(/!\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)/g)
  ];

  for (const match of references) {
    const imagePath = match[1];
    if (/^(?:https?:)?\/\//.test(imagePath) || imagePath.startsWith('data:')) continue;
    const location = `${relative(root, note)}:${source.slice(0, match.index).split('\n').length}`;
    const absolutePath = resolve(dirname(note), imagePath);
    if (!absolutePath.startsWith(`${imagesDirectory}/`)) {
      errors.push(`${location}: store local images in ${relative(root, imagesDirectory)} and use a file-relative path: ${imagePath}`);
      continue;
    }
    if (!existsSync(absolutePath)) {
      errors.push(`${location}: image not found: ${imagePath}`);
      continue;
    }
    usedImages.add(absolutePath);
  }
}

for (const image of filesIn(imagesDirectory).filter(path => imageExtensions.test(path))) {
  if (!usedImages.has(image)) errors.push(`${relative(root, image)}: not referenced by a note`);
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else {
  console.log(`Checked ${usedImages.size} note images.`);
}
