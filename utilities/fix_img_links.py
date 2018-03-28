from pathlib import Path
import shutil

_path = Path("..", "content", "articles")

pathfiles = list(_path.glob("*.md"))

old = "://new.mmngreco.org/images/"
new = "://mmngreco.org/images/"

for f in pathfiles:
    shutil.copy(str(f), str(f) + ".bak")
    with open(f, 'r') as infile:
        data = infile.read()
    with open(f, "w") as outfile:
        outfile.write(data.replace(old, new))
