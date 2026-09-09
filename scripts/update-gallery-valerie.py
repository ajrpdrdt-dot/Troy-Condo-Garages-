from pathlib import Path

gallery = Path("site/gallery.html")
assets = sorted(Path("site/assets/valerie-ave").glob("valerie-ave-*.jpg"))
if not assets:
    raise SystemExit("no valerie-ave images found")

items = []
for p in assets:
    src = f"/assets/valerie-ave/{p.name}"
    n = p.stem.split("-")[-1]
    items.append(
        f'        <a href="{src}" target="_blank" rel="noopener">'
        f'<img src="{src}" alt="Troy Condo Garages Valerie Ave facility photo {n}" '
        f'loading="lazy" width="900" height="600" /></a>'
    )

section = (
    '\n    <section class="section section-muted" id="valerie-ave">\n'
    '      <div class="container">\n'
    '        <div class="section-head">\n'
    '          <p class="eyebrow">663 Valerie Ave</p>\n'
    '          <h2>Valerie Ave facility</h2>\n'
    '          <p class="lead">MLS photos of the Hudson campus and unit interiors.</p>\n'
    '        </div>\n'
    '        <div class="gallery-grid">\n'
    + "\n".join(items)
    + "\n        </div>\n"
    "      </div>\n"
    "    </section>\n"
)

text = gallery.read_text(encoding="utf-8")
if 'id="valerie-ave"' in text:
    raise SystemExit("valerie-ave section already present")

anchor = '    <section class="section section-dark">'
if anchor not in text:
    raise SystemExit("CTA section anchor not found")
gallery.write_text(text.replace(anchor, section + "\n" + anchor, 1), encoding="utf-8")
print(f"gallery.html: added {len(assets)} Valerie Ave images")
