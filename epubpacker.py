from zipfile import ZipFile, ZIP_DEFLATED
import re
from xml.etree import ElementTree, ElementInclude

file_allow = 'mimetype|.*.xhtml|.*.xml|.*toc.ncx|.*xhtml|.*html|.*content.opf'

exclude_tags = [
    'link',
    'script',
    'style',
    'img',
    'picture',
    'audio',
    'video',
    'meta',
]

exclude_attrs = [
    'class',
    'id',
    'style',
]

with ZipFile('out.epub', 'w', compression=ZIP_DEFLATED, compresslevel=9) as newepub:
    with ZipFile('t.epub') as epub:
        for file in epub.namelist():
            if re.match(file_allow, file):
                if file.endswith('html'):
                    xml = epub.open(file).read().decode('utf8')

                    # Remove the default namespace definition
                    xml = re.sub(r'\sxmlns="[^"]+"', '', xml, count=1)
                    xml = ElementTree.canonicalize(xml, strip_text=True, exclude_tags=exclude_tags, exclude_attrs = exclude_attrs)
                    # Ensure correct namespace definition
                    xml = re.sub(r'<html', '<html xmlns="http://www.w3.org/1999/xhtml"', xml)
                    newepub.writestr(file, xml)
                else:
                    newepub.writestr(file, epub.read(file))
