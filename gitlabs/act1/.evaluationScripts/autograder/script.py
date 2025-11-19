# pip install GitPython

import git
import json
import tarfile
import os

overall = {
    "data":[
        {
            "testid": "1",
            "status": "failure",
            "score": 0,
            "maximum marks": 11,
            "message": ""
        }
    ],
    "status": "success"
}

# Write initial json
with open('../evaluate.json', 'w') as f:
    json.dump(overall, f, indent=4)

my_tar = tarfile.open('/home/labDirectory/working_directory.tar.gz')
my_tar.extractall("./")
my_tar.close()
os.system('clear')

# Try opening repo
try:
    repo = git.Repo("./working_directory/")
except:
    overall['data'][0]["score"] = 0
    overall['data'][0]["message"] = "Could Not Find project folder"
    overall['data'][0]["status"] = "failure"
    overall["status"] = "success"   # top-level success but testcase failed
    print(json.dumps(overall, indent=4))

    with open('../evaluate.json', 'w') as f:
        json.dump(overall, f, indent=4)

    os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")
    exit()

branchResult = 0
commitResult = 0

try:
    # ----- Checking branches -----
    heads = repo.heads
    for head in heads:
        if head.name == 'master':
            branchResult += 1

    if branchResult == 0:
        overall['data'][0]["score"] = 0
        overall['data'][0]["message"] = "The \"master\" branch does not seem to exist."
        overall['data'][0]["status"] = "failure"
        print(json.dumps(overall, indent=4))
        with open('../evaluate.json', 'w') as f:
            json.dump(overall, f, indent=4)
        os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")
        exit()

    if len(heads) == 1:
        branchResult += 1
    else:
        overall['data'][0]["score"] = branchResult
        overall['data'][0]["message"] = "There seems to be more than one branch."
        overall['data'][0]["status"] = "failure"
        print(json.dumps(overall, indent=4))
        with open('../evaluate.json', 'w') as f:
            json.dump(overall, f, indent=4)
        os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")
        exit()

    # ----- Checking commits -----
    commits = list(repo.iter_commits("master"))

    if len(commits) != 3:
        overall['data'][0]["score"] = branchResult
        overall['data'][0]["message"] = "There should be exactly 3 commits."
        overall['data'][0]["status"] = "failure"
        print(json.dumps(overall, indent=4))
        with open('../evaluate.json', 'w') as f:
            json.dump(overall, f, indent=4)
        os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")
        exit()

    # Message checks
    if commits[2].message.strip().lower() == "added readme.txt":
        commitResult += 1
    else:
        overall['data'][0]["score"] = branchResult + commitResult
        overall['data'][0]["message"] = "First commit message wrong."
        overall['data'][0]["status"] = "failure"
        print(json.dumps(overall, indent=4))
        with open('../evaluate.json', 'w') as f:
            json.dump(overall, f, indent=4)
        os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")
        exit()

    if commits[1].message.strip().lower() == "added add.h":
        commitResult += 1
    else:
        overall['data'][0]["score"] = branchResult + commitResult
        overall['data'][0]["message"] = "Second commit message wrong."
        overall['data'][0]["status"] = "failure"
        print(json.dumps(overall, indent=4))
        with open('../evaluate.json', 'w') as f:
            json.dump(overall, f, indent=4)
        os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")
        exit()

    if commits[0].message.strip().lower() == "added main.cpp":
        commitResult += 1
    else:
        overall['data'][0]["score"] = branchResult + commitResult
        overall['data'][0]["message"] = "Third commit message wrong."
        overall['data'][0]["status"] = "failure"
        print(json.dumps(overall, indent=4))
        with open('../evaluate.json', 'w') as f:
            json.dump(overall, f, indent=4)
        os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")
        exit()

    # ----- Checking file trees -----
    msg = ""

    for i in range(3):
        tree = commits[i].tree

        if len(tree.trees) > 0:
            msg += f"There is a subdirectory in commit {3-i}."
        else:
            file_list = [entry.name for entry in tree]

            if i == 2: 
                if len(tree.blobs) != 1 or tree.blobs[0].name != 'README.txt':
                    msg += f"Files incorrect in commit {3-i}."
                else:
                    msg += f"Commit {3-i} is as expected."
                    commitResult += 2

            elif i == 1:
                if len(tree.blobs) != 2 or ('README.txt' not in file_list) or ('add.h' not in file_list):
                    msg += f"Files incorrect in commit {3-i}."
                else:
                    msg += f"Commit {3-i} is as expected."
                    commitResult += 2

            else:  # commit 1
                if len(tree.blobs) != 3 or not all(f in file_list for f in ['README.txt', 'add.h', 'main.cpp']):
                    msg += f"Files incorrect in commit {3-i}."
                else:
                    msg += f"Commit {3-i} is as expected."
                    commitResult += 2

    # ---- FINAL SUCCESS ----
    overall['data'][0]["score"] = branchResult + commitResult
    overall['data'][0]["message"] = msg
    overall['data'][0]["status"] = "success" 
    overall["status"] = "success"         

    print(json.dumps(overall, indent=4))

    with open('../evaluate.json', 'w') as f:
        json.dump(overall, f, indent=4)

except Exception as e:
    print("Some error occurred", e)
    exit()

os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")
