#!/usr/bin/env python3
import sys
import re
import json
import os
import base64
import hashlib
from collections import defaultdict

EVALUATE_FILE = "/home/.evaluationScripts/evaluate.json"

def b64(s):
    return base64.b64encode(s.encode()).decode()

def db64(s):
    return base64.b64decode(s.encode()).decode()

def h(s):
    return hashlib.sha256(s.encode()).hexdigest()

def normalize_val(v):
    return re.sub(r'\s+', ' ', v.strip().lower().replace('!important', '')).strip()

def parse_css_blocks(text):
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
    "fixed_width": h(db64("OTYwcHg=")),
    "fixed_bg": h(db64("I2ZmZmJlNg==")),
    "fixed_border_color": h(db64("I2U2ZDY3YQ==")),
    "fixed_header_bg": h(db64("I2Y5ZTc5Zg==")),
    "fixed_header_padding": [h(db64("MXJlbQ=="))],
    "fixed_footer_padding": [h(db64("MC43NXJlbQ==")), h(db64("Ljc1cmVt"))],
    "liquid_width": h(db64("ODAl")),
    "liquid_max_width": h(db64("MTIwMHB4")),
    "liquid_bg": h(db64("I2U4ZjhmZg==")),
    "liquid_border_color": h(db64("I2JmZWFmNw==")),
    "liquid_header_bg": h(db64("I2Q3ZjNmZg==")),
    "liquid_header_padding": [h(db64("MXJlbQ=="))],
    "liquid_footer_padding": [h(db64("MC43NXJlbQ==")), h(db64("Ljc1cmVt"))],
}

def match_hash(value, expected_hash):
    return h(value) == expected_hash

def match_any_hash(value, expected_hashes):
    return any(h(value) == exp for exp in expected_hashes)

def check_width(props, expected_hash):
    v = props.get('width')
    return (v and match_hash(v, expected_hash), f"width = {v}" if v else "width not found")

def check_max_width(props, expected_hash):
    v = props.get('max-width')
    return (v and match_hash(v, expected_hash), f"max-width = {v}" if v else "max-width not found")

def check_background_hex(props, expected_hash):
    v = props.get('background') or props.get('background-color')
    return (v and match_hash(v, expected_hash), f"background = {v}" if v else "background not found")

def check_padding_contains(props, expected_hashes):
    v = props.get('padding')
    if not v:
        for k in props:
            if k.startswith('padding-') and match_any_hash(props[k], expected_hashes):
                return True, f"{k}: {props[k]}"
        return False, "padding not found"
    return (match_any_hash(v, expected_hashes), f"padding = {v}")

def check_border_shorthand_or_parts(props, side=None, expected_width_hash=None, expected_style='solid', expected_color_hash=None):
    keys = [side] if side else []
    keys.append('border')
    width_key = (side + '-width') if side else 'border-width'
    style_key = (side + '-style') if side else 'border-style'
    color_key = (side + '-color') if side else 'border-color'
    for k in keys:
        v = props.get(k)
        if v and expected_style in v:
            parts = v.split()
            if any(match_hash(p, expected_width_hash) for p in parts) and any(match_hash(p, expected_color_hash) for p in parts):
                return True, f"{k} = {v}"
    if all(props.get(k) for k in (width_key, style_key, color_key)):
        if match_hash(props[width_key], expected_width_hash) and props[style_key] == expected_style and match_hash(props[color_key], expected_color_hash):
            return True, f"{width_key}/{style_key}/{color_key} OK"
    return False, "border not matching"

def check_text_align_center(props):
    v = props.get('text-align')
    return ('center' in v, f"text-align = {v}") if v else (False, "text-align not found")

def check_font_weight_bold(props):
    v = props.get('font-weight')
    if not v:
        return False, "font-weight not found"
    if v == 'bold':
        return True, f"font-weight = {v}"
    try:
        if int(v) >= 600:
            return True, f"font-weight = {v}"
    except:
        pass
    return False, f"font-weight = {v} (expected bold or >=600)"

