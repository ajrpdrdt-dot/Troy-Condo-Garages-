"""Restore 46 legacy Troy Condo Garages pages from the static snapshot."""

from __future__ import annotations

import json
import os
import re
import shutil
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup, Comment, Declaration, Doctype, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SNAP = Path(r"C:\Users\rohla\repos\Troy-Condo-Garages-\public")

GROUPS = {
    "A": [
        "garage-condo-climate-control",
        "garage-condos-for-sale-near-twin-cities-minnesota",
        "garage-condo-mezzanine-ideas",
        "blog-garage-condo-vs-storage-unit",
        "blog-what-is-a-garage-condo",
        "car-condo-vs-garage-condo-difference",
        "garage-condos-near-stillwater-mn",
        "st-croix-falls",
        "river-falls",
        "new-richmond-wi",
        "man-cave-garage-wisconsin",
        "enclosed-trailer-storage-hudson-wi",
        "condos",
    ],
    "B": [
        "garage-condos-near-woodbury-lake-elmo-mn",
        "car-lift-installation-garage-condo-hudson-wi",
        "classic-car-storage-near-hudson-wi",
        "snowmobile-atv-storage-hudson-wi",
        "can-you-live-in-a-garage-condo-wisconsin-zoning-rules",
        "hoa-fees-troy-condo-garages-hudson-wi",
        "baldwin",
        "prescott",
        "jet-ski-watercraft-storage-hudson-wi",
        "toy-hauler-camper-van-storage-hudson-wi",
        "why-car-collectors-contractors-choose-garage-condo-ownership",
        "5-ways-to-transform-your-troy-condo-garage-into-a-private-workshop",
    ],
    "C": [
        "boat-storage-hudson-wi",
        "rv-storage-hudson-wi",
        "motorcycle-storage-hudson-wi",
        "home-gym-garage-condo-hudson-wi",
        "epoxy-garage-floor-coating-hudson-wi",
        "garage-condo-small-business-storage-hudson-wi",
        "garage-condo-buying-process",
        "garage-condo-insurance-wisconsin",
        "garage-condo-investment-wisconsin",
        "garage-condo-ownership-vs-401k-building-equity",
        "garage-condo-property-taxes-st-croix-county",
        "garage-condo-resale-value",
        "garage-condo-vs-pole-barn",
        "garage-condo-vs-renting-commercial-warehouse-space-hudson-wi",
        "best-garage-condo-communities-near-hudson-wi-western-wisconsin",
        "how-much-does-a-garage-condo-cost-in-wisconsin",
        "garage-condo-financing-hudson-wi",
    ],
    "D": [
        "privacy-policy",
        "terms-of-service",
        "accessibility-statement",
        "documents",
    ],
}

MONEY = {
    "hoa-fees-troy-condo-garages-hudson-wi",
    "garage-condo-ownership-vs-401k-building-equity",
    "garage-condo-property-taxes-st-croix-county",
    "garage-condo-resale-value",
    "how-much-does-a-garage-condo-cost-in-wisconsin",
    "garage-condo-financing-hudson-wi",
}

