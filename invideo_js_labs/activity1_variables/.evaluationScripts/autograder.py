import subprocess
import json
import os

# Configuration
SUBMISSION_FILE = "/home/.evaluationScripts/student_submission/script.js"
EVALUATE_FILE   = "/home/.evaluationScripts/evaluate.json"

def run_js_and_check(js_code):
checker_code = """
    const { JSDOM } = require("jsdom");
    const dom = new JSDOM("<!DOCTYPE html><div id='output'></div>");
    global.document = dom.window.document;

    try {
        const result = {
            nameDefined: (typeof personName !== "undefined"),
            ageDefined: (typeof age !== "undefined"),
            isStudentDefined: (typeof isStudent !== "undefined"),
            nameCorrect: (typeof personName !== "undefined" && personName === "John"),
            ageCorrect: (typeof age !== "undefined" && age === 20),
            isStudentCorrect: (typeof isStudent !== "undefined" && isStudent === true)
        };
        console.log(JSON.stringify(result));
    } catch (e) {
        console.log(JSON.stringify({error: e.message}));
    }
    """


    completed = subprocess.run(
        ["node", "-e", js_code + "\n" + checker_code],
        capture_output=True, text=True
    )

    if completed.returncode != 0:
        return {"error": completed.stderr.strip()}

    try:
        return json.loads(completed.stdout.strip())
    except json.JSONDecodeError:
        return {"error": "Invalid output from Node.js"}

def main():
    if not os.path.exists(SUBMISSION_FILE):
        print(f"Submission file not found: {SUBMISSION_FILE}")
        return

    with open(SUBMISSION_FILE, "r") as f:
        student_js = f.read()

    result = run_js_and_check(student_js)

    tests = []
    if "error" in result:
        # one global error, mark all tests as failed
        for idx, desc in enumerate(["personName defined", "age defined", "isStudent defined",
                                    "personName correct", "age correct", "isStudent correct"], start=1):
            tests.append({
                "testid": idx,
                "status": "fail",
                "score": 0,
                "maximum marks": 1,
                "message": f"Test case {idx} failed: {result['error']}"
            })
    else:
        # Each check gets its own test case
        checks = [
            ("nameDefined", "personName variable is defined"),
            ("ageDefined", "age variable is defined"),
            ("isStudentDefined", "isStudent variable is defined"),
            ("nameCorrect", "personName variable has correct value"),
            ("ageCorrect", "age variable has correct value"),
            ("isStudentCorrect", "isStudent variable has correct value")
        ]

        for idx, (key, desc) in enumerate(checks, start=1):
            passed = result.get(key, False)
            tests.append({
                "testid": idx,
                "status": "success" if passed else "fail",
                "score": 1 if passed else 0,
                "maximum marks": 1,
                "message": f"Test case {idx} {'passed' if passed else 'failed'}: {desc}"
            })

    # Dump results to evaluate.json
    os.makedirs(os.path.dirname(EVALUATE_FILE), exist_ok=True)
    with open(EVALUATE_FILE, "w") as out:
        json.dump({"data": tests}, out, indent=4)

if __name__ == "__main__":
    main()
