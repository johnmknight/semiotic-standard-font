/**
 * build-font-direct.js
 * Direct pipeline: SVG icons -> SVG font -> TTF -> WOFF -> WOFF2
 * Bypasses svgtofont wrapper, uses underlying libraries directly.
 */
const svgicons2svgfont = require('svgicons2svgfont');
const svg2ttf           = require('svg2ttf');
const ttf2woff          = require('ttf2woff');
const ttf2woff2         = require('ttf2woff2');
const fs                = require('fs');
const path              = require('path');

const SRC_DIR   = path.resolve(__dirname, '../svg/mono/extended');
const FONTS_DIR = path.resolve(__dirname, '../fonts');
const FONT_NAME = 'semiotic-standard';
const START_UNI = 0xE001;

fs.mkdirSync(FONTS_DIR, { recursive: true });

// Collect and sort SVG files
const svgFiles = fs.readdirSync(SRC_DIR)
    .filter(f => f.endsWith('.svg') && f.startsWith('ss-'))
    .sort();

console.log(`Building font from ${svgFiles.length} SVGs...`);

// Unicode map for CSS generation
const unicodeMap = {};

// Step 1: SVG icons -> SVG font
const svgFontPath = path.join(FONTS_DIR, `${FONT_NAME}.svg`);
const fontStream = new svgicons2svgfont({
    fontName: FONT_NAME,
    fontHeight: 1000,
    normalize: true,
    centerHorizontally: true,
    centerVertically: true,
    log: () => {}
});

let svgFontData = '';
fontStream.on('data', chunk => svgFontData += chunk);

fontStream.on('finish', () => {
    fs.writeFileSync(svgFontPath, svgFontData);
    console.log(`✅ SVG font -> ${svgFontPath}`);

    // Step 2: SVG font -> TTF
    const ttf = svg2ttf(svgFontData, { copyright: 'John M. Knight' });
    const ttfBuf = Buffer.from(ttf.buffer);
    const ttfPath = path.join(FONTS_DIR, `${FONT_NAME}.ttf`);
    fs.writeFileSync(ttfPath, ttfBuf);
    console.log(`✅ TTF -> ${ttfPath}`);

    // Step 3: TTF -> WOFF
    const woff = ttf2woff(new Uint8Array(ttfBuf));
    const woffPath = path.join(FONTS_DIR, `${FONT_NAME}.woff`);
    fs.writeFileSync(woffPath, Buffer.from(woff.buffer));
    console.log(`✅ WOFF -> ${woffPath}`);

    // Step 4: TTF -> WOFF2
    const woff2 = ttf2woff2(ttfBuf);
    const woff2Path = path.join(FONTS_DIR, `${FONT_NAME}.woff2`);
    fs.writeFileSync(woff2Path, woff2);
    console.log(`✅ WOFF2 -> ${woff2Path}`);

    // Step 5: Generate CSS
    const cssLines = [
        `@font-face {`,
        `  font-family: '${FONT_NAME}';`,
        `  src: url('../fonts/${FONT_NAME}.woff2') format('woff2'),`,
        `       url('../fonts/${FONT_NAME}.woff') format('woff'),`,
        `       url('../fonts/${FONT_NAME}.ttf') format('truetype');`,
        `  font-weight: normal;`,
        `  font-style: normal;`,
        `}`,
        ``,
        `[class^="ss-"], [class*=" ss-"] {`,
        `  font-family: '${FONT_NAME}' !important;`,
        `  speak: never;`,
        `  font-style: normal;`,
        `  font-weight: normal;`,
        `  font-variant: normal;`,
        `  text-transform: none;`,
        `  line-height: 1;`,
        `  -webkit-font-smoothing: antialiased;`,
        `}`,
        ``
    ];
    Object.entries(unicodeMap).sort((a,b) => a[0].localeCompare(b[0])).forEach(([name, code]) => {
        const cls = name.replace(/^ss-/, '');
        cssLines.push(`.ss-${cls}::before { content: "\\${code.toString(16).toUpperCase()}"; }`);
    });

    const cssDir = path.resolve(__dirname, '../css');
    fs.mkdirSync(cssDir, { recursive: true });
    const cssPath = path.join(cssDir, `${FONT_NAME}.css`);
    fs.writeFileSync(cssPath, cssLines.join('\n'));
    console.log(`✅ CSS -> ${cssPath}`);

    // Step 6: Generate unicode map JSON
    const mapPath = path.join(FONTS_DIR, `${FONT_NAME}.json`);
    fs.writeFileSync(mapPath, JSON.stringify(unicodeMap, null, 2));
    console.log(`✅ Unicode map -> ${mapPath}`);

    console.log(`\n🎉 Font build complete! ${svgFiles.length} glyphs.`);
});

fontStream.on('error', err => {
    console.error('Font stream error:', err);
    process.exit(1);
});

// Write each SVG as a glyph
svgFiles.forEach((file, i) => {
    const name = path.basename(file, '.svg');  // e.g. ss-alcohol
    const codePoint = START_UNI + i;
    const unicode = String.fromCharCode(codePoint);
    unicodeMap[name] = codePoint;

    const glyph = fs.createReadStream(path.join(SRC_DIR, file));
    glyph.metadata = { unicode: [unicode], name };
    fontStream.write(glyph);

    console.log(`  ${name} -> U+${codePoint.toString(16).toUpperCase()}`);
});

fontStream.end();
