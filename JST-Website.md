# James Street Tavern — Website Build Summary

Handoff / state document for the Hugo static site at `/workspaces/JST`.
Use this to pick up work quickly.

---

## 1. Project Status

- **Stack:** Hugo (v0.165.0+extended), no theme — custom layouts live in root `layouts/`.
- **Build:** `hugo` → outputs to `public/`. Clean build, no warnings.
- **Preview with drafts:** `hugo server -D` (archetype defaults new pages to `draft = true`).
- **Not yet done:** `baseURL` in `hugo.toml` is still the `https://example.org/` placeholder — must be changed to the real domain before deploy.

---

## 2. Design System (DESIGN.md)

**`DESIGN.md` is the only design specification for this site.** The layouts and
`static/css/style.css` implement it and nothing else.

- **Colors:** tavern navy `#0F2C5B` (`--tavern-navy`) for the dark canvas; chalk gold `#E8C547` (`--chalk-gold`) rationed as the single accent; chalkboard green-black (`--chalkboard`) for panels; barn wood (`--barn-wood`), honey oak, barn red and beer foam as surface/secondary tones. Off-white for body text.
- **Typography:** three families, each with one job. **Oswald** (500/600/700) for signage — headings, nav, buttons, prices, wordmark. **Source Sans 3** (400/600) for all body copy. **Permanent Marker** (400) is hand-lettered chalk, restricted to exactly two roles: the specials kicker and the specials title. Full role/weight/size/leading map is `DESIGN.md` §3.
- **Shapes:** two radii only. Buttons, toggles and the JST shield at 4px (`--radius-sm`); cards, panels, the chalkboard and dropdowns at 8px (`--radius-md`); 50% (`--radius-badge`) is exclusive to the circular logo badge. Sharp buttons, soft containers.
- **Spacing:** `--space-*` scale; 96px section padding; 40px grid gutter dropping to 24px below 1024px.
- **Depth:** five levels, every shadow warm `rgba(44, 27, 16, …)` rather than grey. Recessed and vignette levels are single-use (chalkboard, hero).
- **Tokens** are declared as CSS custom properties at the top of `static/css/style.css` and mirror `DESIGN.md`'s token names (`--tavern-navy`, `--chalk-gold`, `--space-2xl`, `--radius-md`, `--shadow-recessed`, etc.).

> **Do not** reintroduce the retired HP Electric Blue system (Electric Blue
> `#024ad8`, white/cloud canvas, single-family Inter, 16px card radius, blue
> chevrons, Limelight/Forma display faces). Those specifications are not
> authoritative and are not part of this site. See §10.

### Section reference

`DESIGN.md` is organised as: §1–2 identity, §3 typography, §4 chalkboard panel,
§5 film grain, §6 layout regions, §7 palette, §8 surface depth, §9 motion,
§10 hero, §11 CTA buttons, §12 file & asset naming, §13 implementation notes,
§14 border radius scale, §15 elevation & depth, §16 breakpoints & collapsing
strategy, §17 component inventory, §18 do's and don'ts, §19 iteration guide.

---

## 3. Content Architecture (the menu)

- Each menu section is a top-level folder under `content/` (e.g. `content/pizza/`).
- Each section has a `_index.md` whose `title` becomes the homepage section heading; a `weight` controls section order.
- Each menu item is one Markdown file:
  - **With a picture:** a page bundle — `content/<section>/<item>/index.md` + `content/<section>/<item>/photo-<subject>-hero.jpg` (DESIGN.md §12 naming). The layout auto-detects the image via `.Resources.GetMatch` on the `photoGlob` site param.
  - **Without a picture:** a plain file — `content/<section>/<item>.md`. The card renders without an `<img>`.
- Item front matter (TOML):
  ```toml
  +++
  title = "Classic Margherita"
  price = "$14.99"
  description = "Short description shown on the card."
  weight = 10   # sort order within the section
  +++
  ```
- The homepage iterates `.Site.Sections` and renders every section, in `weight` order.

**Current menu (8 sections, 46 items):**

| Section | Items | Notes |
| --- | --- | --- |
| **Appetizers** | 12 | Flat `.md` files |
| **Hoagies & Sandwiches** | 9 | Flat `.md` files |
| **Pizza** | 5 | Organised **by size** (`large`, `medium`, `small`) + `toppings` + `ultimate-pepperoni` |
| **Salads** | 5 | Flat `.md` files |
| **Stromboli** | 5 | Flat `.md` files |
| **Wings** | 5 | Flat `.md` files, plus `wing-flavors` |
| **Burgers** | 3 | Flat `.md` files |
| **Eggrolls** | 2 | Flat `.md` files |

