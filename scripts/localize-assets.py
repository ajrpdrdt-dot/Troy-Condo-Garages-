"""Download remote Troy media into site/assets and rewrite HTML references."""

from __future__ import annotations

import hashlib
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ASSETS = SITE / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

URL_RE = re.compile(r"https://troycondogarages\.com/wp-content/uploads/[^\s\"'<>]+")


def local_name(url: str) -> str:
    name = Path(url.split("?")[0]).name
    # keep readable names; if collision, hash prefix
    return name


def main() -> None:
    html_files = list(SITE.rglob("*.html"))
    urls: set[str] = set()
    for path in html_files:
        urls.update(URL_RE.findall(path.read_text(encoding="utf-8")))

    mapping: dict[str, str] = {}
    used_names: dict[str, str] = {}

    for url in sorted(urls):
        name = local_name(url)
        if name in used_names and used_names[name] != url:
            stem = Path(name).stem
            suffix = Path(name).suffix
            digest = hashlib.md5(url.encode()).hexdigest()[:8]
            name = f"{stem}-{digest}{suffix}"
        used_names[name] = url
        dest = ASSETS / name
        if not dest.exists():
            print(f"Downloading {url}")
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "TroySiteLocalizer/1.0"})
                with urllib.request.urlopen(req, timeout=60) as resp:
                    dest.write_bytes(resp.read())
            except Exception as exc:  # noqa: BLE001
                print(f"  FAILED: {exc}")
                continue
        else:
            print(f"Exists {name}")
        mapping[url] = f"/assets/{name}"

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        original = text
        for url, local in mapping.items():
            text = text.replace(url, local)
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"Updated {path.name}")

    print(f"Done. {len(mapping)} assets mapped.")


if __name__ == "__main__":
    main()
