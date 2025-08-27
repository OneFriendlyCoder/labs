#!/usr/bin/env python3
import sys
import re
import json
import os
import hashlib
from collections import defaultdict

EVALUATE_FILE = "/home/.evaluationScripts/evaluate.json"

def h(s):
    return hashlib.sha256(s.encode()).hexdigest()

def normalize_val(v):
    if v is None:
        return ''
    return re.sub(r'\s+', ' ', v.strip().lower().replace('!important', '')).strip()

def norm_for_hash(v):
    if v is None:
        return ''
    s = normalize_val(v)
    s = re.sub(r'(^|\s)\.([0-9]+)', lambda m: (m.group(1) or '') + '0.' + m.group(2), s)
    s = re.sub(r'(\d)\s+([a-z%]+)', r'\1\2', s)
    s = re.sub(r'(\d)\s+\.(\d)', r'\1.\2', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def remove_at_rules(text):
    i = 0
    n = len(text)
    out = []
    while i < n:
        if text[i] == '@':
            brace_pos = text.find('{', i)
            if brace_pos == -1:
                out.append(text[i:])
                break
            depth = 1
            k = brace_pos + 1
            while k < n and depth > 0:
                if text[k] == '{':
                    depth += 1
                elif text[k] == '}':
                    depth -= 1
                k += 1
            i = k
        else:
            out.append(text[i])
            i += 1
    return ''.join(out)

def parse_css_blocks(text):
    text_no_at = remove_at_rules(text)
    text_nocomments = re.sub(r'/\*.*?\*/', '', text_no_at, flags=re.S)
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
    "s1_min_height": h(norm_for_hash("260px")),
    "s1_padding": [h(norm_for_hash(".9rem")), h(norm_for_hash("0.9rem")), h(norm_for_hash(".90rem")), h(norm_for_hash("0.90rem"))],
    "s2_min_height": h(norm_for_hash("360px")),
    "s2_padding": [h(norm_for_hash(".9rem")), h(norm_for_hash("0.9rem")), h(norm_for_hash(".90rem")), h(norm_for_hash("0.90rem"))],
    "s3_min_height": h(norm_for_hash("180px")),
    "s3_padding": [h(norm_for_hash(".8rem")), h(norm_for_hash("0.8rem")), h(norm_for_hash(".80rem")), h(norm_for_hash("0.80rem"))],
}

def match_hash(value, expected_hash):
    if value is None:
        return False
    return h(norm_for_hash(value)) == expected_hash

def match_any_hash(value, expected_hashes):
    if value is None:
        return False
    valhash = h(norm_for_hash(value))
    return any(valhash == exp for exp in expected_hashes)

def prop_exists_and_not_placeholder(props, key):
    v = props.get(key)
    if not v:
        return False, f"{key} not found"
    if v in ("''", '""', ''):
        return False, f"{key} empty or placeholder ({v})"
    return True, f"{key} = {v}"

def check_flex_three_value(props, key, grow_min=None, shrink_min=None, basis_expected=None):
    v = props.get(key)
    if not v:
        return False, f"{key} not found"
    s = normalize_val(v)
    s = norm_for_hash(s)
    parts = s.split()
    if len(parts) < 3:
        return False, f"{key} = {v} (expected three-part flex like '1 1 140px')"
    try:
        g = int(parts[0])
        s_val = int(parts[1])
    except:
        return False, f"{key} = {v} (grow/shrink not integer)"
    basis = parts[2]
    if grow_min is not None and g < grow_min:
        return False, f"{key} grow {g} < {grow_min}"
    if shrink_min is not None and s_val < shrink_min:
        return False, f"{key} shrink {s_val} < {shrink_min}"
    if basis_expected and norm_for_hash(basis) != norm_for_hash(basis_expected):
        return False, f"{key} basis {basis} != {norm_for_hash(basis_expected)}"
    return True, f"{key} = {v}"

def check_flex_exact_hash(props, key, expected_hash):
    v = props.get(key)
    if not v:
        return False, f"{key} not found"
    return (match_hash(v, expected_hash), f"{key} = {v}")

