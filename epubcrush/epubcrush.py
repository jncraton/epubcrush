from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
from subprocess import run
import re
from xml.etree import ElementTree
import argparse
import os


def modernize_childrens(text):
    """
    >>> modernize_childrens("You are queer.")
    'You are strange.'
    >>> modernize_childrens("I am a queer boy.")
    'I am a strange boy.'
    >>> modernize_childrens("She was feeling gay.")
    'She was feeling happy.'
    >>> modernize_childrens("Gay children played.")
    'Happy children played.'
    >>> modernize_childrens("Children played, gaily!")
    'Children played, happily!'
    >>> modernize_childrens("Queerer things have happened.")
    'Stranger things have happened.'
    >>> modernize_childrens("We could do with a bit more queerness.")
    'We could do with a bit more strangeness.'
    """

    word_updates = [
        ("queer", "strange"),
        ("queerer", "stranger"),
        ("queerest", "strangest"),
        ("queerness", "strangeness"),
        ("gaily", "happily"),
        ("gay", "happy"),
        ("midget", "little person"),
        ("policeman", "police officer"),
        ("policemen", "police officers"),
        ("mailman", "mail carrier"),
        ("mailmen", "mail carriers"),
        ("fireman", "fire fighter"),
        ("firemen", "fire fighters"),
    ]

    tokens = []

    def modernize_token(token):
        for orig, new in word_updates:
            if token == orig:
                token = new
            elif token == orig.title():
                token = new.title()
            elif token == orig.upper():
                token = new.upper()

        return token

    tokens = [modernize_token(t) for t in re.findall(r"([\w]+|[^\w]+)", text)]

    return "".join(tokens)


def crush_epub(
    filename: str, images=False, quality=100, styles=False, fonts=False, modernize=False
) -> None:
    allowed_files = [
        "mimetype",
        "ncx",
        "opf",
        "xml",
        "xhtml",
        "html",
        "htm",
    ]

    if images:
        allowed_files += ["jpg", "png", "webp", "jpeg", "svg"]

    if styles:
        allowed_files += ["css"]

    if fonts:
        allowed_files += ["ttf", "woff", "otf"]

    file_allow = f"(.*{'|.*'.join(allowed_files)})$"

    backup_filename = f"{filename}.bak.epub"
    os.rename(filename, backup_filename)

    with ZipFile(filename, "w", compression=ZIP_DEFLATED, compresslevel=9) as newepub:
        with ZipFile(backup_filename) as epub:
            for file in epub.namelist():
                if re.match(file_allow, file, flags=re.I):
                    if file.endswith("html") or file.endswith("htm"):
                        xml = epub.open(file).read().decode("utf8")

                        xml = clean_xml(xml, images, styles)

                        if modernize:
                            xml = modernize_childrens(xml)

                        newepub.writestr(file, xml)
                    elif file.endswith("opf"):
                        xml = epub.open(file).read().decode("utf8")

                        xml = ElementTree.canonicalize(xml)

                        xml = re.sub(
                            f"<(opf:)?item.*href="
                            f"\"[^\"]*(?<!{')(?<!'.join(allowed_files)})\".*>"
                            f"</(opf:)?item>",
                            "",
                            xml,
                            flags=re.I,
                        )

                        if not images:
                            xml = re.sub('properties="svg"', "", xml)

                        newepub.writestr(file, xml)

                    elif quality < 100 and re.match(r".*(jpeg|jpg)", file, flags=re.I):
                        jpeg = epub.extract(file, "/tmp")
                        compressed_jpeg = f"{jpeg}.comp.jpeg"
                        try:
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
                        except FileNotFoundError:
                            run(
                                [
                                    "cjpeg",
                                    "-quality",
                                    str(quality),
                                    "-progressive",
                                    "-outfile",
                                    compressed_jpeg,
                                    jpeg,
                                ]
                            )
                        newepub.write(compressed_jpeg, file)
                    elif quality < 100 and re.match(r".*png", file, flags=re.I):
                        png = epub.extract(file, "/tmp")
                        run(
                            [
                                "pngquant",
                                "--quality",
                                f"0-{quality}",
                                "--force",
                                "--ordered",
                                "--speed",
                                "1",
                                "--ext",
                                ".png",
                                png,
                            ]
                        )
                        newepub.write(png, file)
                    elif file == "mimetype":
                        newepub.writestr(
                            file, epub.read(file), compress_type=ZIP_STORED
                        )
                    else:
                        newepub.writestr(file, epub.read(file))


def clean_xml(xml: str, images=False, styles=False) -> str:
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
    '<html xmlns="http://www.w3.org/1999/xhtml"></html>'

    >>> clean_xml('<html><img src="" alt="Image"/></html>')
    '<html xmlns="http://www.w3.org/1999/xhtml"></html>'

    >>> clean_xml('<html><img src="" alt=""/></html>')
    '<html xmlns="http://www.w3.org/1999/xhtml"></html>'

    >>> clean_xml('<html><img src=""/></html>')
    '<html xmlns="http://www.w3.org/1999/xhtml"></html>'
    """

    exclude_tags = [
        "script",
        "audio",
        "video",
        "meta",
    ]

    if not images:
        exclude_tags += ["picture", "svg", "{http://www.w3.org/2000/svg}svg"]

    exclude_attrs = []

    if not styles:
        exclude_tags += ["style", "link"]
        exclude_attrs += ["style", "class"]

    # Remove the default namespace definition
    xml = re.sub(r'\sxmlns="[^"]+"', "", xml, count=1)
    xml = xml.replace("&nbsp;", " ")
    xml = ElementTree.canonicalize(
        xml,
        exclude_tags=exclude_tags,
        exclude_attrs=exclude_attrs,
    )
    # Ensure correct namespace definition
    xml = re.sub(r"<html", '<html xmlns="http://www.w3.org/1999/xhtml"', xml)

    if not images:
        xml = re.sub(r"<img.*>.*?</img>", "", xml)

    return xml


def repack(filename: str) -> None:
    run(["advzip", "-z", "-4", filename])


def main() -> None:
    ap = argparse.ArgumentParser(description="Compress EPUB Files")
    ap.add_argument("files", nargs="+", help="List of EPUB files")
    ap.add_argument(
        "--fast",
        action="store_true",
        help="Run faster. Do not recompress using advcomp",
    )
    ap.add_argument(
        "--modernize",
        action="store_true",
        help="Attempt to modernize language of older children's literature",
    )
    ap.add_argument(
        "--images",
        "-i",
        action="store_true",
        help="Keep images in output",
    )
    ap.add_argument(
        "--styles",
        "-s",
        action="store_true",
        help="Keep styles in output",
    )
    ap.add_argument(
        "--fonts",
        "-f",
        action="store_true",
        help="Keep fonts in output",
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
        crush_epub(
            filename,
            images=args.images,
            styles=args.styles,
            quality=args.quality,
            fonts=args.fonts,
            modernize=args.modernize,
        )
        if not args.fast:
            repack(filename)


if __name__ == "__main__":
    main()
