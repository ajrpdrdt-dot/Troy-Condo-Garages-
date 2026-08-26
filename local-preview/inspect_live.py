import json
from pathlib import Path

p = Path.home() / "AppData/Local/Temp/live-page-18.json"
data = json.loads(p.read_text(encoding="utf-8"))
c = data.get("content", {}).get("rendered", "")
print("modified", data.get("modified"))
print("title", data.get("title", {}).get("rendered"))
print("content_len", len(c))
print("has_elementor", "elementor" in c.lower())
print("snippet", c[:500].replace("\n", " "))
