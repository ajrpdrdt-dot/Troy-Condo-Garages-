from pathlib import Path
import re

root = Path("site")

contact = root / "contact.html"
t = contact.read_text(encoding="utf-8")
old = (
    '<section class="section">\n'
    '      <div class="container grid-2">\n'
    '        <div class="contact-meta">'
)
new = (
    '<section class="section" id="lead-form">\n'
    '      <div class="container grid-2">\n'
    '        <div class="contact-meta">'
)
if old in t:
    contact.write_text(t.replace(old, new, 1), encoding="utf-8")
    print("contact.html: added #lead-form")
else:
    print("contact.html: section already updated or pattern mismatch")

index = root / "index.html"
t = index.read_text(encoding="utf-8")
old = (
    '<section class="section section-dark">\n'
    '      <div class="container">\n'
    '        <div class="section-head">\n'
    "          <h2>Inquire about availability</h2>"
)
new = (
    '<section class="section section-dark" id="lead-form">\n'
    '      <div class="container">\n'
    '        <div class="section-head">\n'
    "          <h2>Inquire about availability</h2>"
)
if old in t:
    index.write_text(t.replace(old, new, 1), encoding="utf-8")
    print("index.html: added #lead-form")
else:
    print("index.html: section already updated or pattern mismatch")

targets = {
    "index.html": "#lead-form",
    "contact.html": "#lead-form",
    "rentals.html": "#inquire",
}
default = "/contact/#lead-form"
pattern = re.compile(r'(href=")tel:6512478384(">Schedule a Tour</a>)')

for p in root.glob("*.html"):
    t = p.read_text(encoding="utf-8")
    href = targets.get(p.name, default)
    nt, n = pattern.subn(rf"\1{href}\2", t)
    if n:
        p.write_text(nt, encoding="utf-8")
        print(f"{p.name}: {n} Schedule a Tour -> {href}")
