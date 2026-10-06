# James Street Tavern — SEO Task List

Findings from an audit of the built output at `/workspaces/JST` (60 generated
HTML pages, Hugo `v0.167.0+extended`). Ordered by impact, not by effort.

Every claim here was measured against `public/` rather than assumed. Figures
come from the build; **no ranking, crawl or Core Web Vitals data was available**
from the working environment, so treat performance items as measured-bytes-only.

---

## 1. Status

| # | Task | Severity | Status |
|---|---|---|---|
| 1 | Fix `baseURL` placeholder | **Blocking** | todo |
| 2 | Rename `locale` → `languageCode` | **Blocking** | todo |
| 3 | Add canonical URLs | High | todo |
| 4 | Add structured data (JSON-LD) | High | todo |
| 5 | Add Open Graph / Twitter cards | High | todo |
| 6 | Resize / re-encode dish photography | Medium | todo |
| 7 | De-duplicate two salad descriptions | Medium | todo |
| 8 | Deal with 10 unadvertised Atom feeds | Low | todo |
| 9 | Add `robots.txt` | Low | todo |

---

## 2. Blocking — must land before launch

### 1. `baseURL` is still the `example.org` placeholder

`hugo.toml` line 2 is `baseURL = 'https://example.org/'`. Every absolute URL
Hugo generates inherits it, so **all 59 sitemap entries and every future
canonical URL point at a domain that does not serve this site.**

Google will index whichever domain actually serves the files and treat the
other as a duplicate site. This also makes the sitemap actively harmful: it
advertises 59 URLs on a domain that returns nothing.

- Set `baseURL` to the real production origin, including scheme and any
  `www`/apex preference, with a trailing slash.
- Hardcoding is unavoidable *here* — this is the one config value that must be
  absolute. Everything downstream reads `.Site.BaseURL`, so nothing else needs
  editing.
- Re-verify after the change: `grep -c example.org public/sitemap.xml` → 0.

### 2. `lang` is driven by a key Hugo does not document

`hugo.toml` line 3 sets `locale = 'en-us'`, and `baseof.html` renders
`<html lang="{{ .Site.Language.Locale | default "en" }}">`, producing
`lang="en-us"`.

Tested both directions: deleting `locale` drops the output to `lang="en"`, so
the key *is* being read — but `hugo config` does not list it, and the documented
key `languageCode` produces byte-identical output.

- Rename `locale` → `languageCode` in `hugo.toml`.
- Leave `baseof.html` alone; `.Site.Language.Locale` resolves correctly from the
  documented key.
- Do not change the value to `en`. `en-us` is correct for a US venue and feeds
  Google's regional targeting.

> **Do not** work around this by hardcoding `lang="en-us"` into `baseof.html`.
> That hides an unrecognised config key rather than fixing it, and the key
> would keep working until a Hugo release drops it.

---

## 3. High — the biggest missed opportunity

### 3. No canonical URLs on any page

Zero of 60 pages carry `<link rel="canonical">`. `head.html` emits `viewport`,
`description`, `theme-color`, icons and the fingerprinted stylesheet, and
nothing else.

- Add one canonical per page in `layouts/partials/head.html`, built from
  `.Permalink`.
- Skip the 404 alongside its existing `noindex` branch.
- This matters most for `/`, which has no self-canonical and would otherwise let
  `/?utm_source=…` variants compete with `/`.

### 4. No structured data anywhere

Zero `application/ld+json` blocks across 60 pages.

This is the highest-value gap for a restaurant: a `LocalBusiness` / `Restaurant`
block can earn rich results (opening hours, menu, price range) in Google, and the
46 menu items map cleanly onto `Menu` / `MenuItem`.

**The data is already maintained — it is just never expressed machine-readably:**

| Needed for schema | Already in |
|---|---|
| `name`, `telephone`, `streetAddress` | `hugo.toml` → `params` |
| `openingHoursSpecification` | `params.barHours` / `restaurantHours` |
| 46 × `MenuItem` name + price | `price` in each item's front matter |
| Section grouping | `.Section` / `menu-sections.html` |

- `hugo.toml` has no `geo` / latitude / longitude yet — needed only for
  `LocalBusiness.geo`, which is optional. Worth adding if the real coordinates
  are known.
- Keep the JSON-LD in a partial rather than in `head.html` directly, so it can
  be shared by the home, section and single templates.

### 5. No Open Graph or Twitter tags

Zero `og:title`, `og:description`, `og:image`, `og:type`, `og:url` and
`twitter:card` tags across all 60 pages. Every shared link renders as a bare
URL with no preview card.

- The pieces are in place: `layouts/partials/blurb.html` already resolves a
  per-page description, and the hero image is **1200×800**, which clears the
  `og:image` guidance of ≥1200×630.
