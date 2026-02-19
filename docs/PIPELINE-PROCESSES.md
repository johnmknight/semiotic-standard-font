# Semiotic Standard — Pipeline Processes

**Contents:** Process 1: Bitmap to SVG Glyph | Process 2: SVG to Font | Process 3: Technical Lessons & Anti-Patterns
Document Version 2.0  //  February 2025
John M. Knight Publishing LLC

# PROCESS 1: Bitmap to SVG Glyph
This document describes the automated pipeline that converts hand-drawn Cobb icon bitmaps into clean, normalized vector SVG files suitable for font compilation. The pipeline is implemented in trace_v2.py.
## 1.1 Input
Each source file is an SVG wrapper containing a base64-encoded PNG image of a complete Cobb Semiotic Standard sign. The PNGs are approximately 200×200 pixels and show the full icon including frame borders, colored label panel, text, separator line, and interior symbol.
Source location: from john/[icon_name].svg
Format: SVG with embedded data:image/png;base64,... in an image href attribute
## 1.2 Output

| Output | Path | Description |
| --- | --- | --- |
| Mono SVG | svg/mono/ss-[name].svg | Raw vtracer output with original coordinates |
| Extended SVG | svg/mono/extended/ss-[name].svg | Normalized to 1000×1000 viewBox, 90% fill, compound path with evenodd fill rule |

## 1.3 Debug Output

| File | Description |
| --- | --- |
| preview/debug/[name]_symbol_crop.png | Cropped region showing just the extracted symbol area |
| preview/debug/[name]_bw.png | Black and white thresholded image fed to vtracer |
| preview/debug/[name]_traced.svg | Raw vtracer SVG output before normalization |

Always check debug output: These intermediate files are essential for diagnosing pipeline failures. If a glyph looks wrong, check the _symbol_crop.png first (was it cropped correctly?), then _bw.png (was the threshold right?), then _traced.svg (did vtracer produce clean paths?).
## 1.4 Pipeline Steps
### Step 1: PNG Extraction
The base64-encoded PNG data is extracted from the SVG wrapper using regex pattern matching, decoded, and loaded as an RGB PIL Image.
pattern: href="data:image/png;base64,([^"]+)"
Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB')
The RGB conversion discards any alpha channel, as the source PNGs have solid backgrounds.
### Step 2: Cobb Border Crop (Color-Based Detection)
The Cobb frame is detected using the COLOR source image, not grayscale brightness. All Cobb frames contain a distinctive dark-red band (R>70, G<40, B<40) regardless of the icon's interior color. This works on both light-background and dark-background icons (frozen_goods, hydroponic, etc.) where grayscale brightness approaches failed.

Algorithm (scripts/step1_extract.py):
1. Scan inward from each edge using the center-50% strip of the color image
2. Detect rows/cols where >5% of pixels match the dark-red frame signature
3. Find the last such row/col before 5 consecutive non-red rows (= past the red band)
4. Add INSET=15px to clear the remaining white band and inner black border ring

Outputs: work/{name}_1_source.png (extracted), work/{name}_2_bw.png (B&W), work/{name}_3_cropped.png (cropped).

Preview: preview/step3_review.html shows source vs cropped for all 16 icons.
Why 10+ consecutive rows: The thin bright bands within the frame border structure are only 1-3 rows wide. The actual interior content area has sustained brightness across many rows. This threshold distinguishes frame artifacts from real content.
Why brightness 160: The symbol area backgrounds are typically 240+ RGB. The label panels are colored (red/green/blue) at various brightness levels. A threshold of 160 catches even the brighter colored panels while rejecting the dark frame borders.
### Step 3: Symbol Isolation
Within the detected interior region, the pipeline must separate the symbol pictogram from the label text area above it:
1. Calculate background brightness (median of pixels above 200)
2. Set adaptive threshold: background brightness minus 50
3. Create symbol mask: all pixels darker than threshold
4. Compute row density (symbol pixels per row)
5. Find the largest vertical gap in the top 60% — this separates label from pictogram
6. Crop to tight bounding box of symbol pixels below the gap, with 5px padding
Known failure mode: When the label text and symbol are close together (no clear brightness gap), the gap detection fails. Workaround: increase padding or use manual separator position override per icon.
### Step 4: Threshold to Black & White
The cropped symbol region is converted to pure black and white using the per-icon adaptive threshold. Pixels darker than threshold become black (symbol); brighter become white (background). The threshold typically falls between 180-200.
Critical: The threshold is per-icon because source PNGs have different brightness characteristics. A global threshold produces poor results on icons with lighter or darker symbol artwork.
### Step 5: Vector Tracing (OpenCV)

