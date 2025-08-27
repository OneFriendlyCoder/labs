# #!/usr/bin/env python3
# """
# evaluate_fixed_styles.py

# Run a set of checks on the fixed-demo CSS rules and write results to
# /home/.evaluationScripts/evaluate.json in the same format used by the lab runner.

# Usage:
#     python3 evaluate_fixed_styles.py path/to/css/styles.css
# """

# import sys
# import re
# import json
# import os
# from collections import defaultdict

# # Output evaluation file (same as your example)
# EVALUATE_FILE = "/home/.evaluationScripts/evaluate.json"

# # ---------- Utilities ----------
# def normalize_val(v):
#     """Lowercase, strip whitespace and remove !important"""
#     return re.sub(r'\s+',' ', v.strip().lower().replace('!important','')).strip()

# def parse_css_blocks(text):
#     """Return dict selector -> properties dict (last occurrence wins)"""
#     # remove comments so commented TODOs don't interfere
#     text_nocomments = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
#     pattern = re.compile(r'([^{]+)\{([^}]*)\}', re.S)
#     blocks = defaultdict(dict)
#     for m in pattern.finditer(text_nocomments):
#         selector_text = m.group(1).strip()
#         body = m.group(2).strip()
#         # split selectors by comma
#         selectors = [s.strip() for s in selector_text.split(',') if s.strip()]
#         # parse properties
#         props = {}
#         for part in body.split(';'):
#             if ':' in part:
#                 k, v = part.split(':', 1)
#                 props[k.strip().lower()] = normalize_val(v)
#         for sel in selectors:
#             blocks[sel].update(props)
#     return blocks

# # property checks with tolerant matching (return (bool, message))
# def check_width(props, expected='960px'):
#     v = props.get('width')
#     if not v:
#         return False, "width not found"
#     if normalize_val(v) == expected:
#         return True, f"width = {v}"
#     return False, f"width = {v} (expected {expected})"

# def check_background_hex(props, expected_hex):
#     v = props.get('background') or props.get('background-color')
#     if not v:
#         return False, "background not found"
#     if expected_hex.lower() in v:
#         return True, f"background = {v}"
#     return False, f"background = {v} (expected to include {expected_hex})"

# def check_padding_contains(props, expected_rem_strs):
#     v = props.get('padding')
#     if not v:
#         # could be padding-left/right etc. Check any padding- prop
#         for k in props:
#             if k.startswith('padding-'):
#                 if any(s in props[k] for s in expected_rem_strs):
#                     return True, f"{k}: {props[k]}"
#         return False, "padding not found"
#     if any(s in v for s in expected_rem_strs):
#         return True, f"padding = {v}"
#     return False, f"padding = {v} (expected to include one of {expected_rem_strs})"

# def check_border_shorthand_or_parts(props, side=None, expected_width='2px', expected_style='solid', expected_color='#e6d67a'):
#     """
#     side: None (any border) or 'border-top' / 'border-bottom'
#     Accepts 'border' shorthand or separate border-width/style/color or border-side variants.
#     """
#     keys_to_try = []
#     if side:
#         keys_to_try.append(side)
#     keys_to_try.append('border')
#     # also try split properties
#     width_key = (side + '-width') if side else 'border-width'
#     style_key = (side + '-style') if side else 'border-style'
#     color_key = (side + '-color') if side else 'border-color'

#     # try shorthand first
#     for k in keys_to_try:
#         v = props.get(k)
#         if v:
#             if expected_width in v and expected_style in v and expected_color in v:
#                 return True, f"{k} = {v}"
#             present = all(x in v for x in (expected_width, expected_style, expected_color))
#             if present:
#                 return True, f"{k} = {v}"
#             return False, f"{k} = {v} (missing one of: {expected_width}, {expected_style}, {expected_color})"

#     # try split properties
#     w = props.get(width_key) or props.get('border-width')
#     s = props.get(style_key) or props.get('border-style')
#     c = props.get(color_key) or props.get('border-color')
#     if w and s and c:
#         if expected_width in w and expected_style in s and expected_color in c:
#             return True, f"{width_key}/{style_key}/{color_key} = {w} / {s} / {c}"
#         else:
#             return False, f"{width_key}/{style_key}/{color_key} = {w} / {s} / {c} (expected {expected_width}/{expected_style}/{expected_color})"
#     return False, "border property not found"

