#!/usr/bin/env python3
import os
import json
import copy
import hashlib
import sys

finaldata = {"data": []}
dataSkel = {
    "testid": 1,
    "status": "fail",
    "score": 0,
    "maximum marks": 1,
    "message": "Autograder Failed!"
}

STUDENT_DIR = "/home/labDirectory"
REFERENCE_FILE = "/tmp/system_update"
OUTPUT_FILE = "/home/.evaluationScripts/evaluate.json"

def find_downloads_dir(base_dir):
    """Return the path to a directory whose name lower() == 'downloads', or None."""
    try:
        for name in os.listdir(base_dir):
            path = os.path.join(base_dir, name)
            if os.path.isdir(path) and name.lower() == "downloads":
                return path
    except FileNotFoundError:
        return None
    return None

def file_sha256_hex(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(4096), b""):
            h.update(block)
    return h.hexdigest()

def run_checks():
    # Find downloads dir
    downloads_dir = find_downloads_dir(STUDENT_DIR)
    if not downloads_dir:
        dataSkel_local = copy.deepcopy(dataSkel)
        dataSkel_local.update({
            "status": "fail",
            "score": 0,
            "message": "No 'downloads' directory (case-insensitive) found in /home/labDirectory."
        })
        finaldata["data"].append(dataSkel_local)
        return

    # Check student file exists
    student_file = os.path.join(downloads_dir, "system_update")
    if not os.path.isfile(student_file):
        dataSkel_local = copy.deepcopy(dataSkel)
        dataSkel_local.update({
            "status": "fail",
            "score": 0,
            "message": f"'system_update' file not found inside {downloads_dir}."
        })
        finaldata["data"].append(dataSkel_local)
        return

    # Check reference file exists
    if not os.path.isfile(REFERENCE_FILE):
        dataSkel_local = copy.deepcopy(dataSkel)
        dataSkel_local.update({
            "status": "fail",
            "score": 0,
            "message": f"Reference file missing on autograder: {REFERENCE_FILE}"
        })
        finaldata["data"].append(dataSkel_local)
        return

    # Hash and compare
    try:
        student_hash = file_sha256_hex(student_file)
        reference_hash = file_sha256_hex(REFERENCE_FILE)
    except Exception as e:
        dataSkel_local = copy.deepcopy(dataSkel)
        dataSkel_local.update({
            "status": "fail",
            "score": 0,
            "message": f"Error hashing files: {str(e)}"
        })
        finaldata["data"].append(dataSkel_local)
        return

    if student_hash != reference_hash:
        dataSkel_local = copy.deepcopy(dataSkel)
        dataSkel_local.update({
            "status": "fail",
            "score": 0,
            "message": "Downloaded 'system_update' does not match the reference (checksum mismatch)."
        })
        finaldata["data"].append(dataSkel_local)
        return

    dataSkel_local = copy.deepcopy(dataSkel)
    dataSkel_local.update({
        "status": "success",
        "score": 1,
        "message": "Test case 1 passed"
    })
    finaldata["data"].append(dataSkel_local)

def main():
    run_checks()
    try:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
            json.dump(finaldata, fh, indent=4)
    except Exception as e:
        print("Failed to write evaluate.json:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
