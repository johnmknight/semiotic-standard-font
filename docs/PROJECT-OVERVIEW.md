# Semiotic Standard Webfont Project

**Bitmap to Font Pipeline** — Based on Ron Cobb's iconography from the Alien franchise (1979–present)
Document Version 2.0  //  February 2025
John M. Knight Publishing LLC

# 1. Project Goal
The Semiotic Standard Webfont project converts hand-drawn bitmap icons into a production-ready webfont. The source material is Ron Cobb's Semiotic Standard iconography, originally designed in 1978 for Ridley Scott's Alien (1979), which defines a universal system of safety and wayfinding pictograms for spacecraft and industrial environments.
The core challenge is that no clean, font-ready vector versions of these icons exist. The available source material consists of hand-drawn artwork, film stills, game screenshots, and community recreations of varying quality. This project builds an automated pipeline to transform those bitmap sources into precise, normalized vector glyphs suitable for webfont compilation.
## 1.1 What We're Building
A modern webfont package containing Cobb's original 30 icons plus franchise extensions, delivered in three rendering tiers:

| Tier | Method | Use Case |
| --- | --- | --- |
| Tier 1: Monochrome | Standard webfont (currentColor) | Inline text, small UI, print, high-contrast |
| Tier 2: Duotone | Dual-layer CSS pseudo-elements | Dashboards, navigation panels, status indicators |
| Tier 3: Full Color SVG | Multi-color SVG sprite sheet | Kiosk displays, large format, immersive sci-fi UI |


## 1.2 Key Design Decision
Final font glyphs MUST include the Cobb border. The Semiotic Standard icons are not just symbols — they are complete signs with a distinctive rounded-rectangle frame, a label area, and an interior pictogram. The border is integral to the icon's identity and recognizability.
However, the SVG conversion pipeline extracts and traces the interior symbol pictogram separately. The Cobb frame border is a standardized geometric shape that is generated programmatically rather than traced from the bitmap source. This produces cleaner, more consistent results than tracing the hand-drawn borders directly.
In summary: SVGs contain symbol-only artwork; borders are composed separately; final glyphs combine both.

# 2. Lessons Learned: What Worked and What Didn't
This section documents the technical approaches attempted across multiple development sessions, capturing what succeeded and what failed so future sessions can avoid repeating mistakes.

## 2.1 The Monochrome Webfont Problem (Critical Discovery)
Status: FAILED — fundamental design conflict identified
The first major attempt used the existing community SVGs from semioticstandard.org (banastas/SemioticStandard.org GitHub repo) compiled directly into a webfont using fantasticon. This produced a technically functional font with all 34 glyphs, but the result was unusable.

What happened: Ron Cobb's Semiotic Standard is fundamentally a COLOR-CODED icon system. The icons were designed so that color carries most of the semantic meaning. Red borders mean danger/access; green means organic/medical; blue means cryogenic; grey means technical systems; orange means hazard/energy; black means vacuum/death.
When a webfont strips all color to monochrome (fonts inherit currentColor), many icons collapse into nearly identical rounded squares with inner squares. pressurised-area becomes an empty frame. storage-organic and storage-non-organic become identical. refrigeration merges with the storage icons. The color WAS the differentiator.

Resolution: Three-pronged approach adopted:
(a) Design every icon to be structurally distinguishable in monochrome first — use progressively different internal symbols, fill patterns, or badge modifiers to encode the information that color previously carried.
(b) Implement a dual-layer duotone font system (Tier 2) using CSS pseudo-elements to stack a colored frame layer with a contrasting symbol layer, following Font Awesome's duotone pattern.
(c) Ship an SVG sprite for Tier 3 full-color rendering in kiosk/display contexts, with inline SVG delivery matching the existing Tabler Icons approach used in ArtemisOps.

Key insight for future skills: Always validate that source material's information architecture survives the target format's constraints BEFORE building the pipeline. A webfont that strips color from color-dependent icons is like a translation that strips tone marks from a tonal language.

## 2.2 SVG Source Acquisition
Status: SUCCEEDED with workarounds
The SVGs live on semioticstandard.org, served from a GitHub Pages repo (banastas/SemioticStandard.org). The backing repo is MIT-licensed code with a note that the symbol designs are Ron Cobb's IP, used for educational/preservation purposes.

