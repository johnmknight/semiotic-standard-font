import re, os, base64, io
import numpy as np
from PIL import Image

src_dir = r"C:\Users\john_\dev\semiotic-standard-font\from john"

icons = [
    "alcohol", "allergen_warning", "beverage_dispenser", "contaminated",
    "emergency_rations", "food_heating", "fresh_produce", "frozen_goods",
    "grain", "hydroponic", "organic_waste", "potable_water",
    "protein", "rations", "utensils", "water_filtration"
]

print("=== SOURCE PNG ANALYSIS: Frame vs Symbol Boundaries ===\n")

for icon in icons:
    fname = icon + ".svg"
    fpath = os.path.join(src_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    m = re.search(r'href="data:image/png;base64,([^"]+)"', content)
    if not m:
        print(f"{icon}: NO BASE64 IMAGE")
        continue
    
    png_data = base64.b64decode(m.group(1))
    img = Image.open(io.BytesIO(png_data)).convert('RGBA')
    arr = np.array(img)
    w, h = img.size
    
    # Analyze: find the frame (outer border) and symbol regions
    # The Cobb icons have: dark background, colored frame border, 
    # separator line, then symbol below
    
    # Convert to grayscale for boundary detection
    gray = np.mean(arr[:,:,:3], axis=2)
    
    # Find rows/cols with non-background content
    # Background is typically very dark (< 30) or very light
    # The frame border is the outermost non-background region
    # The symbol is interior content
    
    # Detect the outer frame boundary (first/last rows/cols with bright pixels)
    threshold = 60
    bright_mask = gray > threshold
    
    rows_with_content = np.any(bright_mask, axis=1)
    cols_with_content = np.any(bright_mask, axis=0)
    
    if not np.any(rows_with_content):
        print(f"{icon}: No bright content found")
        continue
    
    row_indices = np.where(rows_with_content)[0]
    col_indices = np.where(cols_with_content)[0]
    
    frame_top = row_indices[0]
    frame_bot = row_indices[-1]
    frame_left = col_indices[0]
    frame_right = col_indices[-1]
    
    # Now find the separator line - typically a horizontal bright line
    # that divides the icon label area from the symbol area
    # Look for rows that are mostly bright across the middle
    mid_cols = bright_mask[:, w//4:3*w//4]
    row_brightness = np.mean(mid_cols, axis=1)
    
    # The separator line will be a local maximum in brightness
    # between the top frame edge and ~40% down
    search_start = frame_top + 5
    search_end = frame_top + int((frame_bot - frame_top) * 0.45)
    
    sep_line = None
    if search_end > search_start:
        search_region = row_brightness[search_start:search_end]
        if len(search_region) > 0:
            peaks = []
            for i in range(1, len(search_region)-1):
                if search_region[i] > 0.5 and search_region[i] > search_region[i-1] and search_region[i] > search_region[i+1]:
                    peaks.append((search_region[i], i + search_start))
            if peaks:
                peaks.sort(reverse=True)
                sep_line = peaks[0][1]
    
    # Symbol region is below separator (or below top ~30% if no separator found)
    if sep_line:
        symbol_top = sep_line + 2
    else:
        symbol_top = frame_top + int((frame_bot - frame_top) * 0.30)
    
    symbol_bot = frame_bot - 2
    symbol_left = frame_left + 2
    symbol_right = frame_right - 2
    
    # Check for actual symbol content in that region
    symbol_region = bright_mask[symbol_top:symbol_bot, symbol_left:symbol_right]
    sym_rows = np.any(symbol_region, axis=1)
    sym_cols = np.any(symbol_region, axis=0)
    
    if np.any(sym_rows) and np.any(sym_cols):
        sym_r = np.where(sym_rows)[0]
        sym_c = np.where(sym_cols)[0]
        actual_sym_top = symbol_top + sym_r[0]
        actual_sym_bot = symbol_top + sym_r[-1]
        actual_sym_left = symbol_left + sym_c[0]
        actual_sym_right = symbol_left + sym_c[-1]
    else:
        actual_sym_top = symbol_top
        actual_sym_bot = symbol_bot
        actual_sym_left = symbol_left
        actual_sym_right = symbol_right
    
    print(f"{icon} ({w}x{h}):")
    print(f"  Frame:  T={frame_top} B={frame_bot} L={frame_left} R={frame_right}")
    print(f"  Sep line: {sep_line if sep_line else 'not found'}")
    print(f"  Symbol: T={actual_sym_top} B={actual_sym_bot} L={actual_sym_left} R={actual_sym_right}")
    print(f"  Symbol size: {actual_sym_right-actual_sym_left}x{actual_sym_bot-actual_sym_top}")
    print(f"  Margins from frame: top={actual_sym_top-frame_top} bot={frame_bot-actual_sym_bot} L={actual_sym_left-frame_left} R={frame_right-actual_sym_right}")
    print()
