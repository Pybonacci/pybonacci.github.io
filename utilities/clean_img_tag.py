"""
Reemplaza los bonitos img tags de WP por markdown
"""

from pathlib import Path
import re
import shutil

img_tag = re.compile("\[<img.*")
img_title = re.compile('<img[^>]+title="([^">]+)"')
img_src = re.compile('<img[^>]+src="([^">]+)"')

#r.findall(text)[0]
#re.search('<img[^>]+title="([^">]+)"', tag).group(1)
#re.search('<img[^>]+src="([^">]+)"', tag).group(1)


def process_img_tags(text):
    matches = img_tag.findall(text)
    for match in matches:
        replacement_block = process_img_tag_block(match)
        text = text.replace(match, replacement_block)
    old = "://new.pybonacci.org/images/"
    new = "://pybonacci.org/images/"
    text = text.replace(old, new)
    return text


def process_img_tag_block(match):
    src = img_src.search(match).group(1)
    title_match = img_title.search(match)
    if title_match:
        title = title_match.group(1)
    else:
        title = ""

    replacement = "![{title}]({src})".format(title=title, src=src)
    return replacement


def needs_processing(text):
    return img_tag.findall(text)


def process_text(text):
    return process_img_tags(text)


def process_file(f):
    file_text = f.read_text()
    if needs_processing(file_text):
        print("PROCESSING FILE", f)
        #import ipdb;ipdb.set_trace()
        shutil.copy(str(f), str(f) + ".bak")
        processed_text = process_text(file_text)
        with open(f, "w") as outfile:
            outfile.write(processed_text)


def process_files():
    _path = Path("..", "content", "articles")
    pathfiles = sorted(list(_path.glob("*.md")))
    for f in pathfiles:
        process_file(f)


if __name__ == "__main__":
    process_files()

