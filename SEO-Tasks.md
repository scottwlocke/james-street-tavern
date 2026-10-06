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
| 1 | Fix `baseURL` placeholder | **Blocking** | **done** |
| 2 | Rename `locale` → `languageCode` | **Blocking** | todo |
| 3 | Add canonical URLs | High | **done** |
| 4 | Add structured data (JSON-LD) | High | **done** |
| 5 | Add Open Graph / Twitter cards | High | todo |
| 6 | Resize / re-encode dish photography | Medium | **done** |
| 7 | De-duplicate two salad descriptions | Medium | **done** |
| 8 | Deal with 10 unadvertised Atom feeds | Low | **done** |
| 9 | Add `robots.txt` | Low | **done** |

---

## 2. Blocking — must land before launch

### 1. ~~`baseURL` is still the `example.org` placeholder~~ — done

`hugo.toml` line 2 was `baseURL = 'https://example.org/'`. Every absolute URL
Hugo generates inherits it, so **all 59 sitemap entries and every canonical
URL pointed at a domain that does not serve this site.** Google will index
whichever domain actually serves the files and treat the other as a duplicate,
which also made the sitemap actively harmful: it advertised 59 URLs on a domain
that returned nothing.

Now `https://scottwlocke.github.io/james-street-tavern/`, the GitHub Pages
project site for this repository, including scheme and a trailing slash.
Hardcoding was unavoidable *here* — it is the one config value that must be
absolute — and everything downstream reads `.Site.BaseURL`, so nothing else
needed editing.

`.github/workflows/hugo.yml` deliberately does **not** pass `--baseURL`. GitHub's
own starter workflow overrides it from `configure-pages`, which self-heals if
the repository is renamed but means production and a local build silently
disagree the moment the two drift. The value comes from `hugo.toml` and nowhere
else, so `hugo` locally and `hugo` in CI emit byte-identical absolute URLs.

- Re-verified after the change: `grep -c example.org public/sitemap.xml` → 0.
- Renaming the repository or moving to a custom domain is a one-line change to
  `baseURL`; no template holds a domain.

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

### 3. ~~No canonical URLs on any page~~ — done

All 59 indexable pages now carry exactly one `<link rel="canonical">`, emitted
from `layouts/partials/head.html`.

- Built from `.Permalink`, not `.RelPermalink`. A canonical must be absolute; a
  root-relative one is not reliably interpreted across crawlers.
- `.Permalink` is already query-free, which is the point of the homepage case:
  every `/?utm_source=…` variant collapses onto `/` with no cleanup pass, rather
  than being indexed as a separate document competing with it.
- Skipped on the 404, on the same reasoning as its `noindex` and its missing
  JSON-LD — a soft 404 should not be offered as a result, and giving it a
  canonical identity asks for the opposite of what `noindex` does.

Verified by `.tmp/validate-jsonld.py`, which now checks the page shell as well
as the JSON: one canonical per page, absolute, query-free, and equal to the path
the built page actually serves at. Checking against the built file rather than
against `.Permalink` is deliberate — it catches the tag drifting out of step with
an alias or redirect, which is the exact failure the tag exists to prevent.

That check was confirmed to have teeth by injecting five regressions into the
built output — a missing tag, a `?utm_source=` query, a canonical on the 404,
one pointing at `/pizza/` from `/burgers/`, and a root-relative one — and
confirming each produced its own distinct error rather than passing silently.

These resolve against `baseURL`, which is the GitHub Pages project site URL
since task 1 landed. They were correct in shape before that and are now
production-valid too.

### 4. ~~No structured data anywhere~~ — done

`application/ld+json` now ships on 59 of 60 pages, assembled by
`layouts/partials/jsonld.html` (one `<script>` per page, an `@graph` array) with
per-item construction in `layouts/partials/jsonld-menuitem.html`.

| Node | Where |
|---|---|
| `Restaurant` | every non-404 page |
| `Menu` / `MenuSection` / `MenuItem` | `/menu/` (8 sections, 46 items) and the 8 section pages |
| `BreadcrumbList` | the 58 pages below the home page |

Design decisions worth keeping:

- **The 404 gets nothing.** It is `noindex`, and hanging a real business
  identity off a "not found" page risks the markup being read as describing the
  error page.
