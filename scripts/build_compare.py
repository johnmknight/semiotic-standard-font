import re, os, base64
from PIL import Image
import io

src_dir = r"C:\Users\john_\dev\semiotic-standard-font\from john"
mono_dir = r"C:\Users\john_\dev\semiotic-standard-font\svg\mono"
ext_dir = r"C:\Users\john_\dev\semiotic-standard-font\svg\mono\extended"
compare_dir = r"C:\Users\john_\dev\semiotic-standard-font\preview\compare"
preview_dir = r"C:\Users\john_\dev\semiotic-standard-font\preview"

icons = [
    "alcohol", "allergen_warning", "beverage_dispenser", "contaminated",
    "emergency_rations", "food_heating", "fresh_produce", "frozen_goods",
    "grain", "hydroponic", "organic_waste", "potable_water",
    "protein", "rations", "utensils", "water_filtration"
]

html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Source vs Traced Comparison</title>
<style>
body { background: #0a0a1a; color: #ccc; font-family: monospace; padding: 20px; }
h1 { color: #e94560; text-align: center; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; max-width: 1200px; margin: 0 auto; }
.cell { background: #12122a; border: 1px solid #333; border-radius: 8px; padding: 10px; text-align: center; }
.pair { display: flex; gap: 8px; justify-content: center; align-items: center; }
.pair img, .pair object { width: 100px; height: 100px; }
.src { border: 2px solid #2a6; border-radius: 4px; }
.mono { border: 2px solid #e94560; border-radius: 4px; background: white; }
.ext { border: 2px solid #4a9eff; border-radius: 4px; background: white; }
.labels { display: flex; gap: 8px; justify-content: center; font-size: 9px; margin-top: 4px; }
.labels span { padding: 1px 4px; border-radius: 2px; }
.l-src { background: #2a6; color: #000; }
.l-mono { background: #e94560; color: #fff; }
.l-ext { background: #4a9eff; color: #000; }
.name { font-size: 11px; color: #888; margin-top: 6px; }
</style></head><body>
<h1>SOURCE vs TRACED vs EXTENDED</h1>
<p style="text-align:center;color:#888;">Green=Source PNG | Red=Mono SVG (vtracer) | Blue=Extended SVG (simplified)</p>
<div class="grid">
"""

for icon in icons:
    src_png = f"compare/{icon}.png"
    mono_svg = f"../svg/mono/ss-{icon.replace('_','-')}.svg"
    ext_svg = f"../svg/mono/extended/ss-{icon.replace('_','-')}.svg"
    
    html += f"""<div class="cell">
  <div class="pair">
    <img class="src" src="{src_png}">
    <object class="mono" data="{mono_svg}" type="image/svg+xml"></object>
    <object class="ext" data="{ext_svg}" type="image/svg+xml"></object>
  </div>
  <div class="labels"><span class="l-src">SRC</span><span class="l-mono">MONO</span><span class="l-ext">EXT</span></div>
  <div class="name">{icon}</div>
</div>
"""

html += "</div></body></html>"

with open(os.path.join(preview_dir, "compare.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("Built compare.html")
