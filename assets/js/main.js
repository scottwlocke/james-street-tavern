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

  // ---- Specials rotator ----
  // The specials board shows one chalkboard at a time and slides to the next
  // every 20s. Every board ships in the markup and the track is a plain block,
  // so without JS the specials simply stack — the rotation is additive, never
  // load-bearing. That matters here: the specials are the loudest thing on the
  // page, so they must survive intact for anyone who cannot run this.
  //
  // WCAG 2.2.2 (Pause, Stop, Hide): this content moves by itself for longer
  // than five seconds, so the pause control is a requirement rather than a
  // nicety. Rotation also yields on hover and on keyboard focus, because a
  // visitor who has started reading a board should not have it swapped out
  // from under them, and it stops entirely in a background tab.
  //
  // The carousel ARIA is added here rather than in the template, because
  // without JS these are just a stack of specials and "slide 1 of 2" would
  // be a lie.
  const SPECIALS_INTERVAL = 20000;

  function initSpecials(root) {
    const boards = Array.prototype.slice.call(
      root.querySelectorAll('.chalkboards > .chalkboard')
    );

    // A single special has nothing to rotate to, so it stays a plain panel
    // with no controls and no timer.
    if (boards.length < 2) {
      return;
    }

    const total = boards.length;
    const dots = [];
    let index = 0;
    let timer = null;
    let paused = false;   // pressed the pause button
    let hovered = false;  // pointer is over the rotator
    let focused = false;  // a control inside it has focus

    const controls = document.createElement('div');
    controls.className = 'specials-controls';

    boards.forEach(function (board, i) {
      const heading = board.querySelector('.chalk-title');
      const title = heading ? heading.textContent.trim() : '';
      const position = (i + 1) + ' of ' + total + ': ' + title;

      board.setAttribute('role', 'group');
      board.setAttribute('aria-roledescription', 'slide');
      board.setAttribute('aria-label', position);

      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'specials-dot';
      dot.setAttribute('aria-label', 'Show special ' + position);

      const mark = document.createElement('span');
      mark.className = 'specials-dot-mark';
      mark.setAttribute('aria-hidden', 'true');
      dot.appendChild(mark);

      dot.addEventListener('click', function () {
        index = i;
        paint();
        schedule();
      });

      dots.push(dot);
      controls.appendChild(dot);
    });

    const pause = document.createElement('button');
    pause.type = 'button';
    pause.className = 'specials-pause';
    pause.setAttribute('aria-label', 'Pause specials');

    const glyph = document.createElement('span');
    glyph.className = 'specials-pause-icon';
    glyph.setAttribute('aria-hidden', 'true');
    pause.appendChild(glyph);

    pause.addEventListener('click', function () {
      paused = !paused;
      pause.classList.toggle('is-paused', paused);
      pause.setAttribute(
        'aria-label',
        paused ? 'Play specials' : 'Pause specials'
      );
      schedule();
    });

    controls.appendChild(pause);
    root.appendChild(controls);

    // Positions are compared without wrapping, so advancing always moves the
    // outgoing board left and brings the incoming one in from the right. The
    // one concession is the wrap from the last board to the first: that board
    // is already marked is-before, so it enters from the left. Acceptable at
    // a 20s interval, and cheaper than cloning the first slide to fake an
    // endless track.
    function paint() {
      boards.forEach(function (board, i) {
        board.classList.toggle('is-active', i === index);
        board.classList.toggle('is-after', i > index);
        board.classList.toggle('is-before', i < index);
      });

      dots.forEach(function (dot, i) {
        dot.classList.toggle('is-active', i === index);
        if (i === index) {
          dot.setAttribute('aria-current', 'true');
        } else {
          dot.removeAttribute('aria-current');
        }
      });
    }

    function schedule() {
      window.clearTimeout(timer);
      timer = null;
      if (paused || hovered || focused || document.hidden) {
        return;
      }
      timer = window.setTimeout(function () {
        index = (index + 1) % total;
        paint();
        schedule();
      }, SPECIALS_INTERVAL);
    }

    root.addEventListener('mouseenter', function () {
      hovered = true;
      schedule();
    });

    root.addEventListener('mouseleave', function () {
      hovered = false;
      schedule();
    });

    root.addEventListener('focusin', function () {
      focused = true;
      schedule();
    });

    root.addEventListener('focusout', function () {
      focused = false;
      schedule();
    });

    // A tab in the background should not work through the specials either.
    document.addEventListener('visibilitychange', schedule);

    root.setAttribute('role', 'region');
    root.setAttribute('aria-roledescription', 'carousel');
    root.setAttribute('aria-label', 'Specials');
    root.classList.add('specials-rotator');

    paint();
    schedule();
  }

  Array.prototype.forEach.call(
    document.querySelectorAll('[data-specials]'),
    initSpecials
  );
})();
