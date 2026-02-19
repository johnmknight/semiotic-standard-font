# Semiotic Standard Webfont Build Specification

**For All Commercial Trans-Stellar Utility Lifter and Heavy Element Transport Spacecraft**

_Project Author: John M. Knight / Date: February 17, 2026 / Version: 1.1_

# 1. Project Overview
Create a custom webfont based on Ron Cobb’s Semiotic Standard iconography from the Alien franchise (1979–present), extended with additional icons from films, games, and comics across the franchise. The font will be usable as a standard web font via CSS @font-face, with each icon mapped to the Unicode Private Use Area (PUA) and accessible via CSS class names.

## 1.1 Goals
- Package all 30+ original Ron Cobb icons as a webfont (WOFF2, WOFF, TTF, EOT)
- Include extended icons from Alien: Isolation, Aliens (hexagonal variants), Prometheus, Romulus, and Rogue Incursion
- Provide a CSS framework with Cobb’s original color coding system
- Support both monochrome and multi-color rendering modes
- Ensure every icon is structurally distinguishable without color (monochrome-first design)
- Generate a specimen/preview HTML page for visual reference
- Support ligature input (e.g., typing "airlock" renders the icon)
- Create a reusable build pipeline: SVG source → webfont output
- License-compatible for use in personal projects (ArtemisOps, MarchogSystemsOps, etc.)

## 1.2 Target Usage
- ArtemisOps kiosk screens — status indicators, wayfinding, hazard warnings
- MarchogSystemsOps — sci-fi themed UI elements
- General web projects requiring sci-fi industrial iconography
- Offline-capable (locally hosted, no CDN dependency)

# 2. Source Material & References
## 2.1 Primary Source: Ron Cobb’s Original 30 Icons
Originally designed in 1978 for Ridley Scott’s Alien (1979). Published in Cobb’s art book Colorvision (1981). The icons use a consistent design language: rounded-rectangle frames with a separator line dividing a symbolic area from a content/label area.

## 2.2 Available SVG Source Repository
GitHub: louh/semiotic-standard
License: Creative Commons Attribution 4.0 International (CC BY 4.0). Contains all 30 original icons in SVG, PNG, and Affinity Design formats. Vector adaptations based on Brandon Gamm’s icons on The Noun Project.

## 2.3 Additional Source Repositories
GitHub: banastas/SemioticStandard.org — Additional vector recreations and reference material
FontStruct: "Nostromo Semiotic Standard Symbols LR" by sorenzen — Existing bitmap font with 30 symbols + extras
Behance: Boris (Baris) Tovmasyan — Detailed analysis of Cobb’s design grid, frame structure, and color system
Iconfactory: Dave Brasgalla’s iOS 7 grid adaptation — Useful for understanding modern icon grid alignment

## 2.4 Extended Icon Sources (Franchise)

| Source | Details | Icon Type |
| --- | --- | --- |
| Alien (1979) | 30 original square icons, Nostromo | Base set |
| Aliens (1986) | Hexagonal redesign by Cobb, Hadley’s Hope | Variant geometry |
| Alien: Isolation (2014) | Extended set by Jon McKellan (Creative Assembly), Sevastopol Station + USCSS Torrens | 50+ new icons |
| Prometheus (2012) | Ben Proctor concept art, additional unique symbols | Supplementary |
| Alien: Covenant (2017) | Semiotic Standard aboard USCSS Covenant | Continuity |
| Alien: Romulus (2024) | Includes unique icons like "Slippery when wet" | Extended |
| Alien: Rogue Incursion (2024) | Updated set matching original design/colors | Extended |
| Alien: Earth (2025) | FX Networks released 32 app icons as promotional content | App icon set |


# 3. Complete Icon Inventory
## 3.1 Base Set (Ron Cobb Original — 30 Icons)

