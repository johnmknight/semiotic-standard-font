"""Diagnose each source icon's brightness profile and crop viability"""
import re, base64, io, os
from PIL import Image
import numpy as np

SRC = r"C:\Users\john_\dev\semiotic-standard-font\from john"

icons = ["alcohol","allergen_warning","beverage_dispenser","contaminated",
         "emergency_rations","food_heating","fresh_produce","frozen_goods",
         "grain","hydroponic","organic_waste","potable_water",
         "protein","rations","utensils","water_filtration"]

for name in icons:
    path = os.path.join(SRC, name + ".svg")
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    m = re.search(r'href="data:image/png;base64,([^"]+)"', c)
    if not m:
        print(f"{name}: NO PNG FOUND")
        continue
    img = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
    arr = np.array(img)
    gray = np.mean(arr[:,:,:3], axis=2)
    h, w = gray.shape
    
    row_avg = np.mean(gray[:, max(w//5,10):w-max(w//5,10)], axis=1)
    
    # Find sustained bright regions (the interior detection logic)
    def find_sustained(avg, start, end, step):
        count = 0
        first = None
        for i in range(start, end, step):
            if avg[i] > 160:
                count += 1
                if first is None: first = i
                if count >= 10: return first
            else:
                count = 0
                first = None
        return start if step > 0 else end
    
    it = find_sustained(row_avg, 0, h, 1)
    ib = find_sustained(row_avg, h-1, -1, -1)
    
    # Brightness stats
    top10 = row_avg[:10].mean()
    mid10 = row_avg[h//2-5:h//2+5].mean()
    bot10 = row_avg[-10:].mean()
    max_bright = row_avg.max()
    
    int_h = ib - it
    status = "OK" if int_h > 10 else "FAIL"
    
    print(f"{name:25s} {w:3d}x{h:3d}  top={top10:5.1f} mid={mid10:5.1f} bot={bot10:5.1f} max={max_bright:5.1f}  interior=[{it}:{ib}] h={int_h:3d}  {status}")
