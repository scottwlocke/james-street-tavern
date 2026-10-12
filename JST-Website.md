# James Street Tavern — Website Build Summary

Handoff / state document for the Hugo static site at `/workspaces/JST`.
Use this to pick up work quickly.

---

## 1. Project Status

- **Stack:** Hugo (v0.167.0+extended), no theme — custom layouts live in root `layouts/`.
- **Build:** `hugo` → outputs to `public/`. Clean build, no warnings.
- **Preview with drafts:** `hugo server -D` (archetype defaults new pages to `draft = true`).
- **Deploy:** `.github/workflows/hugo.yml` — scans for credentials, builds, publishes to GitHub Pages on push to `main`.
- **`baseURL`:** `https://scottwlocke.github.io/james-street-tavern/` in `hugo.toml` — the single source of truth for every absolute URL.

---

## 2. Design System (DESIGN.md)

**`DESIGN.md` is the only design specification for this site.** The layouts and
`assets/css/style.css` implement it and nothing else.

- **Colors:** tavern navy `#0F2C5B` (`--tavern-navy`) for the dark canvas; chalk gold `#E8C547` (`--chalk-gold`) rationed as the single accent; chalkboard green-black (`--chalkboard`) for panels; barn wood (`--barn-wood`), honey oak, barn red and beer foam as surface/secondary tones. Off-white for body text.
- **Typography:** three families, each with one job. **Oswald** (500/600/700) for signage — headings, nav, buttons, prices, wordmark. **Source Sans 3** (400/600) for all body copy. **Permanent Marker** (400) is hand-lettered chalk, restricted to exactly two roles: the specials kicker and the specials title. Full role/weight/size/leading map is `DESIGN.md` §3.
- **Shapes:** two radii only. Buttons, toggles and the JST shield at 4px (`--radius-sm`); cards, panels and the chalkboard at 8px (`--radius-md`); 50% (`--radius-badge`) is exclusive to the circular logo badge. Sharp buttons, soft containers.
- **Spacing:** `--space-*` scale; 96px section padding; 40px grid gutter dropping to 24px below 1024px.
- **Depth:** five levels, every shadow warm `rgba(44, 27, 16, …)` rather than grey. Recessed and vignette levels are single-use (chalkboard, hero).
- **Tokens** are declared as CSS custom properties at the top of `assets/css/style.css` and mirror `DESIGN.md`'s token names (`--tavern-navy`, `--chalk-gold`, `--space-2xl`, `--radius-md`, `--shadow-recessed`, etc.).

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
- Each section has a `_index.md` whose `title` becomes the homepage section heading; a `weight` controls section order, and each section bundle also carries its card artwork as an SVG (`content/pizza/photo-pizza-hero.svg`).
- Every menu item is a page bundle — `content/<section>/<item>/index.md` plus its
  image `content/<section>/<item>/photo-<slug>-hero.png` (DESIGN.md §12 naming). The
  layout auto-detects the image via `.Resources.GetMatch` on the `photoGlob` site
  param. Bundling is required: a flat `<item>.md` has no resources, so its `<img>`
  is silently skipped. **All 46 items are bundles today.**
- Item front matter (TOML):
  ```toml
  +++
  title = "Classic Margherita"
  price = "$14.99"
  description = "Short description shown on the card."
  weight = 10   # sort order within the section
  +++
  ```
- The homepage renders every menu section via `layouts/partials/menu-sections.html`
  (the single source of truth for the section list), in `weight` order.

**Current menu (8 sections, 46 items):**

| Section | Items | Weight | Notes |
| --- | --- | --- | --- |
| **Pizza** | 5 | 10 | Organised **by size** (`large`, `medium`, `small`) + `toppings` + `ultimate-pepperoni` |
| **Wings** | 5 | 20 | Plus `wing-flavors` |
| **Appetizers** | 12 | 30 | |
| **Burgers** | 3 | 40 | |
| **Hoagies & Sandwiches** | 9 | 50 | |
| **Eggrolls** | 2 | 60 | |
| **Stromboli** | 5 | 70 | |
| **Salads** | 5 | 80 | |

Section order on the homepage comes from the `weight` in each section's
`_index.md`; `menu-sections.html` filters out `nonMenuSections`.

**Note:** this content set replaced an earlier 3-section / 14-item menu.
`pizza` is now organised by size rather than by variety.

