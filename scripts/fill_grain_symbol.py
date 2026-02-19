"""
fill_grain_symbol.py v4 - Simple, effective approach.

The complexity is fighting us. The real fix is simpler:
  - brightness_symbol already captures the whole icon structure correctly
  - black_4 is the wheat stalk silhouette but missing edge pixels
  - We just need to: start with black_4, grow it slightly, then
    constrain it to only pixels that are actually dark in the source
    (so we don't bleed into the cream background or frame)

Also: the wheat stalk is grey (~60-90 brightness), not pure black.
We need a threshold of ~150 to capture all of it, not ~202.
"""

import numpy as np
from PIL import Image
from pathlib import Path
from scipy.ndimage import binary_dilation, binary_fill_holes, label

GRAIN_DIR = Path(r"C:\Users\john_\dev\semiotic-standard-font\svg\masks\grain")

src   = np.array(Image.open(GRAIN_DIR / "_source.png").convert("RGB"))
grey  = src.mean(axis=2)
h, w  = grey.shape

old   = np.array(Image.open(GRAIN_DIR / "mask_black_4.png").convert("L")) > 127

# ── Simple brightness threshold at 150 ────────────────────────────────
# The wheat stalk is ~60-90, the frame border is ~20-50,
# the background cream is ~230-250.
# At threshold 150 we capture stalk + frame.
# Then we isolate just the stalk component (not touching image edge).

dark = grey < 150

# Remove components touching image edge (= the frame border ring)
labeled, n = label(dark)
edge_touch = np.zeros((h, w), bool)
edge_touch[0,:] = edge_touch[-1,:] = edge_touch[:,0] = edge_touch[:,-1] = True
edge_lbls = set(np.unique(labeled[edge_touch & dark]))
edge_lbls.discard(0)

no_frame = dark.copy()
for lbl in edge_lbls:
    no_frame[labeled == lbl] = False

print(f"Dark pixels total: {dark.sum()}")
print(f"After removing frame-touching components: {no_frame.sum()}")

# Keep the largest remaining component
labeled2, n2 = label(no_frame)
if n2 == 0:
    # Try a looser threshold
    dark = grey < 170
    labeled, n = label(dark)
    edge_lbls = set(np.unique(labeled[edge_touch & dark]))
    edge_lbls.discard(0)
    no_frame = dark.copy()
    for lbl in edge_lbls:
        no_frame[labeled == lbl] = False
    labeled2, n2 = label(no_frame)
    print(f"Retrying with threshold 170: {no_frame.sum()} px, {n2} components")

if n2 == 0:
    print("ERROR: still no components"); exit(1)

sizes = [(int((labeled2==i).sum()), i) for i in range(1, n2+1)]
sizes.sort(reverse=True)
print(f"Top 5 components by size: {sizes[:5]}")

symbol = labeled2 == sizes[0][1]
print(f"Symbol component: {symbol.sum()} px")

# Fill holes
symbol_filled = binary_fill_holes(symbol)
print(f"After hole fill: {symbol_filled.sum()} px (+{symbol_filled.sum()-symbol.sum()})")

# 1px dilation
cross = np.array([[0,1,0],[1,1,1],[0,1,0]], dtype=bool)
symbol_final = binary_dilation(symbol_filled, structure=cross, iterations=1)
# Constrain: dilation can only claim pixels that are actually grey (< 220)
symbol_final = symbol_final & (grey < 220)
print(f"After constrained dilation: {symbol_final.sum()} px")

# Save
Image.fromarray((symbol_final.astype(np.uint8))*255).save(GRAIN_DIR / "mask_symbol_filled.png")
print("Saved: mask_symbol_filled.png")

# Overlay comparison
recovered = symbol_final & ~old
overlay = src.copy()
overlay[symbol_final] = (overlay[symbol_final] * 0.25 + np.array([255,255,255]) * 0.75).astype(np.uint8)
overlay[recovered]    = (overlay[recovered]    * 0.25 + np.array([0, 220, 80])  * 0.75).astype(np.uint8)
Image.fromarray(overlay).save(GRAIN_DIR / "_symbol_overlay.png")
print(f"Saved: _symbol_overlay.png  ({recovered.sum()} newly recovered px in green)")
