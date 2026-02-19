from PIL import Image
import numpy as np

img = Image.open(r"C:\Users\john_\dev\semiotic-standard-font\preview\debug\alcohol_crop.png").convert('RGB')
arr = np.array(img)
print(f"Shape: {arr.shape}")

# Sample pixel values across the image
h, w = arr.shape[:2]
print("\nPixel samples (R,G,B):")
for name, y, x in [
    ("Top-left", 5, 5),
    ("Top-center", 5, w//2),
    ("Center", h//2, w//2),
    ("Mid-left", h//2, 5),
    ("Bottom-center", h-5, w//2),
    ("Quarter-down center", h//4, w//2),
]:
    if y < h and x < w:
        print(f"  {name} ({x},{y}): {arr[y,x]}")

# Histogram of brightness values
gray = np.mean(arr, axis=2)
for thresh in [0, 30, 60, 90, 120, 150, 180, 210, 240]:
    count = np.sum((gray >= thresh) & (gray < thresh+30))
    pct = count / gray.size * 100
    bar = '#' * int(pct)
    print(f"  [{thresh:3d}-{thresh+29:3d}]: {count:6d} ({pct:5.1f}%) {bar}")
