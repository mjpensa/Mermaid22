import fitz
import os
import tempfile
import subprocess
from typing import Callable, Optional
from detect import detect_mermaid
from bbox import group_spans_to_blocks, union_bbox
from imaging import svg_to_png

def render_mermaid(code: str, format: str, width: float) -> str:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(code)
        input_file = f.name
    output_file = tempfile.mktemp(suffix='.' + format)
    cmd = ['node', 'renderer/render_mermaid.js', input_file, output_file, str(width), format]
    subprocess.run(cmd, check=True)
    os.unlink(input_file)
    return output_file

def process_pdf(input_path: str, output_path: str, log_callback: Optional[Callable] = None):
    doc = fitz.open(input_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        text_dict = page.get_text('dict')
        spans = []
        for block in text_dict['blocks']:
            if 'lines' in block:
                for line in block['lines']:
                    for span in line['spans']:
                        spans.append(span)
        blocks = group_spans_to_blocks(spans)
        for block_spans in blocks:
            text = ''.join(s['text'] for s in block_spans)
            mermaid_code = detect_mermaid(text)
            if mermaid_code:
                bbox = union_bbox(block_spans)
                if bbox:
                    svg_path = render_mermaid(mermaid_code, 'svg', bbox[2] - bbox[0])
                    png_path = tempfile.mktemp(suffix='.png')
                    svg_to_png(svg_path, png_path, dpi=300)
                    rect = fitz.Rect(bbox)
                    page.insert_image(rect, filename=png_path)
                    os.unlink(svg_path)
                    os.unlink(png_path)
                    if log_callback:
                        log_callback(page_num, text[:120], mermaid_code)
    doc.save(output_path)