**Specials are not a menu section.** `content/specials/` holds two offers
(Monday Night Wings, Taco Tuesday) at `weight = 90`. It is listed in
`nonMenuSections` (`hugo.toml`), so it is kept out of the homepage card grid, the
mobile drawer and the Full Menu page while still being ordinary content — it
drives the homepage chalkboard and its own section page instead.

---

## 4. Layout Architecture

```
layouts/
├── index.html              # Homepage: hero → specials chalkboard → menu sections → contact
├── section.html            # A menu section's full listing (e.g. /pizza/)
├── specials/section.html   # The Specials section page (its own layout: specials are not a menu section)
├── 404.html
├── robots.txt              # Template, NOT static/ — renders the Sitemap: line from baseURL
├── _default/
│   ├── baseof.html         # HTML shell: skip link, head, nav + drawer, <main id="main">, help band, footer, main.js
│   ├── full-menu.html      # /menu/ — every section via menu-section.html
│   └── single.html         # One dish / special detail page
└── partials/
    ├── head.html           # <head>: meta, canonical, OG/Twitter, dns-prefetch, css/style.css
    ├── fonts.html          # @font-face inlined + preloads for the three self-hosted woff2 files
    ├── nav.html            # Logo + Specials / Full Menu / Contact, plus hamburger + mobile drawer
    ├── hero.html           # Hero copy + image (assets/ photo, rendered through dish-image.html)
    ├── dish-image.html     # Page bundle photo → fingerprinted WebP widths + JPEG fallback <picture>
    ├── og-image.html       # 1200×630 JPEG share crop for og:image / twitter:image
    ├── breadcrumb.html / breadcrumb-trail.html   # Visible trail + the shared data the JSON-LD trail reads
    ├── specials.html       # Monday Night Wings chalkboard (DESIGN.md §4)
    ├── menu-section.html / menu-grid-items.html / menu-card.html   # Section title + item grid + one card
    ├── menu-sections.html  # Single source of truth for the section list (grid, drawer, Full Menu)
    ├── sections-grid.html / section-card.html     # Homepage section card grid + one card
    ├── show-image.html / blurb.html               # Image opt-out gate + description-precedence helper
    ├── jsonld.html / jsonld-menuitem.html         # One @graph per page (Restaurant, Menu, BreadcrumbList)
    ├── contact.html        # Visit info + labelled Bar/Kitchen hours from params.hours
    ├── help-band.html
    └── footer.html
assets/
├── css/style.css           # All styles. Piped through minify | fingerprint "sha256" in head.html.
├── js/main.js              # Drawer focus management + specials rotator. Same pipe, minified in baseof.html.
├── fonts/*.woff2           # Oswald, Source Sans 3, Permanent Marker — one self-hosted file per family
└── images/photo-tavern-hero.jpg
static/
├── logo-jst-monogram.svg   # Favicon
└── images/jst-logo.png     # Nav + footer crest
```

> The top bar, the drawer and the logo live in `nav.html`; there is no separate
> `utility-strip.html` partial and — since the redesign — no desktop `Menu`
> dropdown. The section list lives in the mobile drawer, and `Full Menu` opens
> the itemised board one click from the top bar.

---

## 5. Key Decisions & Choices

1. **No theme — custom `baseof.html`.**
   A hand-rolled layout keeps full control over the DESIGN.md tokens instead of fighting an installed theme.

2. **Config-driven content over hardcoding.**
   Address, phone, email, hours, hero copy, and help-band text all live in `[params]` in `hugo.toml`. Update them in one place.

3. **CSS custom properties as the DESIGN.md token layer.**
   `assets/css/style.css` declares the design tokens at `:root`, then components reference the variables. This makes DESIGN.md → CSS mapping explicit and auditable.

4. **Two CSS encoding bugs fixed during development:**
   An initial draft used invalid CSS arithmetic (`var(--space-xxl) * 1.5`). These were replaced with concrete pixel values from the `--space-*` scale, matching `DESIGN.md` §6 spacing.

5. **Image strategy — page bundles auto-detect images.**
   Every item is a page bundle so its image ships with its own markdown. The card
   template looks for a `photo-*-hero.*` resource via the `photoGlob` site param,
   so a flat `.md` would skip the `<img>` entirely. Photo *existence* is decided
   by `Resources.GetMatch`; whether to *render* a found photo is a separate
   opt-out flag, `showimage` (absent = show), resolved once in
   `layouts/partials/show-image.html` for both the card and the detail page.

