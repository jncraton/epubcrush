Method of Operation
-------------------

- Iterate files in container
- Remove all image files
- Remove all styles
- Parse XML files
  - Remove the following tags
    - script
    - style
    - img
    - video
    - audio
  - Remove all tag attributes in HTML body