| Parameter | Value | Purpose |
| --- | --- | --- |
| colormode | binary | Two-color mode for B&W input |
| mode | polygon | Polygon tracing for filled shapes |
| filter_speckle | 4 | Remove noise dots smaller than 4 pixels |
| corner_threshold | 60 | Angle threshold for sharp corners vs curves |
| length_threshold | 4.0 | Minimum path segment length |
| splice_threshold | 45 | Angle for splicing adjacent segments |
| path_precision | 2 | Decimal precision for path coordinates |

OpenCV findContours + approxPolyDP is used instead of vtracer. vtracer's polygon mode was rejected because it lost critical shape information (body width, shoulder curves) even at conservative settings.

Script: scripts/trace_all.py

Settings:
  cv2.findContours(binary, RETR_CCOMP, CHAIN_APPROX_NONE)
  cv2.approxPolyDP(contour, epsilon, closed=True)
  fill-rule: evenodd (handles holes correctly)

Per-icon epsilon values (Feb 2026):
  epsilon=1.3 (default): allergen_warning, beverage_dispenser, contaminated, food_heating,
                         fresh_produce, grain, hydroponic, organic_waste, potable_water,
                         protein, utensils, water_filtration
  epsilon=1.1 (more detail): alcohol, emergency_rations, frozen_goods, rations

Output: work/{name}_4_traced.svg — single compound path, black fill, evenodd rule.

Comparison tools: preview/cv_compare.html, preview/eps_compare.html, preview/flagged_compare.html
Alternative (potrace): Simpler tool, works via CLI: potrace input.bmp -s -o output.svg --flat --turdsize 100 --opttolerance 0.2. Better for clean silhouettes; vtracer better for complex compound paths.
### Step 6: Normalization + Cobb Frame Composition
The traced symbol SVG is normalized to a 1000×1000 viewBox and composed with a programmatically generated Cobb border frame (script: step5_compose.py):
1. Extract all path elements from the traced SVG
2. Calculate bounding box of all path coordinates
3. Compute uniform scale factor to fill active area (preserving aspect ratio)
4. Center the scaled symbol inside the Cobb frame interior
5. Generate Cobb frame subpaths (rounded rect outer + interior knockout)
6. Combine frame + symbol subpaths into a single compound path with fill-rule="evenodd"
Frame geometry: 1000×1000 canvas; outer ring OUTER_X=10 (tight to edge, matches Cobb source proportions); ring thickness ~80u. allergen_warning uses double concentric border (4 subpaths). Per-icon correction table: FLIP_H set (currently empty) and DOUBLE_BORDER dict in step5_compose.py.
Output: svg/mono/extended/ss-{name}.svg — a composed glyph ready for winding correction and font build.

## 1.5 Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Symbol too small in viewBox | Over-aggressive cropping removes symbol edges | Increase padding in crop_symbol_only() from 5px to 10px; reduce threshold |
| Frame border remnants in glyph | Interior bounds detection not finding all borders | Adjust sustained brightness threshold (>160) or minimum run length (10) |
| Label text appearing in symbol | Gap detection failing for this icon | Check row density in debug; use manual separator override |
| Holes filled solid (no cutouts) | Missing evenodd fill rule | Ensure normalize_svg() outputs fill-rule="evenodd" |
| Glyph appears blank/tiny | vtracer found no black paths | Check B&W threshold image; threshold may be wrong |
| Speckle noise in glyph | filter_speckle too low | Increase filter_speckle from 4 to 6 or 8 |


# PROCESS 2: SVG to Font
The composed symbol SVGs in svg/mono/extended/ are compiled into production webfont files using a direct pipeline (scripts/build-font-direct.js) that bypasses the svgtofont wrapper.
## 2.1 Input Requirements
• File name pattern: ss-[icon-name].svg (ss- prefix and .svg extension stripped for glyph name)
• ViewBox: 0 0 1000 1000
• Content: filled paths only (NO strokes, NO gradients, NO images, NO text elements)
Fill rule: evenodd in SVG source (converted to nonzero in step6_fix_winding.py before font build — see section 2.2)
• Single color: all paths use default fill (black) or explicit fill="#000000"
## Step 1 (step6_fix_winding.py): Convert SVG evenodd paths to font-compatible nonzero winding. Corrects frame subpaths explicitly; leaves OpenCV symbol subpaths unchanged (already correct after svgicons2svgfont Y-flip). See Process 3 section 3.9 for full rationale.
Step 2 (build-font-direct.js):
const svgicons2svgfont = require('svgicons2svgfont');
const svg2ttf           = require('svg2ttf');
const ttf2woff          = require('ttf2woff');
const ttf2woff2         = require('ttf2woff2');

