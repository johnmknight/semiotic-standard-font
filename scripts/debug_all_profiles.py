"""
Debug: Look at the actual pixel structure of several icons to understand
the separator line pattern.
"""
import re, os, base64, io
import numpy as np
from PIL import Image

SRC_DIR = r"C:\Users\john_\dev\semiotic-standard-font\from john"

def get_img(name):
    with open(os.path.join(SRC_DIR, name + ".svg"), 'r', encoding='utf-8') as f:
        c = f.read()
    m = re.search(r'href="data:image/png;base64,([^"]+)"', c)
    return Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')

for name in ["alcohol", "grain", "protein", "utensils", "beverage_dispenser", "fresh_produce"]:
    img = get_img(name)
    arr = np.array(img)
    gray = np.mean(arr[:,:,:3], axis=2)
    h, w = gray.shape
    
    margin = max(w // 5, 10)
    strip = gray[:, margin:w-margin]
    row_avg = np.mean(strip, axis=1)
    
    print(f"\n=== {name} ({w}x{h}) ===")
    print("Row profile (every 2 rows):")
    
    prev_zone = None
    for row in range(h):
        avg = row_avg[row]
        if avg < 60: zone = "DARK"
        elif avg < 130: zone = "MED"
        elif avg < 170: zone = "TRANS"
        else: zone = "BRIGHT"
        
        if zone != prev_zone:
            bar = '#' * int(avg / 8)
            print(f"  Row {row:3d}: {avg:6.1f} [{zone:6s}] {bar}")
            prev_zone = zone