# def check_text_align_center(props):
#     v = props.get('text-align')
#     if not v:
#         return False, "text-align not found"
#     if 'center' in v:
#         return True, f"text-align = {v}"
#     return False, f"text-align = {v} (expected 'center')"

# def check_font_weight_bold(props):
#     v = props.get('font-weight')
#     if not v:
#         return False, "font-weight not found"
#     vnorm = v.strip()
#     if vnorm == 'bold':
#         return True, f"font-weight = {v}"
#     try:
#         num = int(vnorm)
#         if num >= 600:
#             return True, f"font-weight = {v}"
#     except:
#         pass
#     return False, f"font-weight = {v} (expected 'bold' or numeric >= 600)"

# # ---------- Tests definition ----------
# # We'll create one test per required item so evaluate.json mirrors the earlier simple structure.
# TEST_DEFINITIONS = [
#     # container tests
#     {"testid": 1, "selector": ".fixed-demo .container", "check": "width", "desc": "container width exactly 960px"},
#     {"testid": 2, "selector": ".fixed-demo .container", "check": "background", "desc": "container background #fffbe6"},
#     {"testid": 3, "selector": ".fixed-demo .container", "check": "border", "desc": "container border 2px solid #e6d67a"},
#     # header tests
#     {"testid": 4, "selector": ".fixed-demo .fixed-header", "check": "background", "desc": "header background #f9e79f"},
#     {"testid": 5, "selector": ".fixed-demo .fixed-header", "check": "padding", "desc": "header padding includes 1rem"},
#     {"testid": 6, "selector": ".fixed-demo .fixed-header", "check": "border-bottom", "desc": "header border-bottom 2px solid #e6d67a"},
#     # footer tests
#     {"testid": 7, "selector": ".fixed-demo .fixed-footer", "check": "background", "desc": "footer background #f9e79f"},
#     {"testid": 8, "selector": ".fixed-demo .fixed-footer", "check": "padding", "desc": "footer padding includes 0.75rem"},
#     {"testid": 9, "selector": ".fixed-demo .fixed-footer", "check": "border-top", "desc": "footer border-top 2px solid #e6d67a"},
#     {"testid":10, "selector": ".fixed-demo .fixed-footer", "check": "text-align", "desc": "footer text-align center"},
#     {"testid":11, "selector": ".fixed-demo .fixed-footer", "check": "font-weight", "desc": "footer font-weight bold/600+"},
# ]

# # ---------- Main ----------
# def evaluate(css_path):
#     # default all tests to fail (mirrors original pattern)
#     results = []
#     for t in TEST_DEFINITIONS:
#         results.append({
#             "testid": t["testid"],
#             "status": "fail",
#             "score": 0,
#             "maximum marks": 1,
#             "message": f"Test case {t['testid']} failed: {t['desc']}"
#         })

#     # load css
#     try:
#         with open(css_path, 'r', encoding='utf-8') as f:
#             css_text = f.read()
#     except Exception as e:
#         # write results (all failed) and an error message
#         for r in results:
#             r['message'] = f"Test case {r['testid']} failed: unable to open CSS file ({e})"
#         _write_evaluation(results)
#         return

#     blocks = parse_css_blocks(css_text)

#     # helper to update result entry by testid
#     def set_result(testid, ok, message=None):
#         idx = next(i for i, tt in enumerate(results) if tt['testid'] == testid)
#         if ok:
#             results[idx].update({
#                 "status": "success",
#                 "score": 1,
#                 "message": f"Test case {testid} success: {message or ''}".strip()
#             })
#         else:
#             results[idx].update({
#                 "status": "fail",
#                 "score": 0,
#                 "message": f"Test case {testid} failed: {message or ''}".strip()
#             })

#     # run each test
#     for t in TEST_DEFINITIONS:
#         sel = t['selector']
#         props = blocks.get(sel, {})
#         tid = t['testid']
#         check = t['check']
#         desc = t['desc']

#         if not props:
#             set_result(tid, False, f"selector {sel} not found")
#             continue

