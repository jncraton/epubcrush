from zipfile import ZipFile, ZIP_DEFLATED
from subprocess import run
import re
from xml.etree import ElementTree
import argparse
import os


def crush_epub(filename: str, keep_images=False, quality=100) -> None:
    allowed_files = [
        "mimetype",
        ".*ncx",
        ".*opf",
        ".*xml",
        ".*xhtml",
        ".*html",
        ".*htm",
    ]

    if keep_images:
        allowed_files += [".*jpg", ".*png", ".*webp"]

    file_allow = f"({'|'.join(allowed_files)})$"

    backup_filename = f"{filename}.bak.epub"
    os.rename(filename, backup_filename)

    with ZipFile(filename, "w", compression=ZIP_DEFLATED, compresslevel=9) as newepub:
        with ZipFile(backup_filename) as epub:
            for file in epub.namelist():
                if re.match(file_allow, file, flags=re.I):
                    if file.endswith("html") or file.endswith("htm"):
                        xml = epub.open(file).read().decode("utf8")

                        xml = clean_xml(xml, keep_images)

                        newepub.writestr(file, xml)
                    elif quality < 100 and re.match(r".*(jpeg|jpg)", file, flags=re.I):
                        jpeg = epub.extract(file, "/tmp")
                        compressed_jpeg = f"{jpeg}.comp.jpeg"
                        run(
                            [
                                "/opt/mozjpeg/bin/cjpeg",
                                "-quality",
                                str(quality),
                                "-progressive",
                                "-quant-table",
                                "2",
                                "-outfile",
                                compressed_jpeg,
                                jpeg,
                            ]
                        )
                        newepub.write(compressed_jpeg, file)
                    else:
                        newepub.writestr(file, epub.read(file))


def clean_xml(xml: str, keep_images=False) -> str:
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

    >>> clean_xml('<html><img src=""/></html>')
    '<html xmlns="http://www.w3.org/1999/xhtml"></html>'
    """

    exclude_tags = [
        "link",
        "script",
        "style",
        "audio",
        "video",
        "meta",
    ]

    if not keep_images:
        exclude_tags += ["picture", "svg", "{http://www.w3.org/2000/svg}svg"]

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

    if not keep_images:
        # Replace images with their alt text
        xml = re.sub(r'<img.* alt="(.*?)".*></img>', r"<p>\g<1></p>", xml)
        xml = re.sub(r"<img.*>.*?</img>", "", xml)

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
    ap.add_argument(
        "--images",
        "-i",
        action="store_true",
        help="Keep images in output",
    )
    ap.add_argument(
        "--quality",
        "-q",
        type=int,
        default=100,
        help="Quality to use for images. 0-100 scale similar to JPEG.",
    )

    args = ap.parse_args()

    for filename in args.files:
        crush_epub(filename, keep_images=args.images, quality=args.quality)
        if args.advcomp:
            repack(filename)


if __name__ == "__main__":
    main()
