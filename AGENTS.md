# AGENTS.md

Hugo static site for "James Street Tavern". Load the Hugo skill (`.opencode/skills/hugo/SKILL.md`) before doing site work — it encodes layout/override/guardrail workflow.

## Current state

- **No theme** — `themes/` is empty and `theme` is not set in `hugo.toml`. All layouts are custom and live in root `layouts/`.
- **Built and working** — 9 content sections (8 menu sections plus `specials`, which is deliberately kept out of the menu), 46 menu items + 2 specials, 60 generated HTML files (59 pages plus `404.html`), no build warnings. `content/`, `layouts/`, `assets/` and `static/` are all populated. `themes/`, `data/` and `i18n/` are empty and unused — no template reads `.Site.Data` or i18n, so leave them alone unless you are adding that feature.
- **Stylesheet** — `assets/css/style.css`, served through Hugo's asset pipeline with a sha256 fingerprint. **Do not move it to `static/`**: an unversioned `/css/style.css` lets browsers silently reuse a stale stylesheet.
- **The same rule covers the homepage photo.** `assets/images/photo-tavern-hero.jpg` is fingerprinted by `layouts/partials/hero.html`. It must not sit loose in `content/` — a bare file there is published verbatim to the site root as an unversioned `/photo-tavern-hero.jpg`.
- **Dish photos are page-bundle resources, and that is a trap.** The 46 sources are 1600×1000 PNG living in each bundle, so Hugo publishes every one of them verbatim whatever the templates do — including the two eggrolls that set `showimage = false`. `layouts/partials/dish-image.html` serves three WebP widths plus a JPEG fallback through `<picture>`, but the originals still land in `public/` (9.35 MB). Only moving them to `assets/` fixes that; see DESIGN.md §5 and task 6 in `SEO-Tasks.md`. Two consequences worth remembering: `.card-media picture` / `.detail-media picture` need `display: block` in the stylesheet or the images collapse out of the media boxes, and `.Fingerprint` as a *method* does not exist on image resources in Hugo 0.167 — use the `fingerprint` **function**.
- **No taxonomies.** `hugo.toml` sets `disableKinds = ["taxonomy", "term"]`. This is load-bearing: an empty `[taxonomies]` table does *not* disable tags/categories, it just blanks the values and leaves Hugo rendering unstyled `/tags/` and `/categories/` pages plus a build warning.
- **`hugo.toml`** carries real `[params]` (address, hours, hero and specials copy, `photoGlob`, section blurbs). `baseURL` is still the `https://example.org/` placeholder — it must be changed to the real domain before deploy.
- **Only `content/` is published.** Source documents live outside it — see `misc/` (design explorations, the vendor menu PDF) and `.opencode/skills/hugo/` (skill references). Nothing in either belongs in `content/`.

## Build / verify

- Build: `hugo` (outputs to `public/`).
- Serve with drafts: `hugo server -D` (required because the archetype defaults every new page to `draft = true`).

## Conventions & guardrails

- **Never edit files inside `themes/`.** Override theme templates by mirroring their path under root `layouts/` (there is no theme yet, so new layouts go straight into `layouts/`).
- **Front matter is TOML** (`+++ ... +++`), matching `archetypes/default.md`.
- **No raw HTML in Markdown.** Goldmark's default has `unsafe = false`, so inline HTML won't render; use shortcodes/templates instead.
- **No hardcoded domains.** Use `{{ .Site.BaseURL }}` / `{{< ref >}}`.
- **HTML/CSS style decisions reference `DESIGN.md`** — the site's design system (colors, typography, spacing, components, tokens). Consult it before writing any styling or layout markup.
- **`DESIGN.md` is the ONLY design specification.** Never style, lay out, or document from `DESIGN-hp.md.old`, `Design2.md.old`, `.devcontainer/design-country.md.old`, or `pizza_shop_page.html` — those are retired HP / country-portal artifacts kept for history only, and they are not published. If one of them conflicts with `DESIGN.md`, `DESIGN.md` wins and the other file is wrong. The tavern brand is dark navy/gold with Oswald + Source Sans 3 + Permanent Marker; there is no white canvas, no Electric Blue, no chevrons, and no 16px card radius.
- Load `opencode.json` — it wires the Hugo skill into OpenCode sessions.
