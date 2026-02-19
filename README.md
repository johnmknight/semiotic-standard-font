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
node scripts/build-font-direct.js   # Build TTF/WOFF/WOFF2/EOT from svg/mono/extended/
npm run build:duotone               # Tier 2 duotone fonts
npm run build:sprite                # Tier 3 SVG sprite sheet
npm run dev                         # Watch & rebuild on SVG changes
npm run test:mono                   # Monochrome differentiation QA
```

> **Note:** `npm run build:font` (svgtofont wrapper) is superseded by `build-font-direct.js`.
> svgtofont v4 silently produced empty glyphs on compound paths and crashes on Node v24.
> The direct pipeline calls `svgicons2svgfont` → `svg2ttf` → `ttf2woff` → `ttf2woff2` directly.

## Bitmap-to-SVG Pipeline (Food & Dining category)

Source icons are hand-drawn PNGs embedded in SVG wrappers in `from john/`. The full
pipeline converts them to font-ready vector glyphs:

| Step | Script | Output |
|------|--------|--------|
| 1. Extract PNG + B&W + crop Cobb border | `scripts/step1_extract.py` | `work/{name}_1–3.png` |
| 2. OpenCV contour trace | `scripts/trace_all.py` | `work/{name}_4_traced.svg` |
| 3. Normalize to 1000×1000 + compose Cobb frame | `scripts/step5_compose.py` | `svg/mono/extended/ss-{name}.svg` |
| 4. Fix path winding for font rasterizer | `scripts/step6_fix_winding.py` | `svg/mono/extended/ss-{name}.svg` (in-place) |
| 5. Build font | `scripts/build-font-direct.js` | `fonts/semiotic-standard.*` |

**Tracing:** ε=1.3 default; ε=1.1 for alcohol, emergency_rations, frozen_goods, rations.

**Frame geometry:** 1000×1000 canvas; outer ring at x=10 (tight to edge, matching Cobb
originals); ring thickness ~80u. `allergen_warning` uses a double concentric border.

**Winding fix:** SVG `fill-rule="evenodd"` is incompatible with font rasterizers (non-zero
winding). Additionally, `svgicons2svgfont` flips the Y-axis on embed, reversing all winding
directions. Step 4 corrects frame subpaths explicitly and leaves OpenCV symbol subpaths
unchanged (already correct after flip). See DECISIONS.md for full rationale and failed
approaches.

Preview pages: `preview/step3_review.html`, `preview/trace_review.html`,
`preview/source_vs_composed.html`, `preview/font-test.html`

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
