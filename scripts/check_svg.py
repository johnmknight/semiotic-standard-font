import re
svg = open(r'C:\Users\john_\dev\semiotic-standard-font\svg\mono\extended\ss-grain.svg').read()
paths = re.findall(r'<path', svg)
print("Paths:", len(paths))
print("SVG chars:", len(svg))
print(svg[:600])
