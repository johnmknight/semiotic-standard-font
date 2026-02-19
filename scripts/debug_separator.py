import re, base64, io
import numpy as np
from PIL import Image

# Check multiple icons to find a consistent separator detection strategy
icons_to_check = ["alcohol", "grain", "protein", "fresh_produce"]

for icon_name in icons_to_check:
    fname = icon_name + ".svg"
    with open(rf"C:\Users\john_\dev\semiotic-standard-font\from john\{fname}", 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'href="data:image/png;base64,([^"]+)"', content)
    img = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
    arr = np.array(img)
    gray = np.mean(arr[:,:,:3], axis=2)
    h, w = gray.shape
    
    margin = int(w * 0.25)
    strip = gray[:, margin:w-margin]
    
    print(f"\n{'='*50}")
    print(f"{icon_name} ({w}x{h})")
    print(f"{'='*50}")
    
    # For each row, compute: avg brightness AND % of pixels that are dark (<120)
    for r in range(0, h, 4):
        row_data = strip[r]
        avg = np.mean(row_data)
        dark_pct = np.sum(row_data < 120) / len(row_data) * 100
        dark_bar = 'D' * int(dark_pct / 2)
        bright_bar = 'B' * int(avg / 8)
        
        if dark_pct > 15:
            label = f" ** {dark_pct:.0f}% dark"
        else:
            label = ""
        
        print(f"  {r:3d}: avg={avg:5.1f} dark={dark_pct:4.1f}% {dark_bar}{label}")