// Collect svg/mono/extended/ss-*.svg, assign unicode U+E001+
// svgicons2svgfont stream → SVG font → svg2ttf → TTF → ttf2woff → WOFF
//                                                   → ttf2woff2 → WOFF2
// CSS and unicode map JSON generated inline.

Why not svgtofont: svgtofont v4 silently produced empty glyphs (0 embedded) on compound paths and its CSS copy-template step crashes on Node v24 with ERR_INVALID_ARG_TYPE. svgicons2svgfont tested directly embedded glyphs correctly. Solution: call underlying libraries directly without the broken wrapper layer.

Output files: fonts/semiotic-standard.{svg,ttf,woff,woff2,eot} + css/semiotic-standard.css + fonts/semiotic-standard.json (unicode map)
## 2.3 Unicode Mapping

| Range | Assignment |
| --- | --- |
| U+E001 – U+E01E | Base set monochrome icons (Cobb originals) |
| U+E020 – U+E02F | Direction variants and combined icons |
| U+E030 – U+E05F | Alien: Isolation extended set |
| U+E060 – U+E07F | Hexagonal variants (Aliens 1986) |
| U+E080 – U+E09F | Custom ArtemisOps icons |
| U+E0A0 – U+E0FF | Reserved for future expansion |
| U+E101 – U+E1FF | Duotone frame layers (Tier 2) |
| U+E201 – U+E2FF | Duotone symbol layers (Tier 2) |

## 2.4 Common Issues

| Issue | Solution |
| --- | --- |
| Glyph appears blank | Check SVG has filled paths (not strokes). svgtofont ignores stroke-only elements. |
| Glyph appears tiny | Ensure viewBox is 0 0 1000 1000 and paths fill the space. Check normalize: true. |
| Glyph has wrong cutouts | Verify fill-rule="evenodd" on compound paths. |
| Font not updating in browser | Browser caches fonts. Add cache-busting ?v=N to font URL. |
| CSS classes not matching | svgtofont derives names from filenames. Ensure ss-[name].svg pattern. |
| Chrome won't load font | file:// URLs blocked by CORS. Serve via localhost HTTP server. |

Common issue: Glyphs appear as solid filled squares (no visible symbol or border ring). Cause: fill-rule="evenodd" not respected by font rasterizer under non-zero winding rule. Fix: run step6_fix_winding.py before font build.

Common issue: Font renders inverted (symbol filled where it should be hole and vice versa). Cause: svgicons2svgfont flips Y-axis on embed, reversing winding. The frame subpaths need CCW for filled areas and CW for holes (opposite of SVG convention). Fix: step6_fix_winding.py handles this correctly — do not adjust frame winding manually without understanding the flip.
# PROCESS 3: Technical Lessons & Anti-Patterns
This section captures patterns and anti-patterns discovered across multiple development sessions. These should inform any future Claude skill for icon-to-font pipelines.

## 3.1 Anti-Pattern: Building Without Validating Format Constraints
What happened: Built an entire SVG-to-webfont pipeline before testing whether the source icons survived conversion to monochrome. The Cobb Semiotic Standard relies on color for semantic differentiation. Stripping color made many icons indistinguishable.
Rule: Always test source material in the target format's constraints (single color, no gradients, fixed size) BEFORE building the pipeline. Create a proof-of-concept with 3-5 representative icons first.

## 3.2 Anti-Pattern: Tight Cropping Without Safety Margins
What happened: The symbol isolation step cropped tightly to the bounding box of detected symbol pixels. Edge pixels near the threshold boundary were sometimes excluded, resulting in clipped artwork.
Rule: Use generous padding (10px minimum) on all crop operations. It's better to include a few pixels of background than to clip artwork. The normalization step will center the result anyway.

## 3.3 Anti-Pattern: Global Thresholds for Variable Input
What happened: Early attempts used a fixed brightness threshold for B&W conversion. Icons with lighter or darker artwork produced poor results (too much or too little detected as symbol).
Rule: Always compute per-image adaptive thresholds. Median brightness of the background region minus a fixed offset (50) works well for this type of icon artwork.

## 3.4 Pattern: Debug Image Pipeline
What works: Saving intermediate images at every pipeline stage (source extract, crop, B&W threshold, traced SVG) with predictable filenames. When a glyph looks wrong, you can inspect each stage to find exactly where the process broke.
Rule: Every image processing pipeline should save debug intermediates by default. The disk cost is trivial; the debugging time savings are enormous.

