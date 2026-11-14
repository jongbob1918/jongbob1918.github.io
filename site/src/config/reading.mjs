import yaml from 'js-yaml';
import source from './reading.yaml?raw';

const config = yaml.load(source);
const headings = ['h2', 'h3', 'h4', 'h5', 'h6'];
const shared = ['content-width', 'page-gutter', 'toc-size', 'caption-size', 'line-height', 'toc-line-height', 'toc-gap', 'caption-gap', 'heading-line-height', 'mobile-breakpoint', 'toc-breakpoint', ...headings.flatMap(h => [`${h}-weight`, `${h}-after`])];
const responsive = ['body-size', 'paragraph-gap', 'math-gap', 'figure-gap', ...headings.flatMap(h => [`${h}-size`, `${h}-before`])];
for (const [section, keys] of Object.entries({ shared, desktop: responsive, mobile: responsive })) {
  for (const key of keys) {
    const value = config?.[section]?.[key];
    if (typeof value !== 'number' || !Number.isFinite(value) || value <= 0) {
      throw new Error(`Set ${section}.${key} to a positive number in site/src/config/reading.yaml`);
    }
  }
}
if (config.shared['toc-breakpoint'] <= config.shared['mobile-breakpoint']) {
  throw new Error('reading.yaml: toc-breakpoint must exceed mobile-breakpoint');
}
for (const heading of headings) {
  if (config.shared[`${heading}-weight`] > 1000) {
    throw new Error(`reading.yaml: shared.${heading}-weight must be at most 1000`);
  }
}
for (const section of ['desktop', 'mobile']) {
  for (let i = 1; i < headings.length; i++) {
    const parent = headings[i - 1];
    const child = headings[i];
    if (config[section][`${parent}-size`] < config[section][`${child}-size`] ||
        config[section][`${parent}-before`] <= config[section][`${child}-before`]) {
      throw new Error(`reading.yaml: ${section}.${parent} must be at least as large as ${child} and have more space above`);
    }
  }
}
const declarations = values => Object.entries(values)
  .map(([key, value]) => `--reading-${key}:${value}${(key.endsWith('line-height') || key.endsWith('-weight')) ? '' : 'px'};`).join('');
export const readingStyles = `
:root { ${declarations(config.shared)} ${declarations(config.desktop)} }
@media (max-width: ${config.shared['mobile-breakpoint']}px) {
  :root { ${declarations(config.mobile)} }
}
@media (max-width: ${config.shared['toc-breakpoint']}px) {
  :root .article-layout { display: flex; flex-direction: column; gap: 0; }
  :root .article-toc { position: static; order: -1; }
}
`;
