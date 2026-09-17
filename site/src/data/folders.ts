import type { CollectionEntry } from 'astro:content';

export interface NoteFolder {
  path: string;
  title: string;
  count: number;
  children: NoteFolder[];
  notes: CollectionEntry<'notes'>[];
}

// Use the source directory name verbatim, independently of Astro's slugged IDs.
export function noteFolder(note: CollectionEntry<'notes'>): string {
  const source = (note.filePath ?? '').replaceAll('\\', '/');
  const relative = source.split('src/content/notes/')[1] ?? '';
  return relative.split('/').slice(0, -1).join('/');
}

export function folderTitle(path: string): string {
  return path.split('/').at(-1) || '전체 글';
}

export function folderUrl(path: string): string {
  return path ? `/notes/folder/${path.split('/').map(encodeURIComponent).join('/')}/` : '/notes/';
}

export function isInFolder(note: CollectionEntry<'notes'>, path: string): boolean {
  const folder = noteFolder(note);
  return folder === path || folder.startsWith(`${path}/`);
}

export function buildFolders(notes: CollectionEntry<'notes'>[]): NoteFolder[] {
  const roots: NoteFolder[] = [];
  for (const note of notes) {
    const parts = noteFolder(note).split('/').filter(Boolean);
    let siblings = roots;
    parts.forEach((title, index) => {
      const path = parts.slice(0, index + 1).join('/');
      let folder = siblings.find(item => item.path === path);
      if (!folder) {
        folder = { path, title, count: 0, children: [], notes: [] };
        siblings.push(folder);
      }
      folder.count += 1;
      if (index === parts.length - 1) folder.notes.push(note);
      siblings = folder.children;
    });
  }
  const sort = (folders: NoteFolder[]): NoteFolder[] => folders
    .sort((a, b) => a.title.localeCompare(b.title, 'ko'))
    .map(folder => ({
      ...folder,
      children: sort(folder.children),
      notes: folder.notes.sort((a, b) =>
        b.data.publishedAt.valueOf() - a.data.publishedAt.valueOf()
        || a.data.title.localeCompare(b.data.title, 'ko', { numeric: true }))
    }));
  return sort(roots);
}

export function flattenFolders(folders: NoteFolder[]): NoteFolder[] {
  return folders.flatMap(folder => [folder, ...flattenFolders(folder.children)]);
}
