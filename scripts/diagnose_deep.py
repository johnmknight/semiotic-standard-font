"""Deep diagnostic: show per-row brightness for problematic icons"""
import re, base64, io, os
from PIL import Image
import numpy as np

SRC = r"C:\Users\john_\dev\semiotic-standard-font\from john"

for name in ["allergen_warning", "food_heating", "contaminated", "frozen_goods", "hydroponic", "potable_water"]:
    path = os.path.join(SRC, name + ".svg")
    with open(path, 'r', encoding='utf-8') as f: c = f.read()
    m = re.search(r'href="data:image/png;base64,([^"]+)"', c)
    img = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
    arr = np.array(img)
    gray = np.mean(arr[:,:,:3], axis=2)
    h, w = gray.shape
    
    margin = max(w // 5, 10)
    strip = gray[:, margin:w-margin]
    row_avg = np.mean(strip, axis=1)
    
    print(f"\n{'='*60}")
    print(f"  {name} ({w}x{h})")
    print(f"{'='*60}")
    # Show brightness profile every 5 rows
    for r in range(0, h, 5):
        bar = '#' * int(row_avg[r] / 5)
        bright = '***' if row_avg[r] > 160 else '   '
        print(f"  row {r:3d}: {row_avg[r]:6.1f} {bright} {bar}")
