"""
Step 5: Normalize traced SVGs to 1000x1000 and compose with Cobb frame.

For each work/{name}_4_traced.svg:
  1. Parse the path(s) and compute bounding box
  2. Scale + center the symbol into the 800x800 active area (100-900 on 1000x1000 canvas)
  3. Compose with a constructed Cobb frame (two concentric rounded rects as fill paths)
  4. Write to svg/mono/extended/ss-{name}.svg

Cobb frame structure (1000x1000 canvas):
  Outer rect: x=50, y=50, w=900, h=900, rx=80  (filled black)
  Inner rect: x=80, y=80, w=840, h=840, rx=60  (filled white = knockout)
  = produces the thick rounded-rect border ring

Symbol is placed in the 800x800 active area centered at 500,500.
Symbol + inner white area combine via evenodd fill rule to show symbol on white.

Run: python scripts/step5_compose.py alcohol
     python scripts/step5_compose.py --all
"""
import re, os, sys
import numpy as np

WORK_DIR = r"C:\Users\john_\dev\semiotic-standard-font\work"
OUT_DIR  = r"C:\Users\john_\dev\semiotic-standard-font\svg\mono\extended"
os.makedirs(OUT_DIR, exist_ok=True)

ICONS = [
    "alcohol","allergen_warning","beverage_dispenser","contaminated",
    "emergency_rations","food_heating","fresh_produce","frozen_goods",
    "grain","hydroponic","organic_waste","potable_water",
    "protein","rations","utensils","water_filtration"
]

# Cobb frame parameters (1000x1000 canvas)
# Outer ring sits tight to canvas edge (~10u margin), matching source proportions
# Ring thickness ~80u (10->90), matching the bold Cobb border weight
CANVAS     = 1000
OUTER_X    = 10;  OUTER_Y = 10;  OUTER_W = 980; OUTER_H = 980; OUTER_RX = 80
INNER_X    = 90;  INNER_Y = 90;  INNER_W = 820; INNER_H = 820; INNER_RX = 60
ACTIVE_X   = 100; ACTIVE_Y = 100
ACTIVE_W   = 800; ACTIVE_H = 800
SYMBOL_PAD = 40

# Double-border icons: two concentric red rings with a stripe between them.
# Measured from source PNGs (228px -> 1000u scale=4.386):
#   dark outer edge: ~31u  -> canvas starts at 50
#   bright outer gap: ~39u -> outer ring starts at ~89
#   red ring 1: ~35u       -> stripe starts at ~124
#   bright stripe: ~26u    -> inner ring starts at ~150 (add 4u dark = 154)
#   red ring 2: ~31u       -> interior starts at ~185
#
# Rect encoding: each rect is a filled subpath; evenodd alternates fill/knockout
#   rect1 (outermost filled):  x=50  w=900  rx=80
#   rect2 (gap knockout):      x=89  w=822  rx=68  -> white outer gap
#   rect3 (ring1 re-fill):     x=124 w=752  rx=58  -> outer red ring
#   rect4 (stripe knockout):   x=159 w=682  rx=50  -> white/colored stripe
#   rect5 (ring2 re-fill):     x=185 w=630  rx=44  -> inner red ring
#   rect6 (interior knockout): x=216 w=568  rx=38  -> interior white area
DOUBLE_BORDER = {
    "allergen_warning": True,
}

# Icons whose traced symbol needs horizontal flip to match source orientation
FLIP_H = set()  # protein flip removed — trace matches source correctly

# Double border rect stack — same proportional logic but with 4 rects
DB_RECTS = [
    (10,  10,  980, 980, 80),  # outermost filled
    (65,  65,  870, 870, 65),  # stripe knockout (colored band)
    (105, 105, 790, 790, 55),  # inner ring re-fill
    (145, 145, 710, 710, 45),  # interior knockout
]

def rounded_rect_path(x, y, w, h, rx):
    """Generate SVG path data for a rounded rectangle."""
    ry = rx
    r = f"M {x+rx},{y} "
    r += f"L {x+w-rx},{y} Q {x+w},{y} {x+w},{y+ry} "
    r += f"L {x+w},{y+h-ry} Q {x+w},{y+h} {x+w-rx},{y+h} "
    r += f"L {x+rx},{y+h} Q {x},{y+h} {x},{y+h-ry} "
    r += f"L {x},{y+ry} Q {x},{y} {x+rx},{y} Z"
    return r

def parse_path_coords(d):
    """Extract all coordinate pairs from an SVG path d string."""
    # Find all numbers
    nums = [float(n) for n in re.findall(r'-?\d+\.?\d*', d)]
    # Pair them up (M/L commands each take x,y)
    coords = []
    i = 0
    while i + 1 < len(nums):
        coords.append((nums[i], nums[i+1]))
        i += 2
    return coords

