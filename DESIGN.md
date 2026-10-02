# Design System — James Street Tavern

> Rustic Country Tavern • Monroeville, PA  
> Design language derived from the “Monday Night Wings” chalkboard specials, warm wood interiors, string lights, and classic American bar fare.

---

## 1. Brand Overview

**Personality**  
Warm, unpretentious, neighborly, and slightly rowdy. Think neighborhood tavern that has been around for decades — chalkboard specials, cold beer, jumbo wings, and good company.

**Core Feeling**  
Cozy, dimly lit, wood-paneled, string-light glow. The kind of place you walk into on a Monday night and immediately feel at home.

**Keywords**  
Rustic • Country • Tavern • Chalkboard • Warm Wood • Craft Beer • Wings • Neighborhood • Authentic • No-frills

---

## 2. Color Palette

### Primary Colors
| Role              | Name              | Hex       | Usage                                      |
|-------------------|-------------------|-----------|--------------------------------------------|
| Brand Blue        | Tavern Navy       | `#0F2C5B` | Logo circle, primary CTAs, headers         |
| Accent Gold       | Chalk Gold        | `#E8C547` | Headlines, prices, special callouts        |
| Deep Charcoal     | Chalkboard Black  | `#1A1A1A` | Backgrounds, chalkboard panels             |
| Warm Wood         | Barn Wood         | `#5C3A21` | Wood textures, secondary backgrounds       |
| Soft Cream        | Off-White         | `#F5F0E6` | Body text on dark, paper-like surfaces     |

### Supporting Colors
| Role              | Name              | Hex       | Usage                                      |
|-------------------|-------------------|-----------|--------------------------------------------|
| Light Wood        | Honey Oak         | `#C4A484` | Borders, subtle dividers, hover states     |
| Muted Red         | Barn Red          | `#8B2E2E` | Reserved — small accent badges. No current consumer; the “JST” badge that owned it was replaced by the crest (§4) |
| Foam White        | Beer Foam         | `#F8F5F0` | Secondary text, light cards                |
| Dark Brown        | Table Top         | `#2C1B10` | Footer, deep backgrounds                   |

### Semantic Colors
- Success / Available: `#4A7C59`
- Warning / Limited: `#C9A227`
- Error / Sold Out: `#8B2E2E`
- Info: `#0F2C5B`

