import pytest
from detect import detect_mermaid, normalize_code

def test_detect_fenced():
    text = '''```mermaid
graph TD
A-->B
```'''
    result = detect_mermaid(text)
    assert result is not None
    assert 'graph TD' in result

def test_normalize():
    code = '• A-->B'
    normalized = normalize_code(code)
    assert normalized == 'A-->B'

# more tests