// One blank line separates Markdown blocks; additional blank lines add space.
// Only inspect gaps between top-level blocks, never the contents of code or math.
export default function preserveBlankLines() {
  return (tree, file) => {
    const source = String(file);
    const children = [];
    for (const node of tree.children) {
      const previous = children.at(-1);
      const start = previous?.position?.end?.offset;
      const end = node.position?.start?.offset;
      if (start !== undefined && end !== undefined) {
        const gap = source.slice(start, end);
        if (/^\s*$/.test(gap)) {
          const extraLines = (gap.match(/\n/g) ?? []).length - 2;
          if (extraLines > 0) {
            children.push({
              type: 'html',
              value: `<div class="note-blank-lines" aria-hidden="true" style="--blank-lines: ${extraLines}"></div>`
            });
          }
        }
      }
      children.push(node);
    }
    tree.children = children;
  };
}
