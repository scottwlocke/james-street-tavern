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

**Last updated:** September 2025  
**Source inspiration:** Official Monday Night Wings promotional photography — James Street Tavern, Monroeville, PA
