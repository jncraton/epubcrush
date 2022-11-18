from zipfile import ZipFile, ZIP_DEFLATED
from subprocess import run
import re
from xml.etree import ElementTree, ElementInclude
import argparse
import os


def crush_epub(filename: str):
    file_allow = "mimetype|.*.xhtml|.*.xml|.*.ncx|.*xhtml|.*html|.*htm|.*.opf"

    exclude_tags = [
        "link",
        "script",
        "style",
        "picture",
        "audio",
        "video",
        "meta",
    ]

    exclude_attrs = [
        "class",
        "id",
        "style",
        "src",
        "height",
        "width",
    ]

    backup_filename = f"{filename}.bak.epub"
    os.rename(filename, backup_filename)

    with ZipFile(filename, "w", compression=ZIP_DEFLATED, compresslevel=9) as newepub:
        with ZipFile(backup_filename) as epub:
            for file in epub.namelist():
                if re.match(file_allow, file):
                    if file.endswith("html") or file.endswith("htm"):
                        xml = epub.open(file).read().decode("utf8")

                        # Remove the default namespace definition
                        xml = re.sub(r"<html.*>", "<html>", xml, count=1)
                        xml = ElementTree.canonicalize(
                            xml,
                            strip_text=True,
                            exclude_tags=exclude_tags,
                            exclude_attrs=exclude_attrs,
                        )
                        # Ensure correct namespace definition
                        xml = re.sub(
                            r"<html", '<html xmlns="http://www.w3.org/1999/xhtml"', xml
                        )
                        # Replace images with their alt text
                        xml = re.sub(r'<img alt="(.*)"></img>', "<p>\g<1></p>", xml)
                        newepub.writestr(file, xml)
                    else:
                        newepub.writestr(file, epub.read(file))


def repack(filename):
    run(["advzip", "-z", "-4", filename])


def main():
    ap = argparse.ArgumentParser(description="Compress EPUB Files")
    ap.add_argument("files", nargs="+", help="List of EPUB files")
    ap.add_argument(
        "--advcomp",
        "-z",
        action="store_true",
        help="Recompress using advcomp",
    )

    args = ap.parse_args()

    for filename in args.files:
        crush_epub(filename)
        if args.advcomp:
            repack(filename)


if __name__ == "__main__":
    main()
