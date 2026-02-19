# Semiotic Standard Font — Design Decisions

## Glyph Composition (Decided Feb 2025)

**Final font glyphs MUST include the Cobb border(s).**

The SVG conversion pipeline (`trace_v2.py`) extracts **symbol-only** artwork from the
hand-drawn source PNGs. The Cobb rounded-rectangle frame borders are composed
separately — not traced from the source images.

- `trace_v2.py` → isolates and traces the interior symbol pictogram only
- `step5_compose.py` composes the traced symbol into a standardized Cobb frame
- The final font glyph = Cobb frame + traced symbol (combined compound path)

## Tracer Choice: OpenCV over vtracer (Decided Feb 2026)

**Use OpenCV `findContours` + `approxPolyDP` for tracing, not vtracer.**

vtracer's polygon mode was too aggressive — it lost body width and shoulder shape on
simple icons like the bottle. OpenCV contour tracing with per-icon epsilon tuning gives
superior fidelity.

- Default epsilon: **1.3** (most icons)
- Exceptions at **1.1**: alcohol, emergency_rations, frozen_goods, rations
- Script: `scripts/trace_all.py` (batch), `scripts/cv_trace.py` (single/comparison)

## Crop Pipeline: Color-based Red Band Detection (Decided Feb 2026)

**Use the COLOR source image to detect Cobb frame boundaries, not grayscale brightness.**

The Cobb frame always contains a dark-red band (R>70, G<40, B<40) regardless of
interior color. Grayscale approaches failed on dark-background icons (frozen_goods,
hydroponic, etc).

Algorithm: find the innermost red band on each edge, then add INSET=15px to clear the
remaining white band + inner black ring. Script: `scripts/step1_extract.py`.

## Frame Geometry: Tight Outer Margin (Decided Feb 2026)

**The outer border ring must sit tight to the canvas edge (~10u margin on a 1000u canvas).**

Early versions used OUTER_X=50 (5% margin), which left too much dead black space outside
the ring. Pixel analysis of source PNGs showed the true outer margin is only 4–8px on a
228–240px source (≈8–35u at 1000u scale). Corrected to OUTER_X=10.

Ring thickness (outer edge to interior knockout) is ~80u, matching the bold visual weight
of the Cobb originals.

## Frame Geometry: Double Border Icons (Decided Feb 2026)

**Two icons use a double concentric border: `allergen_warning` only.**

Pixel scanning of all 16 source PNGs for red band count revealed:
- 15 icons: single red band → single border (2 subpaths: outer fill + interior knockout)
- 1 icon: double red band → double border (`allergen_warning`: 4 subpaths)
- `emergency_rations` initially appeared double-bordered but was reverted to single after
  visual review — the second band was a scan artifact.

The double border structure: outer fill → stripe knockout → inner ring fill → interior
knockout. Encoded in `step5_compose.py` as `DOUBLE_BORDER` dict and `DB_RECTS`.

## Per-Icon Corrections Table (Feb 2026)

| Icon | Issue | Fix |
|------|-------|-----|
| `allergen_warning` | Double Cobb border | `DOUBLE_BORDER` set in step5_compose.py |
| `protein` | Trace correct; source orientation confirmed | No flip needed (FLIP_H set is empty) |

## Font Build: Direct Pipeline over svgtofont (Decided Feb 2026)

**Use `build-font-direct.js` (direct svgicons2svgfont → svg2ttf chain), not svgtofont.**

`svgtofont` v4's wrapper layer had two fatal bugs:
1. Its CSS copy-template step crashed with `ERR_INVALID_ARG_TYPE` on Node v24 (non-fatal
   to font files but caused noisy failures)
2. More critically: the SVG font came out empty (0 glyphs) — svgtofont's internal glyph
   embedding silently failed on our compound evenodd paths

Root cause confirmed by testing `svgicons2svgfont` directly — it embedded glyphs correctly.
Solution: bypass svgtofont entirely and call the underlying libraries directly:
`svgicons2svgfont` → `svg2ttf` → `ttf2woff` → `ttf2woff2`, with CSS generated inline.

## Font Winding: SVG evenodd → Font nonzero (Decided Feb 2026)

**Font rasterizers use non-zero winding rule. Our composed SVGs use evenodd. A conversion
step (`step6_fix_winding.py`) is required between compose and font build.**

### Why evenodd fails in fonts

SVG supports `fill-rule="evenodd"` which alternates fill/hole by subpath index. Font
glyph renderers (FreeType, CoreText, DirectWrite) use the **non-zero winding rule** — a
path area is filled if the signed winding count is non-zero. Under non-zero winding, two
CW subpaths both fill; a CCW subpath inside a CW one creates a hole.

### Additional complication: Y-axis flip

`svgicons2svgfont` flips the Y axis when embedding glyphs (SVG Y increases downward;
font coordinate Y increases upward). This flip **reverses all winding directions**:
- CW in SVG → CCW in font coords → rendered as a **hole**
- CCW in SVG → CW in font coords → rendered as **filled**

This is counter-intuitive: to get a FILLED area in the font, the SVG subpath must be CCW.

### Winding rules applied in step6_fix_winding.py

Frame subpaths (first 2 for single border, first 4 for double border):
- Index 0 (outer fill): → CCW in SVG (fills after Y-flip)
- Index 1 (interior knockout): → CW in SVG (hole after Y-flip)
- Index 2 (inner ring fill, double only): → CCW in SVG
- Index 3 (inner interior, double only): → CW in SVG

Symbol subpaths (remainder, from OpenCV trace):
- OpenCV outer contours are CW in SVG Y-down → after Y-flip → CCW in font → **filled** ✓
- OpenCV hole contours are CCW in SVG Y-down → after Y-flip → CW in font → **hole** ✓
- Symbol subpaths are left unchanged — OpenCV's winding is already correct post-flip.

### Failed approaches

1. **Index-parity approach (v1)**: Reversed every odd-indexed subpath. Worked for simple
   icons but broke hydroponic and others where symbol subpaths have their own internal
   holes — the index parity assumed all subpaths nested cleanly, which they don't.

2. **Containment/depth approach (v2)**: Used ray-casting to compute nesting depth per
   subpath. Conceptually correct but broke most icons because all symbol subpaths are
   geometrically inside the outer frame rect (depth≥1), incorrectly marking them as holes.

3. **Frame-vs-symbol split (v3, current)**: Treat frame subpaths and symbol subpaths
   separately. Frame uses explicit CW/CCW assignment by slot. Symbol subpaths are left
   as-is (OpenCV winding is correct after font Y-flip). This correctly handles all 16 icons
   including hydroponic (11 subpaths, symbol has internal holes).

## Pipeline Status (Feb 2026) — COMPLETE for Food & Dining

| Step | Script | Output |
|------|--------|--------|
| 1. Extract + B&W + crop | `step1_extract.py` | `work/{name}_1_source.png` .. `_3_cropped.png` |
| 2. OpenCV trace | `trace_all.py` | `work/{name}_4_traced.svg` |
| 3. Normalize + compose Cobb frame | `step5_compose.py` | `svg/mono/extended/ss-{name}.svg` |
| 4. Fix winding for font | `step6_fix_winding.py` | `svg/mono/extended/ss-{name}.svg` (in-place) |
| 5. Build font | `build-font-direct.js` | `fonts/semiotic-standard.{ttf,woff,woff2,eot,svg}` |

All 16 Food & Dining glyphs shipped to `fonts/`. Unicode map: U+E001–U+E010.
