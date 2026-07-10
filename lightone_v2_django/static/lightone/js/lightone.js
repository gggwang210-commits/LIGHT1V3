document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.metric-card,.panel-card,.report-card,.strategy-list article,.roadmap-grid div');
  cards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(12px)';
    setTimeout(() => {
      card.style.transition = 'opacity .45s ease, transform .45s ease, box-shadow .2s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 60 + index * 35);
  });

  const navLinks = Array.from(document.querySelectorAll('.nav a'));

  const normalizePath = (path) => path.replace(/\/$/, '') || '/';

  const getCurrentLink = () => {
    const currentHash = window.location.hash;
    const currentPath = normalizePath(window.location.pathname);

    if (currentHash) {
      const hashLink = navLinks.find((link) => link.hash === currentHash);
      if (hashLink) return hashLink;
    }

    return navLinks.find((link) => {
      const linkUrl = new URL(link.getAttribute('href'), window.location.href);
      return !linkUrl.hash && normalizePath(linkUrl.pathname) === currentPath;
    }) || navLinks[0];
  };

  const updateCurrentPage = () => {
    const currentLink = getCurrentLink();

    navLinks.forEach((link) => {
      const isCurrent = link === currentLink;
      link.classList.toggle('active', isCurrent);
      if (isCurrent) {
        link.setAttribute('aria-current', 'page');
      } else {
        link.removeAttribute('aria-current');
      }
    });
  };

  const focusHashTarget = () => {
    const hash = window.location.hash;
    if (!hash) return;

    const target = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!target) return;

    if (!target.hasAttribute('tabindex')) {
      target.setAttribute('tabindex', '-1');
    }
    target.focus({ preventScroll: true });
  };

  const handleRouteChange = () => {
    updateCurrentPage();
    focusHashTarget();
  };

  updateCurrentPage();
  window.addEventListener('hashchange', handleRouteChange);
});
