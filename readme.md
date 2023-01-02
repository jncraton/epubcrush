EPUB Crush
==========

[![PyPI version](https://badge.fury.io/py/epubcrush.svg)](https://badge.fury.io/py/epubcrush)
[![Test](https://github.com/jncraton/epubcrush/actions/workflows/build.yml/badge.svg)](https://github.com/jncraton/epubcrush/actions/workflows/build.yml)

Removes media content and compresses [EPUB](https://en.wikipedia.org/wiki/EPUB) files to reduce size.

By default, all images, fonts, scipts, and styles will be removed from the EPUB.

Installation
------------

This package is available via PyPI and can be installed from there.

```sh
pip install epubcrush
```

Performance
-----------

| File | Original |  txt  | txtz  | Images q=100 | Images q=50  |  No Images   |
| ---- | -------- | ----- | ----- | ------------ | ------------ | ------------ |
|    1 |    584kB |  22kB |   9kB |  580kB (99%) |  289kB (49%) |   22kB ( 4%) |
|    2 |    589kB |  88kB |  30kB |  584kB (99%) |  371kB (63%) |   47kB ( 8%) |
|    3 |     87kB |  89kB |  34kB |   75kB (86%) |   75kB (86%) |   39kB (45%) |

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
