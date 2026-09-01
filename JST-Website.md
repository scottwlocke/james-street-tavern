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

The layouts follow `DESIGN.md` (an HP-style design system) as closely as possible:

- **Colors:** Electric Blue `#024ad8` (`--primary`) is the lone CTA/link/price accent; near-black ink `#1a1a1a` (`--ink`) for text; white canvas `#ffffff`; cloud `#f7f7f7` for alternating section bands; dark ink slabs for help-band + footer.
- **Typography:** single-family **Inter** (weight 400/500/600/700) with Manrope → Arial fallbacks — the closest open-source substitutes for Forma DJR Micro. Headlines at weight 500, line-height 1.0.
- **Shapes:** cards/photos at 16px radius (`--radius-xl`), buttons/inputs at 4px (`--radius-md`). Two-tier split is intentional.
- **Spacing:** 8px base scale; 80px section padding; 24px grid gutter.
- **Tokens** are declared as CSS custom properties at the top of `static/css/style.css` and mirror DESIGN.md's token names (`--primary`, `--cloud`, `--space-section`, `--radius-xl`, etc.).

> **Note:** The original pizza-shop reference HTML used the Limelight display font and blue chevron decorations. Per explicit instruction ("follow the DESIGN.md as best as possible"), Limelight was replaced with single-family Inter, and the chevrons were removed at the user's request.

---

## 3. Content Architecture (the menu)

- Each menu section is a top-level folder under `content/` (e.g. `content/pizza/`).
- Each section has a `_index.md` whose `title` becomes the homepage section heading; a `weight` controls section order.
- Each menu item is one Markdown file:
  - **With a picture:** a page bundle — `content/<section>/<item>/index.md` + `content/<section>/<item>/hero.jpg`. The layout auto-detects the image via `.Resources.GetMatch "hero.*"`.
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

**Current menu (14 items):**

| Section | With image (bundle) | Without image (flat) |
| --- | --- | --- |
| **Pizza** | Margherita, Vegetarian Supreme, Ultimate Pepperoni | Garlic Knots (6pc), Tiramisu |
| **Wings & Things** | Buffalo Wings, BBQ Glazed Wings | Lemon Pepper Wings, Loaded Potato Skins |
| **Salads** | Garden Salad, Caesar Salad | Greek Salad, Caprese Salad |

**Note:** The reference HTML's Caesar Salad appeared in both the pizza grid and the salads grid. In this site it exists once, as a bundle item under `salads/`.

---

## 4. Layout Architecture

```
layouts/
├── _default/
│   ├── baseof.html     # HTML shell: head, utility strip, nav + mobile drawer, <main>, help band, footer, main.js
│   └── single.html     # Individual menu item detail page
├── index.html          # Homepage: hero → menu sections → contact
├── section.html        # A section's full listing (e.g. /pizza/)
├── partials/
│   ├── head.html       # <head>: meta, Google Fonts (Inter), style.css
│   ├── utility-strip.html   # Dark top bar (location, For Business, Sign in)
│   ├── nav.html        # Logo + inline links (desktop) + hamburger toggle + mobile drawer
│   ├── hero.html       # Hero card: copy + image (image = home-bundle resource → heroImage param → placeholder)
│   ├── menu-section.html    # Section title + menu grid
│   ├── menu-card.html       # One menu item card (conditional image)
│   ├── contact.html    # Visit info + two-column Bar/Restaurant hours
│   ├── help-band.html  # Dark "How can we help?" band
│   └── footer.html     # 5-column dark footer
static/
├── css/style.css       # All styles (design tokens + components + responsive)
└── js/main.js          # Hamburger drawer toggle logic
```

---

## 5. Key Decisions & Choices

1. **No theme — custom `baseof.html`.**
   A hand-rolled layout keeps full control over the DESIGN.md tokens instead of fighting an installed theme.

2. **Config-driven content over hardcoding.**
   Address, phone, email, hours, hero copy, and help-band text all live in `[params]` in `hugo.toml`. Update them in one place.

3. **CSS custom properties as the DESIGN.md token layer.**
   `static/css/style.css` declares the design tokens at `:root`, then components reference the variables. This makes DESIGN.md → CSS mapping explicit and auditable.

4. **Two CSS encoding bugs fixed during development:**
   An initial draft used invalid CSS arithmetic (`var(--space-xxl) * 1.5`). These were replaced with concrete pixel values (48px, 64px, 32px, 80px) matching the reference and DESIGN.md spacing.

5. **Image strategy — page bundles auto-detect images.**
   Items with photos live in bundles so the image ships with its markdown. The card template looks for a `hero.*` resource; flat `.md` files naturally skip the `<img>` — no front-matter flag needed.

6. **Hero image resolution order:**
   Home-page bundle resource (`content/hero.jpg`) → `heroImage` site param → `/images/hero.svg` placeholder. Used `.Site.Home` + `.Resources.GetMatch` because `GetPage "content/_index.md"` did not resolve the home bundle resources.

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
| `heroEyebrow` | Wood-Fired & Hand-Tossed |
| `heroTitle` | Authentic Italian Wood-Fired Pizza |
| `heroDescription` | Fresh ingredients, hand-tossed dough... |
| `helpBandText` | Questions about catering, reservations, or private events? |
| `barHours` / `restaurantHours` | Mon–Fri 3PM–2AM; Sat & Sun 12PM–2AM (both columns) |

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

1. **With a photo:** create `content/<section>/<item>/index.md` and drop the photo in as `hero.jpg` (or any `hero.*`).
2. **Without a photo:** create `content/<section>/<item>.md`.
3. Front matter: `title`, `price`, `description`, `weight`.
4. To start a new section: create `content/<newsection>/_index.md` with `title` + `weight`; it appears automatically on the homepage.

---

## 9. Outstanding / Next Steps

- [ ] Set the real domain in `hugo.toml` (`baseURL`) before deploy.
- [ ] Replace placeholder hero image (`content/hero.jpg`) with final photography if desired.
- [ ] Consider adding real menus/PDFs, catering info, or opening navigation links to actual URLs (many footer/nav links still point to `#` anchors).
- [ ] The site has no per-item description body pages beyond the card (single.html renders the card + any `.Content`). Expand if needed.
- [ ] Contact form was removed — if a working form is wanted later, wire a form endpoint or use a service instead of the removed `mailto:` form.