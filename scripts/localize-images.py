#!/usr/bin/env python3
"""Download remote WP upload images into site/assets and rewrite HTML refs."""

from __future__ import annotations

import hashlib
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ASSETS = SITE / "assets"
PREFIX = "https://troycondogarages.com/wp-content/uploads/"
URL_RE = re.compile(r"https://troycondogarages\.com/wp-content/uploads/[^\s\"'\\)>]+")


def safe_name(url: str) -> str:
    path = url.split("?", 1)[0]
    name = Path(path).name
    # keep extension; shorten very long names
    stem = Path(name).stem
    ext = Path(name).suffix.lower() or ".jpg"
    if len(stem) > 80:
        digest = hashlib.sha1(url.encode()).hexdigest()[:10]
        stem = stem[:60] + "-" + digest
    # sanitize
    stem = re.sub(r"[^a-zA-Z0-9._-]+", "-", stem).strip("-")
    return f"{stem}{ext}"


def collect_urls() -> set[str]:
    urls: set[str] = set()
    for html in SITE.glob("*.html"):
        text = html.read_text(encoding="utf-8")
        for match in URL_RE.findall(text):
            urls.add(match.rstrip(".,);"))
    return urls


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        print(f"skip exists {dest.name}")
        return True

    candidates = [url]
    if "troycondogarages.com/wp-content/uploads/" in url:
        candidates.append(
            url.replace(
                "https://troycondogarages.com",
                "https://ijt.ppp.mybluehost.me/website_9b507a73",
            )
        )

    headers = {
        "User-Agent": "Mozilla/5.0 TroySiteLocalizer/1.0",
        "Referer": "https://troycondogarages.com/",
    }
    last_error: Exception | None = None
    for candidate in candidates:
        req = urllib.request.Request(candidate, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            dest.write_bytes(data)
            print(f"ok {dest.name} ({len(data)} bytes) from {candidate.split('/')[2]}")
            return True
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            continue

    print(f"FAIL {url} -> {last_error}")
    return False


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    urls = collect_urls()
    print(f"Found {len(urls)} unique remote upload URLs")

    mapping: dict[str, str] = {}
    failed: list[str] = []

    for url in sorted(urls):
        local_name = safe_name(url)
        dest = ASSETS / local_name
        if download(url, dest):
            mapping[url] = f"/assets/{local_name}"
        else:
            failed.append(url)

    # rewrite HTML
    for html in SITE.glob("*.html"):
        text = html.read_text(encoding="utf-8")
        original = text
        for remote, local in mapping.items():
            text = text.replace(remote, local)
        if text != original:
            html.write_text(text, encoding="utf-8")
            print(f"updated {html.name}")

    # remove placeholder note if present
    gitkeep = ASSETS / ".gitkeep"
    if gitkeep.exists() and any(ASSETS.iterdir()):
        # keep .gitkeep; fine either way
        pass

    print("---")
    print(f"localized {len(mapping)} images")
    if failed:
        print(f"failed {len(failed)}:")
        for u in failed:
            print(" ", u)


if __name__ == "__main__":
    main()
