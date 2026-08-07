const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');

const rokafLogo = document.querySelector('.rokaf-logo');
if (rokafLogo) rokafLogo.src = 'assets/images/rokaf-emblem.png';

const socialLinks = `
  <span class="profile-social" aria-label="Social links">
    <a class="social-icon" href="mailto:jongbob1918@gmail.com" aria-label="Email"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg></a>
    <a class="social-icon" href="https://github.com/jongbob1918" target="_blank" rel="noreferrer" aria-label="GitHub"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.87c-2.78.6-3.37-1.18-3.37-1.18-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.61.07-.61 1 .07 1.53 1.03 1.53 1.03.9 1.53 2.35 1.09 2.92.83.09-.65.35-1.09.64-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02A9.58 9.58 0 0 1 12 6.82a9.6 9.6 0 0 1 2.5.34c1.9-1.29 2.74-1.02 2.74-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.86V21c0 .27.18.58.69.48A10 10 0 0 0 12 2Z"/></svg></a>
    <a class="social-icon" href="https://www.linkedin.com/in/jongmyung-kim-370932341/" target="_blank" rel="noreferrer" aria-label="LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="9" width="4" height="12"/><circle cx="5" cy="5" r="2"/><path d="M11 21V9h4v2c1-1.5 2.5-2.3 4.2-2 1.8.3 2.8 1.8 2.8 4.5V21h-4v-6.5c0-1.4-.5-2.5-1.8-2.5-1.5 0-2.2 1.1-2.2 3V21h-3Z"/></svg></a>
    <a class="social-icon" href="https://www.youtube.com/channel/UCVbvniwYb2V2equijzjjt0Q" target="_blank" rel="noreferrer" aria-label="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 7.5a3 3 0 0 0-2.1-2.1C17.1 5 12 5 12 5s-5.1 0-6.9.4A3 3 0 0 0 3 7.5 31 31 0 0 0 2.6 12 31 31 0 0 0 3 16.5a3 3 0 0 0 2.1 2.1c1.8.4 6.9.4 6.9.4s5.1 0 6.9-.4a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-4.5 31 31 0 0 0-.4-4.5Z"/><path class="play" d="m10 9 5 3-5 3Z"/></svg></a>
  </span>`;

const profilePhoto = document.querySelector('.profile-photo');
if (profilePhoto && !document.querySelector('.profile-social')) profilePhoto.insertAdjacentHTML('afterend', socialLinks);

const isHomePage = Boolean(document.querySelector('[data-project-group]'));
const urlParameters = new URLSearchParams(window.location.search);
const utilityControls = `
  <span class="nav-utilities" aria-label="Display settings">
    ${isHomePage ? '<button class="language-toggle" type="button" aria-label="한국어로 전환"><span data-language="en">EN</span><span data-language="ko">한</span></button>' : ''}
    <button class="theme-toggle" type="button" aria-label="다크 모드로 전환">
      <svg class="sun-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42"/></svg>
      <svg class="moon-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 14.4A8.5 8.5 0 0 1 9.6 3.5a8.5 8.5 0 1 0 10.9 10.9Z"/></svg>
    </button>
  </span>`;

if (nav && !nav.querySelector('.nav-utilities')) nav.insertAdjacentHTML('beforeend', utilityControls);