6. **Hero image resolution order:**
   `assets/images/photo-tavern-hero.jpg` via Hugo Pipes, run through the same
   `dish-image.html` pipeline as the dish photos (fingerprinted WebP widths +
   JPEG fallback, `fetchpriority="high"`). It deliberately does **not** use
   `photoGlob`: a bare file in `content/` is published verbatim to the site root
   as an unversioned `/photo-tavern-hero.jpg`, which a browser will reuse
   indefinitely.

7. **Top bar + hamburger drawer (per DESIGN.md).**
   On **desktop** the bar reads `Logo / Specials / Full Menu / Contact`.
   `Full Menu` opens the itemised board (`/menu/`); the full eight-section list
   lives in the mobile drawer, not a desktop dropdown. Below **1024px**
   `.nav-links` (the whole desktop bar) is hidden and a 44px
   hamburger appears, opening a full-canvas drawer sliding from the right below
   the sticky nav bar (`min-height: 68px` + 2px border ≈ 70px). The drawer
   closes on link click, `Escape`, or resizing above 1024px. Accessibility
   states (`aria-expanded`, `aria-hidden`, `aria-controls`) and, since the audit,
   focus management (focus moves to the first drawer link on open, Tab is
   trapped within the header bar + drawer, focus returns to the toggle on an
   explicit close) are maintained in `assets/js/main.js`, which ships through
   Hugo Pipes (`minify | fingerprint`).

8. **Taxonomies disabled.**
   `disableKinds = ["taxonomy", "term"]` in `hugo.toml` turns off the
   auto-generated `/tags/` and `/categories/` pages. An empty `[taxonomies]`
   table does **not** achieve this — it just blanks the values and leaves Hugo
   rendering unstyled taxonomy pages plus a build warning. Nothing in `content/`
   carries tags or categories.

9. **Single-page contact layout.**
   The original 2-column contact grid (info + form) became single-column after
   the "Send a Message" form was removed. Bar and Kitchen hours render
   side-by-side in `.hours-grid` / `.hours-col` (stack to one column on
   narrow widths). The hours themselves live once in `[[params.hours]]` and are
   consumed by both `contact.html` (labelled columns) and `jsonld.html` (schema).

10. **DNSS-style no-hardcoded-internal-links.**
    Internal URLs use `.Site.BaseURL` / `relURL`; external Unsplash images were downloaded and vendored into the content bundles (no hotlinked remote images in the build).

---

## 6. Site Parameters (hugo.toml `[params]`)

| Param | Value |
| --- | --- |
| `location` | Monroeville, PA (the line under the wordmark in `nav.html`) |
| `address` | 1224 James St, Monroeville, PA 15146 — the display string the footer and contact card print |
| `streetAddress` / `addressLocality` / `addressRegion` / `postalCode` / `addressCountry` | The same address split into parts for schema.org `PostalAddress` (`jsonld.html`); must stay consistent with `address` |
| `phone` | 412-824-8884 |
| `email` | info@jst-tavern.com |
| `latitude` / `longitude` | 40.419373 / -79.808284 — read from the Maps embed; used only for `LocalBusiness.geo` |
| `priceCurrency` | `USD` — so the schema never hardcodes a currency |
| `priceRange` | `$$` — the `$`-band Google expects for local businesses |
| `servesCuisine` | `["American", "Pizza", "Wings", "Burgers", "Sandwiches"]` |
| `googleSiteVerification` | empty by default; paste the Search Console `content=""` value. `head.html` wraps the meta in `with`, so nothing is emitted until a real code lands |
| `heroKicker` / `heroTitle` / `heroDescription` | Your Neighborhood Tavern / Come Hungry. Leave Happy. / Jumbo whole wings, cold beer… |
| `homeTitle` / `homeDescription` | Homepage `<title>` + meta description (search copy only). Reused as the Restaurant node's description in `jsonld.html` |
| `menuKicker` / `menuTitle` / `menuIntro` | The Chalkboard / What's On Today / … |
| `helpBandText` | Got a big party coming, or a question about catering? Give us a call — we'll sort you out. |
| `photoGlob` | `photo-*-hero.*` — the asset-naming pattern layouts resolve images by |
| `nonMenuSections` | `["specials"]` — sections kept out of the card grid, drawer and Full Menu |
| `[[params.hours]]` | Structured hours: one element per **area** (`Bar`, `Kitchen`), each with `groups` of `label` / `days` / `opens` / `closes` (24h). Read by `contact.html` (labelled columns) and `jsonld.html` (schema, deduped on times) |
| `sections.<name>` | Section blurbs for the card grid, defined for all 8 sections in `weight` order. Precedence is reversed from appearances: a section's own `description` (which covers `summary`) wins — this is the last fallback |

