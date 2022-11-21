from zipfile import ZipFile, ZIP_DEFLATED
from subprocess import run
import re
from xml.etree import ElementTree
import argparse
import os


def crush_epub(filename: str) -> None:
    file_allow = "(mimetype|.*ncx|.*opf|.*xml|.*xhtml|.*html|.*htm)$"

    backup_filename = f"{filename}.bak.epub"
    os.rename(filename, backup_filename)

    with ZipFile(filename, "w", compression=ZIP_DEFLATED, compresslevel=9) as newepub:
        with ZipFile(backup_filename) as epub:
            for file in epub.namelist():
                if re.match(file_allow, file):
                    if file.endswith("html") or file.endswith("htm"):
                        xml = epub.open(file).read().decode("utf8")

                        xml = clean_xml(xml)

                        newepub.writestr(file, xml)
                    else:
                        newepub.writestr(file, epub.read(file))


def clean_xml(xml: str) -> str:
    """Cleans unwanted XML tags

    >>> clean_xml('<html></html>')
    '<html xmlns="http://www.w3.org/1999/xhtml"></html>'

    >>> clean_xml('<html><link></link></html>')
    '<html xmlns="http://www.w3.org/1999/xhtml"></html>'

    >>> clean_xml('<html><style></style></html>')
    '<html xmlns="http://www.w3.org/1999/xhtml"></html>'

    >>> clean_xml('<html><script></script></html>')
    '<html xmlns="http://www.w3.org/1999/xhtml"></html>'

    >>> clean_xml('<html><svg></svg></html>')
    '<html xmlns="http://www.w3.org/1999/xhtml"></html>'

    >>> clean_xml('<html><p class="a">test</p></html>')
    '<html xmlns="http://www.w3.org/1999/xhtml"><p>test</p></html>'

    >>> clean_xml('<html><img src="" alt="test"/></html>')
    '<html xmlns="http://www.w3.org/1999/xhtml"><p>test</p></html>'
    """

    exclude_tags = [
        "link",
        "script",
        "style",
        "picture",
        "audio",
        "video",
        "svg",
        "{http://www.w3.org/2000/svg}svg",
        "meta",
    ]

    exclude_attrs = [
        "class",
        "style",
        "{http://www.idpf.org/2007/ops}type",
    ]

    # Remove the default namespace definition
    xml = re.sub(r'\sxmlns="[^"]+"', "", xml, count=1)
    xml = ElementTree.canonicalize(
        xml,
        exclude_tags=exclude_tags,
        exclude_attrs=exclude_attrs,
    )
    # Ensure correct namespace definition
    xml = re.sub(r"<html", '<html xmlns="http://www.w3.org/1999/xhtml"', xml)
    # Replace images with their alt text
    xml = re.sub(r'<img.* alt="(.*?)".*></img>', r"<p>\g<1></p>", xml)

    return xml


def repack(filename: str) -> None:
    run(["advzip", "-z", "-4", filename])


def main() -> None:
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
