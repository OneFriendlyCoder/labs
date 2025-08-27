#!/usr/bin/env python3
import sys
import re
import json
import os

EVALUATE_FILE = "/home/.evaluationScripts/evaluate.json"

try:
    import tinycss2
except ImportError:
    print("Missing dependency: tinycss2. Install with: pip install tinycss2")
    sys.exit(2)

# ------------------- helpers (copied/adapted from working autograder) -------------------
def serialize(tokens):
    return tinycss2.serialize(tokens).strip()

def parse_stylesheet(text):
    return tinycss2.parse_stylesheet(text, skip_whitespace=True, skip_comments=True)

def parse_rule_list_from_tokens(tokens):
    s = serialize(tokens)
    return tinycss2.parse_rule_list(s, skip_whitespace=True, skip_comments=True)

def parse_declaration_list_from_tokens(tokens):
    s = serialize(tokens)
    return tinycss2.parse_declaration_list(s, skip_whitespace=True, skip_comments=True)

def strip_important(val):
    if not isinstance(val, str):
        return val
    return re.sub(r'\s*!important\s*$', '', val.strip())

def normalize_whitespace(s):
    return re.sub(r'\s+', ' ', s.strip())

def find_number_unit_in_value(val):
    if not isinstance(val, str):
        return (None, None)
    v = strip_important(val)
    tokens = re.findall(r'(-?\d*\.?\d+)\s*(px|rem|em|vw|vh|%)', v)
    if not tokens:
        return (None, None)
    n, u = tokens[0]
    try:
        return (float(n), u)
    except:
        return (None, None)

def contains_unit_token(val, unit, approx_number=None, tol=1e-3):
    if val is None or not isinstance(val, str):
        return False
    v = strip_important(val)
    matches = re.findall(r'(-?\d*\.?\d+)\s*' + re.escape(unit), v)
    if not matches:
        return False
    if approx_number is None:
        return True
    for m in matches:
        try:
            if abs(float(m) - approx_number) <= tol:
                return True
        except:
            continue
    return False

def approx_equal(a, b, tol=1e-2):
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False

def resolve_shorthand_values_impl(shorthand_str):
    if shorthand_str is None:
        return (None, None, None, None)
    s = normalize_whitespace(strip_important(shorthand_str))
    parts = s.split(' ')
    if len(parts) == 1:
        return (parts[0], parts[0], parts[0], parts[0])
    if len(parts) == 2:
        a, b = parts
        return (a, b, a, b)
    if len(parts) == 3:
        a, b, c = parts
        return (a, b, c, b)
    if len(parts) >= 4:
        return (parts[0], parts[1], parts[2], parts[3])
    return (None, None, None, None)

def resolve_shorthand_values(shorthand_str):
    return resolve_shorthand_values_impl(shorthand_str)

# ------------------- CSS extraction -------------------
def extract_rules(stylesheet):
    out = []
    for r in stylesheet:
        if r.type == 'qualified-rule':
            sel_text = serialize(r.prelude)
            selectors = [s.strip() for s in sel_text.split(',') if s.strip()]
            decls = {}
            for d in parse_declaration_list_from_tokens(r.content):
                if d.type != 'declaration':
                    continue
                name = d.name.strip()
                value = serialize(d.value).strip()
                decls[name] = strip_important(value)
            out.append({'type': 'qualified', 'selectors': selectors, 'declarations': decls})
        elif r.type == 'at-rule' and r.at_keyword.lower() == 'media':
            media_text = serialize(r.prelude)
            inner = []
            if r.content:
                inner_rules = parse_rule_list_from_tokens(r.content)
                for ir in inner_rules:
                    if ir.type != 'qualified-rule':
                        continue
                    sel_text = serialize(ir.prelude)
                    selectors = [s.strip() for s in sel_text.split(',') if s.strip()]
                    decls = {}
                    for d in parse_declaration_list_from_tokens(ir.content):
                        if d.type != 'declaration':
                            continue
                        name = d.name.strip()
                        value = serialize(d.value).strip()
                        decls[name] = strip_important(value)
                    inner.append({'selectors': selectors, 'declarations': decls})
            out.append({'type': 'media', 'media': media_text, 'rules': inner})
        else:
            continue
    return out

def collect_declarations_for_selector(rules_list, selector):
    merged = {}
    for r in rules_list:
        if r['type'] != 'qualified':
            continue
        if selector in r['selectors']:
            merged.update(r['declarations'])
    return merged

