# Design Note

## PDF Bbox Strategy

To detect Mermaid blocks in PDF, we extract text with bounding boxes using PyMuPDF's page.get_text('dict').

Spans are grouped into blocks by vertical proximity (y-difference <=3pt) and left-edge alignment (x-difference <=3pt).

For each block, detect Mermaid code using heuristics.

Compute union bbox of the spans in the block.

Redact the area with white rectangle.

Render the diagram to SVG at the bbox width, then rasterize to PNG.

Insert the PNG image at the bbox position, scaled to fit width, preserve aspect.

## Normalization Pipeline

1. Remove bullets/line numbers: regex ^\s*([•\-\*\d]+\.)\s+

2. Dehyphenate: (\w)-\n(\w) -> \1\2

3. Normalize whitespace: collapse spaces/tabs, unify newlines

4. Convert smart quotes/dashes to ASCII

5. Trim trailing spaces

6. Validate with seed pattern

If invalid, attempt repairs: common typos like gragh->graph