#         if check == "width":
#             ok, msg = check_width(props, '960px')
#             set_result(tid, ok, msg)
#         elif check == "background":
#             # container uses #fffbe6, header/footer use #f9e79f
#             expected = '#fffbe6' if 'container' in sel else '#f9e79f'
#             ok, msg = check_background_hex(props, expected)
#             set_result(tid, ok, msg)
#         elif check == "border":
#             ok, msg = check_border_shorthand_or_parts(props, side=None, expected_width='2px', expected_style='solid', expected_color='#e6d67a')
#             set_result(tid, ok, msg)
#         elif check == "padding":
#             if 'fixed-header' in sel:
#                 ok, msg = check_padding_contains(props, ['1rem'])
#             else:
#                 ok, msg = check_padding_contains(props, ['0.75rem', '.75rem'])
#             set_result(tid, ok, msg)
#         elif check == "border-bottom":
#             ok, msg = check_border_shorthand_or_parts(props, side='border-bottom', expected_width='2px', expected_style='solid', expected_color='#e6d67a')
#             set_result(tid, ok, msg)
#         elif check == "border-top":
#             ok, msg = check_border_shorthand_or_parts(props, side='border-top', expected_width='2px', expected_style='solid', expected_color='#e6d67a')
#             set_result(tid, ok, msg)
#         elif check == "text-align":
#             ok, msg = check_text_align_center(props)
#             set_result(tid, ok, msg)
#         elif check == "font-weight":
#             ok, msg = check_font_weight_bold(props)
#             set_result(tid, ok, msg)
#         else:
#             set_result(tid, False, f"unknown check {check}")

#     _write_evaluation(results)

# def _write_evaluation(results):
#     try:
#         os.makedirs(os.path.dirname(EVALUATE_FILE), exist_ok=True)
#         with open(EVALUATE_FILE, 'w', encoding='utf-8') as f:
#             json.dump({"data": results}, f, indent=4)
#     except Exception as e:
#         # best effort: try to write to cwd if primary path fails
#         try:
#             with open('evaluate.json', 'w+', encoding='utf-8') as f:
#                 json.dump({"data": results, "error": str(e)}, f, indent=4)
#         except:
#             pass

# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         # nothing printed per your request; just write default failed results
#         evaluate('css/styles.css')
#     else:
#         evaluate(sys.argv[1])




#!/usr/bin/env python3
"""
evaluate_styles.py

Checks for both fixed-demo and liquid-demo CSS implementations
and writes evaluation results to /home/.evaluationScripts/evaluate.json
"""

import sys
import re
import json
import os
from collections import defaultdict

EVALUATE_FILE = "./evaluate.json"

# ---------- Utilities ----------
def normalize_val(v):
    return re.sub(r'\s+',' ', v.strip().lower().replace('!important','')).strip()

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

# Checks
def check_width(props, expected):
    v = props.get('width')
    return (v == expected, f"width = {v}" if v else "width not found")

def check_max_width(props, expected):
    v = props.get('max-width')
    return (v == expected, f"max-width = {v}" if v else "max-width not found")

def check_background_hex(props, expected_hex):
    v = props.get('background') or props.get('background-color')
    return (expected_hex in v, f"background = {v}" if v else "background not found") if v else (False, "background not found")

def check_padding_contains(props, expected_values):
    v = props.get('padding')
    if not v:
        for k in props:
            if k.startswith('padding-') and any(s in props[k] for s in expected_values):
                return True, f"{k}: {props[k]}"
        return False, "padding not found"
    return (any(s in v for s in expected_values), f"padding = {v}")

def check_border_shorthand_or_parts(props, side=None, expected_width='2px', expected_style='solid', expected_color=None):
    keys = [side] if side else []
    keys.append('border')
    width_key = (side + '-width') if side else 'border-width'
    style_key = (side + '-style') if side else 'border-style'
    color_key = (side + '-color') if side else 'border-color'

    for k in keys:
        v = props.get(k)
        if v and all(x in v for x in (expected_width, expected_style, expected_color)):
            return True, f"{k} = {v}"
    if all(props.get(k) for k in (width_key, style_key, color_key)):
        if all(expected_width in props[width_key] and expected_style in props[style_key] and expected_color in props[color_key]):
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