What worked: Using the web_fetch tool to read the HTML pages and extract SVG URLs, then individually fetching each of the 34 SVG files. Git clone was blocked by the egress proxy, so individual file fetch was the reliable path.
What didn't work: Git clone via bash (proxy blocked), direct curl/wget (also blocked). Container network egress only permits whitelisted domains.
Lesson: When git is blocked, fall back to web_fetch on individual file URLs from GitHub's raw content CDN (raw.githubusercontent.com) or the Pages site. Download SVGs one at a time rather than cloning entire repos.

## 2.3 Font Compilation Tooling
Status: SUCCEEDED after tool iteration

Tool 1 — fantasticon: First attempt. Required Node.js, which was not installed on the local Windows machine. Fell back to WSL (Windows Subsystem for Linux) where Node 18.19.1 was available. fantasticon v4 required Node 20+, so downgraded to fantasticon v3.0.0 which worked with Node 18. Successfully compiled all 34 SVGs into WOFF2, TTF, CSS, HTML preview, and JSON mapping.
Tool 2 — svgtofont: Chosen for the production pipeline. Similar to fantasticon but with more configuration options (fontHeight, normalize, centerHorizontally, centerVertically). Uses svgicons2svgfont under the hood. Configured with fontHeight: 1000 to match the 1000×1000 viewBox of the source SVGs.
What didn't work: npm install on Windows PowerShell when Node.js wasn't in PATH. Attempting to use the IcoMoon web app (browser-based, can't be driven programmatically). Using PowerShell && operator (not valid in older PowerShell — use ; instead).
Lesson: Always check Node.js availability before starting npm-based pipelines. WSL is a reliable fallback on Windows. fantasticon v3 is the safe choice for Node 18; v4+ needs Node 20+. svgtofont gives more control for production use.

## 2.4 Bitmap-to-SVG Tracing Pipeline (trace_v2.py)
Status: WORKING with known limitations
The trace_v2.py pipeline converts hand-drawn Cobb icon PNGs (embedded as base64 in SVG wrappers) into clean vector SVGs. This was the most technically complex component.

What worked:
• PIL/NumPy for image analysis: Extracting base64 PNGs from SVG wrappers, brightness profiling, adaptive thresholding.
• Sustained brightness detection: Scanning row averages for 10+ consecutive rows above brightness 160 to find the interior region. This correctly distinguishes thin bright bands within the Cobb frame border (1-3 rows) from the actual content area.
• Symbol isolation via gap detection: Finding the largest vertical gap in the top 60% of the interior to separate label text from the pictogram below.
• vtracer for bitmap-to-vector: Polygon tracing mode with binary colormode, filter_speckle=4, corner_threshold=60, length_threshold=4.0, splice_threshold=45. Produces clean compound paths.
• evenodd fill rule: Critical for glyphs with interior holes (cup handles, enclosed shapes). Without it, holes fill solid.
• 1000×1000 normalization: Uniform scaling to fill 90% of viewBox, centered, all black paths combined into single compound path.

What didn't work / known issues:
• Over-aggressive cropping: Some symbols under-fill the 1000×1000 viewBox (26-50% fill), making glyphs look small. The crop step sometimes clips symbol edges.
• Frame border remnants: The interior bounds detection occasionally fails to exclude all frame border elements, leaving artifacts in the traced output.
• Label text leaking: Gap detection fails for some icons where the label text and symbol are close together or where there's no clear brightness gap.
• vtracer requires file I/O: Cannot operate in-memory; must write temp BMP/PNG to disk and read SVG output from disk.
Lesson: Conservative cropping with generous padding (5px+) is better than tight cropping. Always save and inspect intermediate debug images (crop, B&W, traced) to diagnose pipeline failures per-icon.

## 2.5 Image Processing Approaches Researched
Status: RESEARCH COMPLETED — informed pipeline design
Extensive research was done on bitmap-to-vector tracing methods before building the pipeline. The findings shaped the final trace_v2.py architecture:

HSV Color Masking (OpenCV): Standard approach for isolating specific colors. Used successfully for ArtemisOps trajectory line tracing. HSV separates hue from brightness/saturation, making it much better than RGB for color isolation. Relevant for future Tier 3 work where we need to isolate specific Cobb category colors from the source PNGs.
Morphological Operations: MORPH_CLOSE fills small gaps; MORPH_OPEN removes noise blobs. Used in the preprocessing stage. Key parameters: kernel size (7×7 elliptical for general cleanup).
Skeletonization/Thinning: Zhang-Suen thinning algorithm reduces multi-pixel-wide lines to 1px centerlines. Useful for line tracing but not needed for filled region extraction (our use case).
Potrace: Alternative to vtracer. Used successfully for simple silhouette tracing (astronaut-chair icon). Command: potrace input.bmp -s -o output.svg --flat. Good for clean black-and-white inputs. For our pipeline, vtracer was preferred because it handles complex compound paths better and has a Python binding.
CLAHE (Contrast Limited Adaptive Histogram Equalization): Critical for revealing subtle surface features on uniform-color objects. Applied in the product-photo-analysis skill. Not directly used in the semiotic pipeline but relevant for preprocessing low-contrast source material.

## 2.6 SVG-to-Font Conversion Gotchas
Status: DOCUMENTED from build experience

These are specific technical issues encountered during the SVG-to-font compilation step:
• SVGs MUST have filled paths only — no strokes, no gradients, no images, no text elements. svgtofont silently ignores stroke-only elements, producing blank glyphs.
• viewBox must be exactly 0 0 1000 1000 for consistent glyph sizing when fontHeight is 1000.
• File naming convention ss-[name].svg is stripped to form CSS class .ss-[name]::before.
• Browser font caching is aggressive. Always add cache-busting query strings (?v=N) during development.
• Chrome blocks file:// URL font loading due to CORS. Must serve via localhost HTTP server for preview.
• centerHorizontally and centerVertically in svgtofont config help narrow/short glyphs but can cause issues with glyphs that intentionally occupy non-centered positions.

## 2.7 Cross-Session File Transfer
Status: ONGOING CHALLENGE
Moving files between Claude's container filesystem and the user's local machine is a recurring friction point in this project.

What works:
• Container → User: present_files tool copies to /mnt/user-data/outputs/ and generates a download link.
• User → Container: User uploads files which appear in /mnt/user-data/uploads/.
• Desktop Commander: read_file/write_file for files on the user's Windows machine.
• Copy-Item (PowerShell) for moving files between local directories.

What doesn't work:
• Google Drive search often returns no results for recently saved files (indexing delay or permission scope mismatch).
• Base64 encoding through shell is impractical for files >5KB — output overflows tool response limits.
• Container filesystem resets between sessions — files in /home/claude/ are lost.
Lesson: Use user Downloads folder as the simplest staging area. Ask user to save files to Downloads, then Copy-Item to project directory. Don't over-engineer transfer mechanisms.

# 3. The Pipeline at a Glance
The end-to-end pipeline has three major phases, each documented in its own process document:
## Phase 1: Bitmap to SVG
Hand-drawn Cobb icons (embedded as PNGs inside SVG wrappers) are processed through an automated extraction, cropping, thresholding, and vector tracing pipeline. The output is a clean, normalized 1000×1000 SVG containing only the interior symbol pictogram as filled paths.
Tool: trace_v2.py (Python, using PIL/NumPy for image analysis and vtracer for bitmap-to-vector conversion)
## Phase 2: SVG to Font
The normalized symbol SVGs are compiled into webfont files (WOFF2, WOFF, TTF, EOT) using svgtofont. Unicode codepoints are assigned in the Private Use Area (U+E001–U+E0FF). CSS classes and a specimen preview page are generated alongside the font.
Tool: build-font.js (Node.js, using svgtofont)
## Phase 3: Composition & Delivery
For Tier 2 (duotone) and Tier 3 (full color), the traced symbols are composited with programmatically generated Cobb frame borders. The duotone system uses two stacked font layers (frame + symbol), while Tier 3 uses multi-color SVG sprites with Cobb's original color coding.

# 4. Source Material
## 4.1 Current Icon Set: Food & Dining (16 icons)
The first batch processed through the pipeline are 16 hand-drawn Food & Dining category icons, created as part of the extended icon set following Cobb's design language.
## 4.2 Source Format
Each source icon is an SVG file containing a base64-encoded PNG image. The PNG shows the complete Cobb sign: frame borders, colored label panel, label text, separator line, and interior symbol pictogram. The images are hand-drawn at approximately 200×200 pixels. Source files stored at: from john/[icon_name].svg
## 4.3 Cobb Icon Anatomy

| Region | Position | Content |
| --- | --- | --- |
| Outer frame | Full perimeter | 3 concentric rounded-rect borders (dark/bright/dark bands) |
| Label panel | Top ~30% of interior | Colored background with category text label |
| Separator | Between label and symbol | Thin structural line dividing the two regions |
| Symbol area | Bottom ~70% of interior | The pictographic symbol on a light/cream background |
| Symbol | Centered in symbol area | Medium gray (~70–75 RGB) pictogram on bright (~240+ RGB) background |


# 5. Project Structure
semiotic-standard-font/
├── from john/              # Source SVGs (PNG-embedded hand-drawn icons)
├── svg/
│   ├── mono/              # Traced monochrome SVGs (vtracer output)
│   │   ├── base/          # Original 30 Cobb icons
│   │   └── extended/      # Extended icons (normalized for font)
│   ├── frames/            # Duotone frame layers (Tier 2)
│   ├── symbols/           # Duotone symbol layers (Tier 2)
│   └── color/             # Full-color SVGs (Tier 3)
├── fonts/                 # Generated font files
├── css/                   # Generated CSS + color utilities
├── sprites/               # Generated SVG sprite sheet
├── preview/               # Specimen pages + debug output
├── scripts/               # Build and processing scripts
│   ├── trace_v2.py        # Bitmap-to-SVG pipeline
│   ├── build-font.js      # svgtofont build config
│   └── build-duotone.js   # Tier 2 font builder
├── docs/                  # Specifications and references
├── package.json
└── DECISIONS.md           # Key design decisions log

# 6. Technology Stack

| Component | Technology | Purpose |
| --- | --- | --- |
| Image analysis | Python 3 + PIL + NumPy | PNG extraction, cropping, brightness profiling, thresholding |
| Vector tracing | vtracer (Python binding) | Bitmap-to-SVG path conversion using polygon tracing |
| Alt. tracing | potrace (CLI) | Simpler bitmap-to-SVG for clean B&W silhouettes |
| SVG optimization | SVGO | Path simplification, attribute cleanup |
| Font compilation | svgtofont (Node.js) | SVG → TTF/WOFF2/WOFF/EOT + CSS generation |
| Alt. font tool | fantasticon v3.0.0 | Alternative font compiler (works with Node 18+) |
| Build orchestration | npm scripts | Pipeline sequencing, clean/build/dev workflow |
| Preview & QA | HTML + CSS | Specimen pages, side-by-side comparison, font rendering test |


## 6.1 Environment Notes
• Node.js: Not always available on Windows. WSL (Ubuntu) is the reliable fallback. Check with 'wsl node --version'.
• Python: Available on Windows via Microsoft Store (Python 3.12). Use full path or 'python' command (not 'python3' on Windows).
• PowerShell: Use ; not && to chain commands. Use backtick ` for line continuation, not backslash.
• Container (Claude's Linux): Has apt-get, pip, npm. Use --break-system-packages flag for pip. Network egress restricted to whitelisted domains.

# 7. Current Status
## 7.1 What Works
• Full trace pipeline (trace_v2.py) processes all 16 Food & Dining icons end-to-end
• Symbol isolation successfully separates pictograms from Cobb frame and label regions
• vtracer produces clean vector paths from thresholded bitmap input
• svgtofont compiles normalized SVGs into a working webfont with all 16 glyphs
• Font renders correctly in browser with compound paths and evenodd fill rules
• fantasticon v3.0.0 validated as alternative compiler (34 community SVGs compiled successfully)
## 7.2 Known Issues
• Some symbols under-fill the 1000×1000 viewBox (26–50% fill), resulting in small-looking glyphs
• Occasional frame border remnants leaking into traced symbol paths
• Cobb border composition step (combining traced symbol + generated frame) not yet implemented
• Duotone and full-color tiers (Tier 2 and Tier 3) pending symbol-only pipeline stabilization
• Monochrome glyphs need structural differentiation for icons that relied on color alone
## 7.3 Next Steps
• Improve symbol crop accuracy and viewBox fill percentage
• Implement Cobb border composition (programmatic frame + traced symbol → final glyph)
• Apply monochrome differentiation rules to ambiguous icon families (pressure, radiation, storage)
• Process remaining icon categories (original 30 base Cobb icons, Alien: Isolation extended set)
• Build Tier 2 duotone font layers
• Build Tier 3 SVG sprite sheet with Cobb color system

"In space, no one can hear you kern."