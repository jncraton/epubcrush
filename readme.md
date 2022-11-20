EPUB Crush
==========

[![PyPI version](https://badge.fury.io/py/epubcrush.svg)](https://badge.fury.io/py/epubcrush)
[![Test](https://github.com/jncraton/epubcrush/actions/workflows/build.yml/badge.svg)](https://github.com/jncraton/epubcrush/actions/workflows/build.yml)

Removes media content and compresses [EPUB](https://en.wikipedia.org/wiki/EPUB) files to reduce size.

By default, all images, fonts, scipts, and styles will be removed from the EPUB.

Performance
-----------

| File | Original | txt | txtz | Crushed | Ratio |
| ---- | -------- | --- | ---- | ------- | ----- |
|    1 |  584.504 |  22 |    9 |  22.305 |  3.8% |
|    2 |  589.496 |  88 |   30 |  46.625 |  7.9% |
|    3 |   87.098 |  89 |   34 |   39.31 | 45.1% |
|    4 |  589.702 |  80 |   30 |  40.422 |  6.9% |

Why?
-----

EPUB is a fine format, but it includes many features that may not be desirable from a privacy or efficiency standpoint. This includes full JavaScript support (did you know that you can use WebGL inside an eBook?). Publishers often choose to include high-res images, custom fonts, styles, and other features that bloat the size of EPUBs beyond what is needed for the text content of a book. This application strips away everything but the plain text content.

Why not just plain text?
------------------------

EPUB adds a number of useful reading features (table of contents, metadata, etc) that are useful and not available in basic plain text.

Method of Operation
-------------------

- Iterate files in container
- Remove all files that are not part of the document text or part of the EPUB structure
- Parse XML files
  - Remove the following tags
    - link
    - meta
    - style
    - picture
    - audio
    - video
    - script
  - Replace `img` tags with their alt text in a `p` tag
