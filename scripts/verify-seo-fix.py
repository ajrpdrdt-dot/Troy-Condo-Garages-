import os, json, re
from html.parser import HTMLParser

SITE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")

class Checker(HTMLParser):
    def error(self, message):
        raise ValueError(message)

pages = ["index.html","about.html","contact.html","design-your-space.html","events.html",
         "financing.html","gallery.html","pricing.html","rentals.html","units.html"]

for fname in pages:
    path = os.path.join(SITE_DIR, fname)
    html = open(path, encoding="utf-8", errors="ignore").read()
    # parse check
    try:
        Checker(convert_charrefs=True).feed(html)
        parse_ok = True
    except Exception as e:
        parse_ok = False
        print(f"{fname}: PARSE ERROR {e}")
    # canonical check
    canon = re.search(r'<link rel="canonical" href="([^"]*)"', html)
    # jsonld check
    ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    ld_ok = True
    for block in ld:
        try:
            json.loads(block)
        except Exception as e:
            ld_ok = False
            print(f"{fname}: JSON-LD PARSE ERROR {e}")
    print(f"{fname}: parse_ok={parse_ok} canonical={canon.group(1) if canon else None} jsonld_blocks={len(ld)} jsonld_ok={ld_ok}")

print("\nrobots.txt exists:", os.path.exists(os.path.join(SITE_DIR, "robots.txt")))
print("sitemap.xml exists:", os.path.exists(os.path.join(SITE_DIR, "sitemap.xml")))
try:
    import xml.etree.ElementTree as ET
    ET.parse(os.path.join(SITE_DIR, "sitemap.xml"))
    print("sitemap.xml parses as valid XML")
except Exception as e:
    print("sitemap.xml XML ERROR:", e)
