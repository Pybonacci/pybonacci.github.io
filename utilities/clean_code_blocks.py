from pathlib import Path
import re
import shutil


"""
<pre><.*>([.\s\S]*)<\/code><\/pre>
"<pre><.*>"
matches = re.finditer("<pre><code.*[language-]?(\w*)>([.\s\S]*?)<\/code><\/pre>", text)
re.findall('<pre><code class="(.*)">.*', n.group(0))
"""


def process_inline_code(text):
    matches = re.finditer("<pre><code.*[language-]?>(.*)</code></pre>", text)
    for match in matches:
        replacement_block = process_inline_code_block(match)
        text = text.replace(match.group(0), replacement_block)
    return text


def process_inline_code_block(match):
    lang = re.findall('<pre><code class="(.*)">.*', match.group(0))
    if lang:
        lang = lang[0].replace("language-", "")
    replacement = "    :::{lang}\n    {code}".format(
        lang=lang, code=match.group(1))
    return replacement


def process_multiline_code(text):
    matches = re.finditer("<pre><code.*[language-]?>([.\s\S]*?)</code></pre>", text)
    for match in matches:
        replacement_block = process_multiline_code_block(match)
        text = text.replace(match.group(0), replacement_block)
    return text


def process_multiline_code_block(match):
    lang = re.findall('<pre><code class="(.*)">.*', match.group(0))
    if lang:
        lang = lang[0].replace("language-", "")
    code_replacement = "\n    ".join(match.group(1).split("\n"))
    replacement = "    :::{lang}\n    {code}".format(
        lang=lang, code=code_replacement)
    return replacement


def needs_processing(text):
    return re.findall("<pre><code", text)


def process_text(text):
    return process_multiline_code(process_inline_code(text))


def process_file(f):
    shutil.copy(str(f), str(f) + ".bak")
    file_text = f.read_text()
    if needs_processing(file_text):
        print("PROCESSING FILE", f)
        processed_text = process_text(file_text)
        with open(f, "w") as outfile:
            outfile.write(processed_text)


def process_files():
    _path = Path("..", "content", "articles")
    pathfiles = list(_path.glob("*.md"))
    for f in pathfiles:
        process_file(f)


if __name__ == "__main__":
    process_files()
