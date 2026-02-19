from PIL import Image
import numpy as np

# Load the original source PNG
import re, base64, io
with open(r"C:\Users\john_\dev\semiotic-standard-font\from john\alcohol.svg", 'r', encoding='utf-8') as f:
    content = f.read()
m = re.search(r'href="data:image/png;base64,([^"]+)"', content)
png_data = base64.b64decode(m.group(1))
img = Image.open(io.BytesIO(png_data)).convert('RGB')
arr = np.array(img)
h, w = arr.shape[:2]

print(f"Image: {w}x{h}")
print("\nRow brightness profile (center column strip):")
gray = np.mean(arr[:,:,:3], axis=2)

# Show brightness per row for center strip
center_strip = gray[:, w//3:2*w//3]
for row in range(0, h, 4):
    avg = np.mean(center_strip[row])
    bar = '#' * int(avg / 5)
    print(f"  Row {row:3d}: {avg:6.1f}  {bar}")

print("\nCol brightness profile (center row strip):")
center_hstrip = gray[h//3:2*h//3, :]
for col in range(0, w, 4):
    avg = np.mean(center_hstrip[:, col])
    print(f"  Col {col:3d}: {avg:6.1f}")
