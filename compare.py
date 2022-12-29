import urllib.request
import os
import epubcrush
import subprocess

urls = [
    "https://standardebooks.org/ebooks/james-joyce/poetry/downloads/"
    "james-joyce_poetry.epub",
    "https://standardebooks.org/ebooks/"
    "karl-marx_friedrich-engels/the-communist-manifesto/samuel-moore/downloads/"
    "karl-marx_friedrich-engels_the-communist-manifesto_samuel-moore.epub",
    "https://www.gutenberg.org/cache/epub/41/pg41-images-3.epub",
    "https://standardebooks.org/ebooks/p-t-barnum/the-art-of-money-getting/downloads/"
    "p-t-barnum_the-art-of-money-getting_advanced.epub",
]

print("| File | Original | txt   | txtz  | Crushed | Ratio |")
print("| ---- | -------- | ----- | ----- | ------- | ----- |")

for i, url in enumerate(urls):
    filename, headers = urllib.request.urlretrieve(url)
    original_size = os.stat(filename).st_size // 1000

    filename_txt = filename + ".txt"
    subprocess.run(
        ["pandoc", "--read", "epub", filename, "--write", "plain", "-o", filename_txt]
    )
    txt_size = os.stat(filename_txt).st_size // 1000

    filename_txtz = filename + ".txtz"
    subprocess.run(["advzip", "--quiet", "--add", filename_txtz, filename_txt])
    txtz_size = os.stat(filename_txtz).st_size // 1000

    epubcrush.crush_epub(filename)
    new_size = os.stat(filename).st_size // 1000

    print(
        f"| {i+1:4} | {original_size:6}kB | {txt_size:3}kB | {txtz_size:3}kB "
        f"| {new_size:5}kB | {(new_size/original_size):5.1%} |"
    )
