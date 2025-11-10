from typing import List, Dict, Tuple, Optional

def group_spans_to_blocks(spans: List[Dict], tolerance: float = 3.0) -> List[List[Dict]]:
    spans = sorted(spans, key=lambda s: s['bbox'][1])
    blocks = []
    current_block = []
    for span in spans:
        if not current_block:
            current_block.append(span)
        else:
            last = current_block[-1]
            if abs(span['bbox'][1] - last['bbox'][3]) <= tolerance and abs(span['bbox'][0] - last['bbox'][0]) <= tolerance:
                current_block.append(span)
            else:
                blocks.append(current_block)
                current_block = [span]
    if current_block:
        blocks.append(current_block)
    return blocks

def union_bbox(spans: List[Dict]) -> Optional[Tuple[float, float, float, float]]:
    if not spans:
        return None
    x0 = min(s['bbox'][0] for s in spans)
    y0 = min(s['bbox'][1] for s in spans)
    x1 = max(s['bbox'][2] for s in spans)
    y1 = max(s['bbox'][3] for s in spans)
    return (x0, y0, x1, y1)