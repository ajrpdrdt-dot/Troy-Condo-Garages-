import json, re
from pathlib import Path

raw = Path(".firecrawl/gallery-full.json").read_text(encoding="utf-8")
urls = sorted(
    set(
        re.findall(
            r"https://troycondogarages\.com/wp-content/uploads/[^\s\"'\\)]+",
            raw,
        )
    )
)
for u in urls:
    if any(u.lower().endswith(ext) for ext in (".webp", ".jpg", ".jpeg", ".png")):
        # skip logos/favicons size crops where possible
        print(u)
