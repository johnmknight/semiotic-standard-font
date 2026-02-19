"""
Step 1-3: Extract PNG, B&W, crop Cobb borders.

Uses color image to find the innermost dark-red frame band on each edge,
then adds a fixed inset of 12px to clear the remaining white band + black inner ring.

Run: python scripts/step1_extract.py alcohol
     python scripts/step1_extract.py --all
"""
import re, os, base64, io, sys
import numpy as np
from PIL import Image, ImageDraw

SRC_DIR  = r"C:\Users\john_\dev\semiotic-standard-font\from john"
OUT_DIR  = r"C:\Users\john_\dev\semiotic-standard-font\preview\debug"
WORK_DIR = r"C:\Users\john_\dev\semiotic-standard-font\work"
os.makedirs(OUT_DIR,  exist_ok=True)
os.makedirs(WORK_DIR, exist_ok=True)

ICONS = [
    "alcohol","allergen_warning","beverage_dispenser","contaminated",
    "emergency_rations","food_heating","fresh_produce","frozen_goods",
    "grain","hydroponic","organic_waste","potable_water",
    "protein","rations","utensils","water_filtration"
]

def extract_png(name):
    path = os.path.join(SRC_DIR, name + ".svg")
    with open(path, "r", encoding="utf-8") as f: c = f.read()
    m = re.search(r'href="data:image/png;base64,([^"]+)"', c)
    if not m: raise ValueError(f"No embedded PNG in {path}")
    img = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert("RGB")
    img.save(os.path.join(WORK_DIR, f"{name}_1_source.png"))
    print(f"  [1] Extracted {img.size}")
    return img

def to_bw(img, name, threshold=128):
    gray_arr = np.array(img.convert("L"))
    bw = np.where(gray_arr < threshold, 0, 255).astype(np.uint8)
    Image.fromarray(bw).save(os.path.join(WORK_DIR, f"{name}_2_bw.png"))
    print(f"  [2] B&W saved")
    return bw

def find_interior(color_img, name):
    """
    Find the innermost red band on each edge using COLOR data,
    then add INSET pixels to land cleanly past the white band + black ring.
    """
    arr  = np.array(color_img)
    gray = np.mean(arr[:,:,:3], axis=2)
    h, w = arr.shape[:2]

    cx0, cx1 = w // 4, 3 * w // 4
    cy0, cy1 = h // 4, 3 * h // 4

    # After the innermost red band, add this many pixels to clear remaining frame
    INSET = 15
    EXIT_RUN = 5  # consecutive non-red rows to confirm we passed the band

    def is_red(strip):
        r, g, b = strip[:,0].astype(float), strip[:,1].astype(float), strip[:,2].astype(float)
        return np.sum((r > 70) & (g < 40) & (b < 40)) > len(strip) * 0.05

    def find_innermost_red_edge(start, end, step, axis):
        """Walk from edge inward. Return the index just past the last red band."""
        saw_red = False
        non_red_run = 0
        last_red = start
        for i in range(start, end, step):
            strip = arr[i, cx0:cx1, :3] if axis == 'row' else arr[cy0:cy1, i, :3]
            if is_red(strip):
                saw_red = True
                last_red = i
                non_red_run = 0
            elif saw_red:
                non_red_run += 1
                if non_red_run >= EXIT_RUN:
                    # Return: last_red + step puts us just past the band,
                    # then add INSET to clear the white band + black inner ring
                    return last_red + step * (1 + INSET)
        return start  # fallback: no red found

    top    = find_innermost_red_edge(0,   h,   +1, 'row')
    bottom = find_innermost_red_edge(h-1, -1,  -1, 'row')
    left   = find_innermost_red_edge(0,   w,   +1, 'col')
    right  = find_innermost_red_edge(w-1, -1,  -1, 'col')

    if top >= bottom or left >= right:
        print(f"  [3] WARNING: bad bounds, using 10% inset fallback")
        top, bottom, left, right = h//10, 9*h//10, w//10, 9*w//10

    print(f"  [3] Interior: t={top} b={bottom} l={left} r={right}  ({right-left}x{bottom-top}px)")

    diag = Image.fromarray(np.stack([gray.astype(np.uint8)]*3, axis=2))
    draw = ImageDraw.Draw(diag)
    draw.rectangle([left, top, right, bottom], outline=(0,255,0), width=2)
    draw.line([(0,top),(w,top)],       fill=(255,100,0), width=1)
    draw.line([(0,bottom),(w,bottom)], fill=(255,100,0), width=1)
    draw.line([(left,0),(left,h)],     fill=(255,100,0), width=1)
    draw.line([(right,0),(right,h)],   fill=(255,100,0), width=1)
    diag.save(os.path.join(OUT_DIR, f"{name}_3_bounds.png"))
    return top, bottom, left, right

def crop_interior(bw, top, bottom, left, right, name):
    crop = Image.fromarray(bw[top:bottom+1, left:right+1])
    crop.save(os.path.join(WORK_DIR, f"{name}_3_cropped.png"))
    print(f"  [3] Cropped: {crop.size}")
    return crop

def process(name):
    print(f"\n{'='*50}  {name}")
    img        = extract_png(name)
    bw         = to_bw(img, name)
    t, b, l, r = find_interior(img, name)
    crop_interior(bw, t, b, l, r, name)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        for icon in ICONS:
            try: process(icon)
            except Exception as e: print(f"  ERROR {icon}: {e}")
    else:
        process(sys.argv[1] if len(sys.argv) > 1 else "alcohol")
