---
name: hugo
description: Hugo Static Site Skills
---

# Skill: Hugo Static Site Engineering

System instructions, workflows, and guardrails for managing Hugo static sites, modifying themes, and building custom pages.

## Context Discovery
* **Config File**: Locate `hugo.toml`, `hugo.yaml`, or `config/_default/` to inspect parameters before changing menus or variables.
* **Content Engine**: Uses the Goldmark Markdown processor. Custom HTML is restricted unless `unsafe = true` is explicitly set under markup settings.

---

## 1. Custom Page Creation Workflow
When asked to create a new page, use the appropriate archetype or target bundle.

### Flat Markdown vs. Page Bundles
* Prefer **Page Bundles** (`index.md` inside a dedicated folder) if the page needs local assets like images.
* Use **Flat Files** for simple, text-only content layouts.

### Standard Front Matter Schema
Always include organized front matter (TOML style preferred unless YAML is already dominant in the repo):

```toml
+++
title = "Page Title"
date = 2026-08-28T00:00:00Z
draft = false
layout = "single"
# Custom parameters can go under [params]
+++
```

### Navigation Menu Integration
To add pages to menus natively, use the front matter instead of bloating the global config file:
```toml
[menu]
  [menu.main]
    name = "Page Name"
    weight = 10
```

---

## 2. Theme Customization & Overrides
**Crucial Rule**: Never modify files inside the `themes/` directory directly. Always utilize Hugo's template lookup order to safely override structural layout patterns.

### Safe Template Override Mapping
To alter a theme file, mirror its path layout inside the root project directory:
* Theme Target: `themes/<theme-name>/layouts/partials/header.html`
* Project Override: `layouts/partials/header.html`

### Custom CSS/JS Injection
1. Locate the asset injection hook used by the theme (often a custom parameter in `hugo.toml` such as `customCSS = ["css/custom.css"]`).
2. If no hook exists, safely override the theme's head layout (`layouts/partials/head.html`) and cleanly append the custom style link.
3. Place newly authored asset sheets strictly inside `assets/css/custom.css` (for asset pipeline compilation) or `static/css/custom.css` (for direct passthrough).

---

## 3. Mandatory Guardrails & Negative Constraints
To ensure site builds pass cleanly, you must adhere to these absolute rules:

* **No Hardcoded Domains**: Do not hardcode the `baseURL`. Always use `{{ .Site.BaseURL }}` or relative link structures `{{< ref "filename.md" >}}` for internal references.
* **Draft Validation Check**: Ensure `draft = true` is only used for in-progress work. Remind users they must build with `hugo server -D` to preview drafts locally.
* **Inline CSS Prevention**: Do not inject arbitrary inline `<style>` tags directly into Markdown content files. Instead, route styles via dedicated layout overrides or custom shortcodes.
* **Shortcode Safety Check**: When rendering raw HTML elements or external components inside Markdown, utilize built-in or custom shortcodes rather than raw code formatting blocks.