| # | Name | Cobb Color | Category |
| --- | --- | --- | --- |
| 001 | Pressurised Area | White/Grey | Life Support |
| 002 | Pressurised with Artificial Gravity | White/Grey | Life Support |
| 003 | Artificial Gravity Absent | White/Grey | Life Support |
| 004 | Cryogenic Vault | Blue | Facilities |
| 005 | Airlock | Red/Black | Access/Hazard |
| 006 | Bulkhead Door | Red | Access |
| 007 | Non-Pressurised Area Beyond | Black | Hazard |
| 008 | Pressure Suit Locker | White/Grey | Equipment |
| 009 | Photonic System (Fibre Optics) | Yellow | Systems |
| 010 | Laser | Yellow | Systems/Hazard |
| 011 | Astronic System (Electronics) | Yellow | Systems |
| 012 | Hazard Warning | Red | Hazard |
| 013 | Artificial Gravity, Non-Pressurised, Suit Required | Black/White | Combined |
| 014 | No Pressure, Gravity, Suit Required | Black/White | Combined |
| 015 | Exhaust | Yellow/Red | Hazard |
| 016 | Area Shielded from Radiation | White/Grey | Safety |
| 017 | Radiation Hazard | Yellow | Hazard |
| 018 | High Radioactivity | Red/Yellow | Hazard |
| 019 | Refrigeration | Blue | Systems |
| 020 | Direction (Up) | Red | Wayfinding |
| 020A | Direction (Down) | Red | Wayfinding |
| 020B | Direction (Right) | Red | Wayfinding |
| 020C | Direction (Left) | Red | Wayfinding |
| 021 | Life Support System | Red/White | Life Support |
| 022 | Galley | White/Grey | Facilities |
| 023 | Coffee | White/Grey | Facilities |
| 024 | Bridge | Red | Facilities |
| 025 | Autodoc | Red/White | Medical |
| 026 | Maintenance | Yellow | Systems |
| 027 | Ladderway | White/Grey | Wayfinding |
| 028 | Intercom | Yellow | Communications |
| 029 | Storage, Non-Organic | Grey | Storage |
| 029A | Storage, Organic (Foodstuffs) | Grey/White | Storage |
| 030 | Computer Terminal | Yellow | Systems |


## 3.2 Extended Set (To Be Designed/Sourced)
These additional icons should be created in the Cobb design language (matching frame style, weight, and proportions) to extend the standard for modern usage. Sources include Alien: Isolation’s expanded set and custom additions for ArtemisOps.


| Category | Proposed Icons | Source/Notes |
| --- | --- | --- |
| Access & Security | Security Checkpoint, Emergency Exit, Quarantine Zone, Decontamination | Isolation + custom |
| Medical & Science | Medical Bay, Laboratory, Biohazard, Chemical Hazard, Quarantine | Isolation + Prometheus |
| Engineering | Engine Room, Reactor, Power Distribution, Fuel System, Hydraulics | Isolation + custom |
| Communications | Antenna/Comms Array, Data Terminal, Network Hub, Emergency Beacon | Custom for ArtemisOps |
| Crew & Living | Crew Quarters, Mess Hall, Recreation, Shower/Hygiene, Cargo Bay | Isolation |
| EVA & External | EVA Prep, Tether Point, External Access, Observation Deck, Docking Port | Custom for ArtemisOps |
| Environmental | Oxygen Level, Temperature Warning, Humidity, Fire Suppression, Ventilation | Isolation + custom |
| Navigation | Elevator/Lift, Stairway, Transit Hub, Level Indicator, Emergency Route | Isolation |
| Mission-Specific | Launch Pad, Mission Control, Telemetry, Countdown, Weather Station | Custom for ArtemisOps |


# 4. Multi-Color Strategy
Cobb’s color system carries semantic meaning — red signals danger/alert, yellow marks active energy processes, blue indicates cold/cryogenic, white/grey denotes habitable life-support areas, and black means vacuum/death. A standard webfont glyph is strictly monochrome (inherits currentColor), which flattens this entire information layer. This section defines the strategy for supporting both monochrome and color rendering across different usage contexts.

## 4.1 Core Principle: Monochrome-First Design
Every icon must be structurally distinguishable in pure monochrome. Color is an enhancement layer, never the sole differentiator between icons. This is both an accessibility requirement and a practical necessity — icons will appear monochrome in many contexts including plain text, small sizes, print, high-contrast modes, and screen readers that announce glyph names.

