import hashlib
import shutil
import zipfile
from pathlib import Path

zip_path = Path(r"C:\Users\rohla\Downloads\Valerie Ave Images-20260909T205406Z-1-001.zip")
repo = Path(r"C:\Users\rohla\.cursor\skills\website\troy condo garages website- Gavin")
out_dir = repo / "site" / "assets" / "valerie-ave"
tmp = repo / ".tmp-valerie-ave"

if tmp.exists():
    shutil.rmtree(tmp)
tmp.mkdir(parents=True)

with zipfile.ZipFile(zip_path, "r") as zf:
    zf.extractall(tmp)

if out_dir.exists():
    shutil.rmtree(out_dir)
out_dir.mkdir(parents=True)

seen = {}
copied = []
for p in sorted(tmp.rglob("*")):
    if not p.is_file():
        continue
    if p.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        continue
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    if digest in seen:
        print(f"skip dup {p.name} == {seen[digest]}")
        continue
    idx = len(copied) + 1
    dest_name = f"valerie-ave-{idx:02d}.jpg"
    dest = out_dir / dest_name
    shutil.copy2(p, dest)
    seen[digest] = dest_name
    copied.append(dest_name)
    print(f"ok {dest_name} <- {p.name}")

shutil.rmtree(tmp)
print(f"UNIQUE {len(copied)}")
(out_dir / "_manifest.txt").write_text("\n".join(copied) + "\n", encoding="utf-8")
