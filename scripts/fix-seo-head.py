import re, json, os

SITE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")

# slug -> (path, is_home)
PAGES = {
    "index.html": "/",
    "about.html": "/about/",
    "contact.html": "/contact/",
    "design-your-space.html": "/design-your-space/",
    "events.html": "/events/",
    "financing.html": "/financing/",
    "gallery.html": "/gallery/",
    "pricing.html": "/pricing/",
    "rentals.html": "/rentals/",
    "units.html": "/units/",
}

BASE_URL = "https://troycondogarages.com"

def get_title_desc(html):
    t = re.search(r'<title>(.*?)</title>', html, re.S)
    d = re.search(r'<meta name="description" content="(.*?)"\s*/?>', html, re.S)
    return (t.group(1).strip() if t else ""), (d.group(1).strip() if d else "")

def build_jsonld(slug, title, desc):
    url = BASE_URL + slug
    graph = [
        {
            "@type": "LocalBusiness",
            "@id": BASE_URL + "/#business",
            "name": "Troy Condo Garages",
            "url": BASE_URL + "/",
            "telephone": "+16512478384",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "663 Valerie Avenue",
                "addressLocality": "Hudson",
                "addressRegion": "WI",
                "postalCode": "54016",
                "addressCountry": "US"
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "5.0",
                "reviewCount": "17"
            }
        },
        {
            "@type": "WebPage",
            "@id": url + "#webpage",
            "url": url,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": BASE_URL + "/#website"}
        }
    ]
    if slug == "/":
        graph.append({
            "@type": "WebSite",
            "@id": BASE_URL + "/#website",
            "url": BASE_URL + "/",
            "name": "Troy Condo Garages"
        })
    data = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(data, separators=(",", ":"))

changed = []
for fname, slug in PAGES.items():
    path = os.path.join(SITE_DIR, fname)
    with open(path, "r", encoding="utf-8", errors="ignore", newline="") as f:
        html = f.read()

    if 'rel="canonical"' in html and "application/ld+json" in html:
        print(f"SKIP (already has canonical+jsonld): {fname}")
        continue

    title, desc = get_title_desc(html)
    canonical_url = BASE_URL + slug
    canonical_tag = f'  <link rel="canonical" href="{canonical_url}" />\n'
    jsonld_tag = f'  <script type="application/ld+json">{build_jsonld(slug, title, desc)}</script>\n'

    # Insert canonical right after meta description line
    desc_pattern = re.compile(r'(<meta name="description"[^>]*/?>\n)')
    if desc_pattern.search(html):
        html2 = desc_pattern.sub(lambda m: m.group(1) + canonical_tag, html, count=1)
    else:
        html2 = html.replace("</head>", canonical_tag + "</head>", 1)

    # Insert JSON-LD right before </head>
    html2 = html2.replace("</head>", jsonld_tag + "</head>", 1)

    with open(path, "w", encoding="utf-8", errors="ignore", newline="") as f:
        f.write(html2)
    changed.append(fname)
    print(f"FIXED: {fname}")

print("\nChanged files:", changed)