TESTS = [
    {"id":1, "sel": ".s1 .flexbox", "check": lambda p: ("row" in p.get('flex-direction',''), f"flex-direction = {p.get('flex-direction')}") if p.get('flex-direction') else (False, "flex-direction not found")},
    {"id":2, "sel": ".s1 .flexbox", "check": lambda p: ("wrap" in p.get('flex-wrap',''), f"flex-wrap = {p.get('flex-wrap')}") if p.get('flex-wrap') else (False, "flex-wrap not found")},
    {"id":3, "sel": ".s1 .flexbox", "check": lambda p: ("row" in p.get('flex-flow','') and "wrap" in p.get('flex-flow',''), f"flex-flow = {p.get('flex-flow')}") if p.get('flex-flow') else (False, "flex-flow not found")},
    {"id":4, "sel": ".s1 .flexbox", "check": lambda p: ("space-around" in p.get('justify-content',''), f"justify-content = {p.get('justify-content')}") if p.get('justify-content') else (False, "justify-content not found")},
    {"id":5, "sel": ".s1 .flexbox", "check": lambda p: ("center" in p.get('align-items',''), f"align-items = {p.get('align-items')}") if p.get('align-items') else (False, "align-items not found")},
    {"id":6, "sel": ".s1 .flexbox", "check": lambda p: ("space-between" in p.get('align-content',''), f"align-content = {p.get('align-content')}") if p.get('align-content') else (False, "align-content not found")},
    {"id":7, "sel": ".s1 .flexbox", "check": lambda p: prop_exists_and_not_placeholder(p, 'background')},
    {"id":8, "sel": ".s1 .flexbox", "check": lambda p: prop_exists_and_not_placeholder(p, 'border-color')},
    {"id":9, "sel": ".s1 .flexbox", "check": lambda p: (match_hash(p.get('min-height',''), EXPECTED['s1_min_height']), f"min-height = {p.get('min-height')}") if p.get('min-height') else (False, "min-height not found")},
    {"id":10, "sel": ".s1 .flexbox", "check": lambda p: (match_any_hash(p.get('padding',''), EXPECTED['s1_padding']), f"padding = {p.get('padding')}") if p.get('padding') else (False, "padding not found")},
    {"id":11, "sel": ".s1 .flexbox", "check": lambda p: (('content' not in p) or (p.get('content') not in ("''", '""', '')), "content placeholder removed" if (('content' not in p) or (p.get('content') not in ("''", '""', ''))) else "content placeholder present")},
    {"id":12, "sel": ".s1 .box:nth-child(odd)", "check": lambda p: check_flex_three_value(p, 'flex', grow_min=1, shrink_min=1, basis_expected='140px')},
    {"id":13, "sel": ".s1 .box:nth-child(even)", "check": lambda p: check_flex_exact_hash(p, 'flex', h(norm_for_hash('0 0 100px')) )},
    {"id":14, "sel": ".s2 .flexbox", "check": lambda p: ("column" in p.get('flex-direction',''), f"flex-direction = {p.get('flex-direction')}") if p.get('flex-direction') else (False, "flex-direction not found")},
    {"id":15, "sel": ".s2 .flexbox", "check": lambda p: ("wrap" in p.get('flex-wrap',''), f"flex-wrap = {p.get('flex-wrap')}") if p.get('flex-wrap') else (False, "flex-wrap not found")},
    {"id":16, "sel": ".s2 .flexbox", "check": lambda p: ("column" in p.get('flex-flow','') and "wrap" in p.get('flex-flow',''), f"flex-flow = {p.get('flex-flow')}") if p.get('flex-flow') else (False, "flex-flow not found")},
    {"id":17, "sel": ".s2 .flexbox", "check": lambda p: ("space-between" in p.get('justify-content',''), f"justify-content = {p.get('justify-content')}") if p.get('justify-content') else (False, "justify-content not found")},
    {"id":18, "sel": ".s2 .flexbox", "check": lambda p: ("flex-start" in p.get('align-items',''), f"align-items = {p.get('align-items')}") if p.get('align-items') else (False, "align-items not found")},
    {"id":19, "sel": ".s2 .flexbox", "check": lambda p: ("stretch" in p.get('align-content',''), f"align-content = {p.get('align-content')}") if p.get('align-content') else (False, "align-content not found")},
    {"id":20, "sel": ".s2 .flexbox", "check": lambda p: prop_exists_and_not_placeholder(p, 'background')},
    {"id":21, "sel": ".s2 .flexbox", "check": lambda p: prop_exists_and_not_placeholder(p, 'border-color')},
    {"id":22, "sel": ".s2 .flexbox", "check": lambda p: (match_hash(p.get('min-height',''), EXPECTED['s2_min_height']), f"min-height = {p.get('min-height')}") if p.get('min-height') else (False, "min-height not found")},
    {"id":23, "sel": ".s2 .flexbox", "check": lambda p: (match_any_hash(p.get('padding',''), EXPECTED['s2_padding']), f"padding = {p.get('padding')}") if p.get('padding') else (False, "padding not found")},
    {"id":24, "sel": ".s2 .flexbox", "check": lambda p: (('content' not in p) or (p.get('content') not in ("''", '""', '')), "content placeholder removed" if (('content' not in p) or (p.get('content') not in ("''", '""', ''))) else "content placeholder present")},
    {"id":25, "sel": ".s2 .box", "check": lambda p: (match_hash(p.get('width',''), h(norm_for_hash('100%')) ), f"width = {p.get('width')}") if p.get('width') else (False, "width not found")},
    {"id":26, "sel": ".s2 .box", "check": lambda p: check_flex_exact_hash(p, 'flex', h(norm_for_hash('0 1 auto')) )},
    {"id":27, "sel": ".s3 .flexbox", "check": lambda p: ("row-reverse" in p.get('flex-direction',''), f"flex-direction = {p.get('flex-direction')}") if p.get('flex-direction') else (False, "flex-direction not found")},
    {"id":28, "sel": ".s3 .flexbox", "check": lambda p: ("nowrap" in p.get('flex-wrap',''), f"flex-wrap = {p.get('flex-wrap')}") if p.get('flex-wrap') else (False, "flex-wrap not found")},
    {"id":29, "sel": ".s3 .flexbox", "check": lambda p: ("row-reverse" in p.get('flex-flow','') and "nowrap" in p.get('flex-flow',''), f"flex-flow = {p.get('flex-flow')}") if p.get('flex-flow') else (False, "flex-flow not found")},
    {"id":30, "sel": ".s3 .flexbox", "check": lambda p: ("center" in p.get('justify-content',''), f"justify-content = {p.get('justify-content')}") if p.get('justify-content') else (False, "justify-content not found")},
    {"id":31, "sel": ".s3 .flexbox", "check": lambda p: ("stretch" in p.get('align-items',''), f"align-items = {p.get('align-items')}") if p.get('align-items') else (False, "align-items not found")},
    {"id":32, "sel": ".s3 .flexbox", "check": lambda p: ("stretch" in p.get('align-content',''), f"align-content = {p.get('align-content')}") if p.get('align-content') else (False, "align-content not found")},
    {"id":33, "sel": ".s3 .flexbox", "check": lambda p: prop_exists_and_not_placeholder(p, 'background')},
    {"id":34, "sel": ".s3 .flexbox", "check": lambda p: prop_exists_and_not_placeholder(p, 'border-color')},
    {"id":35, "sel": ".s3 .flexbox", "check": lambda p: (match_hash(p.get('min-height',''), EXPECTED['s3_min_height']), f"min-height = {p.get('min-height')}") if p.get('min-height') else (False, "min-height not found")},
    {"id":36, "sel": ".s3 .flexbox", "check": lambda p: (match_any_hash(p.get('padding',''), EXPECTED['s3_padding']), f"padding = {p.get('padding')}") if p.get('padding') else (False, "padding not found")},
    {"id":37, "sel": ".s3 .flexbox", "check": lambda p: (('content' not in p) or (p.get('content') not in ("''", '""', '')), "content placeholder removed" if (('content' not in p) or (p.get('content') not in ("''", '""', ''))) else "content placeholder present")},
    {"id":38, "sel": ".s3 .box:nth-child(1)", "check": lambda p: check_flex_exact_hash(p, 'flex', h(norm_for_hash('0 0 80px')) )},
    {"id":39, "sel": ".s3 .box:nth-child(2)", "check": lambda p: check_flex_exact_hash(p, 'flex', h(norm_for_hash('1 1 120px')) )},
    {"id":40, "sel": ".s3 .box:nth-child(3)", "check": lambda p: check_flex_exact_hash(p, 'flex', h(norm_for_hash('2 1 140px')) )},
    {"id":41, "sel": ".s3 .box:nth-child(4)", "check": lambda p: check_flex_exact_hash(p, 'flex', h(norm_for_hash('1 1 120px')) )},
    {"id":42, "sel": ".s3 .box:nth-child(5)", "check": lambda p: check_flex_exact_hash(p, 'flex', h(norm_for_hash('0 0 100px')) )},
    {"id":43, "sel": ".s3 .box:nth-child(6)", "check": lambda p: check_flex_exact_hash(p, 'flex', h(norm_for_hash('1 1 100px')) )},
]