def get_bbox(d):
    """Get bounding box of path data."""
    coords = parse_path_coords(d)
    if not coords:
        return None
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    return min(xs), min(ys), max(xs), max(ys)

def scale_path(d, sx, sy, tx, ty):
    """Scale and translate all coordinates in a path string."""
    def replace_coord(m):
        num = float(m.group())
        return m.group()  # placeholder - we'll do it properly below

    # Parse tokens: commands (M, L, Z) and numbers
    tokens = re.findall(r'[MLZQCSTAHVz]|[-]?\d+\.?\d*', d)
    result = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in ('M', 'L'):
            result.append(tok)
            if i + 2 < len(tokens):
                x = float(tokens[i+1]) * sx + tx
                y = float(tokens[i+2]) * sy + ty
                result.append(f"{x:.1f}")
                result.append(f"{y:.1f}")
                i += 3
            else:
                i += 1
        elif tok == 'Q':
            result.append(tok)
            # Quadratic bezier: 4 coords (cx,cy, x,y)
            for _ in range(2):
                if i + 2 < len(tokens):
                    x = float(tokens[i+1]) * sx + tx
                    y = float(tokens[i+2]) * sy + ty
                    result.append(f"{x:.1f}")
                    result.append(f"{y:.1f}")
                    i += 2
            i += 1
        elif tok in ('Z', 'z'):
            result.append('Z')
            i += 1
        else:
            result.append(tok)
            i += 1
    return ' '.join(result)

def normalize_symbol(traced_svg_path, flip_h=False):
    """Read traced SVG, extract path(s), normalize to fit active area."""
    with open(traced_svg_path) as f:
        content = f.read()

    # Extract all path d= attributes
    paths = re.findall(r'd="([^"]+)"', content)
    if not paths:
        print(f"  WARNING: no paths found in {traced_svg_path}")
        return None

    # Combine all paths
    combined_d = ' '.join(paths)

    # Get bounding box
    bbox = get_bbox(combined_d)
    if not bbox:
        return None
    x0, y0, x1, y1 = bbox
    sym_w = x1 - x0
    sym_h = y1 - y0

    if sym_w == 0 or sym_h == 0:
        print(f"  WARNING: zero-size bbox")
        return None

    # Target area: active area minus padding
    target_w = ACTIVE_W - 2 * SYMBOL_PAD
    target_h = ACTIVE_H - 2 * SYMBOL_PAD

    # Uniform scale to fit, preserving aspect ratio
    scale = min(target_w / sym_w, target_h / sym_h)

    # Center in active area
    scaled_w = sym_w * scale
    scaled_h = sym_h * scale
    tx = ACTIVE_X + SYMBOL_PAD + (target_w - scaled_w) / 2 - x0 * scale
    ty = ACTIVE_Y + SYMBOL_PAD + (target_h - scaled_h) / 2 - y0 * scale

    # Apply transform to all paths
    normalized_paths = []
    for d in paths:
        normalized_paths.append(scale_path(d, scale, scale, tx, ty))

    result = ' '.join(normalized_paths)

    # Horizontal flip: mirror around canvas center x=500
    if flip_h:
        result = scale_path(result, -1, 1, CANVAS, 0)

    return result

def compose(name):
    traced = os.path.join(WORK_DIR, f"{name}_4_traced.svg")
    out    = os.path.join(OUT_DIR, f"ss-{name.replace('_','-')}.svg")

    symbol_d = normalize_symbol(traced, flip_h=(name in FLIP_H))
    if symbol_d is None:
        print(f"  ERROR: could not normalize {name}")
        return

    if name in DOUBLE_BORDER:
        # Six alternating rects: fill, knockout, fill, knockout, fill, knockout
        frame_paths = [rounded_rect_path(x, y, w, h, rx) for x, y, w, h, rx in DB_RECTS]
        full_path = ' '.join(frame_paths) + ' ' + symbol_d
    else:
        # Single border: outer fill + inner knockout + symbol
        outer = rounded_rect_path(OUTER_X, OUTER_Y, OUTER_W, OUTER_H, OUTER_RX)
        inner = rounded_rect_path(INNER_X, INNER_Y, INNER_W, INNER_H, INNER_RX)
        full_path = f"{outer} {inner} {symbol_d}"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}">
  <path d="{full_path}" fill="black" fill-rule="evenodd"/>
</svg>'''

    with open(out, 'w') as f:
        f.write(svg)
    border_type = "double" if name in DOUBLE_BORDER else "single"
    print(f"  {name} [{border_type} border] -> {os.path.basename(out)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        for icon in ICONS:
            try: compose(icon)
            except Exception as e: print(f"  ERROR {icon}: {e}")
    else:
        compose(sys.argv[1] if len(sys.argv) > 1 else "alcohol")
