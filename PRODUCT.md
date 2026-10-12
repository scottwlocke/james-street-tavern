# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

People in and around Monroeville deciding where to eat or drink tonight. They arrive on a phone, mid-decision, and the job is to answer hours, menu, prices and directions fast enough to change where they go.

## Product Purpose

The website for James Street Tavern, a neighborhood tavern at 1224 James St, Monroeville, PA. It publishes the full menu, the rotating specials, opening hours and contact details so a prospective visitor can decide and then show up. Success is a visitor getting their answer — is it open, what's on, where is it — without having to call first.

## Positioning

The weeknight ritual. Monday Night Wings and Taco Tuesday give regulars a reason to come in on a Monday, and that offer-and-rhythm is what a neighboring Monroeville spot could not truthfully copy. The site carries it through `content/specials/`, which is deliberately kept outside the regular menu sections.

## Operating Context

- The site is read before the visit, not during it: the decision window is the same evening as the trip.
- Specials rotate and are published as limited-time offers; two are live today — Monday Night Wings and Taco Tuesday.
- Contact routes are the phone number (412-824-8884) and email (info@jst-tavern.com). There is no ordering, booking or messaging channel.
- Opening hours are a factual part of the product and carry equal weight with the menu: a visitor who can't tell whether the kitchen is open has failed the visit.

## Capabilities and Constraints

Confirmed:

- Informational by design. No online ordering, no reservations, no accounts, no delivery integration.
- Footer and nav links that still point to `#` are known placeholders awaiting real URLs — deliberate and tracked, not a defect.
- The menu is published as structured content: 8 menu sections, 46 items, plus 2 specials held outside the menu.
- Bar and Kitchen hours are currently recorded as identical. `hugo.toml` flags this as worth confirming against the real roster rather than assuming it — an undecided fact, not an established one.

Open decisions:

- Which placeholder links get real destinations first (map, social, phone) is not decided.

## Brand Commitments

- Name: James Street Tavern ("JST"), Monroeville, PA.
- Voice: friendly, direct, local. The house line is "Your Neighborhood Tavern" and "Come Hungry. Leave Happy."; hero copy promises no frills, no nonsense.
- `DESIGN.md` is the binding design authority for the site. Product work records facts here and does not redefine it.

## Evidence on Hand

- 46 dish photographs, one per menu item, as page-bundle resources under `content/`; homepage hero photograph at `assets/images/photo-tavern-hero.jpg`.
- The complete menu with prices written as `$12.00`-style strings throughout `content/`.
- Two specials: Monday Night Wings and Taco Tuesday, in `content/specials/`.
- Address, split schema.org address parts, coordinates, phone, email and opening hours in `hugo.toml` `[params]`.

Absent, and future work must not fabricate: testimonials, reviews, customer counts, press, awards, delivery or loyalty programs, years-in-business claims, capacity or catering terms, or any pricing not already in `content/`.

## Product Principles

1. Answer before persuading. Hours, menu, prices and directions come first; anything that delays them is a defect.
2. Mobile is the real surface. The decision happens on a phone, mid-evening, often on a weak signal.
3. The specials are product, not decoration. Weeknight offers are the differentiator and stay outside the regular menu.
4. Informational means informational. No ordering, booking or accounts until the scope question is explicitly revisited.
5. Nothing gets invented. Claims, testimonials and prices that are not in `content/` do not appear.
