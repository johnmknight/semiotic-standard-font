import cv2
import numpy as np

SRC = r'C:\Users\john_\dev\semiotic-standard-font\work\alcohol_3_cropped.png'
img = cv2.imread(SRC, cv2.IMREAD_GRAYSCALE)
h, w = img.shape
_, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

for eps_10 in range(10, 16):
    eps = eps_10 / 10.0
    paths = []
    total_pts = 0
    for cnt in contours:
        if len(cnt) < 3: continue
        s = cv2.approxPolyDP(cnt, eps, closed=True)
        total_pts += len(s)
        pts = s.reshape(-1, 2)
        d = 'M ' + str(pts[0][0]) + ',' + str(pts[0][1])
        for p in pts[1:]:
            d += ' L' + str(p[0]) + ',' + str(p[1])
        d += ' Z'
        paths.append(d)
    combined = ' '.join(paths)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><path d="{combined}" fill="black" fill-rule="evenodd"/></svg>'
    label = str(eps).replace('.', '_')
    fname = fr'C:\Users\john_\dev\semiotic-standard-font\work\alcohol_eps_{label}.svg'
    with open(fname, 'w') as f:
        f.write(svg)
    print(f'eps={eps}: {total_pts} pts -> alcohol_eps_{label}.svg')
