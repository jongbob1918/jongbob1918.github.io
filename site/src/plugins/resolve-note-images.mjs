// Notes use file-relative image paths so Obsidian can preview assets in site/public.
// On the site, public assets are served from the domain root instead.
export default function resolveNoteImages() {
  return tree => {
    const visit = node => {
      if (node.type === 'html') {
        node.value = node.value.replace(/(?:\.\.\/)+public\/images\/notes\//g, '/images/notes/');
      }
      for (const child of node.children ?? []) visit(child);
    };
    visit(tree);
  };
}
