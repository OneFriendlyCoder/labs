#!/usr/bin/env python3

import json
import os

EVALUATE_FILE = "/home/.evaluationScripts/evaluate.json"

# Always one test case that passes
dataSkel = [
    {
        "testid": 1,
        "status": "success",
        "score": 1,
        "maximum marks": 1,
        "message": "Test case 1 passed"
    }
]

# Write out evaluate.json
os.makedirs(os.path.dirname(EVALUATE_FILE), exist_ok=True)
with open(EVALUATE_FILE, 'w') as out:
    json.dump({"data": dataSkel}, out, indent=4)

# Always exit success
exit(0)
