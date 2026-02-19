"""
trace_grain_from_mask.py
Trace grain directly from the brightness_symbol mask PNG.
Skips the color extraction / crop logic in trace_v2 and feeds
the clean mask straight into vtracer, then normalizes to 1000x1000.
"""
import os, re
import numpy as np
from PIL import Image
import vtracer

MASK_PATH = r"C:\Users\john_\dev\semiotic-standard-font\svg\masks\grain\mask_brightness_symbol.png"
OUT_PATH  = r"C:\Users\john_\dev\semiotic-standard-font\svg\mono\extended\ss-grain.svg"
DEBUG_DIR = r"C:\Users\john_\dev\semiotic-standard-font\preview\debug"
os.makedirs(DEBUG_DIR, exist_ok=True)

# Load mask - already clean B&W
mask = Image.open(MASK_PATH).convert("L")
mask_arr = np.array(mask)
h, w = mask_arr.shape

# Tight crop to content bounding box
rows = np.any(mask_arr > 127, axis=1)
cols = np.any(mask_arr > 127, axis=0)
r0, r1 = np.where(rows)[0][[0,-1]]
c0, c1 = np.where(cols)[0][[0,-1]]
pad = 4
r0 = max(0, r0-pad); r1 = min(h-1, r1+pad)
c0 = max(0, c0-pad); c1 = min(w-1, c1+pad)
cropped = mask.crop((c0, r0, c1+1, r1+1))
print(f"Mask size: {w}x{h}, cropped to: {cropped.size}")

# Save cropped for debug
bw_path = os.path.join(DEBUG_DIR, "grain_mask_bw.png")
cropped.save(bw_path)

# Trace with vtracer
traced_path = os.path.join(DEBUG_DIR, "grain_traced_raw.svg")
vtracer.convert_image_to_svg_py(
    bw_path, traced_path,
    colormode="binary", mode="polygon",
    filter_speckle=4, corner_threshold=60,
    length_threshold=4.0, splice_threshold=45,
    path_precision=2
)
svg = open(traced_path, encoding='utf-8').read()
print(f"Raw SVG: {len(re.findall(r'<path', svg))} paths, {len(svg)} chars")

# Normalize to 1000x1000
def normalize(svg_str, target=1000):
    paths = re.findall(r'<path d="([^"]+)"[^>]*/>', svg_str)
    if not paths:
        paths = re.findall(r'<path[^>]*d="([^"]+)"', svg_str)

    all_x, all_y = [], []
    for d in paths:
        nums = [float(n) for n in re.findall(r'-?\d+\.?\d*', d)]
        for i in range(0, len(nums)-1, 2):
            all_x.append(nums[i]); all_y.append(nums[i+1])

    if not all_x: return None
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    sw, sh = max_x - min_x, max_y - min_y
    if sw == 0 or sh == 0: return None

    usable = target * 0.9
    scale = min(usable/sw, usable/sh)
    ox = (target - sw*scale)/2 - min_x*scale
    oy = (target - sh*scale)/2 - min_y*scale

    def xform(d):
        tokens = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|-?\d+\.?\d*', d)
        out = []; i = 0
        while i < len(tokens):
            t = tokens[i]
            if re.match(r'[Zz]', t):
                out.append(t); i += 1
            elif re.match(r'[MLCSQT]', t):
                out.append(t); i += 1
                while i < len(tokens) and re.match(r'-?\d', tokens[i]):
                    out.append(f"{float(tokens[i])*scale+ox:.1f}")
                    out.append(f"{float(tokens[i+1])*scale+oy:.1f}")
                    i += 2
            else:
                out.append(t); i += 1
        return " ".join(out)

    path_elements = "\n".join(f'  <path d="{xform(d)}" fill-rule="evenodd"/>' for d in paths)
    print(f"Normalized: src {sw:.0f}x{sh:.0f} -> scale={scale:.3f}, fill={sw*scale/target*100:.0f}%x{sh*scale/target*100:.0f}%")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {target} {target}">\n{path_elements}\n</svg>'

final = normalize(svg)
if final:
    open(OUT_PATH, 'w', encoding='utf-8').write(final)
    print(f"Saved: {OUT_PATH}")
else:
    print("ERROR: normalization failed")