## 3.5 Pattern: Conservative Approach for Compound Paths
What works: Using evenodd fill rule on all compound paths, even those that don't appear to need it. Missing evenodd causes subtle bugs (holes that should be empty render solid) that are hard to diagnose.
Rule: Default to fill-rule="evenodd" for all compound paths in icon fonts. The cost of using it unnecessarily is zero; the cost of not using it when needed is a broken glyph.

## 3.6 Pattern: WSL as Windows Node.js Fallback
What works: When Node.js isn't in the Windows PATH, WSL Ubuntu typically has it. Files can be accessed via /mnt/c/ paths. The workflow is: 'wsl bash -c "cd /tmp && npm init -y && npm install [tool] && npx [tool] /mnt/c/Users/.../input -o /mnt/c/Users/.../output"'
Rule: Check Windows Node.js first (where.exe node), then fall back to WSL (wsl node --version). Copy files to /tmp/ for faster WSL processing, then copy results back to /mnt/c/.

## 3.7 Pattern: Font Preview via Localhost
What works: Serving the preview HTML through a running local HTTP server (python -m http.server, or an existing project dev server like ArtemisOps on localhost:8080).
What doesn't work: Opening font preview HTML via file:// URLs — Chrome blocks webfont loading due to CORS. Also: trying to open local files via explorer.exe from PowerShell doesn't always trigger the browser.
Rule: Always verify a localhost HTTP server is running before attempting font preview. If the project has a dev server, use its URL path to the preview page.

"In space, no one can hear you kern."

3.9 Anti-Pattern: Assuming evenodd Works in Icon Fonts
What happened: SVG compound paths using fill-rule="evenodd" render correctly as SVGs in the browser (symbol on white background inside ring, ring on black). When embedded in a font via svgicons2svgfont, the glyph renders as a solid white square — no visible ring or symbol. The font rasterizer (FreeType/CoreText/DirectWrite) uses the non-zero winding rule, not evenodd. Under non-zero winding, two CW subpaths both fill; only a CCW subpath inside a CW one creates a hole.
Rule: Always convert evenodd compound paths to nonzero-compatible winding before building a font. This is a separate required pipeline step, not something svgicons2svgfont handles. See step6_fix_winding.py.
3.10 Anti-Pattern: Ignoring Y-Axis Flip in Font Embedding
What happened: After implementing winding correction, most icons rendered but the border ring appeared filled (solid) while the symbol interior appeared as a hole — completely inverted from expected. The winding fix had assigned CW=fill and CCW=hole following SVG convention, but svgicons2svgfont flips the Y-axis when embedding (SVG Y increases downward; font coordinate Y increases upward). This flip reverses all winding directions: CW in SVG becomes CCW in font coords (rendered as a hole); CCW in SVG becomes CW in font coords (rendered as filled).
Rule: When targeting svgicons2svgfont, assign winding OPPOSITE to SVG convention — CCW for filled areas, CW for holes. The Y-flip corrects them at embed time. Symbol subpaths from OpenCV are already correct post-flip and should not be reversed.
3.11 Anti-Pattern: Index-Parity Winding Correction
What happened (v1 approach): Applied winding correction by index parity — reverse every odd-indexed subpath (1st, 3rd...) to make them holes. Worked for simple icons (2-3 subpaths) but corrupted hydroponic and others where the symbol has its own internal holes. The index parity broke down because the symbol's fill/hole subpaths don't follow a simple alternating sequence relative to the frame subpaths.
What happened (v2 approach): Used geometric containment (ray-casting) to compute nesting depth per subpath — depth=0 is fill, depth=1 is hole, etc. Conceptually correct but broke most icons: all symbol subpaths are geometrically inside the outer frame rect, giving them depth≥1 and incorrectly marking them as holes.
What works (v3, current): Treat frame subpaths and symbol subpaths separately. The frame occupies a fixed number of leading subpaths (2 for single border, 4 for double border). Assign frame winding explicitly by slot (accounting for Y-flip). Leave symbol subpaths unchanged — OpenCV's winding is already correct after the font Y-flip.
Rule: Do not use index parity or geometric containment for winding correction in a frame+symbol compound path. Use the known frame structure to assign frame slots explicitly, and trust the tracer's output for symbol subpaths.
## 3.8 Pattern: Per-Icon Epsilon Tuning for Contour Tracing
What works: Using a default epsilon (1.3) for most icons but dialing back to 1.1 for icons with curved or complex shapes (alcohol, emergency_rations, frozen_goods, rations). A visual review pass after batch tracing catches boxy/simplified shapes. Rule: Default epsilon=1.3. Flag icons that look angular or have lost key shape features. Re-run at epsilon=1.1. Record per-icon values in DECISIONS.md.