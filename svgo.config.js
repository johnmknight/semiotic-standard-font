module.exports = {
  plugins: [
    'removeDoctype', 'removeXMLProcInst', 'removeComments',
    'removeMetadata', 'removeEditorsNSData', 'cleanupAttrs',
    'convertPathData', 'mergePaths', 'removeEmptyContainers',
    { name: 'removeAttrs', params: { attrs: '(fill|stroke)' } }
  ]
};
