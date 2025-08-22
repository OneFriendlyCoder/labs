#!/usr/bin/env python3
import subprocess
import re
import json
import time
import math
from pathlib import Path

SOLUTIONS_PATH = Path('/home/labDirectory/submissions.txt')
EVAL_PATH = Path('/home/.evaluationScripts/evaluate.json')

def parse_solutions_file(filename):
    command = None
    if not Path(filename).exists():
        return None
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            if re.match(r'^(?:/.*?/)?ping\b', s):
                command = s
                break
    return command

def extract_flag_value(command, flag):
    if not command:
        return None
    m = re.search(r'(^|\s)-' + re.escape(flag) + r'\s*([0-9]+(?:\.[0-9]+)?)\b', command)
    return m.group(2) if m else None

def fail(details):
    return False, "Test case failed", details

def run_behavioral_check(command):
    details = {}
    if not command:
        return fail(details)

    count_str = extract_flag_value(command, 'c')
    interval_str = extract_flag_value(command, 'i')

    if not count_str or not interval_str:
        return fail(details)

    try:
        count = int(float(count_str))
        interval = float(interval_str)
    except Exception:
        return fail(details)

    if count != 5 or abs(interval - 2.0) > 1e-6:
        return fail(details)

    expected_total = (count - 1) * interval
    timeout_sec = int(math.ceil(expected_total + 10))

    start = time.time()
    try:
        proc = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout_sec)
    except Exception:
        return fail(details)
    end = time.time()
    elapsed = end - start
    details['elapsed_seconds'] = round(elapsed, 3)

    output = (proc.stdout or "") + (proc.stderr or "")

    m = re.search(r'(\d+)\s+packets transmitted,\s+(\d+)\s+received,\s+([0-9]+)%\s+packet loss', output)
    if m:
        transmitted = int(m.group(1))
        received = int(m.group(2))
        packet_loss = int(m.group(3))
    else:
        m2 = re.search(r'(\d+)\s+transmitted,\s+(\d+)\s+received', output)
        if not m2:
            details['ping_output'] = output.strip()[:2000]
            return fail(details)
        transmitted = int(m2.group(1))
        received = int(m2.group(2))
        packet_loss = 0 if transmitted == received else int(round((1 - received/transmitted) * 100))

    details.update({
        'transmitted': transmitted,
        'received': received,
        'packet_loss_percent': packet_loss
    })

    if transmitted != count or received != count or packet_loss != 0:
        return fail(details)

    min_allowed = expected_total * 0.6 if expected_total > 0 else 0
    max_allowed = expected_total + 8.0
    details['expected_total_seconds'] = expected_total
    details['min_allowed_seconds'] = round(min_allowed, 3)
    details['max_allowed_seconds'] = round(max_allowed, 3)

    if elapsed + 0.001 < min_allowed:
        return fail(details)
    if elapsed - 0.001 > max_allowed:
        return fail(details)

    return True, "Test case passed", details

def main():
    command = parse_solutions_file(str(SOLUTIONS_PATH))
    test_result = {
        "testid": 1,
        "status": "fail",
        "score": 0,
        "maximum marks": 1,
        "message": "Test case failed",
        "details": {}
    }

    passed, message, details = run_behavioral_check(command)
    test_result['message'] = message
    test_result['details'] = details
    if passed:
        test_result['status'] = 'success'
        test_result['score'] = 1

    EVAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(EVAL_PATH, 'w', encoding='utf-8') as f:
        json.dump({"data": [test_result]}, f, indent=4)

if __name__ == "__main__":
    main()