- **Hours carry `openingHoursSpecification` but no bare `openingHours`.** Both
  areas run past midnight into the small hours, so there is no `closingHours` to
  pair with an always-open claim. Omitting the shortcut is more honest than
  asserting something the config does not support.
- **`wings/wing-flavors` has an empty `price`** — it is a list of sauces, not
  something you order — so it emits **no `offers` at all** rather than a blank
  one. An empty `Offer` reads to Google as a free item.
- **`pizza/toppings` is a range** (`$1.75 - $3.75`) and emits an `Offer`
  wrapping a `PriceSpecification` with `minPrice`/`maxPrice`. A hyphenated
  price string is what Google rejects.
- **`showimage = false` suppresses the schema image too.** The image gate is
  shared with the card and detail panel, so the schema never claims a photo no
  visitor can see.
- **The section list comes from `menu-sections.html`**, so the schema honours
  `nonMenuSections` exactly like the visible menu — specials are offers, not
  dishes, and stay out.
- **Dish detail pages carry no `Menu`.** Every item is already described on the
  page that lists it, with its URL; repeating one item per detail page adds
  markup without adding a fact.

The data is written once and expressed twice. `params.hours` replaces the old
display strings and `contact.html` fallbacks, so the hours a visitor reads and
the hours a crawler parses cannot drift:

| Needed for schema | Single source |
|---|---|
| `name`, `telephone`, `email` | `hugo.toml` → `params` |
| `streetAddress` … `addressCountry` | `params` (structured, replaces `params.address`) |
| `geo` | `params.latitude` / `params.longitude` |
| `openingHoursSpecification` | `params.hours` (24h `HH:MM`, `days` as the schema.org enum) |
| 46 × `MenuItem` name + price | `price` in each item's front matter |
| Section grouping | `menu-sections.html` |
| `logo`, `image` | `assets/images/photo-*-hero.*` + `images/jst-logo.png` |

Two hazards this work surfaced, both now guarded by comments in place:

- **`hugo.toml` ordering is load-bearing.** A `[[params.hours]]` array parked in
  the middle of `[params]` silently swallows every following bare key into its
  last `[[params.hours.groups]]` element. `nonMenuSections` and `photoGlob`
  stopped resolving, specials leaked back into the menu, and nothing errored —
  the `| default` fallbacks in the partials kept the build green. The block must
  stay below every bare key and after `[params.sections]`.
- **`{{- /* … */ -}}` comments cannot contain `*/`.** Go closes the comment at
  the first one and emits the remainder as literal text on every page. This
  shipped commented-out prose into all 60 pages while the build stayed clean and
  the JSON still parsed.

Verification: `.tmp/validate-jsonld.py` (scratch, gitignored) extracts every
block and asserts strict `json.loads`, required fields, resolvable `@id`
references, absolute URLs, and — the useful part — cross-checks every
`MenuItem` name and price against the front matter it claims to describe, using
`tomllib` so the checked values come from the same parse Hugo uses. It also
rejects raw template syntax in page output, which is what caught the leaked
comment. Current result: **PASS** across 60 pages.

Still open, both harmless and both worth knowing:

- Bar and Kitchen hours are identical because that is what was supplied. Not
  invented, not confirmed; worth checking against the real roster.

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

### 6. ~~Dish photography is served ~2.3× oversized~~ — done

`layouts/partials/dish-image.html` runs each photo through Hugo Pipes and
`menu-card.html` / `single.html` render the result in `<picture>`: three WebP
widths (480 / 768 / 1080) and a 1080px JPEG fallback, all sha256-fingerprinted.

| Slot | Width | Sent | Was |
|---|---|---|---|
| Card | ~357px | **5.1 KB** | 208 KB |
| Detail (LCP) | ~440px | **8.6 KB** | 208 KB |

Per-dish download drops from 206 KB to 5–13 KB depending on slot and density —
a 15–24× reduction. A cold build encodes all 176 derivatives in ~4s.

Two corrections to the original finding, both of which changed the plan:

- **It was ~3.6× oversized, not 2.3×.** `.detail-media` is the *5fr* track of a
  1200px container, so ~440px — not the ~700px assumed. A card is ~357px.
