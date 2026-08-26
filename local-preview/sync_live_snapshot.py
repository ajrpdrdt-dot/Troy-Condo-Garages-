import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
WP = ROOT.parent / "wordpress-backup/ijtpppmy/homedir/public_html/website_9b507a73"
SNAP = WP / "wp-content/live-snapshot"
SNAP.mkdir(parents=True, exist_ok=True)

LIVE = "https://troycondogarages.com"
LOCAL = "http://127.0.0.1:8080"
UA = ["-s", "--max-time", "60", "-L"]


def curl_json(url: str):
    raw = subprocess.check_output(["curl.exe", *UA, url], stderr=subprocess.DEVNULL)
    return json.loads(raw.decode("utf-8"))


def curl_file(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["curl.exe", *UA, "-o", str(dest), url])


def rewrite(html: str) -> str:
    # Point internal page links at local preview, but keep wp-content / wp-includes on live
    # so current CSS, JS, and images load.
    html = html.replace(LIVE + "/wp-content/", "___LIVE_CONTENT___")
    html = html.replace(LIVE + "/wp-includes/", "___LIVE_INCLUDES___")
    html = html.replace("//troycondogarages.com/wp-content/", "___LIVE_CONTENT_SL___")
    html = html.replace(LIVE, LOCAL)
    html = html.replace("___LIVE_CONTENT___", LIVE + "/wp-content/")
    html = html.replace("___LIVE_INCLUDES___", LIVE + "/wp-includes/")
    html = html.replace("___LIVE_CONTENT_SL___", "//troycondogarages.com/wp-content/")
    return html


def slug_to_filename(slug: str) -> str:
    if not slug or slug == "home":
        return "index.html"
    return slug.strip("/") + ".html"


def collect_urls():
    urls = [(LIVE + "/", "index.html")]
    pages = curl_json(f"{LIVE}/wp-json/wp/v2/pages?per_page=100&_fields=slug,link")
    posts = curl_json(f"{LIVE}/wp-json/wp/v2/posts?per_page=100&_fields=slug,link")
    for item in pages + posts:
        link = item.get("link") or f"{LIVE}/{item['slug']}/"
        slug = item.get("slug") or urlparse(link).path.strip("/").replace("/", "-")
        if slug in ("home", ""):
            continue
        urls.append((link, slug_to_filename(slug)))
    # unique by filename
    seen = {}
    for url, name in urls:
        seen[name] = url
    return [(url, name) for name, url in seen.items()]


def main():
    urls = collect_urls()
    print(f"Downloading {len(urls)} pages from live site...")
    index = []
    for url, name in urls:
        dest = SNAP / name
        try:
            curl_file(url, dest)
            html = dest.read_text(encoding="utf-8", errors="replace")
            if "Not Acceptable" in html and "<title>Not Acceptable" in html:
                print("BLOCKED", url)
                dest.unlink(missing_ok=True)
                continue
            dest.write_text(rewrite(html), encoding="utf-8")
            print("OK", name, dest.stat().st_size)
            index.append({"file": name, "source": url})
        except Exception as e:
            print("FAIL", url, e)
    (SNAP / "manifest.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    print("Wrote", len(index), "snapshots to", SNAP)


if __name__ == "__main__":
    main()
