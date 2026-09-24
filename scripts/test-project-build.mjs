import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, copyFile, writeFile, readFile, symlink, unlink, access, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';

const root = resolve(import.meta.dirname, '..');
test('categories, optional content, validation and generated-page lifecycle', async () => {
  const fixture = await mkdtemp(join(tmpdir(), 'portfolio-catalog-test-'));
  try {
    for (const folder of ['scripts', 'templates', 'project-data/en', 'projects']) await mkdir(join(fixture, folder), { recursive: true });
    for (const file of ['scripts/build-projects.mjs', 'templates/project-detail.mjs']) await copyFile(join(root, file), join(fixture, file));
    await symlink(join(root, 'node_modules'), join(fixture, 'node_modules'), 'dir');
    const categories = [
      { id: 'new-category', titleKo: '새 분류', titleEn: 'New category', priority: 3, layout: 'main' },
      { id: 'first', titleKo: '첫 분류', titleEn: 'First', priority: 1, layout: 'compact' },
      { id: 'empty', titleKo: '빈 분류', titleEn: 'Empty', priority: 2, layout: 'main' },
    ];
    const saveCategories = () => writeFile(join(fixture, 'project-data/categories.json'), JSON.stringify(categories));
    const saveProject = async (slug, category, order, detail = false) => {
      await writeFile(join(fixture, `project-data/${slug}.md`), `---\nslug: ${slug}\ncategory: ${category}\norder: ${order}\ndetail: ${detail}\ntitle: 제목\n---\n`);
      await writeFile(join(fixture, `project-data/en/${slug}.md`), `---\nslug: ${slug}\ntitle: Title\n---\n`);
    };
    const build = () => spawnSync(process.execPath, ['scripts/build-projects.mjs'], { cwd: fixture, encoding: 'utf8' });
    const catalog = async () => JSON.parse(await readFile(join(fixture, 'projects.json'), 'utf8'));
    await saveCategories();
    await saveProject('late', 'new-category', 2, true);
    await saveProject('early', 'new-category', 1);
    await saveProject('compact', 'first', 9);
    let result = build();
    assert.equal(result.status, 0, result.stderr);
    let data = await catalog();
    assert.deepEqual(data.categories.map(c => c.id), ['first', 'empty', 'new-category']);
    assert.deepEqual(data.projects.map(p => p.slug), ['compact', 'early', 'late']);
    assert.equal(data.projects[1].detailUrl, null);
    assert.equal(data.projects[1].periodKo, '');
    assert.deepEqual(data.projects[1].keywords, []);
    const html = await readFile(join(fixture, 'projects/late.html'), 'utf8');
    assert.ok(html.includes('#new-category-projects'));
    assert.ok(!html.includes('undefined'));
    assert.ok(!html.includes('class="project-repository"'));
    assert.ok(!html.includes('class="project-overview"'));

    categories[0].priority = 1;
    categories[1].priority = 3;
    await saveCategories();
    result = build();
    assert.equal(result.status, 0, result.stderr);
    assert.deepEqual((await catalog()).projects.map(p => p.slug), ['early', 'late', 'compact']);
    categories[1].priority = 1;
    await saveCategories();
    assert.equal(build().status, 0);
    assert.deepEqual((await catalog()).categories.map(c => c.id), ['first', 'new-category', 'empty']);

    const goodCatalog = await readFile(join(fixture, 'projects.json'), 'utf8');
    await saveProject('bad', 'unknown', 1);
    result = build();
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /unknown category/);
    assert.equal(await readFile(join(fixture, 'projects.json'), 'utf8'), goodCatalog);
    await unlink(join(fixture, 'project-data/bad.md'));
    await writeFile(join(fixture, 'project-data/duplicate.md'), '---\nslug: early\ncategory: first\ntitle: Duplicate\n---\n');
    result = build();
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /duplicate slug/);
    await unlink(join(fixture, 'project-data/duplicate.md'));
    categories.push({ ...categories[0] });
    await saveCategories();
    assert.match(build().stderr, /duplicate id/);
    categories.pop();
    await saveCategories();

    await writeFile(join(fixture, 'projects/manual.html'), '<h1>Keep manual page</h1>');
    await saveProject('late', 'new-category', 2, false);
    assert.equal(build().status, 0);
    await assert.rejects(access(join(fixture, 'projects/late.html')));
    await access(join(fixture, 'projects/manual.html'));
    await saveProject('late', 'new-category', 2, true);
    assert.equal(build().status, 0);
    await unlink(join(fixture, 'project-data/late.md'));
    assert.equal(build().status, 0);
    await assert.rejects(access(join(fixture, 'projects/late.html')));
  } finally {
    await rm(fixture, { recursive: true, force: true });
  }
});