const savedTheme = localStorage.getItem('portfolio-theme') || localStorage.getItem('notes-theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const requestedTheme = urlParameters.get('theme');
const initialTheme = ['light', 'dark'].includes(requestedTheme) ? requestedTheme : savedTheme || (prefersDark ? 'dark' : 'light');
document.documentElement.dataset.theme = initialTheme;

const themeToggle = document.querySelector('.theme-toggle');
const updateThemeButton = () => {
  const dark = document.documentElement.dataset.theme === 'dark';
  if (themeToggle) themeToggle.setAttribute('aria-label', dark ? '라이트 모드로 전환' : '다크 모드로 전환');
};
updateThemeButton();
themeToggle?.addEventListener('click', () => {
  const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = nextTheme;
  localStorage.setItem('portfolio-theme', nextTheme);
  localStorage.setItem('notes-theme', nextTheme);
  updateThemeButton();
});

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
const projectTranslations = {
  javis: {
    title: 'JAVIS — 다목적 모바일 매니퓰레이터',
    description: '9인 팀에서 메인 컨트롤러를 설계하고 Nav2를 최적화했습니다. Smac Planner와 MPPI를 통합해 폭 60cm 협로의 무충돌 주행을 검증했습니다.'
  },
  roomie: {
    title: 'ROOMIE — 호텔 룸서비스 로봇',
    description: '엘리베이터 버튼을 조작하는 3축 로봇팔의 제어기와 궤적 생성기를 개발했습니다. 캘리브레이션과 정렬 액션을 분리해 38일 안에 통합 시연을 완료했습니다.'
  },
  falcon: {
    title: 'FALCON — 활주로 안전 관제 시스템',
    description: '활주로 위험요소 탐지 모델을 커스텀 학습해 정확도 90% 이상을 검증했습니다. ByteTrack 기반 이동 경로 추적과 위험 판단 로직을 통합했습니다.'
  }
};

const copyByLanguage = {
  en: {
    keyProjects: 'Key Projects', sideProjects: 'Side Projects', blog: 'Blog', about: 'About', resume: 'Resume',
    education: 'Education', career: 'Career', viewProject: 'View Project ↗', loadError: 'Project data could not be loaded.',
    educationDetails: ['Department of Aeronautical & Mechanical Engineering', 'AI Robotics Bootcamp · 2025.02–2025.08', 'ROS 2 · Navigation · SLAM · Deep Learning'],
    careerDetails: ['Robotics Software Engineer', '2025.10–Present · Autonomous Navigation', 'Aircraft Maintenance Non-Commissioned Officer', '5 years · KF-16 Avionics Systems Maintenance']
  },
  ko: {
    keyProjects: '주요 프로젝트', sideProjects: '사이드 프로젝트', blog: '블로그', about: '소개', resume: '이력서',
    education: '학력', career: '경력', viewProject: '프로젝트 보기 ↗', loadError: '프로젝트 정보를 불러오지 못했습니다.',
    educationDetails: ['항공기계공학과', 'AI 로보틱스 부트캠프 · 2025.02–2025.08', 'ROS 2 · Navigation · SLAM · Deep Learning'],
    careerDetails: ['로보틱스 소프트웨어 엔지니어', '2025.10–현재 · 자율주행', '항공정비 부사관', '5년 · KF-16 항공전자시스템 정비']
  }
};

const requestedLanguage = urlParameters.get('lang');
let activeLanguage = ['en', 'ko'].includes(requestedLanguage) ? requestedLanguage : localStorage.getItem('portfolio-language') === 'ko' ? 'ko' : 'en';
let loadedProjects = [];

const setAllText = (selector, text) => document.querySelectorAll(selector).forEach(element => { element.textContent = text; });

const renderProjects = () => {
  if (!loadedProjects.length) return;
  const copy = copyByLanguage[activeLanguage];
  projectContainers.forEach(container => {
    const group = container.dataset.projectGroup;
    const groupProjects = loadedProjects.filter(project => project.group === group);
    container.innerHTML = groupProjects.map((project, index) => {
      const localized = activeLanguage === 'ko' ? projectTranslations[project.slug] : null;
      const url = escapeHtml(project.detailUrl);
      const title = escapeHtml(localized?.title || project.title);
      const description = escapeHtml(localized?.description || project.description);
      const projectName = escapeHtml(project.slug.toUpperCase());
      const sideClass = group === 'side' ? ' side-project' : '';
      const loading = group === 'key' && index === 0 ? 'eager' : 'lazy';
      const openLabel = activeLanguage === 'ko' ? `${projectName} 프로젝트 열기` : `Open the ${projectName} project`;
      return `<article class="project-row${sideClass}" data-href="${url}" tabindex="0" role="link" aria-label="${openLabel}">
        <a class="project-media" href="${url}" aria-label="${openLabel}">
          <img src="${escapeHtml(project.image)}" alt="${escapeHtml(project.imageAlt)}" loading="${loading}">
          <span class="project-overlay"><span>${copy.viewProject}</span></span>
        </a>
        <div class="project-copy">
          <a class="project-title" href="${url}">${title}</a>
          <p class="keywords">${project.keywords.map(escapeHtml).join(' · ')}</p>
          <p class="result">${description}</p>
        </div>
      </article>`;
    }).join('');
  });
  bindProjectRows();
};

const applyLanguage = () => {
  const copy = copyByLanguage[activeLanguage];
  document.documentElement.lang = activeLanguage;
  setAllText('.nav a[href$="#key-projects"]', copy.keyProjects);
  setAllText('.nav a[href$="#side-projects"]', copy.sideProjects);
  setAllText('.nav a[href$="notes/"]', copy.blog);
  setAllText('.nav a[href$="#about"]', copy.about);
  setAllText('.nav .disabled[title]', copy.resume);
  setAllText('#key-projects-title', copy.keyProjects);
  setAllText('#side-projects-title', copy.sideProjects);
  setAllText('#about-title', copy.about);
  const factLabels = document.querySelectorAll('.about-facts dt');
  if (factLabels[0]) factLabels[0].textContent = copy.education;
  if (factLabels[1]) factLabels[1].textContent = copy.career;
  const detailLines = document.querySelectorAll('.about-facts small');
  [...copy.educationDetails, ...copy.careerDetails].forEach((text, index) => {
    if (detailLines[index]) detailLines[index].textContent = text;
  });
  document.querySelectorAll('.language-toggle [data-language]').forEach(option => {
    option.classList.toggle('active', option.dataset.language === activeLanguage);
  });
  const languageToggle = document.querySelector('.language-toggle');
  if (languageToggle) languageToggle.setAttribute('aria-label', activeLanguage === 'en' ? '한국어로 전환' : 'Switch to English');
  renderProjects();
};

document.querySelector('.language-toggle')?.addEventListener('click', () => {
  activeLanguage = activeLanguage === 'en' ? 'ko' : 'en';
  localStorage.setItem('portfolio-language', activeLanguage);
  applyLanguage();
});

applyLanguage();

if (projectContainers.length) {
  fetch('projects.json?v=20260808-1')
    .then(response => {
      if (!response.ok) throw new Error(`Project data request failed: ${response.status}`);
      return response.json();
    })
    .then(projects => {
      loadedProjects = projects;
      renderProjects();
    })
    .catch(error => {
      projectContainers.forEach(container => {
        container.innerHTML = `<p class="project-data-error">${copyByLanguage[activeLanguage].loadError}</p>`;
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