Section order on the homepage comes from the `weight` in each section's
`_index.md`. The homepage iterates `.Site.Sections` and renders every section in
that order.

**Note:** this content set replaced an earlier 3-section / 14-item menu, which is
archived in `content-old/`. `pizza` is now organised by size rather than by
variety.

---

## 4. Layout Architecture

```
layouts/
├── _default/
│   ├── baseof.html     # HTML shell: head, nav + mobile drawer, <main>, help band, footer, main.js
│   └── single.html     # Individual menu item detail page
├── index.html          # Homepage: hero → specials chalkboard → menu sections → contact
├── section.html        # A section's full listing (e.g. /pizza/)
├── partials/
│   ├── head.html       # <head>: meta, Google Fonts (Oswald, Source Sans 3,
│   │                   #   Permanent Marker), css/style.css
│   ├── nav.html        # Utility strip + logo + inline links (desktop)
│   │                   #   + hamburger toggle + mobile drawer
│   ├── hero.html       # Hero: copy + image (home-bundle resource via photoGlob → fallback)
│   ├── specials.html   # Monday Night Wings chalkboard special (DESIGN.md §4)
│   ├── menu-section.html   # Section title + menu grid
│   ├── menu-grid-items.html  # Grid container for a section's items
│   ├── menu-card.html  # One menu item card (conditional image)
│   ├── sections-grid.html   # Section card grid on the homepage
│   ├── section-card.html    # One section card
│   ├── contact.html    # Visit info + two-column Bar/Restaurant hours
│   ├── help-band.html  # Dark "How can we help?" band
│   └── footer.html     # Multi-column dark footer
static/
├── css/style.css       # All styles (design tokens + components + responsive)
├── js/main.js          # Hamburger drawer toggle logic
└── logo-jst-monogram.svg  # Favicon + wordmark monogram
```

> The utility strip is part of `nav.html`; there is no separate
> `utility-strip.html` partial.

---

## 5. Key Decisions & Choices

1. **No theme — custom `baseof.html`.**
   A hand-rolled layout keeps full control over the DESIGN.md tokens instead of fighting an installed theme.

2. **Config-driven content over hardcoding.**
   Address, phone, email, hours, hero copy, and help-band text all live in `[params]` in `hugo.toml`. Update them in one place.

3. **CSS custom properties as the DESIGN.md token layer.**
   `static/css/style.css` declares the design tokens at `:root`, then components reference the variables. This makes DESIGN.md → CSS mapping explicit and auditable.

4. **Two CSS encoding bugs fixed during development:**
   An initial draft used invalid CSS arithmetic (`var(--space-xxl) * 1.5`). These were replaced with concrete pixel values from the `--space-*` scale, matching `DESIGN.md` §6 spacing.

5. **Image strategy — page bundles auto-detect images.**
   Items with photos live in bundles so the image ships with its markdown. The card template looks for a `photo-*-hero.*` resource (via the `photoGlob` site param); flat `.md` files naturally skip the `<img>` — no front-matter flag needed.

6. **Hero image resolution order:**
   Home-page bundle resource (`content/photo-tavern-hero.jpg`, matched by `photoGlob`) → `heroImage` site param → no image. If the hero renders copy with no photo, the home bundle resource is missing **and** no `heroImage` param is set. This currently falls through to the last case: `DESIGN.md` §10 calls for copy + image, so restore the bundle photo or set `heroImage`.

7. **Hamburger nav (mobile) per DESIGN.md.**
   Below **1024px** the inline `.nav-links` are hidden and a 44px hamburger toggle appears. It opens a full-canvas drawer sliding from the right (below the 36px utility strip + 64px nav = 100px) with `body-lg` links and a sticky "Sign in" CTA. Drawer closes on link click, Escape, or resizing above 1024px. Accessibility states (`aria-expanded`, `aria-hidden`) are maintained in `static/js/main.js`.

8. **Taxonomies disabled.**
   `[taxonomies] tag = [] category = []` in `hugo.toml` removes the auto-generated category/tag taxonomy pages that triggered "no layout file for kind taxonomy" build warnings.

9. **Single-page contact layout.**
   The original 2-column contact grid (info + form) became single-column after the "Send a Message" form was removed. Bar and Restaurant hours render side-by-side in `.hours-columns` (stack to one column below 768px).

