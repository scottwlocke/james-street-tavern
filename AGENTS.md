# AGENTS.md

Hugo static site for "James Street Tavern". Load the Hugo skill (`.opencode/skills/hugo/SKILL.md`) before doing site work — it encodes layout/override/guardrail workflow.

## Current state (scaffold only)

- **No theme** — `themes/` is empty and `theme` is not set in `hugo.toml`. `hugo` builds but emits "no layout file for kind home" warnings and renders nothing useful. Don't be surprised by a bare/empty build.
- **No content, layouts, assets, static, data, or i18n** — all are empty directories.
- **`hugo.toml` is minimal** (3 lines): `baseURL`, `locale`, `title`. `baseURL` is still the `https://example.org/` placeholder — it must be changed to the real domain before deploy.

## Build / verify

- Build: `hugo` (outputs to `public/`).
- Serve with drafts: `hugo server -D` (required because the archetype defaults every new page to `draft = true`).

## Conventions & guardrails

- **Never edit files inside `themes/`.** Override theme templates by mirroring their path under root `layouts/` (there is no theme yet, so new layouts go straight into `layouts/`).
- **Front matter is TOML** (`+++ ... +++`), matching `archetypes/default.md`.
- **No raw HTML in Markdown.** Goldmark's default has `unsafe = false`, so inline HTML won't render; use shortcodes/templates instead.
- **No hardcoded domains.** Use `{{ .Site.BaseURL }}` / `{{< ref >}}`.
- **HTML/CSS style decisions reference `DESIGN.md`** — the site's design system (colors, typography, spacing, components, tokens). Consult it before writing any styling or layout markup.
- Load `opencode.json` — it wires the Hugo skill into OpenCode sessions.