- **The second bullet's prediction was wrong in a useful way.** Stopping the
  full-size originals shipping is *not* achievable with a template change, because
  Hugo publishes page-bundle resources unconditionally — `showimage = false` on
  the pepperoni eggrolls still shipped its 206 KB PNG. `public/` is therefore
  **12.99 MB, up from 10.10 MB**: the originals are all still there and the
  derivatives add 3.03 MB on top. That is build-output and deploy weight, not
  transfer — no `<img>` references an original any more, and the only thing that
  was paying for them was the payload argument.

So the `showimage` caveat is only *partly* closed: an opted-out dish now
generates no derivatives at all, but its original PNG still ships. Removing that
last 9.35 MB means moving the photos out of `content/` into `assets/`, which is a
content-convention change — see the deferred note below.

Also done, since they were the same class of bug:

- Derivatives are fingerprinted, so a re-encoded photo can invalidate a cached
  one. Dish images were the last unversioned URLs on the site.
- The detail image is the LCP element and now carries `fetchpriority="high"` and
  is not lazy-loaded.
- JSON-LD `image` points at the 1080px WebP derivative, not the original.

**Deferred, and the only remaining part:** the 46 originals in `public/`
(9.35 MB). Moving them to `assets/images/` would drop `public/` to ~1 MB and
retire the `showimage` caveat entirely, at the cost of changing how photos are
resolved — `.Resources.GetMatch` in three templates, the `photoGlob` convention,
and DESIGN.md §5. Worth doing for deploy size, not for page weight.

Verified: every one of the 187 asset URLs referenced across the built site
resolves to a file on disk, no `<img>` points at a PNG original, and the
section SVGs are untouched.

### 7. ~~Two salad pages share a meta description byte-for-byte~~ — done

`content/salads/breaded-chicken-salad/index.md` and
`content/salads/grilled-chicken-salad/index.md` carried the same `description`
string, so both rendered the same `<meta name="description">`.

**The duplication is in the source, not in the transcription.** The vendor menu
(`misc/JST Vertical Menu July 2025 - Convenience Fee Note added.pdf`) prints
identical copy for both salads:

```
Grilled Chicken Salad   Plain or Buffalo Style with Tomato, Onion, Egg, Mozzarella and Fries   $13.00
Breaded Chicken Salad   Plain or Buffalo Style with Tomato, Onion, Egg, Mozzarella and Fries   $13.00
```

So the site was faithfully reproducing what it was given. Re-extracting the text
from the PDF (no `pdftotext` or PDF library in this environment — a small zlib
pass over the content streams did it) confirmed that before any edit, which
matters because the obvious reading of the audit finding was a copy-paste slip
by whoever entered the content.

- The fix states only what is already certain: the dish name, and the shared
  ingredient list from the PDF. Each description now leads with its own chicken
  — `Breaded chicken, plain or buffalo style, …` / `Grilled chicken, plain or
  buffalo style, …` — and nothing else changed.
- **No embellishment.** Tempting to add `crispy` to the breaded one or a
  `lighter` claim to the grilled one, but neither is on the source menu, and a
  description is a claim the venue has to be able to honour. One word of true
  difference beats a sentence of invented one.
- One front matter edit fixes three surfaces: `blurb.html` feeds the meta tag,
  and the same `description` renders the visible card copy and the JSON-LD
  `MenuItem.description`, so none of them can drift apart.

After: **59 distinct descriptions across 60 pages**, no dish shares a
description with any other dish, and the only remaining repeat is `/` and
`/404.html` both falling back to `heroDescription` — which is defensible, since
the 404 is `noindex` and there is nothing better to describe a soft 404 with.
No template change was needed.

---

## 5. Low

### 8. ~~Ten Atom feeds are generated, none advertised~~ — done

The 10 feeds — `index.xml` plus nine section feeds — are gone:

```toml
[outputs]
  home = ["HTML", "Robots"]
  section = ["HTML"]
```

- **Nothing ever advertised them.** No page emitted `<link rel="alternate"
  type="application/atom+xml">`, and grepping `layouts/` for
  `.OutputFormats.Get "rss"` returns nothing (the only matches for `rss` are
  the `openingHoursSpecification` schema key). They were reachable by guessing
  `index.xml` and by no other route.
