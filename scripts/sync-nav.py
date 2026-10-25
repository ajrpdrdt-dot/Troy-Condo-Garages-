NAV_ITEMS = [
    ("/", "Home"),
    ("/units/", "Our Units"),
    ("/design-your-space/", "Design Your Space"),
    ("/gallery/", "Gallery"),
    ("/events/", "Events"),
    ("/rentals/", "Rentals"),
    ("/about/", "About"),
    ("/contact/", "Contact"),
    ("/financing/", "Financing"),
    ("/pricing/", "Pricing"),
]

PAGE_CURRENT = {
    "index.html": "/",
    "units.html": "/units/",
    "design-your-space.html": "/design-your-space/",
    "gallery.html": "/gallery/",
    "events.html": "/events/",
    "rentals.html": "/rentals/",
    "about.html": "/about/",
    "contact.html": "/contact/",
    "financing.html": "/financing/",
    "pricing.html": "/pricing/",
    "thank-you.html": "/",
}

GTAG_BASE = """  <!-- Google tag (gtag.js) AW-18398757431 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=AW-18398757431"></script>
  <script src="/js/analytics.js"></script>
"""

GTAG_CONVERSION = """  <!-- Event snippet: Submit lead form -->
  <script src="/js/conversion-lead.js"></script>
"""

import re
from pathlib import Path

site = Path("site")
header_pattern = re.compile(
    r'(<nav class="site-nav" id="primary-nav" aria-label="Primary">\s*<ul>)(.*?)(</ul>\s*</nav>)',
    re.S,
)
footer_pattern = re.compile(
    r'(<ul class="footer-links">)(.*?)(</ul>)',
    re.S,
)


def nav_html(current: str) -> str:
    items = []
    for href, label in NAV_ITEMS:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'          <li><a href="{href}"{cur}>{label}</a></li>')
    return "\n".join(items)


def footer_links_html() -> str:
    items = []
    for href, label in NAV_ITEMS:
        items.append(f'          <li><a href="{href}">{label}</a></li>')
    return "\n".join(items)


def ensure_analytics(text: str, name: str) -> str:
    text = re.sub(r"\s*<!-- Google Ads:.*?-->\s*", "\n", text)
    if "AW-18398757431" not in text:
        text = text.replace("</head>", GTAG_BASE + "</head>", 1)
    if name == "thank-you.html" and "conversion-lead.js" not in text:
        text = text.replace("</head>", GTAG_CONVERSION + "</head>", 1)
    return text


for name, current in PAGE_CURRENT.items():
    path = site / name
    if not path.exists():
        print("skip missing", name)
        continue
    text = path.read_text(encoding="utf-8")
    text2, n1 = header_pattern.subn(
        lambda m: m.group(1) + "\n" + nav_html(current) + "\n        " + m.group(3),
        text,
        count=1,
    )
    text3, n2 = footer_pattern.subn(
        lambda m: m.group(1) + "\n" + footer_links_html() + "\n        " + m.group(3),
        text2,
        count=1,
    )
    if 'href="/css/pages.css"' not in text3 and 'href="/css/theme.css"' in text3:
        text3 = text3.replace(
            '<link rel="stylesheet" href="/css/theme.css" />',
            '<link rel="stylesheet" href="/css/theme.css" />\n  <link rel="stylesheet" href="/css/pages.css" />',
        )
    text3 = ensure_analytics(text3, name)
    path.write_text(text3, encoding="utf-8")
    print(f"{name}: nav={n1} footer={n2}")
