"""
reextract.py - Re-extract grain and hydroponic with tuned parameters.

Findings from inspect_icon.py:
- grain: interior is warm cream/beige, symbol is low-contrast tan/grey. 
  No meaningful hue. Need more clusters to split symbol from background,
  or use adaptive threshold rather than k-means.
- hydroponic: dark olive-green plant material (avg RGB 45,59,42) was being 
  collapsed into "black". Need to lower sat threshold and add dark-green.

Strategy:
  1. Save annotated source at 4x scale with pixel value overlay
  2. Run k-means with more clusters (10) and lower sat threshold
  3. For grain: also try a brightness-threshold approach (symbol = darker than background)
  4. Save masks and a composite comparison image
"""

import base64, io, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from sklearn.cluster import KMeans

SRC_DIR = Path(r"C:\Users\john_\dev\semiotic-standard-font\from john")
OUT_DIR = Path(r"C:\Users\john_\dev\semiotic-standard-font\svg\masks")

NAMED_COLORS = {
    "frame_border": (110, 25, 25),   # the dark red Cobb border ring
    "black":        (10, 10, 10),
    "dark_grey":    (50, 50, 50),
    "mid_grey":     (110, 110, 110),
    "light_grey":   (160, 155, 148),
    "cream":        (220, 210, 195),
    "white":        (245, 240, 228),
    "red":          (180, 40, 40),
    "dark_red":     (100, 15, 15),
    "green":        (40, 140, 60),
    "dark_green":   (45, 65, 42),    # hydroponic plant color
    "olive":        (80, 85, 55),
    "blue":         (35, 60, 115),
    "yellow":       (240, 195, 40),
    "orange":       (200, 120, 30),
    "tan":          (160, 130, 100),
}

def color_distance(c1, c2):
    return sum((a-b)**2 for a,b in zip(c1,c2))**0.5

def nearest_color_name(rgb):
    return min(NAMED_COLORS.items(), key=lambda kv: color_distance(rgb, kv[1]))[0]

def extract_png(svg_path):
    content = svg_path.read_text(encoding='utf-8', errors='replace')
    for pattern in [r'href="data:image/png;base64,([^"]+)"',
                    r'xlink:href="data:image/png;base64,([^"]+)"']:
        m = re.search(pattern, content)
        if m:
            data = m.group(1).replace('\n','').replace(' ','')
            return Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB')
    return None

def save_mask(mask_2d, path):
    arr = mask_2d.astype(np.uint8) * 255
    Image.fromarray(arr).save(path)

def make_composite(source_img, masks, out_path):
    """Side-by-side: source + all masks in a grid."""
    n = len(masks) + 1
    size = 200
    cols = min(n, 8)
    rows = (n + cols - 1) // cols
    W = cols * (size + 4) + 4
    H = rows * (size + 20 + 4) + 4
    comp = Image.new("RGB", (W, H), (17, 17, 17))
    draw = ImageDraw.Draw(comp)

    items = [("SOURCE", source_img)] + [(name, None, mask) for name, mask in masks]
    for i, item in enumerate(items):
        col = i % cols
        row = i // cols
        x = 4 + col * (size + 4)
        y = 4 + row * (size + 20 + 4)
        if i == 0:
            label = item[0]
            thumb = item[1].resize((size, size), Image.LANCZOS)
        else:
            label = item[0]
            mask_arr = item[2].astype(np.uint8) * 255
            thumb = Image.fromarray(mask_arr).resize((size, size), Image.NEAREST)
        comp.paste(thumb, (x, y))
        draw.text((x, y + size + 2), label, fill=(180, 130, 50))

    comp.save(out_path)
    print(f"  Saved composite: {out_path.name}")

def process(icon_name, n_clusters=10):
    print(f"\n{'='*50}")
    print(f"Re-extracting: {icon_name} (n_clusters={n_clusters})")
    svg_path = SRC_DIR / f"{icon_name}.svg"
    img = extract_png(svg_path)
    if img is None:
        print("  ERROR: could not extract PNG"); return

    out_dir = OUT_DIR / icon_name
    out_dir.mkdir(parents=True, exist_ok=True)
    img.save(out_dir / "_source.png")

    arr = np.array(img)
    h, w = arr.shape[:2]
    pixels = arr.reshape(-1, 3).astype(np.float32)

    km = KMeans(n_clusters=n_clusters, n_init=15, random_state=42)
    labels = km.fit_predict(pixels)
    centers = km.cluster_centers_.astype(int)

    # Track name collisions
    name_counts = {}
    for c in centers:
        n = nearest_color_name(tuple(c))
        name_counts[n] = name_counts.get(n, 0) + 1

    name_seen = {}
    masks_out = []
    for i, center in enumerate(centers):
        mask_flat = labels == i
        count = int(mask_flat.sum())
        pct = count / (h*w) * 100
        if pct < 0.5:
            continue
        n = nearest_color_name(tuple(center))
        name_seen[n] = name_seen.get(n, 0) + 1
        label = f"{n}_{name_seen[n]}" if name_counts[n] > 1 else n

        mask_2d = mask_flat.reshape(h, w)
        out_path = out_dir / f"mask_{label}.png"
        save_mask(mask_2d, out_path)
        print(f"  {label:<22} RGB({center[0]:3d},{center[1]:3d},{center[2]:3d})  {pct:.1f}%")
        masks_out.append((label, mask_2d))

    # Also do brightness-threshold mask for grain (symbol = darker than background median)
    if icon_name == "grain":
        grey = arr.mean(axis=2)
        # Interior region: exclude top/bottom 15% (frame area)
        margin = int(h * 0.15)
        interior = grey[margin:h-margin, margin:w-margin]
        bg_brightness = np.median(interior[interior > 150]) if (interior > 150).any() else 200
        threshold = bg_brightness - 40
        symbol_mask = grey < threshold
        save_mask(symbol_mask, out_dir / "mask_brightness_symbol.png")
        print(f"  brightness_symbol       threshold={threshold:.0f} (bg={bg_brightness:.0f})  {symbol_mask.mean()*100:.1f}%")
        masks_out.append(("brightness_symbol", symbol_mask))

    make_composite(img, masks_out, out_dir / "_composite.png")
    return masks_out

process("grain", n_clusters=10)
process("hydroponic", n_clusters=10)
print("\nDone.")
