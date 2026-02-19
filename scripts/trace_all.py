"""
Trace all 16 icons with OpenCV at epsilon=1.3
Output: work/{name}_4_traced.svg
"""
import cv2
import numpy as np
import os

WORK_DIR = r"C:\Users\john_\dev\semiotic-standard-font\work"
EPS = 1.3

ICONS = [
    "alcohol","allergen_warning","beverage_dispenser","contaminated",
    "emergency_rations","food_heating","fresh_produce","frozen_goods",
    "grain","hydroponic","organic_waste","potable_water",
    "protein","rations","utensils","water_filtration"
]

for name in ICONS:
    src = os.path.join(WORK_DIR, f"{name}_3_cropped.png")
    out = os.path.join(WORK_DIR, f"{name}_4_traced.svg")

    img = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"  SKIP {name} - file not found")
        continue
    h, w = img.shape

    _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    paths = []
    total_pts = 0
    for cnt in contours:
        if len(cnt) < 3:
            continue
        s = cv2.approxPolyDP(cnt, EPS, closed=True)
        total_pts += len(s)
        pts = s.reshape(-1, 2)
        d = f"M {pts[0][0]},{pts[0][1]}"
        for p in pts[1:]:
            d += f" L{p[0]},{p[1]}"
        d += " Z"
        paths.append(d)

    combined = " ".join(paths)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
           f'<path d="{combined}" fill="black" fill-rule="evenodd"/></svg>')

    with open(out, 'w') as f:
        f.write(svg)
    print(f"  {name}: {len(contours)} contours, {total_pts} pts -> {name}_4_traced.svg")

print("\nDone.")