def evaluate(css_path):
    results = [{"testid": t["id"], "status": "fail", "score": 0, "maximum marks": 1, "message": "Test failed"} for t in TESTS]
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_text = f.read()
    except Exception as e:
        for r in results:
            r['message'] = f"unable to open CSS file ({e})"
        return _write_eval(results)

    blocks = parse_css_blocks(css_text)

    for t in TESTS:
        props = blocks.get(t["sel"], {})
        if not props:
            results[t["id"]-1]["message"] = f"selector {t['sel']} not found"
            continue
        ok, msg = t["check"](props)
        if ok is True:
            results[t["id"]-1].update({"status": "success", "score": 1, "message": f"Test {t['id']} passed: {msg}"})
        elif ok is False:
            results[t["id"]-1]["message"] = f"Test {t['id']} failed: {msg}"
        else:
            if isinstance(ok, bool) and ok:
                results[t["id"]-1].update({"status": "success", "score": 1, "message": f"Test {t['id']} passed: {msg}"})
            else:
                results[t["id"]-1]["message"] = f"Test {t['id']} failed: {msg}"

    return _write_eval(results)

def _write_eval(results):
    os.makedirs(os.path.dirname(EVALUATE_FILE), exist_ok=True)
    with open(EVALUATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"data": results}, f, indent=4)
    # for r in results:
    #     print(f"Test {r['testid']}: {r['status']} - {r.get('message','')}")
    return results

if __name__ == "__main__":
    evaluate(sys.argv[1] if len(sys.argv) > 1 else "/home/labDirectory/css/styles.css")
