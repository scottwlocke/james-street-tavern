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

  // ---- Menu dropdown ----
  // Desktop (>= 1025px) only: the whole .nav-menu block is display:none in the
  // mobile media query, where the drawer above carries the same section list.
  const menu = document.querySelector('.nav-menu');
  const menuToggle = document.querySelector('.nav-menu-toggle');

  function setMenuOpen(open) {
    if (!menu || !menuToggle) {
      return;
    }
    menu.classList.toggle('open', open);
    menuToggle.setAttribute('aria-expanded', String(open));
  }

  if (menu && menuToggle) {
    menuToggle.addEventListener('click', function (event) {
      event.stopPropagation();
      setMenuOpen(menuToggle.getAttribute('aria-expanded') !== 'true');
    });

    // A click anywhere outside dismisses the panel.
    document.addEventListener('click', function (event) {
      if (!menu.contains(event.target)) {
        setMenuOpen(false);
      }
    });

    // Escape closes it, and focus returns to the control that opened it.
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menu.classList.contains('open')) {
        setMenuOpen(false);
        menuToggle.focus();
      }
    });

    // Leaving the desktop range hides .nav-menu via CSS; clear the open state so
    // it cannot be revealed stale when the layout returns to desktop.
    window.addEventListener('resize', function () {
      if (window.innerWidth <= 1024) {
        setMenuOpen(false);
      }
    });
  }

  // The top-right "Find Us" control is a plain link to #map, so there is no
  // dropdown logic left to maintain there.
})();