# ---------- Tests ----------
TESTS = [
    # Fixed Container
    {"id": 1, "sel": ".fixed-demo .container", "check": lambda p: check_width(p, '960px'), "desc": "fixed container width 960px"},
    {"id": 2, "sel": ".fixed-demo .container", "check": lambda p: check_background_hex(p, '#fffbe6'), "desc": "fixed container background"},
    {"id": 3, "sel": ".fixed-demo .container", "check": lambda p: check_border_shorthand_or_parts(p, None, '2px', 'solid', '#e6d67a'), "desc": "fixed container border"},

    # Fixed Header
    {"id": 4, "sel": ".fixed-demo .fixed-header", "check": lambda p: check_background_hex(p, '#f9e79f'), "desc": "fixed header background"},
    {"id": 5, "sel": ".fixed-demo .fixed-header", "check": lambda p: check_padding_contains(p, ['1rem']), "desc": "fixed header padding"},
    {"id": 6, "sel": ".fixed-demo .fixed-header", "check": lambda p: check_border_shorthand_or_parts(p, 'border-bottom', '2px', 'solid', '#e6d67a'), "desc": "fixed header border-bottom"},

    # Fixed Footer
    {"id": 7, "sel": ".fixed-demo .fixed-footer", "check": lambda p: check_background_hex(p, '#f9e79f'), "desc": "fixed footer background"},
    {"id": 8, "sel": ".fixed-demo .fixed-footer", "check": lambda p: check_padding_contains(p, ['0.75rem', '.75rem']), "desc": "fixed footer padding"},
    {"id": 9, "sel": ".fixed-demo .fixed-footer", "check": lambda p: check_border_shorthand_or_parts(p, 'border-top', '2px', 'solid', '#e6d67a'), "desc": "fixed footer border-top"},
    {"id":10, "sel": ".fixed-demo .fixed-footer", "check": check_text_align_center, "desc": "fixed footer text-align center"},
    {"id":11, "sel": ".fixed-demo .fixed-footer", "check": check_font_weight_bold, "desc": "fixed footer font-weight bold/600+"},

    # Liquid Container
    {"id":12, "sel": ".liquid-demo .container", "check": lambda p: check_width(p, '80%'), "desc": "liquid container width 80%"},
    {"id":13, "sel": ".liquid-demo .container", "check": lambda p: check_max_width(p, '1200px'), "desc": "liquid container max-width 1200px"},
    {"id":14, "sel": ".liquid-demo .container", "check": lambda p: check_background_hex(p, '#e8f8ff'), "desc": "liquid container background"},
    {"id":15, "sel": ".liquid-demo .container", "check": lambda p: check_border_shorthand_or_parts(p, None, '2px', 'solid', '#bfeaf7'), "desc": "liquid container border"},

    # Liquid Header
    {"id":16, "sel": ".liquid-demo .liquid-header", "check": lambda p: check_background_hex(p, '#d7f3ff'), "desc": "liquid header background"},
    {"id":17, "sel": ".liquid-demo .liquid-header", "check": lambda p: check_padding_contains(p, ['1rem']), "desc": "liquid header padding"},
    {"id":18, "sel": ".liquid-demo .liquid-header", "check": lambda p: check_border_shorthand_or_parts(p, 'border-bottom', '2px', 'solid', '#bfeaf7'), "desc": "liquid header border-bottom"},

    # Liquid Footer
    {"id":19, "sel": ".liquid-demo .liquid-footer", "check": lambda p: check_background_hex(p, '#d7f3ff'), "desc": "liquid footer background"},
    {"id":20, "sel": ".liquid-demo .liquid-footer", "check": lambda p: check_padding_contains(p, ['0.75rem', '.75rem']), "desc": "liquid footer padding"},
    {"id":21, "sel": ".liquid-demo .liquid-footer", "check": lambda p: check_border_shorthand_or_parts(p, 'border-top', '2px', 'solid', '#bfeaf7'), "desc": "liquid footer border-top"},
    {"id":22, "sel": ".liquid-demo .liquid-footer", "check": check_text_align_center, "desc": "liquid footer text-align center"},
    {"id":23, "sel": ".liquid-demo .liquid-footer", "check": check_font_weight_bold, "desc": "liquid footer font-weight bold/600+"},
]

def evaluate(css_path):
    results = [{"testid": t["id"], "status": "fail", "score": 0, "maximum marks": 1, "message": f"Test case {t['id']} failed: {t['desc']}"} for t in TESTS]

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
            results[t["id"]-1].update({"status": "success", "score": 1, "message": f"Test case {t['id']} success: {msg}"})
        else:
            results[t["id"]-1]["message"] = f"Test case {t['id']} failed: {msg}"

    _write_eval(results)

def _write_eval(results):
    os.makedirs(os.path.dirname(EVALUATE_FILE), exist_ok=True)
    with open(EVALUATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"data": results}, f, indent=4)

if __name__ == "__main__":
    evaluate(sys.argv[1] if len(sys.argv) > 1 else "css/styles.css")
