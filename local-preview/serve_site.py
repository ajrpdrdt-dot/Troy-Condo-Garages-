#!/usr/bin/env python
"""
Local preview server for the new static site (site/), separate from the
legacy WordPress/Elementor export served from public/.

Usage:
    python local-preview/serve_site.py [port]

Then open:
    http://127.0.0.1:8080/            (build-status hub)
    http://127.0.0.1:8080/rentals.html
"""
import http.server
import os
import sys
import socketserver

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)


if __name__ == "__main__":
    if not os.path.isdir(ROOT):
        print(f"ERROR: static site folder not found at {ROOT}")
        sys.exit(1)
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Serving {ROOT}")
        print(f"  http://127.0.0.1:{PORT}/")
        print(f"  http://127.0.0.1:{PORT}/rentals.html")
        httpd.serve_forever()
