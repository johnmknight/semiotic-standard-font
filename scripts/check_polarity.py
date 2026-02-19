"""
check_polarity.py - For each icon's hero mask, determine if it needs inversion.
A mask is "correct polarity" for vtracer if the symbol pixels are BLACK on WHITE background.
We check by: sample the 4 corners (should be background = white if correct, black if inverted).
"""
import numpy as np
from PIL import Image
from pathlib import Path

MASKS = Path(r"C:\Users\john_\dev\semiotic-standard-font\svg\masks")

# Hero masks we care about per icon
HEROES = {
    "grain":        ["mask_black_4.png", "mask_brightness_symbol.png"],
    "hydroponic":   ["mask_dark_green.png", "mask_white_2.png"],
    "alcohol":      ["mask_white_1.png"],
    "allergen_warning": ["mask_yellow_1.png"],
    "beverage_dispenser": ["mask_white_1.png"],
    "contaminated": ["mask_white_1.png"],
    "emergency_rations": ["mask_white_1.png"],
    "food_heating": ["mask_yellow.png"],
    "fresh_produce": ["mask_white_1.png"],
    "frozen_goods": ["mask_white.png"],
    "organic_waste": ["mask_yellow.png"],
    "potable_water": ["mask_white_1.png"],
    "protein":      ["mask_white_1.png"],
    "rations":      ["mask_white.png"],
    "utensils":     ["mask_white.png"],
    "water_filtration": ["mask_white_1.png"],
}

print(f"{'ICON':<22} {'MASK':<30} {'CORNERS':<8} {'CENTER':<8} {'POLARITY'}")
print("-"*80)
for icon, masks in HEROES.items():
    for mname in masks:
        path = MASKS / icon / mname
        if not path.exists():
            print(f"{icon:<22} {mname:<30} MISSING")
            continue
        arr = np.array(Image.open(path).convert("L"))
        h, w = arr.shape
        # Sample corners (5x5 patch)
        corners = [
            arr[:5,:5].mean(), arr[:5,-5:].mean(),
            arr[-5:,:5].mean(), arr[-5:,-5:].mean()
        ]
        corner_mean = np.mean(corners)
        center = arr[h//3:2*h//3, w//3:2*w//3].mean()
        # Correct polarity: corners=0 (black bg), symbol somewhere brighter
        # OR corners=255 (white bg), symbol is dark
        # For vtracer we want: background=WHITE(255), symbol=BLACK(0)
        # So correct = corners near 255, center varies
        if corner_mean > 200:
            polarity = "OK  (bg=white)"
        elif corner_mean < 50:
            polarity = "INVERT NEEDED (bg=black)"
        else:
            polarity = f"MIXED (corner={corner_mean:.0f})"
        print(f"{icon:<22} {mname:<30} {corner_mean:<8.0f} {center:<8.0f} {polarity}")
