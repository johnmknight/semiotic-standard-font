const svgtofont = require('svgtofont');
const path = require('path');

// Build monochrome font (Tier 1)
svgtofont({
  src: path.resolve(__dirname, '../svg/mono'),
  dist: path.resolve(__dirname, '../fonts'),
  fontName: 'semiotic-standard',
  css: true,
  startUnicode: 0xE001,
  svgicons2svgfont: { 
    fontHeight: 1000, 
    normalize: true,
    centerHorizontally: true,
    centerVertically: true
  }
}).then(() => {
  console.log('Tier 1 monochrome font built successfully.');
}).catch((err) => {
  console.error('Build failed:', err);
});
