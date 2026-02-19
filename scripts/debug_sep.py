from PIL import Image
import numpy as np, re, base64, io

with open(r"C:\Users\john_\dev\semiotic-standard-font\from john\alcohol.svg", 'r', encoding='utf-8') as f:
    c = f.read()
m = re.search(r'href="data:image/png;base64,([^"]+)"', c)
img = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
arr = np.array(img)
gray = np.mean(arr[:,:,:3], axis=2)
h, w = gray.shape
strip = gray[:, w//3:2*w//3]

print("Rows 80-120 brightness (looking for separator):")
for row in range(80, 120):
    avg = np.mean(strip[row])
    marker = " <-- SEPARATOR?" if avg > 170 and np.mean(strip[min(row+3, h-1)]) < 150 else ""
    print(f"  Row {row}: {avg:.1f}{marker}")

print("\nFull interior strip, marking transitions:")
prev_zone = None
for row in range(h):
    avg = np.mean(strip[row])
    if avg < 80:
        zone = "DARK"
    elif avg < 150:
        zone = "SYMBOL"
    elif avg < 180:
        zone = "TRANSITION"
    else:
        zone = "BRIGHT"
    
    if zone != prev_zone:
        print(f"  Row {row}: {avg:.1f} -- ZONE: {zone}")
        prev_zone = zone
