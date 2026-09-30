(function () {
  'use strict';

  // ---- Mobile navigation drawer ----
  const toggle = document.querySelector('.nav-toggle');
  const drawer = document.getElementById('mobile-nav');

  function setOpen(open) {
    if (!toggle || !drawer) {
      return;
    }
    drawer.classList.toggle('open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    toggle.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('nav-open', open);
  }

  if (toggle && drawer) {
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
  }

  // The top-right "Find Us" control is a plain link to #map, so there is no
  // dropdown logic left to maintain here.
})();
