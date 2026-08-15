const githubIcon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.87c-2.78.6-3.37-1.18-3.37-1.18-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.61.07-.61 1 .07 1.53 1.03 1.53 1.03.9 1.53 2.35 1.09 2.92.83.09-.65.35-1.09.64-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02A9.58 9.58 0 0 1 12 6.82a9.6 9.6 0 0 1 2.5.34c1.9-1.29 2.74-1.02 2.74-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.86V21c0 .27.18.58.69.48A10 10 0 0 0 12 2Z"/></svg>';
const backIcon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2Z"/></svg>';

const escapeHtml = value => String(value).replace(/[&<>"']/g, character => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
})[character]);

const renderSections = (sections, language) => sections.map(section => `
        <section class="case-section" id="${escapeHtml(`${language}-${section.id}`)}">
          <div class="case-heading"><h2>${escapeHtml(section.title)}</h2></div>
          ${section.body}
        </section>`).join('\n');

const renderDemo = (demo, language) => {
  if (!demo?.src) return '';

  const type = demo.type || 'image';
  const sequence = Array.isArray(demo.sequence) ? demo.sequence : [];
  const sequenceAttribute = sequence.length > 1
    ? ` data-media-sequence="${escapeHtml(JSON.stringify(sequence))}"`
    : '';
  let media;

  if (type === 'video') {
    const poster = demo.poster ? ` poster="${escapeHtml(demo.poster)}"` : '';
    media = `<video controls preload="metadata"${poster}><source src="${escapeHtml(demo.src)}">${language === 'ko' ? '이 브라우저는 동영상 재생을 지원하지 않습니다.' : 'Your browser does not support video playback.'}</video>`;
  } else if (type === 'youtube') {
    media = `<div class="video-embed"><iframe src="${escapeHtml(demo.src)}" title="${escapeHtml(demo.title || demo.alt || (language === 'ko' ? '프로젝트 시연 영상' : 'Project demonstration video'))}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>`;
  } else {
    media = `<img src="${escapeHtml(demo.src)}" alt="${escapeHtml(demo.alt || '')}"${sequenceAttribute}>`;
  }

  return `<section class="demo-section" id="demo-${language}"><figure class="feature-media">${media}</figure></section>`;
};

const renderOverviewNote = note => {
  if (!note?.title || !Array.isArray(note.paragraphs) || !note.paragraphs.length) return '';
  return `<div class="overview-note"><h3>${escapeHtml(note.title)}</h3>${note.paragraphs.map(paragraph => `<p>${escapeHtml(paragraph)}</p>`).join('')}</div>`;
};

const renderLocalizedProject = (project, sharedProject, language) => {
  const teamLabel = language === 'ko' ? '팀' : 'Team';
  const periodLabel = language === 'ko' ? '기간' : 'Period';
  const roleLabel = language === 'ko' ? '담당' : 'Role';
  const repositoryLabel = language === 'ko' ? `${sharedProject.shortName} GitHub 저장소 열기` : `Open the ${sharedProject.shortName} GitHub repository`;
  const demo = project.demo ?? sharedProject.demo;
  return `<div class="project-language" data-language-content="${language}"${language === 'en' ? ' hidden' : ''}>
    <header class="project-header">
      <h1>${escapeHtml(project.title)}</h1>
      <div class="meta">${project.team ? `<span><strong>${teamLabel}:</strong> ${escapeHtml(project.team)}</span>` : ''}<span><strong>${periodLabel}:</strong> ${escapeHtml(project.period)}</span>${project.role ? `<span><strong>${roleLabel}:</strong> ${escapeHtml(project.role)}</span>` : ''}</div>
      <p class="project-skills">${sharedProject.skills.map(escapeHtml).join(' · ')}</p>
      <a class="project-repository" href="${escapeHtml(sharedProject.repository)}" target="_blank" rel="noreferrer" aria-label="${escapeHtml(repositoryLabel)}">${githubIcon}</a>
    </header>

    <section class="project-overview" id="overview-${language}">
      <h2>Overview</h2>
      <p class="lead">${escapeHtml(project.overview)}</p>${renderOverviewNote(project.overviewNote)}
    </section>

    ${renderDemo(demo, language)}

    <div class="case-layout">
      <article class="case-study">${renderSections(project.sections, language)}
      </article>
    </div>
  </div>`;
};

export const renderProjectDetail = (project, translations, sourceFile = `${project.slug}.md`) => `<!doctype html>
<!-- Generated from project-data/${sourceFile} by templates/project-detail.mjs. -->
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="${escapeHtml(project.description)}">
  <title>${escapeHtml(project.shortName)} — Jongmyung Kim</title>
  <link rel="icon" type="image/svg+xml" href="../favicon.svg?v=2">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css?v=20260809-1">
</head>
<body data-page="project-detail" data-title-ko="${escapeHtml(translations.ko.title)} — Jongmyung Kim" data-title-en="${escapeHtml(translations.en.title)} — Jongmyung Kim" data-description-ko="${escapeHtml(translations.ko.description)}" data-description-en="${escapeHtml(translations.en.description)}">
  <div class="reading-progress" aria-hidden="true"></div>
  <header class="site-header"><div class="wrap header-inner"><a class="name" href="../index.html">Jongmyung Kim</a><button class="menu-toggle" type="button" aria-label="메뉴 열기" aria-expanded="false"><span></span></button><nav class="nav" aria-label="주요 메뉴"><a href="../index.html#key-projects">Key Projects</a><a href="../index.html#side-projects">Side Projects</a><a href="../index.html#about">About</a></nav></div></header>

  <main class="wrap case-page">
    <a class="back" href="../index.html#${project.group === 'key' ? 'key-projects' : 'side-projects'}" aria-label="프로젝트 목록으로 돌아가기" data-label-ko="프로젝트 목록으로 돌아가기" data-label-en="Back to project list">${backIcon}</a>
    ${renderLocalizedProject(translations.ko, project, 'ko')}
    ${renderLocalizedProject(translations.en, project, 'en')}
  </main>
  <script src="../script.js?v=20260809-1"></script>
</body>
</html>
`;
