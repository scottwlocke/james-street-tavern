---
design-system: "Terra & Horizon: Global Country Portal"
version: "1.0.0"
tokens:
  colors:
    primary: "#0B3C5D"        # Deep Heritage Blue (Trust, official governance, stability)
    primary-light: "#328CC1"  # Sky/Lake Accent Blue (Tourism, interactive elements)
    accent: "#D9B310"         # Golden Sun / Brass Accent (Culture, premium feel, highlights)
    background: "#F9F9FA"     # Crisp Off-White (Clean, readable, modern canvas)
    surface: "#FFFFFF"        # Pure White (Cards, distinct sections, navigation)
    text-main: "#1D2731"      # Dark Slate (High-contrast typography)
    text-muted: "#5C6B73"     # Charcoal (Captions, secondary data, metadata)
    border: "#E2E8F0"         # Soft Grey (Divider lines, subtle card structures)

  typography:
    font-display: "Playfair Display, Georgia, serif" # Formal titles, heritage headers
    font-sans: "Inter, system-ui, sans-serif"        # Body copy, navigation, interface actions
    scale:
      h1: "2.5rem"    # 40px - Main Hero Headers
      h2: "2.0rem"    # 32px - Section Headings
      h3: "1.5rem"    # 24px - Sub-headings & Card titles
      body: "1.0rem"  # 16px - Base text
      sm: "0.875rem"  # 14px - Captions, tags, and footer notes

  spacing:
    base: "4px"
    scale:
      xs: "8px"    # Inline elements, labels
      sm: "16px"   # Internal card padding
      md: "24px"   # Standard layout gaps
      lg: "48px"   # Vertical section spacing
      xl: "80px"   # Large hero block boundaries

  radius:
    none: "0px"
    sm: "4px"      # Button corners, small tags
    md: "12px"     # Main UI cards, featured image frames

  shadows:
    subtle: "0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1)"
    card: "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)"
---

# Design Rationale & Execution Plan

## 1. Visual Identity & Mood
The interface bridges traditional national heritage with modern digital accessibility. It uses high-contrast typography and extensive white space to convey authority, elegance, and openness. Photography (landscapes, historical monuments, citizens) drives the visual narrative.

## 2. Core Layout & Components

### 🌐 Global Navigation (Header)
- **Structure:** Clean, fixed/sticky horizontal bar using standard text tokens (`font-sans`). Left-aligned national emblem or logo placeholder, followed by main navigation categories: *Discover, Culture, Travel, E-Services*.
- **Styling:** `background: surface`, `border-bottom: 1px solid border`. Links use `text-main` shifting to `primary-light` on hover. Include a country language selector dropdown on the top right.

### 🏔️ Hero Section (Welcome / Overview)
- **Layout:** Asymmetric split or full-bleed high-resolution regional backdrop image overlayed with a linear dark gradient overlay to ensure text legibility.
- **Typography:** Main hook uses `h1` (`font-display`) colored in `#FFFFFF` with primary value propositions.
- **Call-to-Action (CTA):** A primary button wrapped in `primary` blue with a sharp, premium corner execution (`radius: sm`).

### 🗺️ Interactive Discovery Grid (Cards)
- **Layout:** 3-column elastic grid showcasing curated highlights (e.g., Nature, History, Local Gastronomy).
- **Card Design:** Wrapped in `surface` color with a `shadows: card` structure and `radius: md`. Images inside cards fill the top section flawlessly with matching top-border radiuses.
- **Typography:** Titles feature `h3` (`font-sans`) bolded, metadata features `text-muted`.

### 🏛️ Heritage / Quick Facts Component
- **Structure:** A dedicated horizontal strip or minimalist text-heavy block showcasing crucial data callouts (e.g., Population, Currency, Capital, Time Zone).
- **Styling:** Large numeric stats should be amplified using `accent` color (Golden Sun) utilizing large weights to function as strong focal anchors.

## 3. Interactive Behaviors & States
- **Hover Transitions:** All anchor links and card components transition using `duration: 200ms ease-in-out`.
- **Card Hover:** Cards slightly elevate (`transform: translateY(-4px)`) and deepen their drop shadow to indicate interactive capability.
- **Focus Rings:** Accessible elements utilize `outline: 2px solid primary-light` with a 2px offset on keyboard focus.
