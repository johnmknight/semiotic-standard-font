"""
OpenCV contour trace comparison for alcohol_3_cropped.png
Produces 3 variants: raw, smooth e=1.5, smooth e=3.0
Correctly handles holes via RETR_CCOMP hierarchy.
"""
import cv2
import numpy as np

SRC  = r"C:\Users\john_\dev\semiotic-standard-font\work\alcohol_3_cropped.png"
OUT  = r"C:\Users\john_\dev\semiotic-standard-font\work\alcohol_cv_{variant}.svg"

img  = cv2.imread(SRC, cv2.IMREAD_GRAYSCALE)
h, w = img.shape
print(f"Image: {w}x{h}")

_, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
hier = hierarchy[0]  # shape: (N, 4) = [next, prev, first_child, parent]
print(f"Contours found: {len(contours)}")
for i, cnt in enumerate(contours):
    print(f"  [{i}] pts={len(cnt)}  parent={hier[i][3]}")

def make_svg(contours, hier, w, h, epsilon=None):
    """Build SVG with proper hole handling.
    Top-level contours (parent==-1) are outer shapes (fill).
    Children (parent>=0) are holes (fill with white / use evenodd).
    """
    paths = []
    for i, cnt in enumerate(contours):
        if len(cnt) < 3:
            continue
        if epsilon:
            cnt = cv2.approxPolyDP(cnt, epsilon, closed=True)
        pts = cnt.reshape(-1, 2)
        d = f"M {pts[0][0]},{pts[0][1]} "
        d += " ".join(f"L{p[0]},{p[1]}" for p in pts[1:])
        d += " Z"
        paths.append(d)

    combined = " ".join(paths)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">
  <path d="{combined}" fill="black" fill-rule="evenodd"/>
</svg>'''

for label, eps in [("raw", None), ("smooth15", 1.5), ("smooth30", 3.0)]:
    svg = make_svg(contours, hier, w, h, epsilon=eps)
    path = OUT.format(variant=label)
    with open(path, 'w') as f:
        f.write(svg)
    print(f"Saved: {path}")

print("Done")