HUB = {
    "Buying & Costs": [
        "blog-what-is-a-garage-condo",
        "car-condo-vs-garage-condo-difference",
        "blog-garage-condo-vs-storage-unit",
        "can-you-live-in-a-garage-condo-wisconsin-zoning-rules",
        "why-car-collectors-contractors-choose-garage-condo-ownership",
        "hoa-fees-troy-condo-garages-hudson-wi",
        "garage-condo-buying-process",
        "garage-condo-insurance-wisconsin",
        "garage-condo-investment-wisconsin",
        "garage-condo-ownership-vs-401k-building-equity",
        "garage-condo-property-taxes-st-croix-county",
        "garage-condo-resale-value",
        "garage-condo-vs-pole-barn",
        "garage-condo-vs-renting-commercial-warehouse-space-hudson-wi",
        "best-garage-condo-communities-near-hudson-wi-western-wisconsin",
        "how-much-does-a-garage-condo-cost-in-wisconsin",
        "garage-condo-financing-hudson-wi",
    ],
    "Storage Uses": [
        "man-cave-garage-wisconsin",
        "enclosed-trailer-storage-hudson-wi",
        "classic-car-storage-near-hudson-wi",
        "snowmobile-atv-storage-hudson-wi",
        "jet-ski-watercraft-storage-hudson-wi",
        "toy-hauler-camper-van-storage-hudson-wi",
        "boat-storage-hudson-wi",
        "rv-storage-hudson-wi",
        "motorcycle-storage-hudson-wi",
        "home-gym-garage-condo-hudson-wi",
        "garage-condo-small-business-storage-hudson-wi",
    ],
    "Build-Out & Design": [
        "garage-condo-climate-control",
        "garage-condo-mezzanine-ideas",
        "condos",
        "car-lift-installation-garage-condo-hudson-wi",
        "epoxy-garage-floor-coating-hudson-wi",
        "5-ways-to-transform-your-troy-condo-garage-into-a-private-workshop",
    ],
    "Nearby Areas": [
        "garage-condos-for-sale-near-twin-cities-minnesota",
        "garage-condos-near-stillwater-mn",
        "garage-condos-near-woodbury-lake-elmo-mn",
        "st-croix-falls",
        "river-falls",
        "new-richmond-wi",
        "baldwin",
        "prescott",
    ],
}

REDIRECTS = {
    "/ultimate-guide-to-premium-garage-condos/": "/blog-what-is-a-garage-condo/",
    "/garage-condo-vs-storage-unit-hudson-wi/": "/blog-garage-condo-vs-storage-unit/",
    "/hoa-fees-troy-condo-garage-hudson-wi/": "/hoa-fees-troy-condo-garages-hudson-wi/",
    "/boat-rv-storage/": "/boat-storage-hudson-wi/",
    "/workshop-man-cave/": "/man-cave-garage-wisconsin/",
    "/car-storage-collector-storage/": "/classic-car-storage-near-hudson-wi/",
    "/garage-condo-tax-benefits-section-179-wisconsin/": "/garage-condo-investment-wisconsin/",
    "/real-estate-investment-angle/": "/garage-condo-investment-wisconsin/",
    "/own-vs-rent/": "/pricing/",
    "/garage-condo/": "/blog-what-is-a-garage-condo/",
    "/location-based/": "/",
    "/troy-condo-garages-inquiry/": "/contact/",
    "/6512478384/": "/contact/",
    "/info@troycondogarages.com/": "/contact/",
    "/faq/": "/",
    "/condo-garages-hudson-wi/": "/",
    "/garage-condos-for-sale-hudson-wi-pricing-size/": "/pricing/",
    "/garage-condo-financing-rates-2027/": "/garage-condo-financing-hudson-wi/",
    "/financing-options/": "/financing/",
    "/phase-iii-at-troy-condo-garages-whats-new-for-buyers/": "/units/",
    "/open-house/": "/events/",
    "/open-house-car-show/": "/events/",
    "/eau-claire/": "/",
    "/chippewa-falls/": "/",
    "/menomonie/": "/",
    "/la-crosse/": "/",
}

LIVE = {
    "",
    "units",
    "design-your-space",
    "gallery",
    "events",
    "rentals",
    "about",
    "contact",
    "financing",
    "pricing",
    "thank-you",
    "guides",
}

LETTER = {slug: letter for letter, slugs in GROUPS.items() for slug in slugs}
RESTORED = set(LETTER)
MERGE = {
    "blog-what-is-a-garage-condo": "ultimate-guide-to-premium-garage-condos",
    "blog-garage-condo-vs-storage-unit": "garage-condo-vs-storage-unit-hudson-wi",
}
IMG_EXT = re.compile(r"\.(?:jpe?g|png|gif|webp|avif|svg)$", re.I)
COPIED: set[str] = set()


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def upload_path(url: str) -> str | None:
    if not url or "wp-content/uploads/" not in url:
        return None
    path = url.split("wp-content/uploads/", 1)[1].split("?")[0].split("#")[0]
    path = path.strip()
    if not IMG_EXT.search(path):
        return None
    return "wp-content/uploads/" + path


