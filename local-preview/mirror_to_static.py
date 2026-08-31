"""
Mirror troycondogarages.com (live WordPress) into a static ./public folder
for Vercel deployment. Downloads pages + assets, rewrites internal links to
relative paths, and injects the Google Ads gtag snippet into every page.
"""
import hashlib
import re
import time
from pathlib import Path
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"
LIVE = "https://troycondogarages.com"

GTAG_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18398757431"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'AW-18398757431');
</script>
"""

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; TroyCondoMirror/1.0)"})

visited_pages = {}   # url -> local relative path
asset_map = {}        # url -> local relative path (wp-content/wp-includes etc)
to_visit = [LIVE + "/"]
seen_urls = set(to_visit)

SKIP_EXT = (".zip", ".pdf.orig",)


def local_page_path(url: str) -> Path:
    path = urlparse(url).path.strip("/")
    if path == "":
        return OUT / "index.html"
    return OUT / path / "index.html"


def url_to_page_relpath(url: str) -> str:
    path = urlparse(url).path.strip("/")
    if path == "":
        return "/"
    return "/" + path + "/"


def is_internal_page(url: str) -> bool:
    u = urlparse(url)
    if u.netloc not in ("", "troycondogarages.com", "www.troycondogarages.com"):
        return False
    path = u.path
    if any(seg in path for seg in ("/wp-content/", "/wp-includes/", "/wp-json/", "/wp-admin/", "/feed/", "/xmlrpc.php")):
        return False
    if re.search(r"\.(jpg|jpeg|png|gif|webp|svg|css|js|ico|woff|woff2|ttf|eot|xml|txt|json)$", path, re.I):
        return False
    return True


def is_asset(url: str) -> bool:
    u = urlparse(url)
    if u.netloc not in ("", "troycondogarages.com", "www.troycondogarages.com"):
        return False
    return "/wp-content/" in u.path or "/wp-includes/" in u.path


def fetch(url: str):
    for attempt in range(3):
        try:
            r = session.get(url, timeout=30)
            if r.status_code == 200:
                return r
        except requests.RequestException:
            time.sleep(1)
    return None


def _shorten_component(name: str, max_len: int = 100) -> str:
    if len(name) <= max_len:
        return name
    h = hashlib.sha1(name.encode("utf-8")).hexdigest()[:10]
    dot = name.rfind(".")
    ext = name[dot:] if dot != -1 else ""
    stem = name[:dot] if dot != -1 else name
    keep = max_len - len(ext) - len(h) - 1
    return stem[:keep] + "-" + h + ext


def save_asset(url: str) -> str:
    """Download an asset (css/js/image under wp-content/wp-includes) and
    return its local relative path (relative to site root, e.g. /wp-content/x.js)."""
    if url in asset_map:
        return asset_map[url]
    u = urlparse(url)
    rel_path = u.path  # e.g. /wp-content/themes/astra/...
    safe_parts = [_shorten_component(p) for p in rel_path.split("/") if p != ""]
    safe_rel_path = "/" + "/".join(safe_parts)
    dest = OUT.joinpath(*safe_parts)
    if not dest.exists():
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            r = fetch(url)
            if r is None:
                asset_map[url] = safe_rel_path
                return safe_rel_path
            dest.write_bytes(r.content)
        except OSError as e:
            print("  SKIP asset (path issue)", url, e)
            asset_map[url] = safe_rel_path
            return safe_rel_path
        # If it's CSS, also grab its own asset refs (fonts, url())
        if rel_path.endswith(".css"):
            try:
                text = r.content.decode("utf-8", errors="ignore")
                for m in re.finditer(r"url\(([^)]+)\)", text):
                    ref = m.group(1).strip("'\" ")
                    if ref.startswith("data:"):
                        continue
                    abs_ref = urljoin(url, ref)
                    if is_asset(abs_ref):
                        save_asset(abs_ref)
            except Exception:
                pass
    asset_map[url] = safe_rel_path
    return safe_rel_path


def process_page(url: str, html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Rewrite <a href>
    for a in soup.find_all("a", href=True):
        href = a["href"]
        abs_href = urljoin(url, href)
        if is_internal_page(abs_href):
            rel = url_to_page_relpath(abs_href)
            a["href"] = rel
            if abs_href not in seen_urls:
                seen_urls.add(abs_href)
                to_visit.append(abs_href)

    # Rewrite asset refs: img src/srcset, script src, link href
    for tag, attr in [("img", "src"), ("script", "src"), ("link", "href"), ("source", "src")]:
        for el in soup.find_all(tag):
            val = el.get(attr)
            if val:
                abs_val = urljoin(url, val)
                if is_asset(abs_val):
                    rel = save_asset(abs_val)
                    el[attr] = rel
            srcset = el.get("srcset")
            if srcset:
                parts = []
                for piece in srcset.split(","):
                    bits = piece.strip().split(" ")
                    if bits and bits[0]:
                        abs_val = urljoin(url, bits[0])
                        if is_asset(abs_val):
                            bits[0] = save_asset(abs_val)
                    parts.append(" ".join(bits))
                el["srcset"] = ", ".join(parts)

    # Inject gtag snippet right after <head>
    head = soup.find("head")
    if head is not None:
        snippet_soup = BeautifulSoup(GTAG_SNIPPET, "html.parser")
        head.insert(0, snippet_soup)

    return str(soup)


def run():
    OUT.mkdir(exist_ok=True)
    count = 0
    while to_visit:
        url = to_visit.pop(0)
        if url in visited_pages:
            continue
        print("Fetching", url)
        r = fetch(url)
        if r is None:
            print("  FAILED", url)
            continue
        html = r.text
        new_html = process_page(url, html)
        dest = local_page_path(url)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(new_html, encoding="utf-8")
        visited_pages[url] = str(dest)
        count += 1
    print(f"Done. {count} pages, {len(asset_map)} assets.")


if __name__ == "__main__":
    run()
