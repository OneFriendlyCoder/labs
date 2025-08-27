import sys
import re
import json
import os
from collections import defaultdict

# CHANGE THIS PATH to match your environment if needed
EVALUATE_FILE = "/home/.evaluationScripts/evaluate.json"

class Grader:
    """
    A class to encapsulate the autograding logic for the CSS lab.
    """
    
    def __init__(self, css_path):
        self.css_path = css_path
        self.css_text = ""
        self.merged_blocks = defaultdict(dict)
        self.occurrences = defaultdict(list)
        self.results = []
        self.load_and_parse_css()

    def normalize_val(self, v):
        """Normalize CSS property values by stripping whitespace and removing !important."""
        if v is None:
            return ''
        return re.sub(r'\s+', ' ', v.strip().lower().replace('!important', '')).strip()

    def parse_css_blocks_with_occurrences(self, text):
        """
        Parse CSS into a merged view and an occurrences list.
        - merged_blocks: selector -> props (later declarations override earlier ones)
        - occurrences: selector -> [props_dicts in order of appearance]
        """
        text_nocomments = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
        pattern = re.compile(r'([^{]+)\{([^}]*)\}', re.S)
        
        merged = defaultdict(dict)
        occurrences = defaultdict(list)

        for m in pattern.finditer(text_nocomments):
            selectors_raw = m.group(1).strip()
            body_raw = m.group(2).strip()
            selectors = [s.strip() for s in selectors_raw.split(',') if s.strip()]
            
            props = {}
            for part in [p for p in body_raw.split(';') if p.strip()]:
                if ':' in part:
                    k, v = part.split(':', 1)
                    props[k.strip().lower()] = self.normalize_val(v)
            
            for sel in selectors:
                occurrences[sel].append(dict(props))
                merged[sel].update(props)
        return merged, occurrences

    def find_property_values(self, selector, prop, css_text):
        """
        Search the whole css_text (including inside @media) for occurrences of `selector`
        and extract the property's value.
        """
        css_no_comments = re.sub(r'/\*.*?\*/', '', css_text, flags=re.S)
        pattern = re.compile(r'(?:(?:^|[,\n])\s*' + re.escape(selector) + r'\s*)\{([^}]*)\}', re.S | re.I)
        
        values = []
        for m in pattern.finditer(css_no_comments):
            body = m.group(1)
            prop_pattern = re.compile(r'\b' + re.escape(prop) + r'\s*:\s*([^;}]*)', re.I)
            pm = prop_pattern.search(body)
            if pm:
                values.append(self.normalize_val(pm.group(1)))
        return values

    def normalize_check_result(self, res):
        """Normalizes a check result to a (bool, message) tuple."""
        if isinstance(res, tuple) and len(res) >= 2:
            return bool(res[0]), str(res[1])
        if isinstance(res, bool):
            return res, "ok" if res else "failed"
        if isinstance(res, str):
            return True, res
        return False, "check returned unexpected type"

    def prop_present_and_nonempty(self, props, prop):
        """Checks if a property exists and is not empty."""
        v = props.get(prop)
        if not v:
            return False, f"{prop} not found"
        if v in ("''", '""', ''):
            return False, f"{prop} looks empty: {v}"
        return True, f"{prop} = {v}"

    def check_value_contains(self, props, prop, candidates):
        """Checks if a property's value contains any of the candidate strings."""
        ok, msg = self.prop_present_and_nonempty(props, prop)
        if not ok:
            return False, msg
        val = props.get(prop, '')
        for c in candidates:
            if c in val:
                return True, f"{prop} = {val}"
        return False, f"{prop} = {val} (does not contain any of {candidates})"

    def any_occurrence_has_in_css(self, selector, prop, candidates):
        """
        Checks if any occurrence of a selector-property combination
        (including inside @media) contains a candidate substring.
        """
        vals = self.find_property_values(selector, prop, self.css_text)
        if not vals:
            return False, f"no occurrences of {selector} with property {prop}"
        for i, v in enumerate(vals):
            for c in candidates:
                if c in v:
                    return True, f"occurrence #{i+1} {prop} = {v}"
        return False, f"no occurrence had {prop} containing any of {candidates}. Found values: {vals}"

    def load_and_parse_css(self):
        """Loads and parses the CSS file."""
        try:
            with open(self.css_path, 'r', encoding='utf-8') as f:
                self.css_text = f.read()
            self.merged_blocks, self.occurrences = self.parse_css_blocks_with_occurrences(self.css_text)
        except Exception as e:
            self.results.append({
                "testid": 0, 
                "status": "fail", 
                "score": 0, 
                "maximum marks": 1, 
                "message": f"Unable to open CSS file: {e}"
            })

    def run_tests(self):
        """Defines and runs all tests."""
        tests = [
            (1, ".hero-inner - max-width", [".hero-inner"], lambda: self.check_value_contains(self.merged_blocks.get(".hero-inner", {}), 'max-width', ['var(--site-width)', '1200px'])),
            (2, ".hero-inner - margin", [".hero-inner"], lambda: self.check_value_contains(self.merged_blocks.get(".hero-inner", {}), 'margin', ['0 auto', '0px auto', 'auto'])),
            (3, ".hero-inner - padding", [".hero-inner"], lambda: self.check_value_contains(self.merged_blocks.get(".hero-inner", {}), 'padding', ['0 20px', '0px 20px'])),
            (4, ".hero-inner - display", [".hero-inner"], lambda: self.check_value_contains(self.merged_blocks.get(".hero-inner", {}), 'display', ['flex'])),
            (5, ".hero-inner - align-items", [".hero-inner"], lambda: self.check_hero_align()),
            (6, ".hero-inner - justify-content", [".hero-inner"], lambda: self.check_value_contains(self.merged_blocks.get(".hero-inner", {}), 'justify-content', ['space-between'])),
            (7, ".hero-inner - gap", [".hero-inner"], lambda: self.check_value_contains(self.merged_blocks.get(".hero-inner", {}), 'gap', ['12px'])),
            (8, ".site-header - display:flex", [".site-header"], lambda: self.check_value_contains(self.merged_blocks.get(".site-header", {}), 'display', ['flex'])),
            (9, ".site-header - align-items", [".site-header"], lambda: self.check_value_contains(self.merged_blocks.get(".site-header", {}), 'align-items', ['center'])),
            (10, ".site-header - justify-content", [".site-header"], lambda: self.check_value_contains(self.merged_blocks.get(".site-header", {}), 'justify-content', ['space-between'])),
            (11, ".site-header - gap", [".site-header"], lambda: self.check_value_contains(self.merged_blocks.get(".site-header", {}), 'gap', ['12px'])),
            (12, ".filters - display:flex", [".filters"], lambda: self.check_value_contains(self.merged_blocks.get(".filters", {}), 'display', ['flex'])),
            (13, ".filters - gap", [".filters"], lambda: self.check_value_contains(self.merged_blocks.get(".filters", {}), 'gap', ['12px'])),
            (14, ".filters - align-items", [".filters"], lambda: self.check_filters_align()),
            (15, ".filters - margin", [".filters"], lambda: self.check_value_contains(self.merged_blocks.get(".filters", {}), 'margin', ['18px 0', '18px 0px'])),
            (16, ".filters - flex-wrap", [".filters"], lambda: self.check_value_contains(self.merged_blocks.get(".filters", {}), 'flex-wrap', ['wrap'])),
        ]

        for tid, desc, sels, check_fn in tests:
            if not any(s in self.merged_blocks or s in self.occurrences or re.search(r'\b' + re.escape(s) + r'\b', self.css_text) for s in sels):
                self.results.append({"testid": tid, "status": "fail", "score": 0, "maximum marks": 1, "message": f"Selector(s) {sels} not present in CSS"})
                continue

            try:
                ok, msg = self.normalize_check_result(check_fn())
                self.results.append({
                    "testid": tid,
                    "status": "success" if ok else "fail",
                    "score": 1 if ok else 0,
                    "maximum marks": 1,
                    "message": f"Passed: {desc}. {msg}" if ok else f"Failed: {desc}. {msg}"
                })
            except Exception as e:
                self.results.append({
                    "testid": tid,
                    "status": "fail",
                    "score": 0,
                    "maximum marks": 1,
                    "message": f"Error during check: {e}"
                })
        
        return self.write_eval()

    # def check_hero_align(self):
    #     """Check for .hero-inner align-items, allowing responsive overrides."""
    #     ok1, msg1 = self.check_value_contains(self.merged_blocks.get(".hero-inner", {}), 'align-items', ['center'])
    #     if ok1:
    #         return True, msg1
    #     return self.any_occurrence_has_in_css(".hero-inner", 'align-items', ['center', 'flex-start'])
    
    def check_hero_align(self):
        return self.check_value_contains(
            self.merged_blocks.get(".hero-inner", {}),
            'align-items',
            ['center']
        )

    def check_filters_align(self):
        return self.check_value_contains(
            self.merged_blocks.get(".filters", {}),
            'align-items',
            ['center']
        )

    def check_mobile_adjustments(self):
        """Checks for mobile-specific styles for a small-screen resolution."""
        ok1, m1 = self.any_occurrence_has_in_css(".hero-inner", 'padding', ['0 8px', '0px 8px'])
        ok2, m2 = self.any_occurrence_has_in_css(".site-wrap", 'padding', ['14px'])
        ok3a, m3a = self.any_occurrence_has_in_css(".nft-meta", 'flex-direction', ['column'])
        ok3b, m3b = self.any_occurrence_has_in_css(".nft-meta", 'align-items', ['flex-start'])
        ok3c, m3c = self.any_occurrence_has_in_css(".nft-meta", 'gap', ['6px'])
        
        passed = ok1 and ok2 and ok3a and ok3b and ok3c
        detail = f"hero-inner padding: {m1}; site-wrap padding: {m2}; nft-meta: {m3a}, {m3b}, {m3c}"
        return (passed, detail)

    def write_eval(self):
        """Writes the evaluation results to a JSON file."""
        os.makedirs(os.path.dirname(EVALUATE_FILE), exist_ok=True)
        payload = {"data": self.results}
        with open(EVALUATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=4)
        return payload

if __name__ == "__main__":
    css_path = sys.argv[1] if len(sys.argv) > 1 else "/home/labDirectory/css/styles.css"
    grader = Grader(css_path)
    result = grader.run_tests()
    print(json.dumps(result, indent=2))