def remember_image(url: str) -> str | None:
    rel = upload_path(url)
    if not rel:
        return None
    COPIED.add(rel)
    return "/" + rel


def remember_srcset(srcset: str) -> None:
    for part in (srcset or "").split(","):
        remember_image(part.strip().split(" ")[0])


def closest(path: str) -> str:
    text = path.lower()
    if any(word in text for word in ("gallery", "photo")):
        return "/gallery/"
    if any(word in text for word in ("contact", "inquir", "tour")):
        return "/contact/"
    if any(word in text for word in ("pric", "cost")):
        return "/pricing/"
    if "financ" in text:
        return "/financing/"
    if "rent" in text:
        return "/rentals/"
    if any(word in text for word in ("event", "open-house")):
        return "/events/"
    if "about" in text:
        return "/about/"
    if "design" in text:
        return "/design-your-space/"
    if any(word in text for word in ("unit", "amenity")):
        return "/units/"
    return "/"


def rewrite(href: str, page_slug: str) -> str:
    if not href:
        return ""
    href = href.strip()
    lower = href.lower()
    if lower.startswith(("mailto:", "tel:", "javascript:", "#")):
        return href
    absolute = urljoin(f"https://troycondogarages.com/{page_slug}/", href)
    parsed = urlparse(absolute)
    host = parsed.netloc.lower().split(":")[0]
    internal = host.endswith("troycondogarages.com") or host.endswith("mybluehost.me") or host == ""
    if parsed.scheme in {"http", "https"} and not internal:
        return href
    path = parsed.path or "/"
    upload = upload_path(path)
    if upload:
        remember_image(path)
        return "/" + upload
    if path.startswith("/documents/legal/") and path.lower().endswith(".pdf"):
        return path
    if path != "/" and not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
        path += "/"
    if path in REDIRECTS:
        return REDIRECTS[path]
    slug = path.strip("/")
    if slug in RESTORED or slug in LIVE:
        return "/" if slug == "" else f"/{slug}/"
    return closest(path)


def classes(tag: Tag) -> str:
    return " ".join(tag.get("class") or [])


def skip_tag(tag: Tag) -> bool:
    name = tag.name or ""
    if name in {"script", "style", "form", "iframe", "noscript", "svg", "button", "input", "textarea", "select", "label"}:
        return True
    kind = classes(tag)
    if any(
        token in kind
        for token in (
            "elementor-widget-form",
            "elementor-widget-shortcode",
            "elementor-widget-divider",
            "source-inline-chip",
            "related-posts",
            "yarpp",
        )
    ):
        return True
    return False


