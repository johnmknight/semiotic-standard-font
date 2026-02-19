import re, base64, io
import numpy as np
from PIL import Image

with open(r"C:\Users\john_\dev\semiotic-standard-font\from john\alcohol.svg", 'r', encoding='utf-8') as f:
    content = f.read()
m = re.search(r'href="data:image/png;base64,([^"]+)"', content)
img = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
arr = np.array(img)
gray = np.mean(arr[:,:,:3], axis=2)
h, w = gray.shape

margin_x = int(w * 0.20)
print(f"Image: {w}x{h}, margin_x={margin_x}, sampling cols [{margin_x}:{w-margin_x}]")
print(f"\nRow brightness profile (20% margin strip):")
for r in range(0, h, 2):
    val = np.mean(gray[r, margin_x:w-margin_x])
    bar = '#' * int(val / 4)
    label = ""
    if val > 160:
        label = " <-- BRIGHT"
    elif val < 60:
        label = " <-- DARK"
    print(f"  {r:3d}: {val:6.1f} {bar}{label}")
