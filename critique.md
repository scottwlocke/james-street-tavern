# Layout Critique — James Street Tavern

## Summary
The Hugo static site for James Street Tavern is well-structured and consistent with the DESIGN.md design system. All layouts correctly implement the design tokens, responsive patterns, and content opt-outs described in the specification. The site builds successfully with `hugo` (62 pages, no warnings).

## What Works Well

### 1. Hero Layout (`layouts/hero.html`)
- Photo lives in `assets/`, not `content/` — prevents unversioned `/photo-tavern-hero.jpg`
- Hugo Pipes with fingerprint `"sha256"` gives URL content hash on image change
- Derivative widths (480/768/1080/1200) with `sizes="100vw"` for full hero box
- `fetchpriority="high"` + `decoding="async"` for LCP element
- Correctly uses same `dish-image.html` partial for derivative generation

### 2. Specials Chalkboard (`layouts/specials.html`)
- All boards ship in markup; `.chalkboards` is an ordinary grid
- No `.specials-rotator` class emitted server-side (JS handles hiding)
- `.is-active` on first board server-side so rotator has starting state
- No `data-specials` hook — rotation is homepage-only device
- Correctly kept out of menu listings via `nonMenuSections = ["specials"]` in `hugo.toml`

### 3. Section Grid & Menu Surfaces (`layouts/sections-grid.html`, `menu-sections.html`)
- `menu-sections.html` is the **single source of truth** for section list
- Read by: homepage card grid, mobile drawer (`nav.html`), full menu page (`full-menu.html`)
- `nonMenuSections` opt-out in `hugo.toml` keeps specials out of all surfaces
- No inline filtering of `.Site.Sections` at call sites

### 4. Dish Cards (`layouts/partials/menu-card.html`)
- `show-image.html` gate with `isset .Params "showimage"` — correct opt-out behavior
- `showimage = false` omits `.card-media` entirely + adds `.is-text` class
- Responsive `<picture>` with WebP srcset (480/768/1080) + JPEG fallback
- Correct `sizes` per grid state: 357px card, 440px detail
- Price from front matter, description from front matter
- `.is-text` sets `align-self: start` so card sizes to its own content

### 5. Section Cards (`layouts/partials/section-card.html`)
- `photoGlob` resolution for section placeholder art
- Blurb via `blurb.html` with correct precedence: page description → params.sections → lead
- Section always keeps art (opt-out different from dishes — sections are always "card of something")
- Blurb appears in both card **and** meta description (keeps two from quoting different text)

### 6. Contact (`layouts/partials/contact.html`)
- Address/phone/email from `hugo.toml` params (single source of truth)
- Hours also from `hugo.toml` params — same table renders as display table **and** JSON-LD `openingHoursSpecification`
- Map iframe with `loading="lazy"` + `referrerpolicy="strict-origin-when-cross-origin"`

### 7. Typography & Tokens
- **Oswald** for all structural text: headings, prices, buttons, nav, labels — always uppercase with positive tracking
- **Source Sans 3** for body copy at weight 400, 1.6 line height
- **Permanent Marker** rationed to two roles only: specials title + section kicker
- All tokens referenced from DESIGN.md inventory, never re-derived in prose or CSS

### 8. Responsive Grid
- 3 columns → 2 → 1 via CSS media queries
- Cards keep `{rounded.md}` (8px) and warm shadow (`0 8px 24px rgba(44,27,16,0.35)`) at all sizes
- Only column count changes per breakpoint
- Gutters: 24px mobile → 40px desktop

### 9. Navigation (`layouts/nav.html`)
- Top bar: Logo / Specials / Full Menu / Contact (no Menu dropdown — "Full Menu" already opens itemised board)
- Specials is a peer control, not a menu section (kept out via `nonMenuSections`)
- Mobile drawer carries identical section list via `$menuSections` partial
- Logo `alt` carries full site name (`James Street Tavern — Monroeville, PA`) — the only accessible name

### 10. Full Menu (`layouts/_default/full-menu.html`)
- `$count` shows total dishes across sections
- Renders each section via `menu-section.html` partial
- Section count and dish count always in sync (both read from `menu-sections.html`)

### 11. JSON-LD (`layouts/partials/jsonld.html`, `jsonld-menuitem.html`)
- Single `@graph` array per page
- Photo gate shared: `showimage = false` drops schema image where it drops card/detail images
- Price from front matter once — no restatement
- Section list from same `menu-sections.html` partial — `nonMenuSections` honored identically
- Hours from `params.hours` — same table renders as display table **and** schema
- 404 carries no structured data (it is `noindex`)

### 12. Hugo.toml Structure
- `[[params.hours]]` array placed **last** below every bare key and after all `[params.*]` sub-tables
- Load-bearing ordering: array-of-tables blocks go last
- `photoGlob = "photo-*-hero.*"` for dish photo resolution
- `nonMenuSections = ["specials"]` keeps specials out of menu surfaces
- `home = ["HTML", "Robots"]` + `section = ["HTML"]` — RSS deliberately absent
- `disableKinds = ["taxonomy", "term"]` — taxonomies switched off

## Design Token Compliance
| Category | Status |
|---|---|
| Color palette | All tokens used correctly (navy `#0F2C5B`, gold `#E8C547`, charcoal `#1A1A1A`, wood `#5C3A21`, cream `#F5F0E6`) |
| Typography | Oswald/Source Sans 3/Permanent Marker mapped to correct roles |
| Spacing | 8px base unit, correct gutter progression (24→40px) |
| Border radius | Buttons at `{rounded.sm}` (4px), cards at `{rounded.md}` (8px) |
| Elevation | Warm shadows `0 8px 24px rgba(44,27,16,0.35)` on cards/panels |
| Breakpoints | Mobile (<768px), Tablet (768–1023px), Desktop (≥1024px) — correct collapsing |
| Accessibility | 44px minimum touch targets, gold contrast checked, reduced-motion friendly |
| Imagery | Photos in `assets/`, fingerprinted, derivatives via Hugo Pipes |
| File naming | Per §12 conventions (photo-<section>-hero.svg in bundles, assets/images/dishes/ mirror) |

## No Critical Issues
The layouts are largely **correct and well-implemented** per DESIGN.md. The site:
- Builds cleanly with `hugo` (no warnings)
- Has consistent single sources of truth (params, menu-sections.html, show-image.html gate)
- Properly opt-outs `showimage = false` without leaving originals in `public/`
- Keeps specials out of all menu surfaces via `nonMenuSections`
- Uses correct Hugo 0.167 patterns (`fingerprint` as function, not method)
- Maintains accessibility contrast and touch targets

## Verification
- `hugo` build: succeeds, 62 pages, 181 processed images, 0 warnings
- JSON-LD validation: `.tmp/validate-jsonld.py` (scratch tool, gitignored)
- No hardcoded domains — all URLs from `.Permalink` / `absURL` inheriting `baseURL`
- No raw HTML in Markdown content — Goldmark `unsafe = false`

## Recommended Next Steps (Optional)
If adding new sections/dishes:
- Ensure `nonMenuSections` in `hugo.toml` is updated if specials-like behavior needed
- Place `[[params.hours]]` array last in TOML (load-bearing ordering)
- Keep `photoGlob = "photo-*-hero.*"` for new dish photo resolution
- Section placeholder SVGs at `content/<section>/photo-<section>-hero.svg` (optional, for fallback)
- Run `hugo server -D` to preview with drafts

The site is production-ready with no required layout changes.