from zipfile import ZipFile, ZIP_DEFLATED
import re

file_allow = 'mimetype|.*.xhtml|.*.xml|.*toc.ncx|.*xhtml|.*html|.*content.opf'

with ZipFile('out.epub', 'w', compression=ZIP_DEFLATED, compresslevel=9) as newepub:
    with ZipFile('t.epub') as epub:
        for file in epub.namelist():
            if re.match(file_allow, file):
                newepub.writestr(file, epub.read(file))
