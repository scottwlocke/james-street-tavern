# James Street Tavern — Impeccable Audit

`/impeccable audit` — 2026-10-06 (re-run). Technical quality audit of the rendered build, CSS, JS, structured data and the bundled detector output. No changes made at the time; this is the tracking document for follow-up commands.

> **Reconciled 2026-10-12.** Every finding below has since been fixed in the
> code, and each one carries a **Resolved** line naming the change and where it
> lives. The audit itself was **not** re-run — this container still has no
> browser (see *Untested* at the end) — so the numeric health score below is the
> audit-day value, kept as a baseline rather than re-measured. The resolution
> notes come from reading the source, not from a fresh detector pass. The one
> action left open is running the validator in CI, and it is called out where it
> appears (the validator is `.gitignore`d scratch tooling).

Build under test at audit time: `hugo` (extended 0.167, `baseURL` from `hugo.toml`) → 60 pages, 297 files, 14 MB `public/`. Current output: 60 pages, 322 files, **6.4 MB** — the 46 unreferenced PNG originals no longer publish, while the self-hosted fonts and the per-page 1200×630 Open Graph crops were added.

## Verdict

**PASS.** The implementation expresses one coherent, product-specific system: token-lit CSS in `DESIGN.md`'s vocabulary, tavern-specific chalkboard/wood language, a WCAG 2.2.2-correct specials rotator that degrades to a stacked panel without JS, and strict image/alt discipline. The bundled detector reported 63 findings; **62 are demonstrable false positives**, 1 is real. Independent checks surfaced three issues the detector cannot see: a heading skip, duplicated structured-data hours, and a validator that rejects the documented build. The one real detector finding and all three independent issues are now fixed; see the **Resolved** lines below.

## Audit Health Score

| # | Dimension | Score | Key Finding |
|---|-----------|-------|-------------|
| 1 | Accessibility | **3** | All AA contrast passes; no skip link, drawer focus can leave behind the open panel |
| 2 | Performance | **3** | 9.5 MB dead PNGs in the deploy; unminified CSS/JS; 260 KB single-size hero |
| 3 | Responsive Design | **3** | 2 breakpoints, 44 px+ targets, no overflow hacks; gestures untested (no browser) |
| 4 | Theming | **3** | Full token system; 3 hard-coded button states, 6 surplus tokens |
| 5 | Implementation Integrity | **3** | Coherent system; duplicate `openingHoursSpecification` on all 59 pages |
| **Total** | | **15/20** | **Good — address weak dimensions** |

Issue count: P0 = 0 · P1 = 1 · P2 = 4 · P3 = 6 — **all 11 findings fixed** (2026-10-12). Accessibility, Performance and Implementation Integrity would all score higher on a re-run; that is deliberately not claimed here, because no re-run happened.

## Detector findings — verified in context

`impeccable detect --json public layouts assets/css` → 63 findings.

