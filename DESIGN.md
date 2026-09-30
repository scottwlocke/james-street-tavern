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
| Muted Red         | Barn Red          | `#8B2E2E` | Small accent badges (like the “JST” badge) |
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
| `{type.wordmark}` | `.logo-text` | Oswald | 700 | 1.375rem | 1.1 | 0.02em | Nav wordmark, uppercase |
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

---

## 4. Logo & Branding

**Primary Logo**  
Circular blue badge with white “JAMES STREET TAVERN” wordmark and small red “JST” shield at top. Location line “Monroeville, PA” in smaller type.

**Clear Space**  
Minimum clear space equal to the height of the “JST” badge on all sides.

**Logo Variations**
- Full color (preferred on light or dark)
- White monochrome (for dark wood or chalkboard backgrounds)
- Single-color gold (for premium/special moments)

**Favicon / App Icon**  
Simplified blue circle with “JST” monogram.

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

### Form Inputs
- Dark background with light cream text
- Gold focus ring
- Placeholder text in muted wood tone

### Navigation
- Sticky top bar on dark wood or semi-transparent
- Gold underline on active link
- Mobile: full-width drawer with chalkboard background

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

---

## 12. File & Asset Naming Conventions

```
logo-jst-primary.svg
logo-jst-white.svg
texture-wood-dark.jpg
texture-chalkboard.png
icon-wings.svg
icon-beer.svg
photo-wings-hero.jpg
```

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
| `{rounded.sm}` | `4px` | All buttons, the nav toggle, the "Find Us" link, the JST shield |
| `{rounded.md}` | `8px` | Cards, chalkboard panel, detail panels, contact cards, map, dropdowns |
| `{rounded.badge}` | `50%` | The circular logo badge only |

**Principles**

- Never round a button past `{rounded.sm}`. A 12px button reads as a consumer app,
  not a tavern.
- Never round a card past `{rounded.md}`. The system has exactly two corner radii;
  a third reads as drift.
- `{rounded.badge}` is exclusive to the logo. It is not a "large" radius and must
  not be reused for avatars, thumbnails, or pills.
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
| Desktop | ≥ 1024px | Three-column grids; full inline nav and the "Find Us" link; gutters 40px |

**Collapsing strategy**

- **"Find Us" link** — hidden below 1024px. It anchors to `#map` in the contact
  band, where the address, phone, and hours are also rendered, so nothing is lost.
- **Top nav** — the inline link list and the "Find Us" link collapse into a
  44px hamburger below 1024px. The drawer is full-canvas chalkboard with 56px link
  rows. Closes on link click, `Escape`, or resizing above 1024px.
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
  text is 15px.
- Tap areas extend beyond the visible glyph where needed — nav and footer links
  use `min-height` rows rather than padding the text run.
- The mobile drawer's links are 56px tall, above the 44px floor, because it is a
  thumb-only surface.

**Reduced motion**

`@media (prefers-reduced-motion: reduce)` collapses every transition and animation
to 0.01ms and disables smooth scrolling. This covers the hero entrance (§9) as
well as hover transitions. Do not add motion that opts out of this block.

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
| `chalk-price` | `.chalk-price`, `.chalk-price-flourish` | `{type.price-hero}`, `{rounded.flourish}` |
| `card` | `.card` | `{colors.panel}`, `{rounded.md}`, `{elev.rest}` |
| `card-hover` | `a.card:hover` | `{elev.hover}` + 3px lift (§9) |
| `card-media` | `.card-media`, `.card-media-empty` | 16:10, wood fill, warm grade |
| `detail-panel` | `.detail-panel` | `{colors.panel}`, `{elev.rest}` |
| `contact-card` | `.contact-card` | `{colors.panel}`, `{elev.rest}` |
| `contact-map` | `.contact-map` | `{rounded.md}`, desaturated iframe |
| `nav-bar` | `.nav-bar` | Sticky chalkboard, 2px gold underline |
| `nav-link` + active | `.nav-links a`, `.active` | `{type.nav}`, gold scaleX underline |
| `logo` | `.logo`, `.logo-badge`, `.logo-shield` | `{rounded.badge}`, `{colors.barn-red}` |
| `logo--mono` | `.logo--mono` | White monochrome for chalkboard (§4) |
| `logo--gold` | `.logo--gold` | Single-colour gold for premium moments |
| `find-us-link` | `.nav-utility-toggle` | `{rounded.sm}`, honey-oak → gold on hover; anchors to `#map` |
| `mobile-drawer` | `.mobile-nav.open` | Full-canvas chalkboard, 56px rows |
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
- Ship real text for specials and prices. Never bake copy into an image.
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
9. Name assets per §12. Photography is `photo-<subject>-hero.<ext>` and is
   resolved through the `photoGlob` site param, not a hardcoded filename.

---

**Last updated:** September 2026  
**Source inspiration:** Official Monday Night Wings promotional photography — James Street Tavern, Monroeville, PA
