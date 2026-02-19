"""
make_masks.py - Step 1: Create color masks for each icon

For each source SVG in 'from john/', extract the embedded PNG and create
one mask PNG per significant color region found in the image.

Output: svg/masks/[icon_name]/mask_[color_name].png
"""

import base64
import io
import os
import re
import sys
import numpy as np
from PIL import Image
from pathlib import Path
from sklearn.cluster import KMeans

SRC_DIR = Path(r"C:\Users\john_\dev\semiotic-standard-font\from john")
OUT_DIR = Path(r"C:\Users\john_\dev\semiotic-standard-font\svg\masks")
DEBUG_DIR = Path(r"C:\Users\john_\dev\semiotic-standard-font\preview\debug")

# Cobb color palette - approximate HSV ranges
# We'll use RGB proximity to named colors
NAMED_COLORS = {
    "black":  (20, 20, 20),
    "white":  (230, 230, 230),
    "red":    (180, 40, 40),
    "green":  (40, 140, 60),
    "blue":   (40, 80, 160),
    "orange": (200, 120, 30),
    "grey":   (120, 120, 120),
    "yellow": (210, 200, 50),
}

def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def nearest_color_name(rgb):
    best = min(NAMED_COLORS.items(), key=lambda kv: color_distance(rgb, kv[1]))
    return best[0]

def extract_png(svg_path):
    content = svg_path.read_text(encoding='utf-8', errors='replace')
    pattern = r'href="data:image/png;base64,([^"]+)"'
    m = re.search(pattern, content)
    if not m:
        # try xlink:href
        pattern2 = r'xlink:href="data:image/png;base64,([^"]+)"'
        m = re.search(pattern2, content)
    if not m:
        print(f"  WARNING: no embedded PNG found in {svg_path.name}")
        return None
    data = m.group(1).replace('\n', '').replace(' ', '')
    img = Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB')
    return img

def find_color_regions(img, n_clusters=6, tolerance=30):
    """
    K-means cluster the image pixels into n_clusters color groups.
    Returns list of (label, mean_rgb, pixel_mask) for significant clusters.
    Skips near-white and near-black clusters that are frame/background.
    """
    arr = np.array(img)
    h, w = arr.shape[:2]
    pixels = arr.reshape(-1, 3).astype(np.float32)

    km = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    labels = km.fit_predict(pixels)
    centers = km.cluster_centers_.astype(int)

    results = []
    for i, center in enumerate(centers):
        mask_flat = labels == i
        count = mask_flat.sum()
        pct = count / (h * w) * 100

        # Skip tiny clusters (< 1% of image)
        if pct < 1.0:
            continue

        name = nearest_color_name(tuple(center))
        mask_2d = mask_flat.reshape(h, w)

        results.append({
            "cluster_id": i,
            "name": name,
            "rgb": tuple(center),
            "count": int(count),
            "pct": pct,
            "mask": mask_2d,
        })

    return results

def save_mask(mask_2d, out_path):
    """Save boolean mask as white-on-black PNG."""
    arr = (mask_2d.astype(np.uint8)) * 255
    img = Image.fromarray(arr, mode='L')
    img.save(out_path)

def process_icon(svg_path):
    name = svg_path.stem
    print(f"\nProcessing: {name}")

    img = extract_png(svg_path)
    if img is None:
        return

    print(f"  Image size: {img.size}")

    out_dir = OUT_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save the source PNG for reference
    img.save(out_dir / "_source.png")

    regions = find_color_regions(img, n_clusters=7)

    # Handle duplicate color names by adding suffix
    name_counts = {}
    for r in regions:
        n = r["name"]
        name_counts[n] = name_counts.get(n, 0) + 1

    name_seen = {}
    for r in regions:
        n = r["name"]
        name_seen[n] = name_seen.get(n, 0) + 1
        if name_counts[n] > 1:
            label = f"{n}_{name_seen[n]}"
        else:
            label = n

        out_path = out_dir / f"mask_{label}.png"
        save_mask(r["mask"], out_path)
        print(f"  Cluster {r['cluster_id']}: {label} RGB{r['rgb']} {r['pct']:.1f}% -> {out_path.name}")

    print(f"  Saved {len(regions)} masks to {out_dir}")
    return regions

def main():
    svgs = sorted(SRC_DIR.glob("*.svg"))
    if not svgs:
        print(f"No SVG files found in {SRC_DIR}")
        sys.exit(1)

    print(f"Found {len(svgs)} source icons")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for svg_path in svgs:
        process_icon(svg_path)

    print("\nDone. Masks written to:", OUT_DIR)

if __name__ == "__main__":
    main()
