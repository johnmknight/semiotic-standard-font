import re, os, base64
from PIL import Image
import io

src_dir = r"C:\Users\john_\dev\semiotic-standard-font\from john"
mono_dir = r"C:\Users\john_\dev\semiotic-standard-font\svg\mono"
ext_dir = r"C:\Users\john_\dev\semiotic-standard-font\svg\mono\extended"
out_dir = r"C:\Users\john_\dev\semiotic-standard-font\preview\compare"
os.makedirs(out_dir, exist_ok=True)

# Extract PNGs from source SVGs to see originals
for fname in os.listdir(src_dir):
    if not fname.endswith('.svg'):
        continue
    with open(os.path.join(src_dir, fname), 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'href="data:image/png;base64,([^"]+)"', content)
    if m:
        png_data = base64.b64decode(m.group(1))
        img = Image.open(io.BytesIO(png_data))
        out_name = fname.replace('.svg', '.png')
        img.save(os.path.join(out_dir, out_name))
        print(f"{fname} -> {img.size}")
    else:
        print(f"{fname}: no base64 image found")
