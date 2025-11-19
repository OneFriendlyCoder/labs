import os
import json
import tarfile
import git

# Output format
overall = {
    "data": [
        {
            "testid": "Git Workflow Simulation",
            "status": "success",
            "score": 0,
            "maximum marks": 25,
            "message": "",
        }
    ]
}

# Extract student repo
try:
    with tarfile.open("/home/labDirectory/merge_repo.tar.gz") as tar:
        tar.extractall("./")
except Exception as e:
    overall["data"][0]["status"] = "failure"
    overall["data"][0]["message"] = f"Failed to extract repo: {e}"
    print(json.dumps(overall, indent=4))
    exit(1)

repo_path = "./merge_repo"
if not os.path.exists(repo_path):
    overall["data"][0]["status"] = "failure"
    overall["data"][0]["message"] = "merge_repo directory not found after extraction"
    print(json.dumps(overall, indent=4))
    exit(1)

try:
    repo = git.Repo(repo_path)
except Exception:
    overall["data"][0]["status"] = "failure"
    overall["data"][0]["message"] = "Could not open Git repo"
    print(json.dumps(overall, indent=4))
    exit(1)

score = 0
msg = []

# ---- TEST 1: Commit History (Structure) ----
# CHANGE 1: Use "master" instead of "main"
commits = list(repo.iter_commits("master"))
commit_msgs = [c.message.strip() for c in commits]

expected_msgs = [
    "RECOVERED: parser",  # From recover-parser branch
    "UPDATED: parser AND xml_handler AND README",
    "UPDATED: parser AND serializer",
    "first commit",
]

# Reversed due to Git log being newest -> oldest
commit_msgs.reverse()

if all(msg in commit_msgs for msg in expected_msgs):
    score += 5
    msg.append("Correct commit messages found.")
else:
    msg.append("Commit messages or sequence incorrect.")
    overall["data"][0]["status"] = "failure"


# ---- TEST 2: File Contents in Each Commit ----
def file_ends_with(commit, filename, line):
    try:
        blob = commit.tree / filename
        return blob.data_stream.read().decode("utf-8").strip().endswith(line)
    except:
        return False


# Look for commit that added "# parser updated"
for c in commits:
    if c.message.strip() == "UPDATED: parser AND serializer":
        if file_ends_with(c, "parser.py", "# parser updated") and file_ends_with(
            c, "serializer.py", "# serializer updated"
        ):
            score += 4
            msg.append("Correct updates in parser.py and serializer.py.")
        else:
            msg.append("parser.py or serializer.py not updated correctly.")
        break

# Check utils.py, xml_handler.py, README.md in next commit
for c in commits:
    if c.message.strip() == "UPDATED: parser AND xml_handler AND README":
        if (
            file_ends_with(c, "utils.py", "# utils updated")
            and file_ends_with(c, "xml_handler.py", "# xml handler updated")
            and file_ends_with(c, "README.md", "# readme updated")
        ):
            score += 4
            msg.append("Correct updates in utils.py, xml_handler.py, and README.md.")
        else:
            msg.append("One or more files in second update commit are incorrect.")
        break

# ---- TEST 3: Branch recover-parser and parser_recovered.py ----
if "recover-parser" in repo.branches:
    score += 2
    msg.append("recover-parser branch found.")
    # Checkout recover-parser to inspect
    repo.git.checkout("recover-parser")
    head_commit = repo.head.commit
    if "parser_recovered.py" in [b.name for b in head_commit.tree.blobs]:
        score += 3
        msg.append("parser_recovered.py exists in recover-parser branch.")
        if (
            file_ends_with(head_commit, "parser_recovered.py", "# parser updated")
            is False
        ):
            score += 2
            msg.append("parser_recovered.py was restored from original version.")
        else:
            msg.append(
                "parser_recovered.py has modified content. Should match original parser.py."
            )
    else:
        msg.append("parser_recovered.py not found.")
else:
    msg.append("recover-parser branch missing.")
    overall["data"][0]["status"] = "failure"

# ---- TEST 4: Back on main and parser.py is modified ----
# CHANGE 2: Use "master" instead of "main"
repo.git.checkout("master")
if file_ends_with(repo.head.commit, "parser.py", "# parser updated"):
    score += 2
    msg.append("master branch contains modified parser.py.")
else:
    msg.append("parser.py not in modified form on master branch.")

# ---- FINALIZE ----
overall["data"][0]["score"] = score
overall["data"][0]["message"] = "\n".join(msg)
if score < 15:
    overall["data"][0]["status"] = "failure"

print(json.dumps(overall, indent=4))
with open("../evaluate.json", "w") as f:
    json.dump(overall, f, indent=4)

# Cleanup
os.system("rm -rf ./merge_repo ./merge_repo.tar.gz")