- `flat-type-hierarchy` (×60) — **false positive.** The detector cannot resolve the stylesheet when scanning `public/`: the `<link>` href is `/james-street-tavern/css/style.<sha>.css` (baseURL subpath + fingerprint), so it reports *"could not read linked stylesheet"* for every page and falls back to a 16 px root with all headings at 16 px. The real values are in `assets/css/style.css`: body `1.125rem` (18 px, line 115), `.hero h1` `clamp(2.75rem, 7vw, 3.5rem)` (599), `.section-title`/`.menu-name` `2.25rem` (265/1236), `.help-band h2` `1.875rem` (1460), `.card-title` `1.5rem` (1071). Every body→heading step is ≥ 1.33× (target 1.25×). Running the detector against `layouts` + `assets/css` avoids the unresolvable path and reports only the two items below.
- `side-tab` (×2) — **false positive.** `assets/css/style.css:948` is `border-left: 12px solid var(--beer-foam)` — the CSS triangle that becomes the *play glyph* inside `.specials-pause-icon` when paused, not a card accent.
- `skipped-heading` (×1) — **real, now fixed.** Only `public/menu/index.html`: `h1 "Full Menu"` → `h3 "Pizza"` with no `h2`. **Resolved:** `layouts/partials/menu-section.html` renders the section title as an `h2` (the partial is only ever called directly under `/menu/`'s `h1`), so the outline is clean on all 60 pages — re-verified on the whole build by `.tmp/validate-jsonld.py`, which now checks heading order page by page.

## Detailed findings by severity

### P1

- **No skip link**
  - **Location**: `layouts/_default/baseof.html:7-11` (`<header>` before `<main>`, `main` has no `id`) — all 60 pages
  - **Category**: Accessibility
  - **Impact**: keyboard and screen-reader users tab through the whole logo + nav cluster (logo link, 3 nav links, or on narrow widths the toggle) before reaching content, on every page
  - **WCAG/Standard**: 2.4.1 Bypass Blocks (AA)
  - **Recommendation**: render a visually-hidden-until-focused `Skip to content` link as the first focusable element in `<body>`, `href="#main"`, give `<main>` `id="main"`, style it with the existing `:focus-visible` gold outline
  - **Suggested command**: `/impeccable harden`
  - **Resolved:** `layouts/_default/baseof.html` now renders
    `<a class="skip-link" href="#main">Skip to content</a>` as the first
    focusable element in `<body>`, and `<main id="main">` wraps the content
    block. `.skip-link` (`assets/css/style.css:188`) is visually hidden until it
    takes focus, using the existing gold `:focus-visible` outline.

### P2

- **Menu page skips h1 → h3**
  - **Location**: `layouts/partials/menu-section.html:7` (`<h3 class="menu-section-title">`), called only from `layouts/_default/full-menu.html:26`
  - **Category**: Accessibility
  - **Impact**: on the site's primary menu page, heading navigation jumps "Full Menu" (h1) straight to h3 eight times; the eight section headings are invisible to a heading-level reader, and the next h2 on the page is the unrelated help band
  - **WCAG/Standard**: 1.3.1 Info and Relationships (A) / heading-outline best practice
  - **Recommendation**: promote the section title to `<h2>` — it is only ever rendered directly under the page's h1, so no other page's outline changes
  - **Suggested command**: `/impeccable typeset`
  - **Resolved:** `layouts/partials/menu-section.html:12` renders
    `<h2 class="menu-section-title">`; styling is by class, so the change is
    invisible. `/menu/` is now `h1` followed by nine `h2`s (eight sections plus
    the help band), no skip.

- **Every `openingHoursSpecification` is emitted twice**
  - **Location**: `layouts/partials/jsonld.html:49-60` reading `hugo.toml:137-169` (two `[[params.hours]]` areas, Bar and Kitchen, with three identical groups each)
  - **Category**: Implementation Integrity
  - **Impact**: all 59 structured-data pages declare 6 specs where there are 3 unique ones — each day's hours stated twice with nothing to distinguish them, because the template drops `area`. Harmless-looking today, but the moment Bar and Kitchen hours diverge the schema will publish two conflicting open windows for the same day with no way to tell them apart
  - **Standard**: schema.org `Restaurant.openingHoursSpecification`; Google structured-data quality
  - **Recommendation**: dedupe after building the slice (e.g. `uniq` on the marshalled dict), or associate each spec with its `area` so duplicates become distinct claims
  - **Suggested command**: `/impeccable harden`
  - **Resolved:** `layouts/partials/jsonld.html:51-81` dedupes as it builds,
    keying on `days|opens|closes` in a `newScratch` set (deliberately not
    relying on Hugo's set operations comparing two maps). Built output now
    carries **3** `OpeningHoursSpecification` nodes per page, not 6. `hugo.toml`'s
    hours block records the choice: identical windows collapse to one claim, and
    a future Bar/Kitchen divergence yields two genuinely distinct windows that
    both belong in the schema.

- **Drawer focus can leave into content the open panel covers**
  - **Location**: `assets/js/main.js:8-40`, `layouts/partials/nav.html:57`; CSS `.mobile-nav` `inset: var(--nav-h) 0 0`, z-index 99
  - **Category**: Accessibility
  - **Impact**: opening does not move focus into the drawer, and nothing contains it there — after the last drawer link, Tab walks into `<main>` content that sits *behind* an opaque full-viewport panel, so the focus ring is invisible and the reader loses their place. Escape, `aria-expanded`/`aria-hidden` sync and `visibility: hidden` when closed are all correct; `body.nav-open { overflow: hidden }` locks scroll but not focus
  - **WCAG/Standard**: 2.4.3 Focus Order (A)
  - **Recommendation**: move focus to the first drawer link on open, trap Tab within the drawer while open, and return focus to the toggle on close (or mark the drawer and background `inert`)
  - **Suggested command**: `/impeccable harden`
  - **Resolved:** `assets/js/main.js` moves focus to the first drawer link on
    open (`setOpen`), traps Tab within the header bar plus drawer
    (`focusables()` drops the hidden desktop links via `getClientRects()`), and
    returns focus to the toggle only on an explicit close — a link activation
    keeps the browser's own focus move so the in-page `#contact` jump is not
    undone.

- **The documented build makes the documented validator report 59 false failures**
  - **Location**: `.tmp/validate-jsonld.py:227` (`<link rel=canonical href="?…`) vs `AGENTS.md` "Build: `hugo`"; CI uses `hugo --gc --minify` (`.github/workflows/hugo.yml:92`)
  - **Category**: Implementation Integrity
  - **Impact**: the regex only matches *unquoted* attributes, which is what `--minify` produces. On a plain `hugo` build every page still carries a correct `<link rel="canonical" href="…">`, but the validator prints `expected exactly 1 canonical, got 0` 59 times and exits 1 — so the project's own verification step fails against the project's own build command, and a real canonical regression would be indistinguishable from that noise. Verified: `hugo --minify` + validator → `PASS`; plain `hugo` + validator → 59 errors
  - **Recommendation**: accept both attribute forms (`rel=?"canonical"`), and/or state the `--minify` pairing next to the validate command. Consider running the validator in CI, which today only scans for credentials and builds
  - **Suggested command**: `/impeccable harden`
  - **Resolved:** `.tmp/validate-jsonld.py:225-231` matches `rel="?canonical"?`
    and `href="?…"?`, so it now passes on both a plain `hugo` and
    `hugo --minify` build. **Not done, and left open:** the validator is still
    not run in CI — it is scratch tooling that `.gitignore` excludes, so CI
    would have to commit it first. The workflow (`scan` → `build` → `deploy`)
    is unchanged.

### P3

- **9.5 MB of unreferenced PNGs ship in the build**
  - **Location**: `public/**/photo-*-hero.png` — 46 originals, ~208 KB each; zero `<img src>` references anywhere in the output
  - **Category**: Performance
  - **Impact**: 68% of the 14 MB artifact is fetched by nobody; deploy and clone weight only (no user-facing cost, which is why this is not P2)
  - **Recommendation**: move the 46 sources from the page bundles into `assets/` (the open task in `AGENTS.md`); derivatives are already generated from there by `dish-image.html`
  - **Suggested command**: `/impeccable optimize`
  - **Resolved, by a different route:** the sources stayed in the page bundles,
    but every menu section's `_index.md` (and `content/specials/_index.md`)
    carries `[cascade.build] publishResources = false`, so Hugo stops publishing
    bundle resources verbatim. Built output now contains **0**
    `photo-*-hero.png`. See `AGENTS.md` — that cascade is the whole reason the
    originals stay out; removing it roughly triples `public/`.

- **CSS and JS ship unminified**
  - **Location**: `public/css/style.<sha>.css` 42,400 B / 1,672 lines (11,116 B gzipped); `assets/js/main.js` 6,757 B (2,302 B gzipped)
  - **Category**: Performance
  - **Impact**: GitHub Pages serves gzip, so the shipped cost is already modest — but `hugo --minify` demonstrably does **not** touch the fingerprinted stylesheet (byte-identical output, comments and blank lines intact), so CI's `--minify` buys HTML only
  - **Recommendation**: run the CSS through `resources.Minify` in `layouts/partials/head.html:68` before fingerprinting
  - **Suggested command**: `/impeccable optimize`
  - **Resolved:** `layouts/partials/head.html` pipes the CSS through
    `minify | fingerprint "sha256"` (in that order), and
    `layouts/_default/baseof.html:29` does the same for `js/main.js`. Both ship
    minified, and the fingerprint still changes whenever the bytes do. The
    ordering is deliberate: piping a resource means `hugo --minify` leaves it
    byte-identical, which is why the minify step lives in the template.

- **The homepage LCP image is a single 260 KB JPEG with no priority hint**
  - **Location**: `assets/images/photo-tavern-hero.jpg` (259,933 B, 1200×800), rendered at `layouts/partials/hero.html:17`
  - **Category**: Performance
  - **Impact**: largest single asset on the landing page and 57% of its first-load bytes; unlike the 46 dish photos it gets no responsive derivatives, no `srcset`, no `fetchpriority="high"` and no `decoding="async"`. It is `position: absolute; inset: 0`, so the missing `width`/`height` do **not** cause layout shift — that part is fine
  - **Recommendation**: put it through the same pipe as `dish-image.html` (WebP widths + JPEG fallback) and add `fetchpriority="high"`
  - **Suggested command**: `/impeccable optimize`
  - **Resolved:** `layouts/partials/hero.html` now renders the hero through
    `dish-image.html` — 480 / 768 / 1080 / 1200 WebP widths plus a JPEG
    fallback, all fingerprinted, with `fetchpriority="high"` and no
    lazy-loading. JSON-LD's home `image` points at the largest WebP, not the
    260 KB original.

- **Render-blocking Google Fonts stylesheet**
  - **Location**: `layouts/partials/head.html:12`
  - **Category**: Performance
  - **Impact**: a font-hosting stall holds first paint; `preconnect` + `display=swap` bound the damage, self-hosting removes the third-party dependency entirely
  - **Suggested command**: `/impeccable optimize`
  - **Resolved:** fonts are self-hosted. Three variable `woff2` files in
    `assets/fonts/` (Oswald, Source Sans 3, Permanent Marker) are fingerprinted,
    `@font-face`-inlined and preloaded by `layouts/partials/fonts.html`. No
    `fonts.googleapis.com` request remains in `layouts/` or `assets/`. The one
    third-party request left is the Google Maps `<iframe>` in
    `partials/contact.html` — the map itself, which this origin cannot host.

- **Global reduced-motion kill, and one layout-property transition**
  - **Location**: `assets/css/style.css:1661-1671` (`animation-duration`/`transition-duration: 0.01ms !important`); `style.css:903-904` (`.specials-dot-mark` animates `width`)
  - **Category**: Accessibility / Performance
  - **Impact**: the rubric flags the blanket 0.01 ms rule. It is compliant *here* — every animation is decorative, state changes still land instantly, the rotator yields while a board's own link holds focus and has its mandatory pause control — but it also flattens the pause button's colour feedback. The dot's `width` 10→26 px is the only layout-property animation on the site; everything else is transform/opacity/colour
  - **Recommendation**: keep the blanket rule; exempt focus/colour feedback from it if it tightens further, and swap the dot's `width` for `transform: scaleX`
  - **Suggested command**: `/impeccable animate`
  - **Resolved (the actionable half):** `.specials-dot-mark` now animates
    `transform: scaleX(2.6)` (`assets/css/style.css:1006-1023`) instead of
    `width`, so no layout property is animated anywhere. The blanket
    reduced-motion rule is kept on purpose, exactly as this finding advised.

- **Three hard-coded button-state colours, six surplus tokens**
  - **Location**: `assets/css/style.css:498-505` (`#163a75`, `#0a1f42`), `style.css:528-529` (`#f0d469`); unused `--barn-red`, `--success`, `--warning`, `--error`, `--info`, `--panel-raised` (defined at lines 17, 23-26, 31, never read)
  - **Category**: Theming
  - **Impact**: the token system is otherwise complete and every other colour resolves through `var()`; derived hover/active tokens keep the ratios auditable. `--radius-none` and `--radius-badge` are also unused but that is deliberate per DESIGN §14 (reserved), so they are not findings
  - **Suggested command**: `/impeccable polish`
  - **Resolved:** the three button-state literals are now tokens —
    `--tavern-navy-hover`, `--tavern-navy-active`, `--chalk-gold-hover`
    (`assets/css/style.css:55-57`) — so every button-state pair is auditable
    from `:root`. The remaining names are kept deliberately and now say why in
    place: `--barn-red` is reserved palette (`style.css:18`), and
    `--success/--warning/--error/--info` are DESIGN.md's Semantic Colors table
    (`style.css:27-36`) — palette a component may spend later, not dead code.
    `--panel-raised` turned out to be read by both wood gradients.

## Systemic patterns

1. **The detector's evidence path degrades on fingerprinted, baseURL-prefixed assets.** Scanning `public/` makes it unable to read the stylesheet, which manufactures 60 flat-type-hierarchy findings from a 16 px default. Always pair a `public/` scan with a `layouts` + `assets/css` scan, or add an ignore rule for `flat-type-hierarchy` if audits become routine.
2. **Two sources of truth for hours — resolved.** `params.hours` is consumed by `partials/contact.html` (as labelled Bar/Kitchen columns) and by `partials/jsonld.html` (as a flat spec list). The schema side still has no place for the label, but it now dedupes on the times, so two areas that agree produce one claim and a future divergence produces two genuinely distinct windows instead of two indistinguishable copies. The silent duplicate-emission bug is gone.
3. **Local build and CI build — reconciled.** CI runs `hugo --gc --minify` and `AGENTS.md` documents `hugo`; the validator now accepts both attribute spellings, so it passes against either. `baseURL` is read from `hugo.toml` in both, so the two stay byte-comparable apart from whitespace. The one loose end this pattern named is that the validator is still not a CI step (it is scratch tooling).

## Positive findings

- **262/262 images carry `alt`** — 105 meaningful, 157 decorative (`alt=""` + `aria-hidden`), zero bare. The nav crest's alt is the link's only accessible name; the footer crest is correctly the opposite.
- **All 24 measured colour pairs pass AA.** Lowest real pair 6.01:1 (chalk gold on barn wood, `.help-band h2` at 30 px); most are ≥ 8:1 — off-white/chalkboard 15.32, off-white/panel 14.54, gold/chalkboard 10.37, muted-on-panel 7.44. The known trap (honey oak on barn wood, 4.32:1) never carries text: `.section-wood .section-kicker` overrides to gold, and every other honey-oak run sits on panel or chalkboard.
- **Specials rotator implements WCAG 2.2.2 properly**: runtime pause/play with action-stating labels, yields while a board's own link holds focus, parks in background tabs, no `aria-live`, carousel semantics added only when JS runs, and no-JS degrades to a readable stack (`.specials-rotator` never appears in the template).
- **Structure is clean across all 60 pages**: exactly one `h1` each, zero duplicate `id`s, `header`/`nav`/`main`/`footer` landmarks present everywhere, `lang="en-us"`, every page has a title and description, every `#fragment` resolves to an in-page target, `aria-current="page"` correct on `/menu/` and across the whole Specials section.
- **Loading discipline**: 96 lazy / 44 `fetchpriority="high"`, `width`+`height` on every derivative (the 9 images without them are the absolutely-positioned hero and the 8 `aspect-ratio: 16/10` SVG placeholders — both box-reserved, no CLS), SRI `integrity` on CSS and JS, sha256 fingerprinting on CSS, JS and the hero.
- **No overflow hacks**: zero `overflow-x`, zero `100vw`, fixed pixel values appear only as breakpoint media queries, two-column splits use `minmax(0, …)`, and every interactive element measures ≥ 44 px (`min-height`/`min-width`, not padding tricks).
- **Responsive images are well-built**: three WebP widths + JPEG fallback per dish with per-call-site `sizes` written from the actual grid (357 px card / 440 px detail), `display: block` on `<picture>`, vector art explicitly exempted in the partial.

## Recommended actions

All six are done (2026-10-12) except where noted:

1. **[P1] `/impeccable harden`**: skip link + `id="main"`, drawer focus move/contain/restore — **done**
2. **[P2] `/impeccable typeset`**: promote the menu page's section titles from h3 to h2 — **done**
3. **[P2] `/impeccable harden`**: dedupe `openingHoursSpecification` — **done**; validator now accepts both `rel` spellings — **done**; run the validator in CI — **not done** (scratch tooling, `.gitignore`d)
4. **[P3] `/impeccable optimize`**: the 46 PNG originals no longer publish — **done**; `minify` the CSS — **done**; responsive hero + `fetchpriority` — **done**; self-host fonts — **done**
5. **[P3] `/impeccable animate`**: dot `width` → `transform: scaleX` — **done**; the blanket reduced-motion rule is kept on purpose
6. **[P3] `/impeccable polish`**: button-state colours are now tokens — **done**; the remaining unused names are kept and documented as reserved palette

## Untested — honest limits

No usable browser in this container (`chromium-browser` is an uninstalled snap stub, no Node/Playwright), so no rendered viewport, no synthesized touch for the drawer gesture, no live horizontal-overflow or 200 % text-scaling check, and no measured contrast sampled from painted pixels. Evidence is static HTML/CSS/JS inspection, computed contrast from the token values, JSON parsed out of the built pages, and `impeccable detect` over `public` + `layouts` + `assets/css`. Hero-button contrast over photography is argued from the scrim construction (`.hero::before` at 0.92 alpha over a `brightness(0.72)` image), not measured.

Re-run `/impeccable audit` after fixes to re-measure the score. As of 2026-10-12 the fixes have landed but the re-run has not — there is still no browser in this container — so the score above remains the 2026-10-06 value.
