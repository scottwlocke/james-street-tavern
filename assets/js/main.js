(function () {
  'use strict';

  // ---- Mobile navigation drawer ----
  const toggle = document.querySelector('.nav-toggle');
  const drawer = document.getElementById('mobile-nav');

  // Everything that can hold focus while the drawer is open: the header bar
  // (crest, the three desktop links, the toggle) plus the drawer's own list.
  // The desktop links resolve to no boxes at drawer widths, so they are
  // filtered out rather than left as dead stops in the wrap.
  function focusables() {
    return Array.prototype.slice
      .call(document.querySelectorAll('header a[href], header button, #mobile-nav a[href]'))
      .filter(function (el) {
        return el.getClientRects().length > 0;
      });
  }

  function isOpen() {
    return !!drawer && drawer.classList.contains('open');
  }

  function setOpen(open, restoreFocus) {
    if (!toggle || !drawer) {
      return;
    }
    drawer.classList.toggle('open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    toggle.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('nav-open', open);

    if (open) {
      // Focus has to enter the drawer, otherwise the first Tab starts from
      // the toggle and runs straight into the content the open panel covers.
      const first = drawer.querySelector('a[href]');
      if (first) {
        first.focus();
      }
    } else if (restoreFocus) {
      // Only on an explicit close (Escape, or the toggle itself). On link
      // activation the browser is about to move focus to the target — or, for
      // the in-page #contact link, already has — and yanking it back to the
      // top of the page would undo the jump the visitor just asked for.
      toggle.focus();
    }
  }

  if (toggle && drawer) {
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true', false);
    });

    drawer.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        setOpen(false, false);
      });
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        if (isOpen()) {
          setOpen(false, true);
        }
        return;
      }

      // 2.4.3 Focus Order: while the panel is open, Tab must cycle through the
      // bar and the drawer instead of continuing into <main>, which sits
      // behind an opaque full-viewport panel. Without this the focus ring is
      // painted where nobody can see it.
      if (event.key !== 'Tab' || !isOpen()) {
        return;
      }

      const items = focusables();
      if (items.length === 0) {
        return;
      }

      const first = items[0];
      const last = items[items.length - 1];
      const active = document.activeElement;
      const inside = items.indexOf(active) !== -1;

      if (event.shiftKey) {
        if (!inside || active === first) {
          event.preventDefault();
          last.focus();
        }
      } else if (!inside || active === last) {
        event.preventDefault();
        first.focus();
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 1024) {
        setOpen(false, false);
      }
    });
  }

  // The desktop "Menu" dropdown and the top-right "Find Us" control have both
  // been removed from the markup, so their handlers went with them. The drawer
  // above is now the only place the section-by-section list appears, and it
  // needs no open/close logic beyond the toggle that is already here.

  // ---- Specials rotator ----
  // The specials board shows one chalkboard at a time and slides to the next
  // every 5s. Every board ships in the markup and the track is a plain block,
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
  const SPECIALS_INTERVAL = 5000;

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
    // a 5s interval, and cheaper than cloning the first slide to fake an
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
