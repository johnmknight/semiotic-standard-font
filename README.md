# Semiotic Standard Webfont

Custom webfont based on Ron Cobb's **Semiotic Standard** iconography from the Alien franchise (1979–present), extended with additional icons from films, games, and comics across the franchise.

> *"In space, no one can hear you kern."*

## Overview

The Semiotic Standard is a set of pictographic icons originally designed by Ron Cobb in 1978 for Ridley Scott's *Alien* (1979). This project packages those icons — plus franchise extensions and custom additions — as a modern webfont with three rendering tiers:

| Tier | Method | Use Case |
|------|--------|----------|
| **Tier 1: Monochrome** | Standard webfont (`currentColor`) | Inline text, small UI, print, high-contrast |
| **Tier 2: Duotone** | Dual-layer CSS pseudo-elements | Dashboards, navigation panels, status indicators |
| **Tier 3: Full Color SVG** | Multi-color SVG sprite sheet | Kiosk displays, large format, immersive sci-fi UI |

## Icon Set

- **30 base icons** — Ron Cobb originals from the Nostromo
- **28 extended icons** — Gap analysis from franchise canon (Isolation, Prometheus, Moon, Romulus, Rogue Incursion)
- **Custom ArtemisOps icons** — Mission-specific additions

## Cobb Color System

| Color | Hex | Meaning |
|-------|-----|---------|
| Red | `#C0392B` | Danger, alert, access control, critical |
| Yellow | `#D4A017` | Active energy, systems, chemical |
| Blue | `#2471A3` | Cryogenic, cold, low thermal |
| White/Grey | `#ECEFF1` | Life support, habitable, neutral |
| Black | `#1A1A2E` | Vacuum, death, lethal environment |

## Usage

```html
<!-- Tier 1: Monochrome in text -->
<i class="ss-icon ss-airlock ss-red"></i>

<!-- Tier 2: Duotone on dashboard -->
<span class="ss-duo ss-red-frame">
  <i class="ss-frame ss-airlock-frame"></i>
  <i class="ss-symbol ss-airlock-sym"></i>
</span>

<!-- Tier 3: Full SVG on kiosk -->
<svg class="ss-icon-svg" width="96" height="96">
  <use href="sprite.svg#ss-airlock" />
</svg>
```

## Build

```bash
npm install
npm run build        # Full build: SVG optimize → fonts → CSS → sprite → preview
npm run build:font   # Tier 1 monochrome font only
npm run build:duotone # Tier 2 duotone fonts
npm run build:sprite  # Tier 3 SVG sprite sheet
npm run dev          # Watch & rebuild on SVG changes
npm run test:mono    # Monochrome differentiation QA
```

## Project Structure

```
semiotic-standard-font/
├── svg/
│   ├── mono/          # Monochrome combined glyphs
│   │   ├── base/      # Original 30 Cobb icons
│   │   └── extended/  # Additional franchise + custom icons
│   ├── frames/        # Duotone frame layers
│   ├── symbols/       # Duotone symbol layers
│   └── color/         # Full-color SVGs for Tier 3
├── fonts/             # Generated font files (WOFF2, WOFF, TTF, EOT)
├── css/               # Generated CSS + color utilities
├── sprites/           # Generated SVG sprite sheet
├── preview/           # Specimen HTML page
├── scripts/           # Build scripts
├── docs/              # Specification documents
├── svgo.config.js
├── package.json
└── README.md
```

## Licensing & Attribution

- **Ron Cobb** (1937–2020) — Original Semiotic Standard design (1978)
- **Brandon Gamm / The Noun Project** — Vector recreations
- **louh/semiotic-standard** — SVG source files (CC BY 4.0)
- **Jon McKellan / Creative Assembly** — Alien: Isolation extended icons (reference)
- **Boris Tovmasyan** — Design analysis and grid documentation

Font released under **SIL Open Font License 1.1** (OFL).
