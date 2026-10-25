import re
from pathlib import Path

left = 0
for p in Path("site").glob("*.html"):
    t = p.read_text(encoding="utf-8")
    m = re.findall(
        r"https://troycondogarages\.com/wp-content/uploads/[^\s\"'\\>]+",
        t,
    )
    if m:
        print(p.name, len(m))
        left += len(m)
print("remaining remote refs", left)
print("asset files", len([p for p in Path("site/assets").glob("*.*") if p.name != ".gitkeep"]))