### Gradients & Overlays
- Chalkboard gradient: linear-gradient(180deg, #1A1A1A 0%, #2A2A2A 100%)
- Warm wood overlay: rgba(92, 58, 33, 0.85)
- String-light glow: radial-gradient(circle, rgba(232, 197, 71, 0.15) 0%, transparent 70%)

---

## 3. Typography

### Font Stack

**Display / Headlines**  
`Oswald` or `Bebas Neue` (bold, condensed, slightly industrial)  
Fallback: `Impact`, `Arial Black`, sans-serif

**Chalkboard Style**  
`Permanent Marker` or `Caveat` (for specials & hand-written feel)  
Fallback: cursive

**Body / UI**  
`Source Sans 3` or `Inter`  
Fallback: system-ui, -apple-system, sans-serif

**Accent / Prices**  
`Oswald` Bold or `Roboto Condensed` Bold

### Type Scale

| Element           | Font              | Weight | Size (desktop) | Line Height | Letter Spacing |
|-------------------|-------------------|--------|----------------|-------------|----------------|
| Hero Headline     | Oswald            | 700    | 3.5rem         | 1.1         | 0.02em         |
| Section Title     | Oswald            | 600    | 2.25rem        | 1.2         | 0.01em         |
| Specials Title    | Permanent Marker  | 400    | 2rem           | 1.3         | 0              |
| Price             | Oswald            | 700    | 3rem           | 1           | 0.03em         |
| Body              | Source Sans 3     | 400    | 1.125rem       | 1.6         | 0              |
| Small / Caption   | Source Sans 3     | 400    | 0.875rem       | 1.4         | 0.01em         |
| Button            | Oswald            | 600    | 1rem           | 1           | 0.05em         |

### Text Treatments
- Chalkboard titles: slight letter-spacing + subtle text-shadow for chalk dust effect
- Prices: large, gold, with a thin underline or decorative flourish
- All-caps for specials and CTAs

### Type Tokens

Every text style in the system has a named role. Use the token — never a raw
`rem` value — when adding markup. Sizes are the desktop values; headings marked
`clamp()` scale with the viewport, everything else steps down at the 768px
breakpoint (§16). **†** marks a line-height that is inherited from `body` (1.6)
rather than declared on the component — those are the condensed-cap roles, which
get their shape from the font rather than from leading.

| Token | Class | Font | Weight | Size | Line Height | Tracking | Use |
|---|---|---|---|---|---|---|---|
| `{type.hero}` | `.hero h1` | Oswald | 700 | `clamp(2.75rem, 7vw, 3.5rem)` | 1.1 | 0.02em | Homepage hero headline |
| `{type.title}` | `.section-title` | Oswald | 600 | 2.25rem | 1.2 | 0.01em | Section headings |
| `{type.specials}` | `.chalk-title` | Permanent Marker | 400 | `clamp(1.75rem, 4vw, 2rem)` | 1.3 | 0 | Chalkboard specials title |
| `{type.subtitle}` | `.menu-section-title` | Oswald | 600 | 1.75rem | 1.2 | 0 | Menu-section headings |
| `{type.card-title}` | `.card-title` | Oswald | 600 | 1.5rem | 1.2 | 0 | Section card titles |
| `{type.price-hero}` | `.chalk-price` | Oswald | 700 | 3rem | 1 | 0.03em | Specials price stamp |
| `{type.price}` | `.menu-price` | Oswald | 700 | 1.375rem | 1.6 † | 0.03em | Card and detail price |
| `{type.kicker}` | `.section-kicker` | Permanent Marker | 400 | 1.25rem | 1.6 † | 0 | Eyebrow above a heading |
| `{type.button}` | `.btn` | Oswald | 600 | 1rem | 1.6 † | 0.05em | All CTAs, uppercase |
| `{type.nav}` | `.nav-links a` | Oswald | 500 | 1rem | 1.6 † | 0.05em | Desktop nav, uppercase |
| `{type.heading-sm}` | `.hours-col h4` | Oswald | 600 | 1rem | 1.6 † | 0.12em | Column headings, uppercase |
| `{type.label}` | `.contact-line-label` | Oswald | 600 | 0.875rem | 1.6 † | 0.1em | Field labels, uppercase |
| `{type.eyebrow-sm}` | `.footer-col h4` | Oswald | 600 | 0.9375rem | 1.6 † | 0.14em | Footer column headings |
| `{type.body}` | `body` | Source Sans 3 | 400 | 1.125rem | 1.6 | 0 | Default body copy |
| `{type.body-sm}` | `.card-meta`, `.menu-desc` | Source Sans 3 | 400 | 1rem | 1.6 | 0 | Card and menu descriptions |
| `{type.caption}` | `.footer-col a` | Source Sans 3 | 400 | 0.9375rem | 1.6 † | 0 | Footer links |

**Principles**

- The display family (Oswald) carries every *structural* label — headings, prices,
  buttons, nav, labels — and is always uppercase with positive tracking
  (0.01em–0.14em). It is the tavern's signage voice.
- The chalk family (Permanent Marker) is rationed to two roles only: the specials
  board title and the section kicker. More than that and it reads as a novelty
  rather than a tavern.
- Body copy never uses the display or chalk family. Source Sans 3 at weight 400 is
  the only reading face.
- Oswald carries the tightest line-heights in the system (1 on prices) because its
  condensed caps need almost no leading. Source Sans 3 needs 1.6 to stay readable.
  Do not normalise them.
- There is no wordmark type token. The tavern name is set in the crest artwork
  (§4), not in live text — the nav link's accessible name comes from its `alt`.

---

## 4. Logo & Branding

**Primary Logo**  
`static/images/jst-logo.png` — the supplied crest: a 287×265 full-colour RGBA
shield with a banner wordmark, in blue, red and white. It is the whole lockup;
the tavern name and "Monroeville, PA" are baked into the artwork, not live text.

Because the name lives in the image, the nav link **must** carry an `alt` of
`James Street Tavern — Monroeville, PA`. That `alt` is the link's only accessible
name; dropping it removes the site name from the accessibility tree entirely.

Rendered at `height: var(--logo-clear)` with `width: auto`. The `<img>` also needs
its intrinsic `width`/`height` attributes so the browser reserves the box and
derives the aspect ratio without a layout shift.

**Logo size**

`--logo-clear` is the single knob for logo height, and it is **88px**. It also
defines the required clear space, and `.logo` carries `min-height: var(--logo-clear)`
so the link keeps its 44px+ touch target (§11) at any logo size.

**Clear Space**  
Minimum clear space equal to the logo height on all sides. Horizontally this is
held by the container gutter; vertically by the nav bar.

**Nav chrome derives from the logo — do not hardcode these**

Three values are computed from `--logo-clear` and must stay that way:

| Token | Derives | Used by |
|---|---|---|
| `--logo-clear` | authored (`88px`) | `.logo-img` height, `.logo` min-height |
| `--nav-h` | `--logo-clear + 2 × {space.sm}` (104px) | `.nav-inner` min-height, `.mobile-nav` inset |
| `--nav-clearance` | `--nav-h + {space.md}` (120px) | `html` `scroll-padding-top` |

The drawer and the scroll padding are the reason this matters: `.mobile-nav` is
`position: fixed` and begins at `--nav-h`, so a stale value slides its first rows
under the nav; `scroll-padding-top` is what keeps the nav's Contact and Find Us
anchor jumps clear of a sticky bar. When the logo is resized, change
`--logo-clear` and nothing else.

**Logo Variations**

The supplied crest is a raster PNG, so **the logo cannot be recoloured in CSS**.
The previous white-monochrome and gold lockups were CSS recolours of a drawn
lockup and no longer exist. Variants must be supplied as separate image files —
`logo-jst-primary.png`, `logo-jst-white.png` — and swapped at the markup, not via
a class. Neither has been supplied yet.

Because the crest is full-colour, its navy field sits low-contrast against the
chalkboard nav (`#1A1A1A`). This is accepted: the crest carries enough white and
light blue to read as a shield. If it proves illegible on the dark bar, the fix is
a supplied white variant, never a CSS filter.

**Favicon / App Icon**  
The crest PNG, referenced by both `rel="icon"` and `rel="apple-touch-icon"`. A
detailed 287×265 crest is not legible at 16px, so a simplified monogram would be
the better tab icon; `static/logo-jst-monogram.svg` still exists on disk but is
unused and unreferenced.

---

## 5. Imagery Guidelines

### Photography Style
- Warm, slightly desaturated tones
- Soft string-light bokeh in backgrounds
- Focus on real food (wings, beer, checkered paper) and authentic interior wood textures
- Prefer natural window light mixed with warm interior lighting
- Avoid overly polished or sterile food photography

### Recommended Subjects
- Jumbo whole wings on checkered paper or black boats
- Frosty beer mugs with condensation
- Chalkboard specials
- Wooden bar tops and stools
- String lights and rustic wall textures

### Image Treatments
- Subtle warm overlay (`#5C3A21` at 10–15% opacity)
- Soft vignette on hero images
- Slight film grain optional for authentic tavern feel

### Icons & Illustrations
- Simple line icons with rounded ends
- Prefer hand-drawn or chalkboard-style icons for specials
- Wing, beer mug, chalkboard, and location pin as core icons

### Placeholder Art
Until real photography exists, a section's card art is a placeholder SVG built
from the system's own tokens, not a grey box. The convention:

- One per section, at `content/<section>/photo-<section>-hero.svg`. It lives in
  the **section bundle**, which is what makes `photoGlob` resolve it — no layout
  change is needed to add or replace one.
- Built from the `--wood-gradient` stops (`#5C3A21 → #3A2415 → #2C1B10`), the §5
  vignette, and the stylesheet's own `feTurbulence` grain. 1600×1000, matching
  `.card-media`'s 16:10 so `object-fit: cover` never crops.
- The section name sits in the chalk-white `--font-display` stack over a gold
  flourish, with a `PLACEHOLDER · REPLACE photo-<name>-hero.svg` caption so
  nobody mistakes it for final art.
- Handing off to a real photo needs no deletion step: with both
  `photo-pizza-hero.svg` and a real `.jpg` in the bundle, `GetMatch` returns the
  **jpg**. Dropping in photography wins automatically.

Where no art resolves at all, `.card-media-empty` renders the wood fill with the
grain — a legitimate fallback, not a failure, but prefer a placeholder over
leaving it bare.

---

## 6. UI Components

Component behaviour is specified here. The full inventory of what actually
exists, with the tokens each one draws on, is in §17; corner radii are governed
by §14 and depth by §15.

### Buttons

**Primary Button**
- Background: `#0F2C5B`
- Text: `#F5F0E6`
- Border-radius: 4px (slightly soft, not pill)
- Hover: lighten 8% + subtle gold underline
- Active: darker navy

**Secondary / Outline**
- Border: 2px solid `#E8C547`
- Text: `#E8C547`
- Hover: fill with gold, text becomes dark

**Special / Promo Button**
- Background: `#E8C547`
- Text: `#1A1A1A`
- Slight chalk texture optional

### Cards
- Background: `#2C1B10` or soft cream
- Border: 1px solid `#C4A484` at 30% opacity
- Shadow: soft, warm (0 8px 24px rgba(44, 27, 16, 0.35))
- Border-radius: 6–8px

### Chalkboard Panel Component
- Background: `#1A1A1A`
- Subtle noise texture
- Gold decorative flourishes (swirls) on corners
- White/gold chalk-style text
- Optional hanging chain or string-light accent at top

### Specials Rotator
One chalkboard is visible at a time; the next special slides in every **20
seconds**. The slide is 3rem of horizontal travel with a fade, on the standard
`--duration` (250ms) / `--easing` pair — grounded, no overshoot (§9).

**The markup ships every board.** `.chalkboards` is the shared wrapper: an
ordinary grid holding all the boards, so with JS off they simply stack, spaced
by the wrapper's `gap`, and the specials stay complete and readable.
`assets/js/main.js` adds `.specials-rotator` to the wrapper, which is the *only*
thing that scopes the hiding rules:

| Selector | Effect |
|---|---|
| `.chalkboards` | `display: grid`, `gap: var(--space-xl)` — separates stacked boards. Once the rotator runs every board is in the single `1/1` cell below, so there is one row and one column and the gap stops applying. |
| `.specials-rotator .chalkboard.is-*` | `grid-area: 1 / 1` — only state\'d boards share the cell |
| `.specials-rotator .chalkboard.is-active` | Shown, centred |
| `….chalkboard.is-before` | Off to the left, faded |
| `….chalkboard.is-after` | Off to the right, faded |
| `.specials-controls` | Dots + pause, injected by JS |

Three rules that are easy to get wrong here:

- **`.specials-rotator` must never appear in the template.** Every hide rule is
  scoped under it, so emitting the class server-side hides all but the first
  special for anyone without JS. The wrapper carries only `data-specials`.
- **`grid-area` belongs on the `.is-*` classes, not on `.chalkboard`.** A board
  that JS has not yet given a state stays in normal flow and fully visible, so a
  half-initialised rotator stacks its specials instead of piling several opaque
  boards into one cell on top of each other. Assigning the cell only once a
  board has a state makes "JS has not run yet" degrade to readable rather than
  to a pile.
- **Inactive boards use `visibility: hidden`, not `display: none`.** Visibility
  takes a board out of the tab order and the accessibility tree while still
  transitioning discretely, so the outgoing board finishes its slide. `display:
  none` would remove it mid-flight and it would blink out instead.
- **`align-items: start`** on the track. The grid cell sizes to the tallest board
  so the section does not jump as the rotation advances; without `start` the
  shorter boards stretch to match.

Rotation advances forward and wraps. Positions compare without wrapping, so the
outgoing board always leaves leftward and the incoming one enters from the
right; the wrap from last back to first is the one case where the incoming board
enters from the left. Cheaper than cloning the first slide to fake an endless
track, and invisible at a 20s interval.

**A single special gets no rotator** — no controls, no timer, just the panel.

### Specials Controls
- Dots are 10px marks in a **44×44px** target (§11); the active one grows to a
  26px gold lozenge. `border-radius: 50%` is literal — a dot's shape, not a
  radius-scale value, so it does not borrow `{rounded.badge}` (§14).
- Pause is a 44×44px button whose two bars become a play triangle when paused.
  Both glyphs are drawn in CSS; the site ships no icon assets (§5).
- The controls are built by JS, not rendered in the template. A dot that cannot
  do anything without JS is worse than no dot at all.
- The controls never contain text, so gold stays scarce (§18): one gold element.

### Form Inputs
- Dark background with light cream text
- Gold focus ring
- Placeholder text in muted wood tone

### Navigation
- Sticky top bar on dark wood or semi-transparent
- Gold underline on active link
- **The eight top-level sections roll up under a single `Menu` control**, so the
  bar reads `Logo / Menu / Full Menu / Contact / Find Us` instead of nine inline
  links. `Full Menu` is the itemised board (§7). The dropdown panel lists every
  section with the active one marked, closes on outside click and on Escape
  (focus returns to the toggle), and is desktop only — below 1024px `.nav-menu`
  is `display:none` and the drawer takes over.
- Mobile: full-width drawer with chalkboard background, opening with a `Menu`
  heading above the same section list so both navigations read alike

### The menu section list is centralised

`layouts/partials/menu-sections.html` returns `.Site.Sections` minus
`params.nonMenuSections`, and it is the **only** source for the section list.
Five surfaces read it: the homepage card grid, the nav dropdown, the mobile
drawer, the footer's `Menu` column, and the Full Menu page.

Opt a section out by adding its slug to `nonMenuSections` in `hugo.toml`. Never
filter `.Site.Sections` inline at a call site — that is how a specials section
would quietly appear as a ninth menu entry in some surfaces and not others.

---

## 7. Layout & Spacing

### Grid
- Max content width: 1200px
- Gutters: 24px (mobile) → 40px (desktop)
- Consistent 8px base unit

### Spacing Scale
| Token   | Value  |
|---------|--------|
| xs      | 4px    |
| sm      | 8px    |
| md      | 16px   |
| lg      | 24px   |
| xl      | 40px   |
| 2xl     | 64px   |
| 3xl     | 96px   |

### Section Rhythm
- Generous vertical padding (80–120px) on desktop
- Tighter on mobile (48–64px)
- Use wood texture or subtle string-light backgrounds between major sections

### Page Inventory
The homepage is a landing page, not a menu. Itemised cards live on `/menu/`.

| Page | Contains |
|---|---|
| `/` | Hero, specials chalkboard, the **eight** section cards, contact |
| `/menu/` | All items, grouped under their eight sections. `46 dishes across 8 sections` count under the intro |
| `/<section>/` | One section's header and its own items. Still a valid drill-in |
| `/specials/` | The specials section's own page (see below) |

Each `.menu-section` on `/menu/` carries `id="<section>"`, so `/menu/#pizza`
deep-links work. No extra scroll offset is needed for those — `html`'s
`scroll-padding-top: var(--nav-clearance)` already covers fragment navigation
against the sticky bar.

### Specials are content, not config
Specials are ordinary pages in `content/specials/`, rendered into the homepage
chalkboard — one `.chalkboard` per item, so a single offer looks as it always
did and a second stacks another board. The board renders nothing when the section
is empty, and keeps `id="specials"`, which the footer links to.

Item front matter: `title`, `kicker`, `price`, `priceUnit`, `lead`, `details`
(list), `weight`. The board is the loudest thing on the page (§18) — specials
belong there and nowhere else.

`/specials/` is a real section, so Hugo builds it and it is reachable by direct
URL, but it is deliberately **unlinked**: `nonMenuSections` keeps it out of the
five menu surfaces, and no navigation points at it.

---

## 8. Texture & Surface Treatments

- **Wood**: high-quality seamless wood grain (dark barn wood preferred)
- **Chalkboard**: subtle noise + soft edge wear
- **Paper**: blue-and-white checkered pattern for food containers
- **Metal**: brushed or slightly aged for hardware accents
- **Glass**: condensation and soft reflections on beer mugs

Avoid pure flat digital surfaces. Always introduce at least a light texture or warm overlay.

---

## 9. Motion & Interaction

- Transitions: 200–300ms ease-out
- Hover states: subtle lift (2–4px) + warm shadow
- Chalk text: optional slight “dust” particle on load (very light)
- Page load: soft fade + slight scale on hero elements
- Avoid bouncy or overly playful animations — keep it grounded and tavern-like

---

## 10. Tone of Voice

**Writing Style**
- Friendly, direct, and local
- Use contractions and everyday language
- Emphasize “weekly specials,” “dine-in only,” “jumbo whole wings”
- Avoid corporate or overly polished marketing speak

**Examples**
- “Monday Night Wings — $1.50 each. Minimum of 3 of the same flavor. Dine-in only.”
- “Come hungry. Leave happy.”
- “Your neighborhood tavern in Monroeville.”

---

## 11. Accessibility

- Maintain WCAG AA contrast (especially gold on dark and cream on navy)
- Focus indicators: 3px gold outline
- All interactive elements minimum 44×44px touch target
- Prefer real text over text-in-image for specials when possible
- Provide alt text that describes the rustic atmosphere and food
- **Auto-rotating content needs a stop control.** WCAG 2.2.2 applies to the
  specials rotator (§6): it changes by itself and runs for longer than five
  seconds, so the pause button is mandatory, not decorative. The rotator also
  yields to hover and to keyboard focus, so a visitor mid-read does not have a
  board swapped out from under them, and it does not run in a background tab.
- **An auto-rotating region is not a live region.** No `aria-live` on the track —
  announcing every 20s is hostile. The carousel semantics are added by JS, not by
  the template: the wrapper becomes `role="region"` +
  `aria-roledescription="carousel"`, each board becomes `role="group"` +
  `aria-roledescription="slide"` labelled `"n of m: <title>"`, and only the
  active board is in the accessibility tree (§6).
- **The pause button's label states the action**, flipping between "Pause
  specials" and "Play specials". A label that names the current state instead
  ("Paused") leaves the reader guessing what pressing it does.
- **The crest is the one sanctioned text-in-image.** Its wordmark is artwork, so
  its accessible name must come from `alt` (§4). The nav link's `alt` is the
  site's brand name; decorative art elsewhere in the header should take
  `alt=""`. Every placeholder SVG is decorative and carries empty alt or
  `aria-hidden` — its caption text names the section, so announcing the SVG
  filename would be noise

---

## 12. File & Asset Naming Conventions

```
static/images/jst-logo.png         the supplied crest — logo, favicon, touch icon
logo-jst-primary.png               NOT SUPPLIED — colour variant of the crest
logo-jst-white.png                 NOT SUPPLIED — white variant, for dark surfaces
logo-jst-monogram.svg              simplified tab monogram — present, unused (§4)
photo-<section>-hero.svg           section placeholder art, in the section bundle
photo-<subject>-hero.<ext>         real photography, in a page bundle
specials/<slug>.md                 a special; front matter per §7
texture-wood-dark.jpg
texture-chalkboard.png
icon-wings.svg
icon-beer.svg
```

Photography and placeholder art are both resolved through the `photoGlob` site
param (`photo-*-hero.*`), never a hardcoded filename. Placeholders are named
exactly like photography on purpose, so swapping one for the other needs no
template change.

---

## 13. Implementation Notes

- Prefer CSS custom properties for the entire color and spacing system
- Use `background-blend-mode` and subtle noise overlays for authentic chalkboard and wood feels
- Load Google Fonts: Oswald + Source Sans 3 + Permanent Marker (or system alternatives)
- Dark mode is the default (true to the tavern atmosphere); light mode is secondary and should still feel warm

---

## 14. Border Radius Scale

Corners are the system's clearest signal. The rule is **buttons stay sharp,
containers stay soft** — 4px on anything you press, 8px on anything that holds
content.

| Token | Value | Use |
|---|---|---|
| `{rounded.none}` | `0px` | Chalkboard corner flourishes, hairline ends, full-bleed bands |
| `{rounded.flourish}` | `2px` | Price underline, hairline caps |
| `{rounded.sm}` | `4px` | All buttons, the nav toggle, the "Find Us" link |
| `{rounded.md}` | `8px` | Cards, chalkboard panel, detail panels, contact cards, map, dropdowns |
| `{rounded.badge}` | `50%` | Reserved. No current consumer — the circular logo badge was replaced by the crest (§4) |

**Principles**

- Never round a button past `{rounded.sm}`. A 12px button reads as a consumer app,
  not a tavern.
- Never round a card past `{rounded.md}`. The system has exactly two corner radii;
  a third reads as drift.
- `{rounded.badge}` is reserved and currently unused: the only element that owned
  it was the CSS-drawn circular logo badge, replaced by the crest image (§4). Keep
  it reserved — it is not a "large" radius and must not be reused for avatars,
  thumbnails, or pills. Note the crest itself brings its own circular and banner
  shapes; those are artwork, not a radius token.
- Full-bleed photography and wood textures sit square — no rounding.

---

## 15. Elevation & Depth

Depth is communicated by **warm shadow**, never by a neutral grey one. Every
shadow in the system carries the table-top brown (`rgba(44, 27, 16, …)`) so
lifted surfaces still read as wood and candlelight.

| Level | Token | Treatment | Use |
|---|---|---|---|
| 0 — Flat | — | No border, no shadow | Section bands, body canvas, full-bleed hero |
| 1 — Warm | `{elev.rest}` | `0 8px 24px rgba(44, 27, 16, 0.35)` | Cards, detail panels, contact cards, map, dropdown |
| 2 — Lifted | `{elev.hover}` | `0 12px 32px rgba(44, 27, 16, 0.5)` | Hover state of every level-1 surface |
| 3 — Recessed | `{elev.recessed}` | Level 1 + `inset 0 0 90px rgba(0, 0, 0, 0.75)` | The chalkboard specials panel only |
| 4 — Vignette | `{elev.vignette}` | `inset 0 0 220px 60px rgba(26, 26, 26, 0.9)` | Hero image edge falloff only |

**Principles**

- Level 1 is the workhorse. Cards, panels, the map, and the dropdown are the only
  things that get it. Section bands stay flat — the texture does that work.
- Level 2 is reserved for hover. If a surface has a resting shadow, it gets
  exactly one lifted state.
- Levels 3 and 4 are **single-use**. The recessed inset belongs to the chalkboard
  and nowhere else; the vignette belongs to the hero and nowhere else. Both exist
  to sell one object each.
- Depth never replaces a border. A bordered surface is level 0 with a 1px
  `rgba(196, 164, 132, 0.3)` wood hairline, not a level-1 surface.

---

## 16. Breakpoints & Collapsing Strategy

Two breakpoints. The system is deliberately not fluid — a tavern menu is a short,
fixed set of pages, and extra breakpoints only add untested states.

| Name | Width | Key changes |
|---|---|---|
| Mobile | < 768px | Single-column everything; hamburger drawer; gutters 24px; section padding 56px; hero ≥ 520px |
| Tablet | 768–1023px | Two-column card and menu grids; 3-column footer; detail and contact layouts stack; gutters 24px |
| Desktop | ≥ 1024px | Three-column grids; `Menu` dropdown, `Full Menu`, `Contact`, and the "Find Us" link; gutters 40px |

**Collapsing strategy**

- **Logo** — a fixed-height image, so it cannot reflow or overflow at any width,
  and it takes no breakpoint step. It is 88px tall and ~95px wide, against ~387px
  for the text lockup it replaced, so the header is now markedly narrower than it
  was and there is no narrow-viewport risk left on this element. Its box is
  `max-width: 100%`, so an oversized future logo shrinks rather than pushing the
  bar wide.
  This replaces a real earlier bug: the previous 18-character uppercase-Oswald
  wordmark with `white-space: nowrap` needed ~387px and dragged the whole page
  into horizontal scroll below ~435px. It was fixed by scaling and un-wrapping
  the text, not by `overflow-x: hidden` — that would have clipped the logo rather
  than fixing the width and hidden any other overflow. **Never reintroduce
  `overflow-x: hidden` on `.nav-bar`** to suppress a width problem; measure the
  width instead.
- **"Find Us" link** — hidden below 1024px. It anchors to `#map` in the contact
  band, where the address, phone, and hours are also rendered, so nothing is lost.
- **Top nav** — the `Menu` dropdown, `Full Menu`, `Contact`, and the "Find Us" link collapse
  into a 44px hamburger below 1024px. The drawer is full-canvas chalkboard with
  56px link rows and a `Menu` heading. Closes on link click, `Escape`, or
  resizing above 1024px.
- **Card / menu grids** — 3 columns → 2 → 1. Cards keep `{rounded.md}` and their
  shadow at every size; only the column count changes.
- **Detail and contact layouts** — the 5/7 two-column split stacks to one column
  at 1024px. Image leads, panel follows.
- **Chalkboard panel** — the price block and the details list go from side-by-side
  to stacked at 1024px. The wooden border thins from 10px to 6px at 768px.
- **Hero** — scales via `clamp()` only. The vignette and wood overlay are
  percentage-based and need no breakpoint.

**Touch targets (§11)**

- Every interactive element clears 44×44px. Buttons are 44px tall; nav rows are
  44px; the hamburger is 44×44; footer links are 44px tall rows even though the
  text is 15px; the specials dots and pause button are 44×44 (§6).
- Tap areas extend beyond the visible glyph where needed — nav and footer links
  use `min-height` rows rather than padding the text run.
- The mobile drawer's links are 56px tall, above the 44px floor, because it is a
  thumb-only surface.

**Reduced motion**

`@media (prefers-reduced-motion: reduce)` collapses every transition and animation
to 0.01ms and disables smooth scrolling. This covers the hero entrance (§9) as
well as hover transitions. Do not add motion that opts out of this block.

The specials rotator (§6) is covered by this block for free: its slide is a
transition, so reduced-motion visitors get an instant swap rather than travel.
The 20s rotation itself still runs — the request was to rotate, and an instant
swap is not motion — and the pause control (§11) is always there. If auto-advance
is ever dropped wholesale under reduced motion, that is a deliberate change to
§6, not a side effect.

---

## 17. Component Inventory

The named components that exist today, with the tokens each one draws on. States
are separate entries, never buried in prose.

| Component | Class | Draws on |
|---|---|---|
| `button-primary` | `.btn-primary` | `{colors.tavern-navy}`, `{type.button}`, `{rounded.sm}` |
| `button-primary-hover` | `.btn-primary:hover` | Lightened 8% + gold underline |
| `button-primary-active` | `.btn-primary:active` | Darker navy |
| `button-outline` | `.btn-outline` | `{colors.chalk-gold}` border + label |
| `button-gold` | `.btn-gold` | `{colors.chalk-gold}` fill, chalkboard label |
| `chalkboard-panel` | `.chalkboard` | `{elev.recessed}`, wood frame, corner flourishes |
| `specials-rotator` | `.specials-rotator`, `.chalkboards` | JS-added, homepage only; stacks boards into one grid cell and slides one at a time every 20s (§6) |
| `chalkboards` | `.chalkboards`, `.chalkboard` | Stack of boards; plain grid with a gap when not rotating. `/specials/` renders the same panels, all at once (§6) |
| `specials-slide` | `.chalkboard.is-active`, `.is-before`, `.is-after` | `visibility` + `opacity` + `translateX`; `--duration`/`--easing` |
| `specials-dot` | `.specials-dot`, `.specials-dot-mark` | 44×44 target, 10px mark; honey oak → gold lozenge when active |
| `specials-pause` | `.specials-pause`, `.specials-pause-icon` | 44×44, CSS-drawn pause/play glyphs; required by WCAG 2.2.2 (§11) |
| `chalk-price` | `.chalk-price`, `.chalk-price-flourish` | `{type.price-hero}`, `{rounded.flourish}` |
| `card` | `.card` | `{colors.panel}`, `{rounded.md}`, `{elev.rest}` |
| `card-hover` | `a.card:hover` | `{elev.hover}` + 3px lift (§9) |
| `card-media` | `.card-media`, `.card-media-empty` | 16:10, wood fill, warm grade |
| `detail-panel` | `.detail-panel` | `{colors.panel}`, `{elev.rest}` |
| `contact-card` | `.contact-card` | `{colors.panel}`, `{elev.rest}` |
| `contact-map` | `.contact-map` | `{rounded.md}`, desaturated iframe |
| `nav-bar` | `.nav-bar` | Sticky chalkboard, 2px gold underline |
| `nav-link` + active | `.nav-links a`, `.active` | `{type.nav}`, gold scaleX underline |
| `menu-dropdown` | `.nav-menu-toggle`, `.nav-menu-panel` | Rolls the 8 sections under one `Menu` control; caret flips on open; active row gets a gold inset bar |
| `logo` | `.logo`, `.logo-img` | `--logo-clear` height; the anchor holds the §4 clear space and the 44px touch target |
| `nav-chrome` | `--nav-h`, `--nav-clearance` | Bar height and anchor clearance, both derived from `--logo-clear` (§4) |
| `section-header-cta` | `.section-header .btn` | Pairs the section heading with its Full Menu button |
| `find-us-link` | `.nav-utility-toggle` | `{rounded.sm}`, honey-oak → gold on hover; anchors to `#map` |
| `mobile-drawer` | `.mobile-nav.open` | Full-canvas chalkboard, 56px rows, `Menu` heading above the list |
| `section-band-wood` | `.section-wood` | Wood gradient + grain |
| `help-band` | `.help-band` | Wood gradient, double gold rule |
| `footer` | `.site-footer` | `{colors.table-top}`, 5-column grid |
| `hero` | `.hero`, `.hero-media` | Warm grade, wood overlay, `{elev.vignette}` |
| `hours-grid` | `.hours-grid`, `.hours-col` | Two-up hours, hairline rules |

**Not yet built** (referenced by the spec, absent from the code — do not assume
these exist):

- Form inputs (§6) — no form on the site; the contact block is address/hours only
- Icon set (§5) — no icon assets; the core wing/beer/chalkboard/pin icons are absent
- Texture files (§12) — wood and chalkboard are generated in CSS, not loaded as
  `texture-*.jpg`
- Logo variants (§4, §12) — only `jst-logo.png` exists. `logo-jst-primary.png`
  and `logo-jst-white.png` have no artwork, and the crest cannot be recoloured
  in CSS, so there is currently no white-on-chalkboard lockup
- Tab monogram (§4) — `logo-jst-monogram.svg` exists but is unreferenced; the
  favicon is the full crest

---

## 18. Do's and Don'ts

### Do

- Ration `{colors.chalk-gold}` the way the tavern rations the specials board —
  headlines, prices, and the specials callout. Two gold elements per viewport is
  a lot.
- Keep the chalk family to two roles (§3): specials title and section kicker.
- Pair the chalkboard base with a wood or panel surface for depth, and let the
  warm shadow do the lifting.
- Hold buttons at `{rounded.sm}` and cards at `{rounded.md}` — the two-radius
  split is the signature.
- Keep body copy in Source Sans 3; use Oswald for structure and Permanent Marker
  for the chalkboard only.
- Give every interactive element a 44px minimum target, even where the visual
  is a text link.
- Ship real text for specials and prices. Never bake copy into an image — the crest
  (§4) is the sole exception, and it pays for that by requiring a real `alt`.
- Credit photography with a warm 10–15% wood overlay and let the grain run.

### Don't

- Don't introduce a fourth corner radius, a second chalk font, or a new
  saturated hue. The vocabulary is fixed (§2, §14).
- Don't set body copy in Oswald or the chalk font. It reads as signage, not prose.
- Don't use cool greys for shadows or borders — warmth is the whole point
  (`rgba(44, 27, 16, …)` only).
- Don't let a flat, untextured surface span a full section band (§8).
- Don't apply the recessed inset anywhere but the chalkboard, or the hero
  vignette anywhere but the hero.
- Don't put body or price text in honey oak on a wood band. That pairing is
  4.32:1 and fails AA for normal text (§11) — use chalk gold there instead.
- Don't add bounce, spring, or overshoot easing. The system is grounded
  (`cubic-bezier(0.16, 1, 0.3, 1)`); bouncy motion reads as a kids' menu.
- Don't animate anything without a `prefers-reduced-motion` fallback (§16).
- Don't let the specials board stop being the loudest thing on the page. It is
  the reason people come on a Monday.
- Don't add anything that rotates, auto-plays or scrolls without a way to stop
  it (§11). If it moves on its own for more than five seconds it needs a control.
- Don't hide content behind JS. The rotator ships every board and only
  `.specials-rotator`, added by JS, ever hides one (§6).

---

## 19. Iteration Guide

1. Work one component at a time. Don't refactor a whole section in a pass.
2. Reference tokens directly (`{colors.chalk-gold}`, `{type.button}`,
   `{rounded.md}`, `{elev.rest}`) — never re-derive a hex or px value in prose
   or in a new rule.
3. Check the value against §17 before inventing one. If it isn't in the
   inventory and isn't in the scales (§2, §3, §7, §14, §15), it needs adding to
   the spec first, not just to the CSS.
4. Add new states as separate inventory rows or separate rules (`-hover`,
   `-active`, `-focused`). Never bury a state inside an existing selector.
5. Verify contrast before shipping any new colour pairing. Compute it — don't
   eyeball it. Honey oak on wood is the known trap (§18).
6. Keep gold scarce. If a new component introduces a third gold element in one
   viewport, reconsider the accent or the layout.
7. Every new surface must declare its texture. "No texture" is not a valid
   default under §8.
8. Build with `hugo` before committing; preview drafts with `hugo server -D`.
   `public/` is generated and gitignored — never commit it.
9. Name assets per §12. Photography and section placeholders are both
   `photo-<name>-hero.<ext>` and are resolved through the `photoGlob` site param,
   not a hardcoded filename.
10. A section that is not part of the menu goes in `params.nonMenuSections` (§6).
    Read the section list from `menu-sections.html`; never filter `.Site.Sections`
    inline, and never hardcode a nav or bar height that §4 derives from the logo.

---

**Last updated:** October 2026  
**Source inspiration:** Official Monday Night Wings promotional photography — James Street Tavern, Monroeville, PA