10. **DNSS-style no-hardcoded-internal-links.**
    Internal URLs use `.Site.BaseURL` / `relURL`; external Unsplash images were downloaded and vendored into the content bundles (no hotlinked remote images in the build).

---

## 6. Site Parameters (hugo.toml `[params]`)

| Param | Value |
| --- | --- |
| `location` | Monroeville, PA (utility strip) |
| `address` | 1224 James St, Monroeville, PA 15146 |
| `phone` | 412-824-8884 |
| `email` | info@jst-tavern.com |
| `heroKicker` | Your Neighborhood Tavern |
| `heroTitle` | Come Hungry. Leave Happy. |
| `heroDescription` | Jumbo whole wings, cold beer, and a wood-fired kitchen… |
| `specialsKicker` / `specialsTitle` | Monday Night / Monday Night Wings |
| `specialsPrice` / `specialsPriceUnit` | $1.50 / each |
| `menuKicker` / `menuTitle` / `menuIntro` | The Chalkboard / What's On Today / … |
| `helpBandText` | Questions about catering, reservations, or private events? |
| `photoGlob` | `photo-*-hero.*` — the asset-naming pattern layouts resolve images by |
| `barHours` / `restaurantHours` | Mon–Fri 3PM–2AM; Sat & Sun 12PM–2AM (both columns) |
| `sections.<name>` | Section blurbs. Currently defined for `pizza`, `wings`, `salads` only — the other five sections fall back to their own front matter. |

---

## 7. Current Business Hours

| Day | Hours |
| --- | --- |
| Monday – Friday | 3 PM – 2 AM |
| Saturday | 12 PM – 2 AM |
| Sunday | 12 PM – 2 AM |

Shown twice on the homepage — once under **Bar**, once under **Restaurant** — from the separate `barHours` / `restaurantHours` params (edit them independently if the hours ever diverge).

---

## 8. How to Add / Change Menu Items

1. **With a photo:** create `content/<section>/<item>/index.md` and drop the photo in as `photo-<subject>-hero.jpg` (DESIGN.md §12).
2. **Without a photo:** create `content/<section>/<item>.md`.
3. Front matter: `title`, `price`, `description`, `weight`.
4. To start a new section: create `content/<newsection>/_index.md` with `title` + `weight`; it appears automatically on the homepage.

---

## 9. Outstanding / Next Steps

- [ ] Set the real domain in `hugo.toml` (`baseURL`) before deploy.
- [ ] **Restore the hero image.** `content/photo-tavern-hero.jpg` was moved to `content-old/` during the content restructure, so `DESIGN.md` §10's hero currently renders copy with no photo. Either move it back to `content/` or set a `heroImage` param.
- [ ] Add `[params.sections]` blurbs for the five sections that lack one: `appetizers`, `burgers`, `eggrolls`, `hoagies-sandwiches`, `stromboli`.
- [ ] Consider adding real menus/PDFs, catering info, or opening navigation links to actual URLs (many footer/nav links still point to `#` anchors).
- [ ] The site has no per-item description body pages beyond the card (single.html renders the card + any `.Content`). Expand if needed.
- [ ] Contact form was removed — if a working form is wanted later, wire a form endpoint or use a service instead of the removed `mailto:` form.

---

## 10. Retired Specifications

These are **not** design references. Do not style, lay out, or document the site
from them. They are kept only as history:

| File | What it was | Status |
| --- | --- | --- |
| `DESIGN-hp.md.old` | HP Electric Blue system | retired |
| `Design2.md.old` | "Terra & Horizon" country portal | retired |
| `.devcontainer/design-country.md.old` | Byte-identical copy of `Design2.md.old` | retired |
| `pizza_shop_page.html.old` | Standalone 729-line HP Electric Blue mockup, titled "James Street Tavern — Fresh, Hot & Delicious Pizza". Orphan: never linked or published. | retired |
| `pizzeria-bella-page.html.old` | Standalone "Pizzeria Bella" mockup in an unrelated palette. Orphan: never linked or published. | retired |
| `content-old/` | Pre-restructure 3-section / 14-item menu | archive |
| `conetnt-md` | Byte-identical duplicate of the published menu PDF | deleted |

**`DESIGN.md` is the single source of truth.** If a spec conflicts with
`DESIGN.md`, `DESIGN.md` wins — and the conflict is a bug in the other file, not
in the code.