If two icons cannot be told apart when rendered in a single flat color at 24px on a white background, they need structural redesign before they enter the font. This is the litmus test applied to every glyph in the set.

## 4.2 Three Rendering Tiers
The font system supports three rendering modes, each suited to different contexts:


| Tier | Method | Use Case | Color Source |
| --- | --- | --- | --- |
| Tier 1: Monochrome | Standard webfont, single currentColor | Inline text, small UI indicators, print, high-contrast mode, plain backgrounds | Inherits from CSS color property |
| Tier 2: Duotone | Dual-layer CSS pseudo-elements (::before + ::after) | Medium UI elements, dashboards, navigation panels, status indicators | CSS classes apply Cobb color per layer |
| Tier 3: Full Color SVG | Multi-color SVG sprite sheet with <use> references | Kiosk displays, large format, immersive sci-fi interfaces, maximum Cobb fidelity | Colors baked into SVG fills |


## 4.3 Tier 2 Duotone Implementation
The duotone approach uses two Unicode codepoints per icon — one for the frame/border layer, one for the interior symbol layer. CSS composites them using stacked pseudo-elements. This is the same technique used by Font Awesome’s duotone icon set and is well-tested across browsers.

### 4.3.1 Glyph Layer Split
- Layer A (Frame): The outer rounded-rectangle border, separator line, and any structural frame elements. Typically rendered in the Cobb category color (red, yellow, blue, etc.)
- Layer B (Symbol): The interior pictographic symbol. Typically rendered in a contrasting color (white on dark backgrounds, dark on light backgrounds)
- Each layer is a separate glyph in the font, mapped to adjacent PUA codepoints

### 4.3.2 Unicode Mapping for Duotone

| Range | Layer | Example |
| --- | --- | --- |
| U+E001 – U+E0FF | Combined (monochrome, single glyph) | U+E005 = Airlock (complete icon) |
| U+E101 – U+E1FF | Frame layer only (duotone layer A) | U+E105 = Airlock frame |
| U+E201 – U+E2FF | Symbol layer only (duotone layer B) | U+E205 = Airlock interior symbol |


### 4.3.3 CSS Duotone Classes
/* Monochrome (Tier 1) — single glyph, inherits color */
.ss-icon { font-family: 'semiotic-standard'; font-style: normal; }
.ss-airlock::before { content: '\e005'; }

/* Duotone (Tier 2) — stacked layers */
.ss-duo { position: relative; display: inline-block; }
.ss-duo .ss-frame,
.ss-duo .ss-symbol {
font-family: 'semiotic-standard';
font-style: normal;
}
.ss-duo .ss-frame { color: var(--ss-frame-color); }
.ss-duo .ss-symbol {
position: absolute; left: 0; top: 0;
color: var(--ss-symbol-color);
}

/* Usage: */
/* <span class="ss-duo ss-red-frame">       */
/*   <i class="ss-frame ss-airlock-frame"></i> */
/*   <i class="ss-symbol ss-airlock-sym"></i>  */
/* </span>                                    */

