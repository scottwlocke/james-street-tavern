(function () {
  'use strict';

  const toggle = document.querySelector('.nav-toggle');
  const drawer = document.getElementById('mobile-nav');

  if (!toggle || !drawer) {
    return;
  }

  function setOpen(open) {
    drawer.classList.toggle('open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    toggle.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('nav-open', open);
  }

  toggle.addEventListener('click', function () {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });

  drawer.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      setOpen(false);
    });
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      setOpen(false);
    }
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth > 1024) {
      setOpen(false);
    }
  });
})();