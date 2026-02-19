"""
Generate epsilon variants for flagged icons: alcohol, emergency_rations, frozen_goods, rations
"""
import cv2
import numpy as np
import os

WORK_DIR = r"C:\Users\john_\dev\semiotic-standard-font\work"
FLAGGED = ["alcohol", "emergency_rations", "frozen_goods", "rations"]
EPSILONS = [1.0, 1.1, 1.2, 1.3]

for name in FLAGGED:
    src = os.path.join(WORK_DIR, f"{name}_3_cropped.png")
    img = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    for eps in EPSILONS:
        paths = []
        total_pts = 0
        for cnt in contours:
            if len(cnt) < 3: continue
            s = cv2.approxPolyDP(cnt, eps, closed=True)
            total_pts += len(s)
            pts = s.reshape(-1, 2)
            d = f"M {pts[0][0]},{pts[0][1]}"
            for p in pts[1:]: d += f" L{p[0]},{p[1]}"
            d += " Z"
            paths.append(d)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
               f'<path d="{" ".join(paths)}" fill="black" fill-rule="evenodd"/></svg>')
        label = str(eps).replace('.', '_')
        out = os.path.join(WORK_DIR, f"{name}_eps_{label}.svg")
        with open(out, 'w') as f: f.write(svg)
        print(f"  {name} e={eps}: {total_pts} pts")
