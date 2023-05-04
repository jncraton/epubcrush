EPUB Crush
==========

[![PyPI version](https://badge.fury.io/py/epubcrush.svg)](https://badge.fury.io/py/epubcrush)
[![Test](https://github.com/jncraton/epubcrush/actions/workflows/build.yml/badge.svg)](https://github.com/jncraton/epubcrush/actions/workflows/build.yml)

Compresses [EPUB](https://en.wikipedia.org/wiki/EPUB) files to reduce size.

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
|    1 |    589kB |  27kB |  11kB |  571kB (97%) |  243kB (41%) |   13kB ( 2%) |
|    2 |    589kB |  91kB |  31kB |  548kB (93%) |  248kB (42%) |   10kB ( 2%) |
|    3 |     87kB |  89kB |  34kB |   76kB (87%) |   50kB (57%) |   39kB (45%) |

Why?
-----

EPUBs may include features that may not be desirable from a privacy or efficiency standpoint. Publishers may choose to include high-res images, custom fonts, styles, scripts, and other features that bloat the size of EPUBs beyond what is needed for the text content of a book. This application strips away everything but the plain text content.

Why not use plain text?
-----------------------

EPUB adds a number of useful reading features (table of contents, metadata, etc) that are useful and not available in basic plain text. EPUBs are also compressed, so they will often be smaller than simple plain text.

Method of Operation
-------------------

- Iterate files in container
- Remove all files that are not part of the document text or part of the EPUB structure
- Parse XML files
  - Remove the following tags
    - link
    - meta
    - style
    - img
    - picture
    - audio
    - video
    - script
- Parse opf file removing references to files that no longer exist
- Remove print page lists
