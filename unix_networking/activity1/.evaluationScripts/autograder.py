import subprocess
import json
import time
import os
import re
import math
from pathlib import Path

SUBMISSION_FILE = "/home/labDirectory/submissions.txt"
EVALUATE_FILE   = "/home/.evaluationScripts/evaluate.json"

correct_cmds = [
    ["ss -t", "ss -t state established"],
    ["ss -t -n"],
    ["ss -u"],
    ["ss -u -n"],
    ["ss -t -l", "ss -t state listen"],
    ["ss -u -l", "ss -u state listen"],
]

def run_command(cmd):
    try:
        parts = cmd.strip().split()
        return subprocess.check_output(parts, stderr=subprocess.STDOUT, text=True).strip()
    except subprocess.CalledProcessError as e:
        return e.output.strip()
    except Exception as exc:
        return f"ERROR: {exc}"

def parse_ping_command(filename):
    ping_command = None
    if not Path(filename).exists():
        return None
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            if re.match(r'^\s*ping\b', s):
                ping_command = s
                break
    return ping_command

def run_behavioral_check(command):
    details = {}
    if not command:
        return False, "Test case failed: no ping command found", details

    def extract_flag_value(cmd, flag):
        m = re.search(r'(^|\s)-' + re.escape(flag) + r'\s*([0-9]+(?:\.[0-9]+)?)\b', cmd)
        return m.group(2) if m else None

    count_str = extract_flag_value(command, 'c')
    interval_str = extract_flag_value(command, 'i')

    if not count_str or not interval_str:
        return False, "Test case failed: ping command must use '-c' and '-i' flags", details

    try:
        count = int(float(count_str))
        interval = float(interval_str)
    except Exception:
        return False, "Test case failed: invalid '-c' or '-i' values", details

    if count != 5 or abs(interval - 2.0) > 1e-6:
        return False, "Test case failed: '-c' must be 5 and '-i' must be 2.0", details

    expected_total = (count - 1) * interval
    timeout_sec = int(math.ceil(expected_total + 10))

    start = time.time()
    try:
        # run the student's command exactly as written
        proc = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout_sec)
    except Exception as e:
        details['exception_type'] = type(e).__name__
        details['exception_message'] = str(e)
        return False, "Test case failed: exception during ping execution", details
    end = time.time()
    elapsed = end - start
    details['elapsed_seconds'] = round(elapsed, 3)

    output = (proc.stdout or "") + (proc.stderr or "")

    # match both common ping formats
    m = re.search(r'(\d+)\s+packets transmitted,\s+(\d+)\s+received,\s+([0-9]+)%\s+packet loss', output)
    if m:
        transmitted = int(m.group(1))
        received = int(m.group(2))
        packet_loss = int(m.group(3))
    else:
        m2 = re.search(r'(\d+)\s+transmitted,\s+(\d+)\s+received', output)
        if not m2:
            details['ping_output'] = output.strip()[:2000]
            return False, "Test case failed: could not parse ping output", details
        transmitted = int(m2.group(1))
        received = int(m2.group(2))
        packet_loss = 0 if transmitted == received else int(round((1 - received/transmitted) * 100))

    details.update({
        'transmitted': transmitted,
        'received': received,
        'packet_loss_percent': packet_loss
    })
    if transmitted != count or received != count or packet_loss != 0:
        return False, f"Test case failed: expected {count} packets, got {received}", details

    min_allowed = expected_total * 0.6 if expected_total > 0 else 0
    max_allowed = expected_total + 8.0
    details['expected_total_seconds'] = expected_total
    details['min_allowed_seconds'] = round(min_allowed, 3)
    details['max_allowed_seconds'] = round(max_allowed, 3)

    if elapsed + 0.001 < min_allowed:
        return False, "Test case failed: ping finished too quickly", details
    if elapsed - 0.001 > max_allowed:
        return False, "Test case failed: ping ran too long", details

    return True, "Test case passed", details


def main():
    if not os.path.exists(SUBMISSION_FILE):
        print(f"Submission file not found: {SUBMISSION_FILE}")
        return
    with open(SUBMISSION_FILE, 'r', encoding='utf-8') as f:
        student_cmds = [line.strip() for line in f if line.strip()]
    results = []
    for idx, expected_variants in enumerate(correct_cmds, start=1):
        if idx <= len(student_cmds):
            student_cmd = student_cmds[idx-1]
            student_out = run_command(student_cmd)
            canonical_outputs = []
            for c in expected_variants:
                canonical_outputs.append({
                    "cmd": c,
                    "out": run_command(c)
                })
            matched_index = None
            for i, co in enumerate(canonical_outputs):
                if student_out == co["out"]:
                    matched_index = i
                    break
            passed = (matched_index is not None)
            result = {
                "testid": idx,
                "status": "success" if passed else "fail",
                "score": 1 if passed else 0,
                "maximum marks": 1,
                "message": f"Test case {idx} {'passed' if passed else 'failed'}"
            }
            if passed:
                result["details"] = {
                    "student_command": student_cmd,
                    "matched_canonical_command": canonical_outputs[matched_index]["cmd"]
                }
            else:
                result["details"] = {
                    "student_command": student_cmd,
                    "student_output_preview": (student_out or "")[:2000],
                    "canonical_candidates": [
                        {"cmd": co["cmd"], "output_preview": (co["out"] or "")[:2000]}
                        for co in canonical_outputs
                    ]
                }
            results.append(result)
        else:
            results.append({
                "testid": idx,
                "status": "fail",
                "score": 0,
                "maximum marks": 1,
                "message": f"Test case {idx} failed: no submission provided"
            })
    ping_submission = parse_ping_command(SUBMISSION_FILE)
    passed_ping, message_ping, details_ping = run_behavioral_check(ping_submission)
    results.append({
        "testid": 7,
        "status": "success" if passed_ping else "fail",
        "score": 1 if passed_ping else 0,
        "maximum marks": 1,
        "message": message_ping,
        "details": details_ping
    })
    os.makedirs(os.path.dirname(EVALUATE_FILE), exist_ok=True)
    with open(EVALUATE_FILE, 'w', encoding='utf-8') as out:
        json.dump({"data": results}, out, indent=4)

if __name__ == "__main__":
    main()
