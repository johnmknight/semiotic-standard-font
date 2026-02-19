"""
Semiotic Standard SVG Trace Pipeline v2
- Detects Cobb frame border (alternating dark/bright bands)  
- Crops to interior only
- Uses adaptive threshold per-icon for symbol extraction
- Traces with vtracer, normalizes to 1000x1000
"""
import re, os, base64, io, sys
import numpy as np
from PIL import Image

try:
    import vtracer
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "vtracer", "--quiet"])
    import vtracer

SRC_DIR = r"C:\Users\john_\dev\semiotic-standard-font\from john"
OUT_MONO = r"C:\Users\john_\dev\semiotic-standard-font\svg\mono"
OUT_EXT = r"C:\Users\john_\dev\semiotic-standard-font\svg\mono\extended"
DEBUG_DIR = r"C:\Users\john_\dev\semiotic-standard-font\preview\debug"
os.makedirs(DEBUG_DIR, exist_ok=True)

def extract_png(svg_path):
    with open(svg_path, 'r', encoding='utf-8') as f: c = f.read()
    m = re.search(r'href="data:image/png;base64,([^"]+)"', c)
    if not m: return None
    return Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')

def find_interior_bounds(gray):
    """
    Find the interior of a Cobb icon by detecting the frame border pattern.
    The Cobb frame has 3 concentric rounded-rect borders creating 
    alternating dark/bright bands. The interior starts after the last band.
    
    We detect this by finding the first SUSTAINED bright region (>10 consecutive
    rows of avg brightness > 160) — that's the interior, not the frame border
    bright bands which are only 1-3 rows wide.
    """
    h, w = gray.shape
    margin = max(w // 5, 10)
    strip = gray[:, margin:w-margin]
    row_avg = np.mean(strip, axis=1)
    
    def find_sustained_bright(avg, start, end, step):
        """Find first position where brightness > 160 for >= 10 consecutive rows"""
        count = 0
        first_bright = None
        rng = range(start, end, step)
        for i in rng:
            if avg[i] > 160:
                count += 1
                if first_bright is None:
                    first_bright = i
                if count >= 10:
                    return first_bright
            else:
                count = 0
                first_bright = None
        return start if step > 0 else end
    
    # Top: scan downward for first sustained bright region
    interior_top = find_sustained_bright(row_avg, 0, h, 1)
    # Bottom: scan upward for first sustained bright region  
    interior_bot = find_sustained_bright(row_avg, h-1, -1, -1)
    
    # Left/right: use same approach on columns
    col_strip = gray[h//3:2*h//3, :]
    col_avg = np.mean(col_strip, axis=0)
    interior_left = find_sustained_bright(col_avg, 0, w, 1)
    interior_right = find_sustained_bright(col_avg, w-1, -1, -1)
    
    return interior_top, interior_bot, interior_left, interior_right

def find_symbol_region(img):
    """
    Locate the symbol-only region. Strategy:
    1. Find interior bounds (past frame border)
    2. Find the separator line (bright line dividing label from symbol)
    3. Crop to symbol-only with tight bbox on actual symbol pixels
    """
    arr = np.array(img)
    gray = np.mean(arr[:,:,:3], axis=2)
    h, w = gray.shape
    
    it, ib, il, ir = find_interior_bounds(gray)
    print(f"  Interior: [{it}:{ib}, {il}:{ir}] = {ir-il}x{ib-it}px")
    
    # The interior contains: label area (top ~30%) + symbol area (bottom ~70%)
    # The separator is a structural element of the Cobb icon.
    # 
    # Instead of trying to find a separator line (which varies per icon),
    # we'll detect the symbol by finding NON-BACKGROUND pixels.
    # The background inside the Cobb icon is the brightest region (~230-250).
    # The symbol is anything significantly darker than the background.
    
    interior = gray[it:ib+1, il:ir+1]
    int_h, int_w = interior.shape
    
    # Find background brightness (mode of bright pixels)
    bright_pixels = interior[interior > 200]
    if len(bright_pixels) > 0:
        bg_brightness = np.median(bright_pixels)
    else:
        bg_brightness = 240
    
    # Symbol pixels are those significantly darker than background
    # Use adaptive threshold: anything < (background - 50) is symbol
    threshold = bg_brightness - 50
    symbol_mask = interior < threshold
    
    print(f"  Background brightness: {bg_brightness:.0f}, threshold: {threshold:.0f}")
    print(f"  Symbol pixels: {np.sum(symbol_mask)} ({np.sum(symbol_mask)/(int_h*int_w)*100:.1f}%)")
    
    # Find tight bbox of symbol pixels
    sym_rows = np.any(symbol_mask, axis=1)
    sym_cols = np.any(symbol_mask, axis=0)
    
    if not np.any(sym_rows) or not np.any(sym_cols):
        print("  WARNING: No symbol content found!")
        return it, ib, il, ir, threshold
    
    sr = np.where(sym_rows)[0]
    sc = np.where(sym_cols)[0]
    
    # Convert back to full image coordinates
    sym_top = it + sr[0]
    sym_bot = it + sr[-1]
    sym_left = il + sc[0]
    sym_right = il + sc[-1]
    
    # The label text is also "symbol" colored but at the top.
    # We need to exclude it. The label is in the top portion.
    # Strategy: find the largest vertical gap in symbol pixels
    # (the gap between label text and the actual pictogram)
    
    # Count symbol pixels per row
    row_density = np.sum(symbol_mask, axis=1)
    
    # Look for the biggest gap (run of zeros or very low density)
    # in the top 60% of the interior
    search_limit = int(int_h * 0.6)
    best_gap_start = 0
    best_gap_end = 0
    best_gap_len = 0
    
    gap_start = None
    for row in range(search_limit):
        if row_density[row] < 3:  # essentially empty row
            if gap_start is None:
                gap_start = row
        else:
            if gap_start is not None:
                gap_len = row - gap_start
                if gap_len > best_gap_len:
                    best_gap_len = gap_len
                    best_gap_start = gap_start
                    best_gap_end = row - 1
                gap_start = None
    
    # If we found a significant gap (>5px), the symbol starts after it
    if best_gap_len > 5:
        symbol_start_interior = best_gap_end + 1
        sym_top = it + symbol_start_interior
        print(f"  Label-symbol gap: rows {best_gap_start}-{best_gap_end} ({best_gap_len}px gap)")
    else:
        print(f"  No clear label-symbol gap found, using full interior")
    
    # Generous padding
    pad = 5
    sym_top = max(0, sym_top - pad)
    sym_bot = min(h-1, sym_bot + pad)
    sym_left = max(0, sym_left - pad)
    sym_right = min(w-1, sym_right + pad)
    
    sym_w = sym_right - sym_left
    sym_h = sym_bot - sym_top
    print(f"  Symbol bbox: [{sym_top}:{sym_bot}, {sym_left}:{sym_right}] = {sym_w}x{sym_h}px")
    
    return sym_top, sym_bot, sym_left, sym_right, threshold

def crop_symbol_only(img, debug_name=None):
    result = find_symbol_region(img)
    sym_top, sym_bot, sym_left, sym_right, threshold = result
    arr = np.array(img)
    cropped = Image.fromarray(arr[sym_top:sym_bot+1, sym_left:sym_right+1])
    if debug_name:
        cropped.save(os.path.join(DEBUG_DIR, f"{debug_name}_symbol_crop.png"))
    return cropped, threshold

def threshold_bw(img, threshold):
    """Convert to B&W using per-icon adaptive threshold"""
    arr = np.array(img.convert('L'))
    return Image.fromarray(np.where(arr < threshold, 0, 255).astype(np.uint8))

def trace_to_svg(bw_img, debug_name=None):
    temp = os.path.join(DEBUG_DIR, f"{debug_name}_bw.png" if debug_name else "temp_bw.png")
    out = os.path.join(DEBUG_DIR, f"{debug_name}_traced.svg" if debug_name else "temp.svg")
    bw_img.save(temp)
    vtracer.convert_image_to_svg_py(temp, out,
        colormode="binary", mode="polygon", filter_speckle=4,
        corner_threshold=60, length_threshold=4.0,
        splice_threshold=45, path_precision=2)
    with open(out, 'r', encoding='utf-8') as f: return f.read()

def transform_path(path_d, scale, ox, oy):
    tokens = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|-?\d+\.?\d*', path_d)
    result = []; i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in 'Zz': result.append(t); i += 1
        elif t in 'MLCSQT':
            result.append(t); i += 1
            pairs = {'M':1,'L':1,'C':3,'S':2,'Q':2,'T':1}[t]
            while i < len(tokens) and re.match(r'-?\d', tokens[i]):
                for _ in range(pairs):
                    if i+1 >= len(tokens): break
                    result.extend([f"{float(tokens[i])*scale+ox:.1f}",
                                   f"{float(tokens[i+1])*scale+oy:.1f}"]); i += 2
                if t in 'ML' and i < len(tokens) and re.match(r'-?\d', tokens[i]): continue
                break
        elif t == 'H':
            result.append(t); i += 1
            while i < len(tokens) and re.match(r'-?\d', tokens[i]):
                result.append(f"{float(tokens[i])*scale+ox:.1f}"); i += 1
        elif t == 'V':
            result.append(t); i += 1
            while i < len(tokens) and re.match(r'-?\d', tokens[i]):
                result.append(f"{float(tokens[i])*scale+oy:.1f}"); i += 1
        elif re.match(r'-?\d', t):
            if i+1 < len(tokens) and re.match(r'-?\d', tokens[i+1]):
                result.extend([f"{float(tokens[i])*scale+ox:.1f}",
                               f"{float(tokens[i+1])*scale+oy:.1f}"]); i += 2
            else: result.append(t); i += 1
        else: result.append(t); i += 1
    return " ".join(result)

def normalize_svg(svg_str, target_size=1000):
    paths = re.findall(r'<path d="([^"]+)"[^>]*fill="([^"]*)"[^>]*/>', svg_str)
    if not paths: paths = re.findall(r'<path[^>]*d="([^"]+)"[^>]*fill="([^"]*)"', svg_str)
    black = [(d,f) for d,f in paths if f in ('#000000','#000','black','rgb(0,0,0)')]
    if not black: black = paths
    all_x, all_y = [], []
    for d, _ in black:
        nums = [float(n) for n in re.findall(r'-?\d+\.?\d*', d)]
        for i in range(0, len(nums)-1, 2): all_x.append(nums[i]); all_y.append(nums[i+1])
    if not all_x: return None
    min_x, max_x, min_y, max_y = min(all_x), max(all_x), min(all_y), max(all_y)
    sw, sh = max_x-min_x, max_y-min_y
    if sw == 0 or sh == 0: return None
    usable = target_size * 0.90
    scale = min(usable/sw, usable/sh)
    ssw, ssh = sw*scale, sh*scale
    ox = (target_size-ssw)/2 - min_x*scale
    oy = (target_size-ssh)/2 - min_y*scale
    xf = [transform_path(d, scale, ox, oy) for d, _ in black]
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {target_size} {target_size}">\n'
    svg += f'  <path d="{" ".join(xf)}" fill-rule="evenodd"/>\n</svg>'
    print(f"  Normalized: {sw:.0f}x{sh:.0f} scale={scale:.2f} fill={ssw/target_size*100:.0f}%x{ssh/target_size*100:.0f}%")
    return svg

def process_icon(icon_name):
    src = os.path.join(SRC_DIR, icon_name + ".svg")
    svg_name = "ss-" + icon_name.replace("_", "-")
    print(f"\n{'='*60}\n  {icon_name}\n{'='*60}")
    img = extract_png(src)
    if not img: print("  ERROR: No PNG"); return False
    print(f"  Source: {img.size}")
    cropped, threshold = crop_symbol_only(img, debug_name=icon_name)
    print(f"  Cropped: {cropped.size}")
    bw = threshold_bw(cropped, threshold)
    raw_svg = trace_to_svg(bw, debug_name=icon_name)
    final = normalize_svg(raw_svg)
    if not final: print("  ERROR: Normalize failed"); return False
    for p, c in [(os.path.join(OUT_EXT, svg_name+".svg"), final),
                 (os.path.join(OUT_MONO, svg_name+".svg"), raw_svg)]:
        with open(p, 'w', encoding='utf-8') as f: f.write(c)
    print(f"  DONE -> {svg_name}.svg"); return True

if __name__ == "__main__":
    icons = ["alcohol","allergen_warning","beverage_dispenser","contaminated",
             "emergency_rations","food_heating","fresh_produce","frozen_goods",
             "grain","hydroponic","organic_waste","potable_water",
             "protein","rations","utensils","water_filtration"]
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        ok = sum(1 for i in icons if process_icon(i))
        print(f"\n{'='*60}\n  Result: {ok}/{len(icons)} icons\n{'='*60}")
    else:
        process_icon(sys.argv[1] if len(sys.argv) > 1 else "alcohol")
        print("\nRun with --all to process all 16.")
