import re
from typing import Optional

FENCE_PATTERNS = [
    re.compile(r'(?is)^\s*```+\s*mermaid\b.*?$([\s\S]*?)^\s*```+\s*$'),
    re.compile(r'(?is)^\s*```+\s*$([\s\S]*?)^\s*```+\s*$'),
]

WRAPPER_PATTERNS = [
    re.compile(r'(?is)<mermaid\b[^>]*>([\s\S]*?)</mermaid>'),
    re.compile(r'(?is)\[mermaid\]([\s\S]*?)\[/mermaid\]'),
    re.compile(r'(?is)\\begin\{mermaid\}([\s\S]*?)\\end\{mermaid\}'),
]

FENCE_VARIANTS = [
    re.compile(r'(?is)^\s*\'\'\'+\s*mermaid\b.*?$([\s\S]*?)^\s*\'\'\'+\s*$'),
    re.compile(r'(?is)^\s*\'\'\'+\s*$([\s\S]*?)^\s*\'\'\'+\s*$'),
    re.compile(r'(?is)^\s*~~~+\s*mermaid\b.*?$([\s\S]*?)^\s*~~~+\s*$'),
    re.compile(r'(?is)^\s*~~~+\s*$([\s\S]*?)^\s*~~~+\s*$'),
]

SEED_PATTERN = re.compile(r'(?i)\b(graph\s+(TD|LR|RL|BT)|flowchart|sequenceDiagram|classDiagram|erDiagram|stateDiagram|journey|gantt|pie|gitGraph)\b')

STOP_WORDS = re.compile(r'(?i)\b(email|url|http|www|com|org|net)\b')

def detect_mermaid(text: str) -> Optional[str]:
    # Try fence patterns
    for pattern in FENCE_PATTERNS + FENCE_VARIANTS:
        matches = pattern.findall(text)
        if matches:
            for match in matches:
                normalized = normalize_code(match)
                if validate_mermaid(normalized):
                    return normalized
    # Try wrapper
    for pattern in WRAPPER_PATTERNS:
        matches = pattern.findall(text)
        if matches:
            for match in matches:
                normalized = normalize_code(match)
                if validate_mermaid(normalized):
                    return normalized
    # Fence-less
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if SEED_PATTERN.search(line):
            block_lines = []
            for j in range(i, len(lines)):
                l = lines[j]
                if not l.strip():
                    break
                if STOP_WORDS.search(l):
                    break
                block_lines.append(l)
            if block_lines:
                code = '\n'.join(block_lines)
                normalized = normalize_code(code)
                if validate_mermaid(normalized):
                    return normalized
    return None

def normalize_code(code: str) -> str:
    # remove bullets
    code = re.sub(r'^\s*([•\-\*\d]+\.)\s+', '', code, flags=re.MULTILINE)
    # dehyphenate
    code = re.sub(r'(\w)-\n(\w)', r'\1\2', code)
    # normalize whitespace
    code = re.sub(r'[ \t]+', ' ', code)
    code = re.sub(r'\n+', '\n', code)
    # normalize quotes
    code = code.replace(''', "'").replace(''', "'").replace('"', '"').replace('"', '"')
    # dashes
    code = code.replace('–', '-').replace('—', '-')
    # trim
    code = '\n'.join(line.rstrip() for line in code.split('\n'))
    return code.strip()

def validate_mermaid(code: str) -> bool:
    return bool(SEED_PATTERN.search(code))