- `og:image` needs an absolute URL (`.Permalink` / `.AbsURL`), unlike the
  relative `src` used in markup.
- Decide on `og:type` per kind: `restaurant.menu_section` on section pages,
  `restaurant.menu_item` on dish pages, `website` on the home page.

---

## 4. Medium

### 6. Dish photography is served ~2.3× oversized

All 46 dish photos are **1600×1000 PNG at ~228 KB**, but the detail page
displays them at roughly 700px wide. That is the bulk of the site's **10.0 MB**
total payload.

Page weight is a ranking factor, so this is worth fixing rather than deferring.

- Route the detail-page image through Hugo Pipes (`Resize` to ~800px, `WebP`),
  which is a template change in `single.html`, not a content change.
- **This also closes the `showimage` caveat.** DESIGN.md §5 records that
  `showimage = false` removes the `<img>` but leaves the PNG in the build,
  because page resources are published regardless of what templates do with
  them. Resizing at the template level at least stops shipping the full-size
  original.
- Cards use the same photos at ~340px wide, so a second smaller variant is
  worth it if `srcset` is added.
- The homepage hero is already correctly handled (253 KB, fingerprinted).

### 7. Two salad pages share a meta description byte-for-byte

`content/salads/breaded-chicken-salad/index.md` and
`content/salads/grilled-chicken-salad/index.md` have identical `description`
front matter, so both render the same `<meta name="description">`.

Audit result: **58 distinct descriptions across 60 pages.** Both pairs are
accounted for:

- `/` and `/404.html` → both fall back to `heroDescription`. Defensible, and
  the 404 is `noindex` anyway.
- The two salad pages → **this is a content bug**, not a code one.

- Differentiate the two `description` lines in front matter. No template change
  needed; `blurb.html` already reads them.

---

## 5. Low

### 8. Ten Atom feeds are generated, none advertised

`public/index.xml` plus nine section feeds exist. No page emits
`<link rel="alternate" type="application/atom+xml">`, so they are unreachable
and unlisted — pure dead weight in the build.

- **Recommendation: disable.** A restaurant menu has nothing to syndicate that
  its HTML does not already say, and a feed nobody links to invites the
  questions it was meant to avoid.
- Disable with `[outputs]` in `hugo.toml`, setting `home` and `section` to
  `["HTML"]` only.
- If kept instead, advertise them with `{{ with .OutputFormats.Get "rss" }}`.

### 9. No `robots.txt`

Hugo does not generate one, and there is none in `static/`.

- Add `static/robots.txt` with a `User-agent: * / Allow: /` stanza and a
  `Sitemap:` line pointing at `.Site.BaseURL` — task 1 must land first, or the
  sitemap line will advertise the placeholder domain.

---

## 6. Already correct — no action

Verified during the audit, recorded so the next pass does not re-check them:

- **`<title>`** — unique across all 60 pages; length range 19–59 chars, so no
  truncation risk. The 404 is titled separately, not left as Hugo's
  "404 Page not found" default.
- **`<h1>`** — exactly one per page, across all 60.
- **Meta descriptions** — present on all 60, 58 distinct (see task 7).
- **`<nav>`** — one `<nav aria-label="Main">` landmark per page.
- **Sitemap** — 59 URLs, correctly excluding the 404.
- **404 handling** — `noindex, follow` on a thin-content page is the correct
  call, not a bug.
- **Head essentials** — `viewport`, `theme-color`, favicon and apple-touch-icon
  present; stylesheet served through the asset pipeline with a sha256
  fingerprint and SRI integrity.

> **Caveat on headings.** Task list item: heading *skips* were reported on 57
> pages in an earlier audit, but the re-check for this document sampled one page
> per template rather than all 60. `h1` → `h2` with no skip on the dish page
> checked. **Re-verify across all pages before treating heading order as
> clean.**

---

## 7. Suggested order

1. Tasks **1** and **2** — two lines in `hugo.toml`, both blocking.
2. Tasks **3**, **5** and **9** — all three live in or beside
   `layouts/partials/head.html`; one sitting closes most of what a crawler or a
   social scrape actually reads.
3. Task **4** — the largest single win, and the most new code.
4. Tasks **6**, **7**, **8** — payload, content hygiene, build tidying.

---

## 8. What this audit could not check

Stated plainly so the list is not mistaken for more than it is:

- **No live data.** Google Search Console, Bing Webmaster, `lighthouse`,
  PageSpeed Insights and `curl` against a production host were all
  unavailable. Every figure here comes from the local build.
- **No Core Web Vitals.** LCP and CLS are unverified. Byte sizes are measured;
  how they render on a real connection is not.
- **No rendering.** Chromium and Playwright are not installed, so nothing was
  checked in a browser. Layout claims are derived from the CSS.
- **No visual confirmation of social previews.** The `og:image` recommendation
  rests on the hero's measured 1200×800, not on an observed card.
