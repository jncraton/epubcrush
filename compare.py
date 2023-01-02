import urllib.request
import os
import subprocess

urls = [
    "https://standardebooks.org/ebooks/james-joyce/poetry/downloads/"
    "james-joyce_poetry.epub",
    "https://standardebooks.org/ebooks/"
    "karl-marx_friedrich-engels/the-communist-manifesto/samuel-moore/downloads/"
    "karl-marx_friedrich-engels_the-communist-manifesto_samuel-moore.epub",
    "https://www.gutenberg.org/cache/epub/41/pg41-images-3.epub",
]

print(
    "| File | Original |  txt  | txtz  | Images q=100 | Images q=50  |  No Images   |"
)
print(
    "| ---- | -------- | ----- | ----- | ------------ | ------------ | ------------ |"
)


def check(epub):
    status = subprocess.run(
        [
            "java",
            "-jar",
            "epubcheck-4.2.6/epubcheck.jar",
            "--quiet",
            epub,
        ]
    )
    assert status.returncode == 0


for i, url in enumerate(urls):
    filename, headers = urllib.request.urlretrieve(url, filename="/tmp/epubcrush.epub")
    original_size = os.stat(filename).st_size // 1000

    filename_txt = filename + ".txt"
    subprocess.run(
        ["pandoc", "--read", "epub", filename, "--write", "plain", "-o", filename_txt]
    )
    txt_size = os.stat(filename_txt).st_size // 1000

    filename_txtz = filename + ".txtz"
    subprocess.run(["advzip", "--quiet", "--add", filename_txtz, filename_txt])
    txtz_size = os.stat(filename_txtz).st_size // 1000

    check(filename)
    subprocess.run(
        ["python3", "epubcrush/epubcrush.py", "--images", "--quality=100", filename]
    )
    images_100_size = os.stat(filename).st_size // 1000
    check(filename)

    subprocess.run(
        ["python3", "epubcrush/epubcrush.py", "--images", "--quality=50", filename]
    )
    images_50_size = os.stat(filename).st_size // 1000

    subprocess.run(["python3", "epubcrush/epubcrush.py", filename])
    check(filename)
    new_size = os.stat(filename).st_size // 1000

    print(
        f"| {i+1:4} | {original_size:6}kB | {txt_size:3}kB | {txtz_size:3}kB "
        f"| {images_100_size:4}kB ({(images_100_size/original_size):3.0%}) "
        f"| {images_50_size:4}kB ({(images_50_size/original_size):3.0%}) "
        f"| {new_size:4}kB ({(new_size/original_size):3.0%}) |"
    )
