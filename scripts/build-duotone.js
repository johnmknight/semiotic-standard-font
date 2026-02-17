const svgtofont = require('svgtofont');
const path = require('path');

async function buildDuotone() {
  // Build frame layers font
  await svgtofont({
    src: path.resolve(__dirname, '../svg/frames'),
    dist: path.resolve(__dirname, '../fonts/duotone'),
    fontName: 'semiotic-standard-frames',
    css: true,
    startUnicode: 0xE101,
    svgicons2svgfont: { fontHeight: 1000, normalize: true },
  });
  console.log('Duotone frames font built.');

  // Build symbol layers font
  await svgtofont({
    src: path.resolve(__dirname, '../svg/symbols'),
    dist: path.resolve(__dirname, '../fonts/duotone'),
    fontName: 'semiotic-standard-symbols',
    css: true,
    startUnicode: 0xE201,
    svgicons2svgfont: { fontHeight: 1000, normalize: true },
  });
  console.log('Duotone symbols font built.');
}

buildDuotone().catch(console.error);
