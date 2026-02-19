"""
compare_grain.py - Side-by-side before/after comparison for grain.
Regenerates the noisy "before" from scratch (original 7-cluster run)
and places it next to the cleaned "after" masks.
"""
import base64, io, re
import numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
from sklearn.cluster import KMeans

SRC = Path(r"C:\Users\john_\dev\semiotic-standard-font\from john\grain.svg")
MASKS = Path(r"C:\Users\john_\dev\semiotic-standard-font\svg\masks\grain")
OUT   = Path(r"C:\Users\john_\dev\semiotic-standard-font\preview\grain_before_after.png")

# ── extract source PNG ──────────────────────────────────────────────
content = SRC.read_text(encoding='utf-8', errors='replace')
m = re.search(r'href="data:image/png;base64,([^"]+)"', content)
data = m.group(1).replace('\n','').replace(' ','')
src_img = Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB')

# ── "before": original 7-cluster K-means, no denoise ───────────────
arr = np.array(src_img)
h, w = arr.shape[:2]
pixels = arr.reshape(-1,3).astype(np.float32)
km = KMeans(n_clusters=7, n_init=10, random_state=42)
labels = km.fit_predict(pixels)
centers = km.cluster_centers_.astype(int)

before_masks = []
for i, center in enumerate(centers):
    mask = (labels == i).reshape(h, w)
    pct = mask.mean()*100
    if pct < 1.0: continue
    before_masks.append((f"before_{i}\n{center}", mask))

# ── "after": load denoised masks from disk ─────────────────────────
after_masks = []
for f in sorted(MASKS.glob("mask_*.png")):
    arr2 = np.array(Image.open(f).convert('L'))
    if arr2.max() == 0: continue          # skip zeroed-out masks
    after_masks.append((f.stem.replace('mask_',''), arr2 > 127))

# ── build composite ────────────────────────────────────────────────
CELL = 180
PAD  = 8
LABEL_H = 28

def make_row(title, items):
    n = len(items) + 1          # +1 for source
    W = PAD + (CELL + PAD) * n
    H = PAD + CELL + LABEL_H + PAD
    row = Image.new("RGB", (W, H), (17,17,17))
    draw = ImageDraw.Draw(row)

    # section title on the left edge (vertical)
    draw.text((2, PAD + CELL//2 - 6), title, fill=(255,160,0))

    # source thumb
    x = PAD
    thumb = src_img.resize((CELL, CELL), Image.LANCZOS)
    row.paste(thumb, (x, PAD))
    draw.text((x, PAD + CELL + 2), "SOURCE", fill=(255,160,0))
    x += CELL + PAD

    for label, mask in items:
        mask_arr = (mask.astype(np.uint8))*255
        thumb = Image.fromarray(mask_arr).resize((CELL, CELL), Image.NEAREST)
        row.paste(thumb, (x, PAD))
        # truncate label for display
        short = label[:14]
        draw.text((x, PAD + CELL + 2), short, fill=(160,160,160))
        x += CELL + PAD

    return row

row_before = make_row("BEFORE", before_masks)
row_after  = make_row("AFTER ", after_masks)

# divider
divW = max(row_before.width, row_after.width)
divider = Image.new("RGB", (divW, 4), (60,60,60))

total_h = row_before.height + 4 + row_after.height
comp = Image.new("RGB", (divW, total_h), (17,17,17))
comp.paste(row_before, (0, 0))
comp.paste(divider,    (0, row_before.height))
comp.paste(row_after,  (0, row_before.height + 4))
comp.save(OUT)
print(f"Saved: {OUT}")
print(f"Before masks: {len(before_masks)}  After masks: {len(after_masks)}")