def render(node, page_slug: str) -> str:
    if isinstance(node, (Comment, Doctype, Declaration)):
        return ""
    if isinstance(node, NavigableString):
        text = str(node)
        if not text.strip():
            return ""
        return esc(text)
    if not isinstance(node, Tag) or skip_tag(node):
        return ""
    name = node.name
    if name == "img":
        remember_srcset(node.get("srcset") or "")
        src = remember_image(node.get("src") or "") or remember_image(node.get("data-src") or "") or remember_image(node.get("data-lazy-src") or "")
        if not src:
            return ""
        alt = esc(node.get("alt") or "")
        return f'<img src="{esc(src)}" alt="{alt}" loading="lazy" />'
    if name == "br":
        return "<br />"
    if name == "a":
        href = rewrite(node.get("href") or "", page_slug)
        inner = "".join(render(child, page_slug) for child in node.children).strip()
        if not inner:
            return ""
        kind = set(node.get("class") or [])
        button = "elementor-button" in kind or "btn" in kind or "wp-block-button__link" in kind
        cls = ' class="btn btn-primary"' if button else ""
        if not href:
            return inner
        return f'<a{cls} href="{esc(href)}">{inner}</a>'
    if name in {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote", "figcaption", "th", "td"}:
        inner = "".join(render(child, page_slug) for child in node.children).strip()
        if not inner:
            return ""
        return f"<{name}>{inner}</{name}>"
    if name in {"ul", "ol"}:
        items = "".join(render(child, page_slug) for child in node.children if getattr(child, "name", None) == "li")
        if not items:
            return ""
        return f"<{name}>{items}</{name}>"
    if name == "figure":
        inner = "".join(render(child, page_slug) for child in node.children).strip()
        return f"<figure>{inner}</figure>" if inner else ""
    if name == "table":
        inner = "".join(render(child, page_slug) for child in node.children).strip()
        return f"<table>{inner}</table>" if inner else ""
    if name in {"thead", "tbody", "tr"}:
        inner = "".join(render(child, page_slug) for child in node.children).strip()
        return f"<{name}>{inner}</{name}>" if inner else ""
    if name in {"head", "title", "meta", "link", "style", "script", "noscript", "iframe", "svg"}:
        return ""
    if name == "div" and "tags" in (node.get("class") or []):
        return ""
    if name == "div":
        block = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "table", "figure", "blockquote", "div", "article", "section", "main", "aside"}
        has_block = any(isinstance(child, Tag) and child.name in block for child in node.children)
        inner = "".join(render(child, page_slug) for child in node.children).strip()
        if not inner or not re.sub(r"<[^>]+>", "", inner).strip() and "<img" not in inner:
            return ""
        if not has_block and not re.search(r"<(?:h[1-6]|p|ul|ol|table|figure|blockquote)\b", inner):
            return f"<p>{inner}</p>"
        return inner
    return "".join(render(child, page_slug) for child in node.children)


def clean_html(entry_html: str, page_slug: str) -> str:
    soup = BeautifulSoup(f"<div id='root'>{entry_html}</div>", "html.parser")
    root = soup.find(id="root")
    html = "".join(render(child, page_slug) for child in root.children)
    html = pretty(html)
    seen = {"n": 0}

    def demote(match: re.Match) -> str:
        seen["n"] += 1
        tag = "h1" if seen["n"] == 1 else "h2"
        return f"<{tag}>{match.group(1)}</{tag}>"

    html = re.sub(r"<h1>(.*?)</h1>", demote, html, flags=re.S)
    return html.strip()


