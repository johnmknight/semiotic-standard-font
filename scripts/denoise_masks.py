"""
denoise_masks.py - Apply morphological cleanup to noisy masks.

Pipeline per mask:
  1. Median filter (3x3) - kills salt-and-pepper speckle
  2. Morphological close (small kernel) - fills tiny holes inside symbol
  3. Morphological open (small kernel) - removes isolated noise blobs
  4. Optional: remove small connected components below min_area threshold
"""

import numpy as np
from PIL import Image
from pathlib import Path
from scipy import ndimage

MASKS_DIR = Path(r"C:\Users\john_\dev\semiotic-standard-font\svg\masks")

# Structuring elements
def disk(r):
    y, x = np.ogrid[-r:r+1, -r:r+1]
    return (x*x + y*y <= r*r).astype(np.uint8)

MEDIAN_SIZE = 3        # median filter window
CLOSE_RADIUS = 2       # morph close kernel radius (fills small holes)
OPEN_RADIUS  = 1       # morph open kernel radius (removes speckle blobs)
MIN_AREA     = 30      # remove connected components smaller than this (px)

def clean_mask(mask_bool):
    arr = mask_bool.astype(np.uint8)

    # 1. Median filter
    from scipy.ndimage import median_filter
    arr = median_filter(arr, size=MEDIAN_SIZE)

    # 2. Morphological close (dilation then erosion) - fill small holes
    struct = disk(CLOSE_RADIUS)
    arr = ndimage.binary_dilation(arr, structure=struct).astype(np.uint8)
    arr = ndimage.binary_erosion(arr,  structure=struct).astype(np.uint8)

    # 3. Morphological open (erosion then dilation) - remove speckle
    struct2 = disk(OPEN_RADIUS)
    arr = ndimage.binary_erosion(arr,  structure=struct2).astype(np.uint8)
    arr = ndimage.binary_dilation(arr, structure=struct2).astype(np.uint8)

    # 4. Remove small connected components
    labeled, num_features = ndimage.label(arr)
    sizes = ndimage.sum(arr, labeled, range(1, num_features+1))
    remove_labels = [i+1 for i, s in enumerate(sizes) if s < MIN_AREA]
    for lbl in remove_labels:
        arr[labeled == lbl] = 0

    return arr.astype(bool)

def process_icon(icon_name):
    icon_dir = MASKS_DIR / icon_name
    mask_files = sorted(icon_dir.glob("mask_*.png"))
    if not mask_files:
        print(f"  No masks found for {icon_name}")
        return

    print(f"\n{icon_name}:")
    for mf in mask_files:
        raw = np.array(Image.open(mf).convert("L")) > 127
        cleaned = clean_mask(raw)

        # Save cleaned version (overwrites)
        out = (cleaned.astype(np.uint8)) * 255
        Image.fromarray(out).save(mf)

        noise_removed = int(raw.sum()) - int(cleaned.sum())
        print(f"  {mf.name:<35} {raw.sum():6d} -> {cleaned.sum():6d} px  ({noise_removed:+d})")

def main():
    icons = sorted([d.name for d in MASKS_DIR.iterdir() if d.is_dir()])
    print(f"Denoising masks for {len(icons)} icons...")
    for icon in icons:
        process_icon(icon)
    print("\nDone.")

if __name__ == "__main__":
    main()