- **Disable rather than advertise**, for the reason the original finding gave:
  this is static menu data that already has a better home in the HTML, and a
  feed nobody subscribes to is an artifact that has to be kept honest forever
  while inviting exactly the questions syndication exists to avoid.
- **`home` keeps `Robots`**, because task 9 hangs `robots.txt` off that same
  list. The two tasks touch the same two lines: at the time task 9 was written
  `RSS` was still listed precisely so that turning robots.txt on did not
  disable the feeds as an accident — and task 8 then removed it on purpose.
  Both comments in `hugo.toml` were updated to say so, since a stale "never
  drop this" comment is how the next reader puts the feeds back.
- **`section = ["HTML"]` removes only feeds.** Sections still render HTML, and
  `sitemap.xml` is untouched — it is its own generator, not an output format on
  `home`, and still lists 59 URLs.

Verified: 10 `index.xml` → 0; `public/` went 307 → 297 files, exactly the ten
feeds and nothing else; no `application/atom+xml` anywhere in the output; the
validator still passes with 60 HTML pages and 59 canonicals intact.

### 9. ~~No `robots.txt`~~ — done

`layouts/robots.txt` now renders to `public/robots.txt`:

```
User-agent: *
Allow: /

Sitemap: https://scottwlocke.github.io/james-street-tavern/sitemap.xml
```

**It is a template, not `static/robots.txt`.** The recommended static file
works for the stanza and fails on the one line that matters: `Sitemap:` must be
an absolute URL, and a file in `static/` has no way to read `.Site.BaseURL`.
Hardcoding it would fix the domain in place and make task 1's correction miss
this file — a second place to edit that nobody would remember. As a template it
rewrites itself when `baseURL` is corrected.

**The subtle part was turning it on.** Hugo parses every file in `layouts/` at
startup, so `layouts/robots.txt` broke the build immediately when its string
literal was malformed — but once it parsed correctly it produced *nothing*, and
the build stayed green. Hugo does not put the `Robots` output format on the home
page by default, so nothing was rendered and nothing warned. It needs an
explicit block in `hugo.toml`:

```toml
[outputs]
  home = ["HTML", "Robots"]
  section = ["HTML"]
```

`RSS` was in that list when this task was written — not for robots.txt's own
sake, but because dropping it here would have disabled task 8's 10 feeds as an
accident of turning robots.txt on. Task 8 has since removed it deliberately, so
the list is now the two entries above. The block sits between `disableKinds`
and `[params]` for the reason `hugo.toml` documents: a new table parked in the
wrong place re-scopes whatever follows it.

Two content decisions:

- **No `Disallow:` at all.** There is no admin, no session state and no
  unpublished page in `public/`, so a directive forbidding something would be
  asserting a fact about the site that is not true. `Allow: /` is the correct
  claim when there is nothing to forbid.
- **The Atom feeds are not listed here.** They never needed to be: task 8
  deleted them outright, and `Disallow`-ing a feed would have drawn a crawler's
  attention to something worth removing rather than hiding.

`Sitemap` sits after a blank line, outside the user-agent group. Both Google and
Bing ignore it inside a group, and the failure is silent — the file looks right
and the sitemap simply never gets submitted.

Verified by `.tmp/validate-jsonld.py`, which now checks robots.txt alongside the
page shell: file exists, `User-agent: *` and `Allow: /` present, no
path-blocking `Disallow`, `Sitemap` absolute and outside its group, and its URL
equal to `baseURL` + `sitemap.xml` pointing at a file that is actually published.
Four injected regressions — deleting the file, moving `Sitemap` into the group,
making it root-relative, and pointing it at `index.xml` — each produced its own
error, and a `Disallow: /admin` produced a warning.

That example read `example.org` until task 1 landed; it now reads the GitHub
Pages project URL, and the sitemap it advertises is the real one.

---

## 6. Already correct — no action

Verified during the audit, recorded so the next pass does not re-check them:

- **`<title>`** — unique across all 60 pages; length range 19–59 chars, so no
  truncation risk. The 404 is titled separately, not left as Hugo's
  "404 Page not found" default.
- **`<h1>`** — exactly one per page, across all 60.
- **Meta descriptions** — present on all 60, 59 distinct (see task 7); the
  one repeat is `/` and `/404.html`.
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