TESTS = [
    {"id": 1, "sel": ".fixed-demo .container", "check": lambda p: check_width(p, EXPECTED["fixed_width"])},
    {"id": 2, "sel": ".fixed-demo .container", "check": lambda p: check_background_hex(p, EXPECTED["fixed_bg"])},
    {"id": 3, "sel": ".fixed-demo .container", "check": lambda p: check_border_shorthand_or_parts(p, None, EXPECTED["fixed_width"], 'solid', EXPECTED["fixed_border_color"])},
    {"id": 4, "sel": ".fixed-demo .fixed-header", "check": lambda p: check_background_hex(p, EXPECTED["fixed_header_bg"])},
    {"id": 5, "sel": ".fixed-demo .fixed-header", "check": lambda p: check_padding_contains(p, EXPECTED["fixed_header_padding"])},
    {"id": 6, "sel": ".fixed-demo .fixed-header", "check": lambda p: check_border_shorthand_or_parts(p, 'border-bottom', EXPECTED["fixed_width"], 'solid', EXPECTED["fixed_border_color"])},
    {"id": 7, "sel": ".fixed-demo .fixed-footer", "check": lambda p: check_background_hex(p, EXPECTED["fixed_header_bg"])},
    {"id": 8, "sel": ".fixed-demo .fixed-footer", "check": lambda p: check_padding_contains(p, EXPECTED["fixed_footer_padding"])},
    {"id": 9, "sel": ".fixed-demo .fixed-footer", "check": lambda p: check_border_shorthand_or_parts(p, 'border-top', EXPECTED["fixed_width"], 'solid', EXPECTED["fixed_border_color"])},
    {"id":10, "sel": ".fixed-demo .fixed-footer", "check": check_text_align_center},
    {"id":11, "sel": ".fixed-demo .fixed-footer", "check": check_font_weight_bold},
    {"id":12, "sel": ".liquid-demo .container", "check": lambda p: check_width(p, EXPECTED["liquid_width"])},
    {"id":13, "sel": ".liquid-demo .container", "check": lambda p: check_max_width(p, EXPECTED["liquid_max_width"])},
    {"id":14, "sel": ".liquid-demo .container", "check": lambda p: check_background_hex(p, EXPECTED["liquid_bg"])},
    {"id":15, "sel": ".liquid-demo .container", "check": lambda p: check_border_shorthand_or_parts(p, None, EXPECTED["liquid_width"], 'solid', EXPECTED["liquid_border_color"])},
    {"id":16, "sel": ".liquid-demo .liquid-header", "check": lambda p: check_background_hex(p, EXPECTED["liquid_header_bg"])},
    {"id":17, "sel": ".liquid-demo .liquid-header", "check": lambda p: check_padding_contains(p, EXPECTED["liquid_header_padding"])},
    {"id":18, "sel": ".liquid-demo .liquid-header", "check": lambda p: check_border_shorthand_or_parts(p, 'border-bottom', EXPECTED["liquid_width"], 'solid', EXPECTED["liquid_border_color"])},
    {"id":19, "sel": ".liquid-demo .liquid-footer", "check": lambda p: check_background_hex(p, EXPECTED["liquid_header_bg"])},
    {"id":20, "sel": ".liquid-demo .liquid-footer", "check": lambda p: check_padding_contains(p, EXPECTED["liquid_footer_padding"])},
    {"id":21, "sel": ".liquid-demo .liquid-footer", "check": lambda p: check_border_shorthand_or_parts(p, 'border-top', EXPECTED["liquid_width"], 'solid', EXPECTED["liquid_border_color"])},
    {"id":22, "sel": ".liquid-demo .liquid-footer", "check": check_text_align_center},
    {"id":23, "sel": ".liquid-demo .liquid-footer", "check": check_font_weight_bold},
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
        if ok:
            results[t["id"]-1].update({"status": "success", "score": 1, "message": f"Test {t['id']} passed"})
        else:
            results[t["id"]-1]["message"] = f"Test {t['id']} failed"
    _write_eval(results)

def _write_eval(results):
    os.makedirs(os.path.dirname(EVALUATE_FILE), exist_ok=True)
    with open(EVALUATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"data": results}, f, indent=4)

if __name__ == "__main__":
    evaluate(sys.argv[1] if len(sys.argv) > 1 else "/home/labDirectory/css/styles.css")
