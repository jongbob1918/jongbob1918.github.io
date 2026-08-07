const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

const headerSocialLinks = `
  <span class="nav-social" aria-label="소셜 링크">
    <a class="nav-icon" href="mailto:jongbob1918@gmail.com" aria-label="Email"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg></a>
    <a class="nav-icon" href="https://github.com/jongbob1918" target="_blank" rel="noreferrer" aria-label="GitHub"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.87c-2.78.6-3.37-1.18-3.37-1.18-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.61.07-.61 1 .07 1.53 1.03 1.53 1.03.9 1.53 2.35 1.09 2.92.83.09-.65.35-1.09.64-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02A9.58 9.58 0 0 1 12 6.82a9.6 9.6 0 0 1 2.5.34c1.9-1.29 2.74-1.02 2.74-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.86V21c0 .27.18.58.69.48A10 10 0 0 0 12 2Z"/></svg></a>
    <a class="nav-icon" href="https://www.linkedin.com/in/jongmyung-kim-370932341/" target="_blank" rel="noreferrer" aria-label="LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="9" width="4" height="12"/><circle cx="5" cy="5" r="2"/><path d="M11 21V9h4v2c1-1.5 2.5-2.3 4.2-2 1.8.3 2.8 1.8 2.8 4.5V21h-4v-6.5c0-1.4-.5-2.5-1.8-2.5-1.5 0-2.2 1.1-2.2 3V21h-3Z"/></svg></a>
    <a class="nav-icon" href="https://www.youtube.com/channel/UCVbvniwYb2V2equijzjjt0Q" target="_blank" rel="noreferrer" aria-label="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 7.5a3 3 0 0 0-2.1-2.1C17.1 5 12 5 12 5s-5.1 0-6.9.4A3 3 0 0 0 3 7.5 31 31 0 0 0 2.6 12 31 31 0 0 0 3 16.5a3 3 0 0 0 2.1 2.1c1.8.4 6.9.4 6.9.4s5.1 0 6.9-.4a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-4.5 31 31 0 0 0-.4-4.5Z"/><path class="play" d="m10 9 5 3-5 3Z"/></svg></a>
  </span>`;

if (nav && !nav.querySelector('.nav-social')) nav.insertAdjacentHTML('beforeend', headerSocialLinks);

if (menuButton && nav) {
  menuButton.addEventListener('click', () => {
    const open = document.body.classList.toggle('menu-open');
    menuButton.setAttribute('aria-expanded', String(open));
  });
  nav.addEventListener('click', event => {
    if (event.target.closest('a')) {
      document.body.classList.remove('menu-open');
      menuButton.setAttribute('aria-expanded', 'false');
    }
  });
}

const escapeHtml = value => String(value).replace(/[&<>"]/g, character => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'
})[character]);

const bindProjectRows = () => {
  document.querySelectorAll('.project-row[data-href]').forEach(row => {
    const openProject = () => { window.location.href = row.dataset.href; };
    row.addEventListener('click', event => {
      if (!event.target.closest('a')) openProject();
    });
    row.addEventListener('keydown', event => {
      if ((event.key === 'Enter' || event.key === ' ') && event.target === row) {
        event.preventDefault();
        openProject();
      }
    });
  });
};

const projectContainers = [...document.querySelectorAll('[data-project-group]')];

if (projectContainers.length) {
  fetch('projects.json?v=20260808-1')
    .then(response => {
      if (!response.ok) throw new Error(`Project data request failed: ${response.status}`);
      return response.json();
    })
    .then(projects => {
      projectContainers.forEach(container => {
        const group = container.dataset.projectGroup;
        const groupProjects = projects.filter(project => project.group === group);
        container.innerHTML = groupProjects.map((project, index) => {
          const url = escapeHtml(project.detailUrl);
          const title = escapeHtml(project.title);
          const sideClass = group === 'side' ? ' side-project' : '';
          const loading = group === 'key' && index === 0 ? 'eager' : 'lazy';
          return `<article class="project-row${sideClass}" data-href="${url}" tabindex="0" role="link" aria-label="Open the ${escapeHtml(project.slug.toUpperCase())} project">
            <a class="project-media" href="${url}" aria-label="Open the ${escapeHtml(project.slug.toUpperCase())} project">
              <img src="${escapeHtml(project.image)}" alt="${escapeHtml(project.imageAlt)}" loading="${loading}">
              <span class="project-overlay"><span>View Project ↗</span></span>
            </a>
            <div class="project-copy">
              <a class="project-title" href="${url}">${title} <span class="arrow">↗</span></a>
              <p class="keywords">${project.keywords.map(escapeHtml).join(' · ')}</p>
              <p class="result">${escapeHtml(project.description)}</p>
            </div>
          </article>`;
        }).join('');
      });
      bindProjectRows();
    })
    .catch(error => {
      projectContainers.forEach(container => {
        container.innerHTML = '<p class="project-data-error">Project data could not be loaded.</p>';
      });
      console.error(error);
    });
} else {
  bindProjectRows();
}

const progress = document.querySelector('.reading-progress');
const sections = [...document.querySelectorAll('.case-section[id]')];
const tocLinks = [...document.querySelectorAll('.toc a')];

if (progress) {
  const updateReadingState = () => {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = `${scrollable > 0 ? Math.min(100, window.scrollY / scrollable * 100) : 0}%`;
    let current = sections[0]?.id;
    sections.forEach(section => { if (section.getBoundingClientRect().top <= 150) current = section.id; });
    tocLinks.forEach(link => link.classList.toggle('active', link.hash === `#${current}`));
  };
  updateReadingState();
  window.addEventListener('scroll', updateReadingState, { passive: true });
}

if (!document.querySelector('.site-footer')) {
  document.body.insertAdjacentHTML('beforeend', `
    <footer class="site-footer">
      <div class="wrap footer-inner"><span>© 2026 Jongmyung Kim</span></div>
    </footer>`);
}
