#!/usr/bin/env python3
"""Serve Troy Condo Garages static site for local preview."""

from __future__ import annotations

import argparse
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


class SiteHandler(SimpleHTTPRequestHandler):
    site_dir: Path

    def translate_path(self, path: str) -> str:
        parsed = urlparse(unquote(path))
        route = parsed.path.strip("/")

        if route == "":
            candidate = self.site_dir / "index.html"
            if candidate.is_file():
                return str(candidate)

        # Pretty routes: /units/ -> units.html, /css/theme.css stays as file path
        candidate = self.site_dir / f"{route}.html"
        if candidate.is_file():
            return str(candidate)

        # Nested-looking routes still map to basename.html (e.g. units/index)
        name = Path(route).name
        if name:
            candidate = self.site_dir / f"{name}.html"
            if candidate.is_file():
                return str(candidate)

        # Static assets under site/ (css/, js/, assets/)
        asset = self.site_dir / route
        if asset.is_file():
            return str(asset)

        return str(self.site_dir / route)

    def log_message(self, format: str, *args) -> None:
        print(f"[local-preview] {self.address_string()} - {format % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Troy Condo Garages local preview server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    site_dir = repo_root / "site"

    if not site_dir.is_dir():
        raise SystemExit(f"Site directory not found: {site_dir}")

    os.chdir(site_dir)
    SiteHandler.site_dir = site_dir

    server = ThreadingHTTPServer((args.host, args.port), SiteHandler)
    url = f"http://{args.host}:{args.port}/"
    print(f"Serving Troy Condo Garages static site at {url}")
    print(f"Site directory: {site_dir}")
    print("Routes: / /units/ /design-your-space/ /gallery/ /events/ /rentals/ /about/ /contact/ /financing/ /pricing/")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
