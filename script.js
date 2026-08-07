const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

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
