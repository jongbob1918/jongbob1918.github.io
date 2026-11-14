import yaml from 'js-yaml';
import source from './reading.yaml?raw';

const config = yaml.load(source);
const shared = ['content-width', 'page-gutter', 'toc-size', 'caption-size', 'line-height', 'toc-line-height', 'toc-gap', 'caption-gap', 'heading-after', 'mobile-breakpoint', 'toc-breakpoint'];
const responsive = ['body-size', 'h2-size', 'h3-size', 'paragraph-gap', 'math-gap', 'figure-gap', 'heading-before'];
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
const declarations = values => Object.entries(values)
  .map(([key, value]) => `--reading-${key}:${value}${key.endsWith('line-height') ? '' : 'px'};`).join('');
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
