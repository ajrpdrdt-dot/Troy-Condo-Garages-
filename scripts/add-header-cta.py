from pathlib import Path
import re

root = Path("site")
cta_re = re.compile(r'<a class="btn header-cta"[^>]*>Book a Tour</a>')
nav_end_re = re.compile(r"</nav>\s*</div>\s*</header>", re.S)

hrefs = {
    "index.html": "#lead-form",
    "contact.html": "#lead-form",
    "rentals.html": "#inquire",
}


for path in sorted(root.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    href = hrefs.get(path.name, "/contact/#lead-form")
    button = f'<a class="btn header-cta" href="{href}">Book a Tour</a>'
    text = cta_re.sub("", text)
    match = nav_end_re.search(text)
    if not match:
        print(f"skip {path.name}: nav/header end not found")
        continue
    text = nav_end_re.sub(f"</nav>\n      {button}\n    </div>\n  </header>", text, count=1)
    path.write_text(text, encoding="utf-8")
    print(f"{path.name}: Book a Tour -> {href}")
