"""
inspect_icon.py - Deep color analysis for grain and hydroponic
Prints pixel color histogram and saves a false-color visualization.
"""
import numpy as np
from PIL import Image
from pathlib import Path

MASKS_DIR = Path(r"C:\Users\john_\dev\semiotic-standard-font\svg\masks")

def analyze(icon_name):
    src = MASKS_DIR / icon_name / "_source.png"
    img = Image.open(src).convert("RGB")
    arr = np.array(img)
    h, w = arr.shape[:2]
    pixels = arr.reshape(-1, 3)

    print(f"\n{'='*50}")
    print(f"ICON: {icon_name}  ({w}x{h})")
    print(f"{'='*50}")

    # Convert to HSV for better color inspection
    img_hsv = img.convert("HSV") if hasattr(Image, "HSV") else None

    # Bucket by hue ranges using numpy
    r, g, b = pixels[:,0], pixels[:,1], pixels[:,2]

    # Compute simple hue approximation (0-360)
    rf, gf, bf = r/255.0, g/255.0, b/255.0
    maxc = np.maximum(np.maximum(rf, gf), bf)
    minc = np.minimum(np.minimum(rf, gf), bf)
    delta = maxc - minc
    sat = np.where(maxc > 0, delta/maxc, 0)
    val = maxc

    # Classify each pixel
    low_sat = sat < 0.15  # near-grey/white/black
    dark = val < 0.15
    bright = val > 0.85

    print(f"Near-black (val<0.15):           {dark.sum():6d} px  {dark.mean()*100:.1f}%")
    print(f"Near-white (val>0.85, sat<0.15): {(bright & low_sat).sum():6d} px  {(bright & low_sat).mean()*100:.1f}%")
    print(f"Colorful   (sat>=0.15):          {(~low_sat).sum():6d} px  {(~low_sat).mean()*100:.1f}%")

    # Among colorful pixels, what hues?
    colorful = ~low_sat & ~dark
    if colorful.sum() > 0:
        # hue in degrees
        hue = np.zeros(len(pixels))
        nonzero = delta > 0
        # hue calc
        rmx = (maxc == rf) & nonzero
        gmx = (maxc == gf) & nonzero
        bmx = (maxc == bf) & nonzero
        hue[rmx] = (60 * ((gf[rmx]-bf[rmx])/delta[rmx])) % 360
        hue[gmx] = (60 * ((bf[gmx]-rf[gmx])/delta[gmx]) + 120) % 360
        hue[bmx] = (60 * ((rf[bmx]-gf[bmx])/delta[bmx]) + 240) % 360

        colorful_hues = hue[colorful]
        print(f"\n  Colorful pixel hue distribution:")
        buckets = [
            ("Red/Orange (0-30)",    (colorful_hues < 30) | (colorful_hues >= 330)),
            ("Orange (30-60)",       (colorful_hues >= 30) & (colorful_hues < 60)),
            ("Yellow (60-90)",       (colorful_hues >= 60) & (colorful_hues < 90)),
            ("Yellow-Green (90-120)",(colorful_hues >= 90) & (colorful_hues < 120)),
            ("Green (120-180)",      (colorful_hues >= 120) & (colorful_hues < 180)),
            ("Cyan (180-210)",       (colorful_hues >= 180) & (colorful_hues < 210)),
            ("Blue (210-270)",       (colorful_hues >= 210) & (colorful_hues < 270)),
            ("Purple (270-330)",     (colorful_hues >= 270) & (colorful_hues < 330)),
        ]
        for name, mask in buckets:
            count = mask.sum()
            if count > 10:
                # Sample mean RGB of these pixels
                idxs = np.where(colorful)[0][mask]
                mean_rgb = pixels[idxs].mean(axis=0).astype(int)
                print(f"    {name:<28} {count:5d} px  avg RGB({mean_rgb[0]},{mean_rgb[1]},{mean_rgb[2]})")
    else:
        print("  No colorful pixels found — truly monochrome icon!")

    # Show the actual distinct color bands by scanning brightness profile
    print(f"\n  Row brightness profile (avg value per row, 10-row chunks):")
    for row_start in range(0, h, h//10):
        row_end = min(row_start + h//10, h)
        chunk = arr[row_start:row_end]
        avg_brightness = chunk.mean(axis=(0,1))
        avg_sat_chunk = sat.reshape(h,w)[row_start:row_end].mean()
        print(f"    rows {row_start:3d}-{row_end:3d}: RGB({avg_brightness[0]:.0f},{avg_brightness[1]:.0f},{avg_brightness[2]:.0f})  sat={avg_sat_chunk:.2f}")

for icon in ["grain", "hydroponic"]:
    analyze(icon)