def pretty(html: str) -> str:
    html = re.sub(r"(</(?:h[1-6]|p|ul|ol|li|figure|table|blockquote|thead|tbody|tr)>)", r"\1\n", html)
    html = re.sub(r"(<(?:h[1-6]|p|ul|ol|figure|table|blockquote)\b)", r"\n\1", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


def replace_contacts(html: str) -> str:
    html = re.sub(r"tel:\+?1?[-.\s]*715[-.\s]*567[-.\s]*5456", "tel:6512478384", html, flags=re.I)
    html = html.replace("info@troycondogarages.com", "troycondogaragesbyvalmark@gmail.com")
    html = html.replace("54022", "54016")
    html = re.sub(
        r"(?<![\d/])\+?1?[\s.\-]*\(?715\)?[\s.\-]*567[\s.\-]*5456",
        "(651) 247-8384",
        html,
    )
    return html


def fix_contacts(html: str) -> str:
    html = replace_contacts(html)
    parts = re.split(r"(<[^>]+>)", html)
    in_a = False
    out = []
    for part in parts:
        if part.startswith("<"):
            if re.match(r"<a\b", part, re.I):
                in_a = True
            elif re.match(r"</a\b", part, re.I):
                in_a = False
            out.append(part)
            continue
        if not in_a:
            part = part.replace(
                "(651) 247-8384",
                '<a href="tel:6512478384">(651) 247-8384</a>',
            )
            part = part.replace(
                "troycondogaragesbyvalmark@gmail.com",
                '<a href="mailto:troycondogaragesbyvalmark@gmail.com">troycondogaragesbyvalmark@gmail.com</a>',
            )
        out.append(part)
    return "".join(out)


def content_root(soup: BeautifulSoup):
    entry = soup.find("div", class_="entry-content")
    if entry and len(entry.get_text(" ", strip=True)) > 40:
        return entry
    content = soup.find(id="content") or soup.find("div", class_="site-content")
    if content is None:
        return entry
    for bad in content.find_all(["header", "footer", "nav", "script", "style"]):
        bad.decompose()
    return content


def strip_chrome(node):
    if node is None:
        return None
    for bad in list(node.find_all(string=lambda text: isinstance(text, (Comment, Doctype, Declaration)))):
        bad.extract()
    for bad in node.find_all(["head", "title", "meta", "link", "style", "script", "noscript", "iframe", "svg"]):
        bad.decompose()
    return node


def load_entry(slug: str) -> tuple[str, str, str]:
    path = SNAP / slug / "index.html"
    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else slug
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag.get("content", "").strip() if desc_tag else ""
    node = strip_chrome(content_root(soup))
    entry_html = node.decode_contents() if node else ""
    return title, description, entry_html


def h2_keys(html: str) -> set[str]:
    keys = set()
    for match in re.finditer(r"<h2>(.*?)</h2>", html, re.S | re.I):
        text = re.sub(r"<[^>]+>", "", match.group(1))
        text = re.sub(r"\s+", " ", text).strip().lower()
        if text:
            keys.add(text)
    return keys


def extra_sections(source_html: str, covered: set[str]) -> str:
    source_html = re.sub(r"<h1>.*?</h1>", "", source_html, count=1, flags=re.S)
    chunks = re.split(r"(?=<h2>)", source_html)
    preamble = chunks[0].strip() if chunks else ""
    added = []
    for chunk in chunks[1:]:
        match = re.match(r"<h2>(.*?)</h2>", chunk, re.S | re.I)
        if not match:
            continue
        key = re.sub(r"<[^>]+>", "", match.group(1))
        key = re.sub(r"\s+", " ", key).strip().lower()
        if key and key not in covered:
            if not added and preamble:
                added.append(preamble)
            added.append(chunk.strip())
            covered.add(key)
    return "\n".join(added)


def first_h1(html: str) -> str:
    match = re.search(r"<h1>(.*?)</h1>", html, re.S | re.I)
    if not match:
        return ""
    return unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", match.group(1)))).strip()


def related(slug: str, titles: dict[str, str]) -> str:
    group = GROUPS[LETTER[slug]]
    index = group.index(slug)
    picks = []
    for step in range(1, len(group)):
        other = group[(index + step) % len(group)]
        if other != slug:
            picks.append(other)
        if len(picks) == 3:
            break
    links = ['<a href="/guides/">All guides</a>']
    links += [f'<a href="/{item}/">{esc(titles.get(item, item))}</a>' for item in picks]
    return "<p>More guides: " + ", ".join(links) + ".</p>"


def page_shell(slug: str, title: str, description: str, body: str) -> str:
    canonical = f"https://troycondogarages.com/{slug}/"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <link rel="icon" href="/assets/cropped-293856347_101769785949118_3680151206583370806_n-32x32.jpg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Quicksand:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/theme.css" />
  <link rel="stylesheet" href="/css/pages.css" />
  <!-- Google tag (gtag.js) AW-18398757431 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=AW-18398757431"></script>
  <script src="/js/analytics.js"></script>
  <script src="/js/call-tracking.js"></script>
  <link rel="canonical" href="{canonical}" />
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="logo" href="/"><img src="/assets/293856347_101769785949118_3680151206583370806_n-Edited-Edited.png" alt="Troy Condo Garages" width="180" height="120" /></a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Menu">☰</button>
      <nav class="site-nav" id="primary-nav" aria-label="Primary">
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/units/">Our Units</a></li>
          <li><a href="/design-your-space/">Design Your Space</a></li>
          <li><a href="/gallery/">Gallery</a></li>
          <li><a href="/events/">Events</a></li>
          <li><a href="/rentals/">Rentals</a></li>
          <li><a href="/about/">About</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/financing/">Financing</a></li>
          <li><a href="/pricing/">Pricing</a></li>
        </ul>
      </nav>
      <a class="btn header-cta" href="/contact/#lead-form">Book a Tour</a>
    </div>
  </header>
  <main id="main">
    <section class="section">
      <div class="container">
{body}
      </div>
    </section>
  </main>
  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <a class="logo" href="/"><img src="/assets/293856347_101769785949118_3680151206583370806_n-Edited.png" alt="Troy Condo Garages" width="160" height="105" /></a>
        <p>Troy Condo Garages LLC by ValMark<br />663 Valerie Ave, Hudson, WI 54016</p>
        <p><a href="tel:6512478384">(651) 247-8384</a><br /><a href="mailto:troycondogaragesbyvalmark@gmail.com">troycondogaragesbyvalmark@gmail.com</a></p>
      </div>
      <div>
        <h3>Quick links</h3>
        <ul class="footer-links">
          <li><a href="/">Home</a></li>
          <li><a href="/units/">Our Units</a></li>
          <li><a href="/design-your-space/">Design Your Space</a></li>
          <li><a href="/gallery/">Gallery</a></li>
          <li><a href="/events/">Events</a></li>
          <li><a href="/rentals/">Rentals</a></li>
          <li><a href="/about/">About</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/financing/">Financing</a></li>
          <li><a href="/pricing/">Pricing</a></li>
          <li><a href="/guides/">Guides</a></li>
          <li><a href="/documents/">HOA Documents</a></li>
          <li><a href="/privacy-policy/">Privacy Policy</a></li>
          <li><a href="/terms-of-service/">Terms</a></li>
        </ul>
      </div>
      <div>
        <h3>Visit</h3>
        <p>663 Valerie Ave, Hudson, WI 54016</p>
        <a class="btn btn-primary" href="/contact/#lead-form">Schedule a Tour</a>
      </div>
    </div>
    <div class="container footer-bottom"><p>&copy; <span id="y"></span> Troy Condo Garages LLC by ValMark.</p></div>
  </footer>
  <script src="/js/nav.js"></script>
  <script>document.getElementById("y").textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def indent_body(html: str) -> str:
    lines = [line for line in html.splitlines() if line.strip()]
    return "\n".join("        " + line.strip() for line in lines)


def win_path(path: Path) -> str:
    text = os.path.abspath(str(path))
    if os.name == "nt" and len(text) >= 240 and not text.startswith("\\\\?\\"):
        return "\\\\?\\" + text
    return text


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    shutil.copy2(win_path(src), win_path(dest))


def copy_assets() -> None:
    fallback = SITE / "assets" / "475852121_592613430197840_8786842729915776913_n.jpg"
    missing = []
    for rel in sorted(COPIED):
        dest = SITE / rel
        src = SNAP / rel
        if src.is_file():
            copy_file(src, dest)
            continue
        if src.name == fallback.name and fallback.is_file():
            copy_file(fallback, dest)
            continue
        missing.append(rel)
    legal = SITE / "documents" / "legal"
    legal.mkdir(parents=True, exist_ok=True)
    for name in (
        "original-declaration.pdf",
        "1st-amendment.pdf",
        "2nd-amendment.pdf",
        "3rd-amendment.pdf",
        "4th-amendment.pdf",
    ):
        copy_file(SNAP / "documents" / "legal" / name, legal / name)
    print("images", len(COPIED))
    if missing:
        print("MISSING IMAGES")
        for rel in missing:
            print(" ", rel)


def write_vercel() -> None:
    config = {
        "cleanUrls": True,
        "trailingSlash": True,
        "headers": [
            {
                "source": "/(.*)",
                "headers": [
                    {"key": "X-Content-Type-Options", "value": "nosniff"},
                    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                ],
            }
        ],
        "redirects": [
            {"source": source, "destination": dest, "statusCode": 301}
            for source, dest in REDIRECTS.items()
        ]
        + [
            {"source": "/info@troycondogarages.com", "destination": "/contact/", "statusCode": 301},
            {"source": "/info%40troycondogarages.com/", "destination": "/contact/", "statusCode": 301},
            {"source": "/info%40troycondogarages.com", "destination": "/contact/", "statusCode": 301},
            {"source": "/:path*/feed", "destination": "/", "statusCode": 301},
            {"source": "/:path*/feed/", "destination": "/", "statusCode": 301},
            {"source": "/feed/", "destination": "/", "statusCode": 301},
            {"source": "/tag/:path*", "destination": "/", "statusCode": 301},
            {"source": "/tag/:path*/", "destination": "/", "statusCode": 301},
            {"source": "/category/:path*", "destination": "/", "statusCode": 301},
            {"source": "/category/:path*/", "destination": "/", "statusCode": 301},
            {"source": "/author/:path*", "destination": "/", "statusCode": 301},
            {"source": "/author/:path*/", "destination": "/", "statusCode": 301},
        ],
    }
    (SITE / "vercel.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


def write_sitemap(slugs: list[str]) -> None:
    urls = [
        "https://troycondogarages.com/",
        "https://troycondogarages.com/units/",
        "https://troycondogarages.com/design-your-space/",
        "https://troycondogarages.com/gallery/",
        "https://troycondogarages.com/events/",
        "https://troycondogarages.com/rentals/",
        "https://troycondogarages.com/about/",
        "https://troycondogarages.com/contact/",
        "https://troycondogarages.com/financing/",
        "https://troycondogarages.com/pricing/",
        "https://troycondogarages.com/guides/",
    ]
    urls += [f"https://troycondogarages.com/{slug}/" for slug in slugs if slug != "documents"]
    if len(urls) != 56:
        raise SystemExit(f"sitemap count {len(urls)} != 56")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append("    <lastmod>2026-10-24</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def patch_footers() -> None:
    extra = """          <li><a href="/pricing/">Pricing</a></li>
          <li><a href="/guides/">Guides</a></li>
          <li><a href="/documents/">HOA Documents</a></li>
          <li><a href="/privacy-policy/">Privacy Policy</a></li>
          <li><a href="/terms-of-service/">Terms</a></li>"""
    for path in SITE.glob("*.html"):
        text = path.read_text(encoding="utf-8")
        if 'href="/guides/"' in text:
            continue
        match = re.search(r'<ul class="footer-links">[\s\S]*?</ul>', text)
        if not match or 'href="/pricing/"' not in match.group(0):
            print("footer not patched", path.name)
            continue
        updated = match.group(0).replace(
            '<li><a href="/pricing/">Pricing</a></li>',
            extra,
            1,
        )
        path.write_text(text.replace(match.group(0), updated, 1), encoding="utf-8")


def patch_homepage() -> None:
    path = SITE / "index.html"
    text = path.read_text(encoding="utf-8")
    needle = "<p>Yes, by appointment only. Storefront retail and residential occupancy are not permitted.</p>"
    insert = needle + '\n        <p>More answers in our <a href="/guides/">garage condo guides</a>.</p>'
    if needle not in text:
        raise SystemExit("homepage FAQ sentence anchor missing")
    if "garage condo guides" not in text:
        path.write_text(text.replace(needle, insert, 1), encoding="utf-8")


def money_report(pages: dict[str, str]) -> None:
    print("\nMONEY")
    for slug in sorted(MONEY):
        text = re.sub(r"<[^>]+>", " ", pages[slug])
        figures = re.findall(
            r"\$\s?\d[\d,]*(?:\.\d+)?|\d+(?:\.\d+)?(?:\s*[–\-]\s*\d+(?:\.\d+)?)?\s?(?:%|percent)",
            text,
            flags=re.I,
        )
        unique = []
        for figure in figures:
            cleaned = re.sub(r"\s+", " ", figure).strip(" .,;")
            if cleaned not in unique:
                unique.append(cleaned)
        print(slug)
        for figure in unique:
            print("  ", figure)


def guides_page(titles: dict[str, str]) -> str:
    parts = [
        "<h1>Garage Condo Guides</h1>",
        "<p class=\"lead\">Guides for buying, outfitting, and using a garage condo at Troy Condo Garages in Hudson, WI, serving the St. Croix Valley and the Twin Cities.</p>",
    ]
    for heading, slugs in HUB.items():
        parts.append(f"<h2>{esc(heading)}</h2>")
        items = "".join(
            f'<li><a href="/{slug}/">{esc(titles[slug])}</a></li>' for slug in slugs
        )
        parts.append(f"<ul>{items}</ul>")
    parts.append('<p><a class="btn btn-primary" href="/#lead-form">Book a tour</a></p>')
    body = indent_body("\n".join(parts))
    return page_shell(
        "guides",
        "Garage Condo Guides for Hudson, WI & the Twin Cities | Troy Condo Garages",
        "Garage condo guides for Hudson, WI and the Twin Cities: buying, costs, storage uses, build-outs, and nearby areas.",
        body,
    )


def main() -> None:
    hub_slugs = [slug for slugs in HUB.values() for slug in slugs]
    expected = GROUPS["A"] + GROUPS["B"] + GROUPS["C"]
    if sorted(hub_slugs) != sorted(expected) or len(hub_slugs) != len(set(hub_slugs)):
        raise SystemExit("guides hub does not list every A–C page once")
    live_or_restored = RESTORED | LIVE
    for source in REDIRECTS:
        if source.strip("/") in live_or_restored:
            raise SystemExit(f"redirect source is a live page: {source}")
    cleaned: dict[str, str] = {}
    titles: dict[str, str] = {}
    doc_titles: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    for slug in LETTER:
        title, description, entry = load_entry(slug)
        body = fix_contacts(clean_html(entry, slug))
        if "<h1>" not in body:
            body = f"<h1>{esc(title)}</h1>\n" + body
        words = len(re.sub(r"<[^>]+>", " ", body).split())
        print(f"{slug} {words}")
        cleaned[slug] = body
        titles[slug] = first_h1(body) or title
        doc_titles[slug] = title
        descriptions[slug] = replace_contacts(description or title)
    for target, source in MERGE.items():
        _, _, entry = load_entry(source)
        extra = fix_contacts(clean_html(entry, target))
        added = extra_sections(extra, h2_keys(cleaned[target]))
        if added:
            cleaned[target] = cleaned[target] + "\n" + added
            print(f"merged sections into {target} from {source}")
        else:
            print(f"no new sections for {target} from {source}")
    for slug, body in cleaned.items():
        cta = (
            '<p><a class="btn btn-primary" href="/#lead-form">Book a tour</a></p>\n'
            + related(slug, titles)
        )
        full = page_shell(slug, doc_titles[slug], descriptions[slug], indent_body(body + "\n" + cta))
        if slug == "documents":
            dest = SITE / "documents" / "index.html"
        else:
            dest = SITE / f"{slug}.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(full, encoding="utf-8")
    (SITE / "guides.html").write_text(guides_page(titles), encoding="utf-8")
    copy_assets()
    patch_footers()
    patch_homepage()
    write_sitemap(list(LETTER))
    write_vercel()
    money_report(cleaned)
    print("pages", len(cleaned))


if __name__ == "__main__":
    main()
