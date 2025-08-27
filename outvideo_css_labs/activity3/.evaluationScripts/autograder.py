import sys
import re
import json
import os
import base64
import hashlib
from collections import defaultdict

EVALUATE_FILE = "/home/.evaluationScripts/evaluate.json"

def b64(s: str) -> str:
    return base64.b64encode(s.encode()).decode()

def db64(s: str) -> str:
    return base64.b64decode(s.encode()).decode()

def h(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

def normalize_val(v: str) -> str:
    return re.sub(r'\s+', ' ', v.strip().lower().replace('!important', '')).strip()

def parse_css_blocks(text: str):
    text_nocomments = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    pattern = re.compile(r'([^{]+)\{([^}]*)\}', re.S)
    blocks = defaultdict(dict)
    for m in pattern.finditer(text_nocomments):
        selectors = [s.strip() for s in m.group(1).strip().split(',') if s.strip()]
        props = {}
        for part in m.group(2).strip().split(';'):
            if ':' in part:
                k, v = part.split(':', 1)
                props[k.strip().lower()] = normalize_val(v)
        for sel in selectors:
            blocks[sel].update(props)
    return blocks

EXPECTED = {
    "align_content_start": h(db64("c3RhcnQ=")),
    "align_content_space_around": h(db64("c3BhY2UtYXJvdW5k")),
    "align_items_start": h(db64("c3RhcnQ=")),
    "align_items_end": h(db64("ZW5k")),
    "justify_content_end": h(db64("ZW5k")),
    "justify_content_space_evenly": h(db64("c3BhY2UtZXZlbmx5")),
    "justify_items_center": h(db64("Y2VudGVy")),
    "justify_items_end": h(db64("ZW5k")),
}

def match_hash(value: str, expected_hash: str) -> bool:
    return h(value) == expected_hash

def check_property(props: dict, propname: str, expected_hash: str):
    v = props.get(propname)
    if not v:
        return False, ""
    ok = match_hash(v, expected_hash)
    return ok, ""

TESTS = [
    {"id": 1, "sel": ".align-content-start", "prop": "align-content", "expected": EXPECTED["align_content_start"]},
    {"id": 2, "sel": ".align-content-space-around", "prop": "align-content", "expected": EXPECTED["align_content_space_around"]},
    {"id": 3, "sel": ".align-items-start", "prop": "align-items", "expected": EXPECTED["align_items_start"]},
    {"id": 4, "sel": ".align-items-end", "prop": "align-items", "expected": EXPECTED["align_items_end"]},
    {"id": 5, "sel": ".justify-content-end", "prop": "justify-content", "expected": EXPECTED["justify_content_end"]},
    {"id": 6, "sel": ".justify-content-space-evenly", "prop": "justify-content", "expected": EXPECTED["justify_content_space_evenly"]},
    {"id": 7, "sel": ".justify-items-center", "prop": "justify-items", "expected": EXPECTED["justify_items_center"]},
    {"id": 8, "sel": ".justify-items-end", "prop": "justify-items", "expected": EXPECTED["justify_items_end"]},
]

def evaluate(css_path: str):
    results = [{"testid": t["id"], "status": "fail", "score": 0, "maximum marks": 1, "message": "Test failed"} for t in TESTS]
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_text = f.read()
    except Exception:
        for r in results:
            r['message'] = "unable to open CSS file"
        return _write_eval(results)
    blocks = parse_css_blocks(css_text)
    for t in TESTS:
        sel = t["sel"]
        props = blocks.get(sel, {})
        if not props:
            results[t["id"] - 1]["message"] = "Test failed"
            continue
        ok, _ = check_property(props, t["prop"], t["expected"])
        if ok:
            results[t["id"] - 1].update({"status": "success", "score": 1, "message": "Test passed"})
        else:
            results[t["id"] - 1]["message"] = "Test failed"
    _write_eval(results)

def _write_eval(results):
    os.makedirs(os.path.dirname(EVALUATE_FILE), exist_ok=True)
    with open(EVALUATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"data": results}, f, indent=4)

if __name__ == "__main__":
    css_path = sys.argv[1] if len(sys.argv) > 1 else "/home/labDirectory/css/styles.css"
    evaluate(css_path)