> **`[[params.hours]]` must stay at the bottom of `hugo.toml`.** TOML assigns a
> bare key to whichever table header most recently preceded it, so an
> `[[params.hours]]` array parked mid-table silently absorbs every following
> param into its last `[[params.hours.groups]]` element. Nothing errors — the
> keys just vanish from `.Site.Params`, and `| default` fallbacks keep the site
> building and looking plausible. That is how specials once leaked back into the
> menu.

The specials chalkboard content (kicker, title, price) is **not** in `[params]`
any more — it comes from the `content/specials/` pages, rendered by
`layouts/partials/specials.html`.

---

## 7. Current Business Hours

| Day | Hours |
| --- | --- |
| Monday – Friday | 3 PM – 2 AM |
| Saturday | 12 PM – 2 AM |
| Sunday | 12 PM – 2 AM |

Written **once** in `hugo.toml` as `[[params.hours]]` and rendered twice on the
homepage — labelled **Bar** and **Kitchen** columns in `contact.html` — then
emitted as `openingHoursSpecification` by `jsonld.html`, which collapses groups
whose days and times are identical (so the two areas produce 3 schema specs, not
6). Bar and Kitchen currently carry identical times; this is left as-is rather
than inventing a difference and is worth confirming against the real roster.

---

## 8. How to Add / Change Menu Items

1. **With a photo:** create `content/<section>/<item>/index.md` and drop the photo in as `photo-<subject>-hero.png` (DESIGN.md §12; the glob is `photo-*-hero.*`, so `.jpg` works too).
2. **Without a photo:** create `content/<section>/<item>.md` — a flat file has no resources, so the card renders without an image.
3. Front matter: `title`, `price`, `description`, `weight`.
4. To start a new section: create `content/<newsection>/_index.md` with `title` + `weight`; it appears automatically on the homepage. Add the section artwork as `photo-<section>-hero.svg` in the same bundle, and add `[cascade.build] publishResources = false` to the `_index.md` so the full-size originals stay out of `public/` (see every existing section's `_index.md`).

---

## 9. Outstanding / Next Steps

- [x] **`baseURL` set.** It is the GitHub Pages project URL
      (`https://scottwlocke.github.io/james-street-tavern/`) and the single
      source of truth for canonicals, sitemap, `robots.txt` and JSON-LD. Change
      it only if the repo is renamed or a custom domain is adopted.
- [x] **Hero image restored and optimised.** `assets/images/photo-tavern-hero.jpg`
      is read by `layouts/partials/hero.html` through `dish-image.html`
      (fingerprinted WebP widths + JPEG fallback, `fetchpriority="high"`).
- [x] **No dead link anchors.** Nav and footer point at real destinations; a
      build-wide check found zero `href="#"` links.
- [ ] **Enable Pages in the repository settings** (Settings → Pages → Source:
      **GitHub Actions**) before the first push will deploy.
- [ ] Consider adding real menus/PDFs or catering info pages.
- [ ] The site has no per-item description body pages beyond the card
      (`single.html` renders the card + any `.Content`). Expand if needed.
- [ ] Contact form was removed — if a working form is wanted later, wire a form
      endpoint or use a service instead of the removed `mailto:` form.
- [ ] **Optional:** run `python3 .tmp/validate-jsonld.py` in CI. It is scratch,
      `.gitignore`d tooling today, so CI would have to commit it first (the
      workflow currently only scans for credentials, builds and deploys).

---

## 10. Retired Specifications

These are **not** design references. Do not style, lay out, or document the site
from them. They are kept only as history:

| File | What it was | Status |
| --- | --- | --- |
| `DESIGN-hp.md.old` | HP Electric Blue system | retired |
| `Design2.md.old` | "Terra & Horizon" country portal | retired |
| `.devcontainer/design-country.md.old` | Byte-identical copy of `Design2.md.old` | deleted |
| `pizza_shop_page.html.old` | Standalone 729-line HP Electric Blue mockup, titled "James Street Tavern — Fresh, Hot & Delicious Pizza". Orphan: never linked or published. | retired |
| `pizzeria-bella-page.html.old` | Standalone "Pizzeria Bella" mockup in an unrelated palette. Orphan: never linked or published. | retired |
| `conetnt-md` | Byte-identical duplicate of the published menu PDF | deleted |

**`DESIGN.md` is the single source of truth.** If a spec conflicts with
`DESIGN.md`, `DESIGN.md` wins — and the conflict is a bug in the other file, not
in the code.