def collect_declarations_in_media(rules_list, media_min_width_px, selector):
    target = None
    for r in rules_list:
        if r['type'] != 'media':
            continue
        m = re.search(r'min-width\s*:\s*(\d+)\s*px', r['media'])
        if m and int(m.group(1)) == media_min_width_px:
            target = r
            break
    if not target:
        return None
    merged = {}
    for inner in target['rules']:
        if selector in inner['selectors']:
            merged.update(inner['declarations'])
    return merged

# ------------------- tests (same semantics as your working autograder) -------------------
def test_header_inner(rules):
    decls = collect_declarations_for_selector(rules, '.header-inner')
    missing = []

    if decls.get('display') != 'flex':
        missing.append('display: flex')
    if decls.get('flex-wrap') != 'wrap':
        missing.append('flex-wrap: wrap')
    if decls.get('align-items') != 'center':
        missing.append('align-items: center')
    if decls.get('justify-content') != 'space-between':
        missing.append('justify-content: space-between')

    top = decls.get('padding-top')
    bottom = decls.get('padding-bottom')
    if top is None and bottom is None:
        pad = decls.get('padding')
        if pad is None:
            missing.append('vertical padding ~1rem (padding or padding-top/bottom required)')
        else:
            t, r, b, l = resolve_shorthand_values(pad)
            top = t
            bottom = b

    def is_vertical_ok(tok):
        if tok is None:
            return False
        n, u = find_number_unit_in_value(tok)
        if n is not None and u == 'rem' and approx_equal(n, 1.0, tol=0.05):
            return True
        if isinstance(tok, str) and tok.strip() in ('1rem', '1.0rem'):
            return True
        return False

    ok = False
    if is_vertical_ok(top) or is_vertical_ok(bottom):
        ok = True
    else:
        if isinstance(top, str) and isinstance(bottom, str) and top.strip() == bottom.strip() and 'var(' in top:
            ok = True

    if not ok:
        missing.append('vertical padding (top or bottom) should be ~1rem or identical var(...)')

    return (len(missing) == 0, missing)

def test_hero_title(rules):
    decls = collect_declarations_for_selector(rules, '.hero-title')
    missing = []
    fs = decls.get('font-size')
    if not fs or not contains_unit_token(fs, 'vw', approx_number=6.0):
        missing.append('font-size should use 6vw (or contain 6vw, e.g. clamp(...,6vw,...))')

    lh = decls.get('line-height')
    if not lh:
        missing.append('line-height ~1.05')
    else:
        n, u = find_number_unit_in_value(lh)
        if n is None:
            try:
                n = float(lh.strip())
            except:
                n = None
        if n is None or not approx_equal(n, 1.05, tol=0.02):
            missing.append('line-height should be approximately 1.05')

    mw = decls.get('max-width')
    ok_mw = False
    if mw:
        if contains_unit_token(mw, 'ch', approx_number=48.0):
            ok_mw = True
        else:
            if mw.strip().endswith('48ch'):
                ok_mw = True
    if not ok_mw:
        missing.append('max-width should be 48ch')

    ml = decls.get('margin-left')
    mr = decls.get('margin-right')
    m = decls.get('margin')
    horiz_ok = False
    if ml == 'auto' and mr == 'auto':
        horiz_ok = True
    elif m and 'auto' in m.split():
        horiz_ok = True
    elif m and re.search(r'\bauto\b', m):
        horiz_ok = True
    else:
        if m and 'auto' in m:
            horiz_ok = True

    if not horiz_ok:
        missing.append('horizontal centering: margin-left/right auto OR margin contains auto')

    return (len(missing) == 0, missing)

def test_hero_img(rules):
    decls = collect_declarations_for_selector(rules, '.hero-img')
    missing = []

    display = decls.get('display')
    if display not in ('block', 'inline-block'):
        missing.append('display: block (or inline-block)')

    width = decls.get('width')
    maxw = decls.get('max-width')
    if not ((width and width.strip() == '100%') or (maxw and maxw.strip() == '100%')):
        missing.append('width:100% OR max-width:100%')

    height = decls.get('height')
    if height != 'auto':
        missing.append('height: auto')

    mt = decls.get('margin-top')
    if mt is None:
        m = decls.get('margin')
        if m:
            t, r, b, l = resolve_shorthand_values_impl(m)
            mt = t
    if mt is None:
        missing.append('margin-top: 1.2rem (or margin shorthand with top of 1.2rem)')
    else:
        n, u = find_number_unit_in_value(mt)
        if not (n is not None and u == 'rem' and approx_equal(n, 1.2, tol=0.05)):
            if not (isinstance(mt, str) and mt.strip() in ('1.2rem', '1.20rem')):
                missing.append('margin-top should be ~1.2rem')

    br = decls.get('border-radius')
    if not br:
        missing.append('border-radius: 6px')
    else:
        if not re.search(r'\b6px\b', br):
            missing.append('border-radius: 6px')

    return (len(missing) == 0, missing)