/* Cobb color presets */
.ss-red-frame    { --ss-frame-color: #C0392B; --ss-symbol-color: #FFFFFF; }
.ss-yellow-frame { --ss-frame-color: #D4A017; --ss-symbol-color: #1A1A2E; }
.ss-blue-frame   { --ss-frame-color: #2471A3; --ss-symbol-color: #FFFFFF; }
.ss-white-frame  { --ss-frame-color: #ECEFF1; --ss-symbol-color: #1A1A2E; }
.ss-black-frame  { --ss-frame-color: #1A1A2E; --ss-symbol-color: #ECEFF1; }

## 4.4 Tier 3 SVG Sprite Implementation
For full Cobb-fidelity rendering (ArtemisOps kiosks, large format displays), generate a multi-color SVG sprite sheet alongside the font. Each icon is a <symbol> element with its authentic color fills:

<svg xmlns="http://www.w3.org/2000/svg" style="display:none">
<symbol id="ss-airlock" viewBox="0 0 1000 1000">
<rect class="ss-frame" fill="#C0392B" ... />
<path class="ss-symbol" fill="#000000" ... />
<rect class="ss-outline" fill="none" stroke="#FFFFFF" ... />
</symbol>
<!-- ... more symbols ... -->
</svg>

<!-- Usage -->
<svg class="ss-icon-svg" width="64" height="64">
<use href="#ss-airlock" />
</svg>

The SVG sprite file is generated as part of the build pipeline from the same source SVGs, with color data pulled from a mapping file (scripts/color-map.json) that assigns Cobb colors to each icon’s frame and symbol layers.

# 5. Monochrome Differentiation Guide
This section identifies icon families where Cobb’s originals rely on color to distinguish between related icons, and defines structural modifications to ensure each icon is uniquely identifiable in monochrome. These modifications must be subtle enough to feel native to Cobb’s design language — no gimmicks, just the kind of practical visual engineering a real spacecraft signage system would employ.

## 5.1 Category Badge System
To preserve the semantic layer that color normally carries, each icon receives a small corner badge indicating its Cobb color category. These badges are structural marks in the monochrome glyph that allow a trained user to identify the category without color. The badges are placed in the top-left corner of the frame, outside the separator line, and use the following shapes:


| Cobb Color | Badge Shape | Meaning | Placement |
| --- | --- | --- | --- |
| Red | Small solid triangle (pointing up) | Danger, alert, access control, critical | Top-left corner of frame |
| Yellow/Orange | Small solid diamond | Active energy process, systems, chemical | Top-left corner of frame |
| Blue | Small solid circle | Cryogenic, cold, low thermal | Top-left corner of frame |
| White/Grey | No badge (clean frame) | Life support, habitable, neutral | N/A — absence is the indicator |
| Black | Small solid square | Vacuum, death, lethal environment | Top-left corner of frame |


The badge is intentionally minimal — approximately 8% of the frame width, tucked into the corner radius. At small sizes (16–24px) it may not be individually legible, but at functional signage sizes (32px+) it provides an additional recognition cue. The badge system is optional and can be toggled in the build config; a "badged" and "unbadged" variant of each monochrome glyph can be generated.

## 5.2 Pressure / Gravity Family (Icons 001–003, 013–014)
Problem: These five icons share nearly identical frames and are primarily differentiated by fill color (white/grey for safe conditions, black for vacuum). In monochrome, icons 001, 002, and 003 are especially difficult to distinguish.


| Icon | Current Differentiator | Proposed Structural Modification |
| --- | --- | --- |
| 001 Pressurised Area | White/grey fill, simple dot pattern | Solid filled interior circle (representing contained atmosphere). Clean, unbroken frame. |
| 002 Pressurised + Gravity | White/grey fill, down arrow + dot | Solid filled interior circle with a downward arrow beneath it (gravity vector). Circle + arrow combination is unique. |
| 003 Gravity Absent | White/grey fill, crossed-out gravity | Dashed/broken interior circle (representing compromised containment). Add diagonal strike-through line across the gravity arrow area. |
| 013 Gravity, Non-Pressurised, Suit Required | Black/white combined fill | Human figure silhouette inside a dashed circle with downward arrow. The figure distinguishes it from 001–003. |
| 014 No Pressure, No Gravity, Suit Required | Black/white combined fill | Human figure silhouette inside a dashed circle with diagonal strike-through. Double negation (dashed + strike) makes it distinct. |


Design rule: Solid circle = pressurised. Dashed circle = non-pressurised. Arrow = gravity present. Strike-through = absent/negated. Human figure = suit required. These primitives combine unambiguously.

## 5.3 Radiation Family (Icons 016–018)
Problem: These three icons use the same trefoil radiation symbol and are distinguished primarily by color intensity (white/grey = shielded/safe, yellow = caution, red = danger). In monochrome they’re nearly identical.


| Icon | Current Differentiator | Proposed Structural Modification |
| --- | --- | --- |
| 016 Shielded from Radiation | White/grey fill (safe) | Small trefoil symbol enclosed within a shield outline (rounded rectangle or chevron shape). Shield = protection. Trefoil is visually contained/small. |
| 017 Radiation Hazard | Yellow fill (caution) | Standard trefoil symbol at medium weight, no enclosure. The "default" radiation icon that people recognize. |
| 018 High Radioactivity | Red fill (danger) | Large/bold trefoil filling most of the symbol area, with concentric emission rings radiating outward. Increased visual density = increased severity. |


Design rule: Escalating severity = escalating visual weight. Small/contained → medium/standard → large/radiating. The progression is readable at a glance even without color.

## 5.4 Storage Family (Icons 029, 029A)
Problem: Storage Non-Organic vs. Storage Organic (Foodstuffs) use similar container symbols differentiated by fill shade.


| Icon | Current Differentiator | Proposed Structural Modification |
| --- | --- | --- |
| 029 Storage, Non-Organic | Grey fill | Box/crate symbol with geometric contents (angular shapes suggesting machinery or materials) |
| 029A Storage, Organic | Grey/white fill | Box/crate symbol with organic contents (leaf or grain symbol inside the container) |


## 5.5 Systems Family (Icons 009, 010, 011)
Problem: Photonic System, Laser, and Astronic System are all yellow-category systems icons. They already have fairly distinct symbols but need verification at small monochrome sizes.


| Icon | Current Symbol | Monochrome Enhancement |
| --- | --- | --- |
| 009 Photonic System | Fibre optic wave pattern | Ensure wave pattern has sufficient stroke weight to render clearly at 24px. Add node dots at wave peaks. |
| 010 Laser | Focused beam symbol | Ensure beam convergence point is sharp and distinct from the broader wave of 009. Add small target/crosshair at focal point. |
| 011 Astronic System | Circuit/electronics symbol | Ensure angular/geometric lines are distinct from the organic curves of 009. Emphasize right angles. |


## 5.6 General Monochrome Design Rules
Apply these rules to all icons in the set, both base and extended:

- Minimum stroke weight: 60 units (out of 1000-unit canvas) for any visible path. Below this, strokes disappear at small render sizes.
- Minimum counter space: 40 units between any two parallel strokes. Below this, counters collapse into solid fills at small sizes.
- No details smaller than 80 x 80 units. Any element below this threshold is unreadable at 24px render size and should be simplified or removed.
- Optical weight balancing: Icons with more internal detail should have slightly thinner frames; icons with simple interiors should have slightly heavier frames. This normalizes perceived weight across the set.
- Test every icon at 16px, 24px, 32px, 48px, and 64px in monochrome on both white and dark (#1A1A2E) backgrounds. All must be identifiable at 24px.
- Silhouette test: When fully filled to a solid silhouette (all detail removed), the outer contour of each icon should still be distinct from every other icon in the same category.
- Avoid relying on interior fill density alone (e.g., solid vs. half-filled vs. empty versions of the same shape). Add structural elements instead.

# 6. Design Specifications
## 6.1 Cobb’s Design System
All icons follow a strict structural grid as documented by Boris Tovmasyan’s analysis of Cobb’s original graph-paper sketches:

- Frame: Rounded rectangle with consistent corner radius and stroke weight
- Separator line: Horizontal divider approximately 1/3 from the top, creating a label zone above and a symbol zone below
- Frame interruptions: Some icons intentionally break the frame (e.g., Exhaust, Direction arrows)
- White outline: All icons should be outlined in white when appearing on dark or colored backgrounds
- Grid: Originally drawn on graph paper; icons should maintain pixel-grid alignment for crisp rendering

## 6.2 Color System
Cobb defined a specific color coding system. In the monochrome webfont (Tier 1), glyphs are single-color via currentColor. In duotone (Tier 2) and SVG (Tier 3) modes, the full color system is applied via CSS classes or SVG fills.


| Color | Hex Value | Meaning |
| --- | --- | --- |
| Red | #C0392B | Viable, alive, sound, alert — danger, access control, critical systems |
| White/Grey | #ECEFF1 / #90A4AE | Life-supporting condition: pressure, temperature, habitable areas |
| Black | #1A1A2E | Vacuum, death, hazard — non-pressurised, lethal environments |
| Yellow/Orange | #D4A017 | Harmful active process: molecular (heat), atomic, chemical, energy systems |
| Blue | #2471A3 | Lowered thermal condition: cryogenics, refrigeration, cold storage |


## 6.3 Font Metrics & SVG Preparation
- Canvas size: 1000 x 1000 units (standard for icon fonts)
- Icon safe area: 100-unit padding on all sides (800 x 800 active area)
- Stroke: Convert all strokes to filled paths (outlined) before font generation
- Colors: All SVGs must be single-color (black fills only) — no gradients, no multi-color
- Paths: Clockwise winding for fills, no overlapping paths (union/merge compound shapes)
- Viewbox: Consistent viewBox="0 0 1000 1000" on all source SVGs
- Naming: Filenames become glyph names: ss-airlock.svg → .ss-airlock CSS class
- Layer variants: For duotone, create ss-airlock-frame.svg and ss-airlock-sym.svg alongside the combined ss-airlock.svg

# 7. Technical Build Pipeline
## 7.1 Project Structure
semiotic-standard-font/
├── svg/
│   ├── mono/                # Monochrome combined glyphs
│   │   ├── base/            # Original 30 Cobb icons
│   │   └── extended/        # Additional franchise + custom icons
│   ├── frames/              # Duotone frame layers only
│   ├── symbols/             # Duotone symbol layers only
│   └── color/               # Full-color SVGs for Tier 3 sprite
├── fonts/                   # Generated font files (WOFF2, WOFF, TTF, EOT)
├── css/                     # Generated CSS + color utility classes
├── sprites/                 # Generated SVG sprite sheet
├── preview/                 # Specimen HTML page
├── scripts/
│   ├── build-font.js        # svgtofont config & runner
│   ├── build-sprite.js      # SVG sprite generator
│   ├── build-css.js         # CSS color utilities generator
│   └── color-map.json       # Icon → Cobb color category mapping
├── svgo.config.js
├── package.json
└── README.md

## 7.2 Build Tool: svgtofont
The primary build tool is svgtofont (npm package). It reads a directory of SVG files and generates TTF, WOFF, WOFF2, EOT, and SVG font files along with CSS, Less, Sass, and Stylus stylesheets. It also generates an HTML preview page.

## 7.3 Build Configuration
Key configuration for the svgtofont build script (scripts/build-font.js):

const svgtofont = require('svgtofont');
const path = require('path');

// Build monochrome font (Tier 1)
svgtofont({
src: path.resolve(__dirname, '../svg/mono'),
dist: path.resolve(__dirname, '../fonts'),
fontName: 'semiotic-standard',
css: true,
startUnicode: 0xE001,
svgicons2svgfont: { fontHeight: 1000, normalize: true },
website: { title: 'Semiotic Standard' }
});

// Build duotone font (Tier 2, frames + symbols)
svgtofont({
src: path.resolve(__dirname, '../svg/frames'),
dist: path.resolve(__dirname, '../fonts/duotone'),
fontName: 'semiotic-standard-frames',
css: true,
startUnicode: 0xE101,
svgicons2svgfont: { fontHeight: 1000, normalize: true },
});
svgtofont({
src: path.resolve(__dirname, '../svg/symbols'),
dist: path.resolve(__dirname, '../fonts/duotone'),
fontName: 'semiotic-standard-symbols',
css: true,
startUnicode: 0xE201,
svgicons2svgfont: { fontHeight: 1000, normalize: true },
});

## 7.4 Unicode Mapping Strategy
All glyphs are mapped to the Unicode Private Use Area to avoid conflicts with standard characters:


| Range | Assignment |
| --- | --- |
| U+E001 – U+E01E | Base set monochrome icons 001–030 (Cobb originals) |
| U+E020 – U+E02F | Direction variants and combined icons |
| U+E030 – U+E05F | Alien: Isolation extended set |
| U+E060 – U+E07F | Hexagonal variants (Aliens 1986) |
| U+E080 – U+E09F | Custom ArtemisOps icons |
| U+E0A0 – U+E0FF | Reserved for future expansion |
| U+E101 – U+E1FF | Duotone frame layers (Tier 2) |
| U+E201 – U+E2FF | Duotone symbol layers (Tier 2) |


## 7.5 CSS Output
The build generates CSS with @font-face declarations and individual icon classes. A supplementary color utility stylesheet applies Cobb’s color system. See Section 4.3.3 for the duotone CSS pattern.

/* Base font-face (Tier 1) */
@font-face {
font-family: 'semiotic-standard';
src: url('./semiotic-standard.woff2') format('woff2'),
url('./semiotic-standard.woff') format('woff');
}

/* Monochrome icon classes */
.ss-icon { font-family: 'semiotic-standard'; font-style: normal; }
.ss-airlock::before { content: '\e005'; }
.ss-bridge::before { content: '\e018'; }

/* Cobb color utilities */
.ss-red    { color: var(--ss-red, #C0392B); }
.ss-white  { color: var(--ss-white, #ECEFF1); }
.ss-black  { color: var(--ss-black, #1A1A2E); }
.ss-yellow { color: var(--ss-yellow, #D4A017); }
.ss-blue   { color: var(--ss-blue, #2471A3); }

# 8. SVG Preparation Workflow
Before SVGs can be converted to a font, they must be normalized. Fonts only support filled paths, not strokes, gradients, or multi-color elements. For the duotone system, each icon requires three SVG files: combined, frame-only, and symbol-only.

## 8.1 Steps for Each SVG
- Set viewBox to "0 0 1000 1000" and remove width/height attributes
- Convert all strokes to filled paths (Object > Path > Stroke to Path in Inkscape, or Expand Stroke in Illustrator)
- Union/merge all overlapping compound shapes into single paths
- Set all fills to black (#000000), remove all color attributes
- Remove any gradients, patterns, filters, masks, clip-paths
- Ensure all paths wind clockwise (counter-clockwise causes inverted fills)
- Run through SVGO for optimization (remove metadata, editor cruft, unnecessary attributes)
- Name file according to convention: ss-[icon-name].svg (e.g., ss-airlock.svg)
- For duotone: create ss-[name]-frame.svg (frame paths only) and ss-[name]-sym.svg (symbol paths only)
- Verify monochrome differentiation: render at 24px and confirm unique silhouette vs. all family members

## 8.2 SVGO Configuration
Include an svgo.config.js in the project root:

module.exports = {
plugins: [
'removeDoctype', 'removeXMLProcInst', 'removeComments',
'removeMetadata', 'removeEditorsNSData', 'cleanupAttrs',
'convertPathData', 'mergePaths', 'removeEmptyContainers',
{ name: 'removeAttrs', params: { attrs: '(fill|stroke)' } }
]
};

# 9. Specimen Page Requirements
The build should auto-generate an HTML specimen page (preview/index.html) that displays all icons with their metadata. This serves as both documentation and a visual QA tool.

## 9.1 Specimen Page Features
- Dark background (matching Nostromo interior aesthetic, e.g., #1A1A2E)
- Grid layout showing each icon at multiple sizes (24px, 32px, 48px, 64px, 96px)
- Each icon card shows: rendered glyph, icon name, CSS class, Unicode codepoint, Cobb color category
- Filter/search by name or category
- Toggle between Tier 1 (monochrome), Tier 2 (duotone), and Tier 3 (full SVG) rendering modes
- Copy-to-clipboard for CSS class name and Unicode value
- Section dividers between Base Set and Extended Set
- Monochrome QA mode: forces all icons to single flat color for differentiation testing
- Responsive layout for desktop and tablet viewing

# 10. Integration Notes
## 10.1 ArtemisOps Integration
The webfont should be hosted locally in the ArtemisOps static assets directory for offline kiosk support (consistent with the existing Tabler Icons and Space Mono/IBM Plex Sans local hosting approach). The kiosk screens will primarily use Tier 2 (duotone) or Tier 3 (SVG) rendering for maximum visual impact on dark backgrounds.

<!-- Tier 1: Monochrome in text -->
<link rel="stylesheet" href="/static/fonts/semiotic-standard/semiotic-standard.css">
<p>Airlock status: <i class="ss-icon ss-airlock ss-red"></i> SEALED</p>

<!-- Tier 2: Duotone on dashboard -->
<span class="ss-duo ss-red-frame">
<i class="ss-frame ss-airlock-frame"></i>
<i class="ss-symbol ss-airlock-sym"></i>
</span>

<!-- Tier 3: Full SVG on kiosk -->
<svg class="ss-icon-svg" width="96" height="96">
<use href="/static/fonts/semiotic-standard/sprite.svg#ss-airlock" />
</svg>

## 10.2 CSS Custom Properties
The color system is exposed as CSS custom properties for theming flexibility:

:root {
--ss-red: #C0392B;
--ss-white: #ECEFF1;
--ss-black: #1A1A2E;
--ss-yellow: #D4A017;
--ss-blue: #2471A3;
--ss-grey: #90A4AE;
}

/* Dark theme override example */
[data-theme="nostromo"] {
--ss-white: #B0BEC5;
--ss-grey: #607D8B;
}

# 11. Build Commands


| Command | Description |
| --- | --- |
| npm run build | Full build: clean, optimize SVGs, generate all tiers + preview |
| npm run build:svg | Optimize SVGs with SVGO only |
| npm run build:font | Generate Tier 1 monochrome font files |
| npm run build:duotone | Generate Tier 2 duotone font files (frames + symbols) |
| npm run build:sprite | Generate Tier 3 full-color SVG sprite sheet |
| npm run build:css | Generate CSS with color utilities + duotone classes |
| npm run build:preview | Generate specimen HTML page with all three tiers |
| npm run dev | Watch SVG directory, rebuild on changes |
| npm run test:mono | Render all icons at 24px monochrome, generate QA sheet |
| npm run clean | Remove all generated files |


# 12. Licensing & Attribution
The original Semiotic Standard icons were created by Ron Cobb (1937–2020) for the 1979 film Alien. The louh/semiotic-standard SVG recreations are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).

## 12.1 Required Attribution
- Ron Cobb — Original Semiotic Standard design (1978)
- Brandon Gamm / The Noun Project — Vector recreations
- louh/semiotic-standard — SVG source files (CC BY 4.0)
- Jon McKellan / Creative Assembly — Alien: Isolation extended icons (reference only)
- Boris Tovmasyan — Design analysis and grid documentation

## 12.2 Font License
The generated webfont should be released under SIL Open Font License 1.1 (OFL), which is compatible with the CC BY 4.0 source material and allows free use, modification, and redistribution with attribution.

# 13. Phased Delivery Plan

## Phase 1: Foundation + Monochrome
- Set up project scaffolding (package.json, directory structure, build scripts)
- Download and normalize the 30 base SVGs from louh/semiotic-standard
- Apply monochrome differentiation modifications (Section 5) to ambiguous icon families
- Implement svgtofont build pipeline for Tier 1 monochrome font
- Generate initial font files (WOFF2, WOFF, TTF)
- Generate base CSS with @font-face and icon classes
- Run monochrome QA: verify all icons distinguishable at 24px
- Create specimen page with dark theme (monochrome mode only)

## Phase 2: Duotone + Color System
- Split each icon into frame and symbol SVG layers
- Build Tier 2 duotone font (frame font + symbol font)
- Implement Cobb color utility CSS classes + CSS custom properties
- Build Tier 3 SVG sprite sheet with full color fills
- Create color-map.json mapping each icon to its Cobb color category
- Enhance specimen page with Tier 1/2/3 toggle and duotone preview
- Add category badge variants (badged vs. unbadged monochrome glyphs)

## Phase 3: Extended Set + Polish
- Design and create extended icons following Cobb’s design system + monochrome rules
- Prioritize ArtemisOps-specific icons (Mission Control, Telemetry, Launch Pad, etc.)
- Add Alien: Isolation reference icons where licensing allows
- Implement ligature support in build config
- Add specimen page features: search/filter, copy-to-clipboard, size toggles
- Integrate into ArtemisOps static assets (all three tiers)
- Update documentation and README

END OF SPECIFICATION
"In space, no one can hear you kern."