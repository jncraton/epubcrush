EPUB Repacker
=============

Repacks [EPUB](https://en.wikipedia.org/wiki/EPUB) files to reduce size.

By default, all images, fonts, scipts, and styles will be removed from the EPUB.

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