def test_image_group(rules):
    selectors = ['.responsive-img', '.hero-img', '.full-width-img']
    errs = []
    for sel in selectors:
        decls = collect_declarations_for_selector(rules, sel)
        width_ok = False
        w = decls.get('width')
        mw = decls.get('max-width')
        if w and w.strip() == '100%':
            width_ok = True
        if mw and mw.strip() == '100%':
            width_ok = True
        if not width_ok:
            errs.append(f"{sel}: width:100% OR max-width:100% required")

        h = decls.get('height')
        if h != 'auto':
            errs.append(f"{sel}: height:auto required")

        disp = decls.get('display')
        if disp not in ('block', 'inline-block') and not (mw and mw.strip() == '100%'):
            errs.append(f"{sel}: display:block (or inline-block) recommended")

    return (len(errs) == 0, errs)

def test_maxwidth_img(rules):
    decls = collect_declarations_for_selector(rules, '.maxwidth-img')
    missing = []
    mw = decls.get('max-width')
    if not (mw and mw.strip() == '100%'):
        missing.append('max-width: 100%')
    if decls.get('height') != 'auto':
        missing.append('height: auto')
    disp = decls.get('display')
    if disp not in (None, 'block', 'inline-block'):
        missing.append('display: block (recommended)')
    return (len(missing) == 0, missing)

def test_media_queries(rules):
    errs = []
    d700 = collect_declarations_in_media(rules, 700, '.hero-title')
    if d700 is None:
        errs.append('@media (min-width: 700px) missing')
    else:
        fs = d700.get('font-size')
        if not fs or not contains_unit_token(fs, 'vw', approx_number=5.2):
            errs.append('@media 700: .hero-title font-size should be 5.2vw (or contain 5.2vw)')

    d1400 = collect_declarations_in_media(rules, 1400, '.hero-title')
    if d1400 is None:
        errs.append('@media (min-width: 1400px) missing')
    else:
        fs = d1400.get('font-size')
        if not fs:
            errs.append('@media 1400: missing font-size')
        else:
            if not re.search(r'(\b72px\b)', fs):
                errs.append('@media 1400: .hero-title font-size should be 72px')

    return (len(errs) == 0, errs)

# ------------------- runner & evaluator writer -------------------
TEST_DEFINITIONS = [
    (1, "Test 1: .header-inner (flex + padding)", test_header_inner),
    (2, "Test 2: .hero-title (fluid heading)", test_hero_title),
    (3, "Test 3: .hero-img (responsive image)", test_hero_img),
    (4, "Test 4: .responsive-img / .hero-img / .full-width-img group", test_image_group),
    (5, "Test 5: .maxwidth-img (no upscale)", test_maxwidth_img),
    (6, "Test 6: @media queries (700px, 1400px)", test_media_queries),
]

def evaluate_to_file(css_path):
    # prepare default fail results
    results = []
    for tid, title, _ in TEST_DEFINITIONS:
        results.append({
            "testid": tid,
            "status": "fail",
            "score": 0,
            "maximum marks": 1,
            "message": "Test failed"
        })

    try:
        with open(css_path, 'r', encoding='utf8') as f:
            css_text = f.read()
    except Exception:
        # Generic file-open error message
        for r in results:
            r['message'] = "unable to open CSS file"
        _write_eval(results)
        return

    sheet = parse_stylesheet(css_text)
    rules = extract_rules(sheet)

    for tid, title, fn in TEST_DEFINITIONS:
        ok, details = fn(rules)
        idx = tid - 1
        if ok:
            results[idx].update({
                "status": "success",
                "score": 1,
                "message": f"Test {tid} passed"
            })
        else:
            # Generic failure message (no descriptive details)
            results[idx].update({
                "status": "fail",
                "score": 0,
                "message": f"Test {tid} failed"
            })

    _write_eval(results)

def _write_eval(results):
    os.makedirs(os.path.dirname(EVALUATE_FILE) or '.', exist_ok=True)
    payload = {"data": results}
    with open(EVALUATE_FILE, 'w', encoding='utf8') as f:
        json.dump(payload, f, indent=4)

def main(argv):
    file_path = "/home/labDirectory/css/styles.css"
    css_path = file_path
    evaluate_to_file(css_path)
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
