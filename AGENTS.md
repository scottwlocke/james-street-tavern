# AGENTS.md

Hugo static site for "James Street Tavern". Load the Hugo skill (`.opencode/skills/hugo/SKILL.md`) before doing site work — it encodes layout/override/guardrail workflow.

## Current state

- **No theme** — `themes/` is empty and `theme` is not set in `hugo.toml`. All layouts are custom and live in root `layouts/`.
- **Built and working** — 8 content sections / 46 menu items, 55 published pages, no build warnings. `content/`, `layouts/`, `assets/`, `static/`, `data/` and `i18n/` are all populated; `themes/` is the only empty one.
- **Stylesheet** — `assets/css/style.css`, served through Hugo's asset pipeline with a sha256 fingerprint. **Do not move it to `static/`**: an unversioned `/css/style.css` lets browsers silently reuse a stale stylesheet.
- **`hugo.toml`** carries real `[params]` (address, hours, hero and specials copy, `photoGlob`, section blurbs). `baseURL` is still the `https://example.org/` placeholder — it must be changed to the real domain before deploy.

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
