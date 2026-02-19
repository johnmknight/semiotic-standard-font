import re, os

ext_dir = r"C:\Users\john_\dev\semiotic-standard-font\svg\mono\extended"
mono_dir = r"C:\Users\john_\dev\semiotic-standard-font\svg\mono"

icons = [
    "alcohol", "allergen-warning", "beverage-dispenser", "contaminated",
    "emergency-rations", "food-heating", "fresh-produce", "frozen-goods",
    "grain", "hydroponic", "organic-waste", "potable-water",
    "protein", "rations", "utensils", "water-filtration"
]

print("=== EXTENDED SVG PATH BOUNDING BOXES ===\n")

for icon in icons:
    fname = f"ss-{icon}.svg"
    fpath = os.path.join(ext_dir, fname)
    if not os.path.exists(fpath):
        print(f"{icon}: FILE NOT FOUND")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all numeric coordinates from path d attributes
    paths = re.findall(r'd="([^"]+)"', content)
    all_coords = []
    for path_d in paths:
        # Extract all numbers (including decimals and negatives)
        nums = re.findall(r'-?\d+\.?\d*', path_d)
        nums = [float(n) for n in nums]
        # Path coords come in x,y pairs after move/line commands
        # Simple approach: collect as x,y pairs
        coords = []
        i = 0
        while i < len(nums) - 1:
            coords.append((nums[i], nums[i+1]))
            i += 2
        all_coords.extend(coords)
    
    if all_coords:
        xs = [c[0] for c in all_coords]
        ys = [c[1] for c in all_coords]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        w = max_x - min_x
        h = max_y - min_y
        print(f"{icon}:")
        print(f"  Bounds: x=[{min_x:.1f}, {max_x:.1f}] y=[{min_y:.1f}, {max_y:.1f}]")
        print(f"  Size: {w:.1f} x {h:.1f} in 1000x1000 viewBox")
        print(f"  Coverage: {w/10:.1f}% x {h/10:.1f}%")
        print(f"  Margins: L={min_x:.1f} R={1000-max_x:.1f} T={min_y:.1f} B={1000-max_y:.1f}")
        print()

print("\n=== MONO SVG (full trace) PATH BOUNDING BOXES ===\n")

for icon in icons:
    fname = f"ss-{icon}.svg"
    fpath = os.path.join(mono_dir, fname)
    if not os.path.exists(fpath):
        print(f"{icon}: FILE NOT FOUND")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    paths = re.findall(r'd="([^"]+)"', content)
    all_coords = []
    for path_d in paths:
        nums = re.findall(r'-?\d+\.?\d*', path_d)
        nums = [float(n) for n in nums]
        coords = []
        i = 0
        while i < len(nums) - 1:
            coords.append((nums[i], nums[i+1]))
            i += 2
        all_coords.extend(coords)
    
    if all_coords:
        xs = [c[0] for c in all_coords]
        ys = [c[1] for c in all_coords]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        w = max_x - min_x
        h = max_y - min_y
        # Check for negative coords (indicates content was cropped badly)
        neg_x = sum(1 for x in xs if x < 0)
        neg_y = sum(1 for y in ys if y < 0)
        over1k_x = sum(1 for x in xs if x > 1000)
        over1k_y = sum(1 for y in ys if y > 1000)
        flags = []
        if neg_x: flags.append(f"{neg_x} neg-X coords")
        if neg_y: flags.append(f"{neg_y} neg-Y coords")
        if over1k_x: flags.append(f"{over1k_x} >1000-X coords")
        if over1k_y: flags.append(f"{over1k_y} >1000-Y coords")
        
        print(f"{icon}:")
        print(f"  Bounds: x=[{min_x:.1f}, {max_x:.1f}] y=[{min_y:.1f}, {max_y:.1f}]")
        print(f"  Size: {w:.1f} x {h:.1f}")
        if flags:
            print(f"  WARNING: {', '.join(flags)}")
        print()
