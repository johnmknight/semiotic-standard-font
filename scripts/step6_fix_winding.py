"""
step6_fix_winding.py v3

Correct approach: frame subpaths and symbol subpaths are handled differently.

Frame subpaths (first 2 for single border, first 4 for double border):
  - Index 0: outer rect -> CW (filled)
  - Index 1: inner rect -> CCW (hole/knockout)
  - Index 2 (double only): inner ring -> CW (filled)
  - Index 3 (double only): interior -> CCW (hole)

Symbol subpaths (everything after the frame subpaths):
  - OpenCV traces filled contours as OUTER contours (CW in SVG Y-down)
  - OpenCV traces holes as INNER contours (CCW in SVG Y-down)
  - These are ALREADY correct — just preserve as-is
  - BUT svgicons2svgfont flips Y, which flips winding, so we reverse all symbol subpaths

Wait — actually svgicons2svgfont handles Y-flip internally via the font coordinate system.
The glyph d= in the SVG font has Y flipped (font coords: Y increases upward).
svgicons2svgfont does: y_font = ascent - y_svg

So in the SVG input:
  CW in SVG (Y-down) -> after Y-flip -> CCW in font coords -> rendered as HOLE
  CCW in SVG (Y-down) -> after Y-flip -> CW in font coords -> rendered as FILL

Therefore to get FILLED areas: SVG subpath must be CCW (so after Y-flip it becomes CW=filled)
To get HOLES: SVG subpath must be CW (so after Y-flip it becomes CCW=hole)

This is the OPPOSITE of what we'd expect without the Y-flip!

Frame:
  outer rect (fill) -> must be CCW in SVG
  inner rect (hole) -> must be CW in SVG

Symbol (OpenCV output — CW=outer contour, CCW=hole contour):
  outer contour (fill) -> CW in SVG -> after flip = CCW in font = FILL ✓  Wait...
  
Let's just test empirically: beverage_dispenser works, alcohol doesn't.
Check what winding they have.
"""
import re, os

SRC = r"C:\Users\john_\dev\semiotic-standard-font\svg\mono\extended"

DOUBLE_BORDER_ICONS = {"ss-allergen-warning"}  # 4 frame subpaths
# All others: 2 frame subpaths

def parse_subpaths(d):
    parts = re.split(r'(?=M\s)', d.strip())
    return [p.strip() for p in parts if p.strip()]

def path_to_coords(sp):
    tokens = re.findall(r'[MLZQz]|[-]?\d+\.?\d*', sp)
    coords = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in ('M','L'):
            if i+2 < len(tokens):
                coords.append((float(tokens[i+1]), float(tokens[i+2]))); i+=3
            else: i+=1
        elif tok == 'Q':
            if i+4 < len(tokens):
                coords.append((float(tokens[i+3]), float(tokens[i+4]))); i+=5
            else: i+=1
        else: i+=1
    return coords

def shoelace(coords):
    n = len(coords)
    if n < 3: return 0
    area = 0
    for i in range(n):
        x1,y1=coords[i]; x2,y2=coords[(i+1)%n]
        area += x1*y2 - x2*y1
    return area/2

def reverse_subpath(sp):
    tokens = re.findall(r'[MLZQz]|[-]?\d+\.?\d*', sp)
    all_pts = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == 'M':
            all_pts.append((float(tokens[i+1]),float(tokens[i+2]))); i+=3
        elif tok == 'L':
            all_pts.append((float(tokens[i+1]),float(tokens[i+2]))); i+=3
        elif tok == 'Q':
            all_pts.append((float(tokens[i+1]),float(tokens[i+2])))
            all_pts.append((float(tokens[i+3]),float(tokens[i+4]))); i+=5
        elif tok in ('Z','z'): i+=1
        else: i+=1
    if not all_pts: return sp
    rev = list(reversed(all_pts))
    parts = [f"M {rev[0][0]:.1f},{rev[0][1]:.1f}"]
    for pt in rev[1:]:
        parts.append(f"L {pt[0]:.1f},{pt[1]:.1f}")
    parts.append("Z")
    return " ".join(parts)

def ensure_cw(sp):
    coords = path_to_coords(sp)
    if shoelace(coords) < 0: return reverse_subpath(sp)
    return sp

def ensure_ccw(sp):
    coords = path_to_coords(sp)
    if shoelace(coords) > 0: return reverse_subpath(sp)
    return sp

def fix_winding(d, fname):
    subpaths = parse_subpaths(d)
    is_double = any(db in fname for db in DOUBLE_BORDER_ICONS)
    n_frame = 4 if is_double else 2
    fixed = []

    # Y-flip means: to FILL in font -> be CCW in SVG; to HOLE -> be CW in SVG
    for i, sp in enumerate(subpaths):
        if i < n_frame:
            # Frame subpaths: alternating fill/hole
            # fill (0, 2) -> CCW in SVG (fills after Y-flip)
            # hole (1, 3) -> CW in SVG (holes after Y-flip)
            if i % 2 == 0:
                sp = ensure_ccw(sp)  # fill -> CCW
            else:
                sp = ensure_cw(sp)   # hole -> CW
        else:
            # Symbol subpaths: from OpenCV
            # OpenCV outer contours are CW in SVG Y-down
            # CW in SVG -> after Y-flip -> CCW in font -> FILL ✓
            # OpenCV hole contours are CCW in SVG Y-down
            # CCW in SVG -> after Y-flip -> CW in font -> HOLE ✓
            # So symbol subpaths are already correct — leave them alone
            pass
        fixed.append(sp)
    return " ".join(fixed)

def process_file(fpath):
    fname = os.path.basename(fpath)
    with open(fpath, encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'd="([^"]+)"', content)
    if not match:
        print(f"  SKIP: {fname}"); return
    fixed_d = fix_winding(match.group(1), fname)
    new_content = content.replace(match.group(0), f'd="{fixed_d}"')
    new_content = re.sub(r'fill-rule="[^"]+"', 'fill-rule="nonzero"', new_content)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    n = len(parse_subpaths(match.group(1)))
    print(f"  {fname}: {n} subpaths")

if __name__ == '__main__':
    import sys
    files = sorted(f for f in os.listdir(SRC) if f.endswith('.svg') and f.startswith('ss-'))
    target = sys.argv[1] if len(sys.argv)>1 else '--all'
    if target != '--all':
        files = [f for f in files if target in f]
    print(f"Fixing winding ({len(files)} files)...")
    for fname in files:
        process_file(os.path.join(SRC, fname))
    print("Done.")
