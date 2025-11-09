# pip install GitPython

import git
import json
import tarfile
import os

overall = {"data":[
	{
		"testid": "1",
		"status": "failure",
		"score": 0,
		"maximum marks" : 11,
		"message": ""
	}
]
}

with open('../evaluate.json', 'w') as f:
	json.dump(overall,f,indent=4)

overall["status"] = "success"

my_tar = tarfile.open('./working_directory.tar.gz')
my_tar.extractall("./")
my_tar.close()
os.system('clear')

try:
	repo = git.Repo("./working_directory/")
except:
	overall['data'][0]["score"] = 0
	overall['data'][0]["message"] = "Could Not Find project folder"
	overall['data'][0]["status"] = "failure"
	print(json.dumps(overall, indent=4))

	with open('../evaluate.json', 'w') as f:
		json.dump(overall,f,indent=4)
	os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")      
	exit()

branchResult = 0
commitResult = 0

# Task that must be present in the assignment
try:    
	# Checking for branches
	heads = repo.heads 
	for head in heads:
		if(head.name=='master'):
			branchResult+=1

	if branchResult==0:
		overall['data'][0]["score"] = branchResult+commitResult
		overall['data'][0]["message"] = "The \"master\" branch does not seem to exist here. Try git branch to see results."
		overall['data'][0]["status"] = "failure"
		print(json.dumps(overall, indent=4))

		with open('../evaluate.json', 'w') as f:
			json.dump(overall,f,indent=4)
		os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")      
		exit()

	if len(heads)==1:
		branchResult+=1
	else:
		overall['data'][0]["score"] = branchResult+commitResult
		overall['data'][0]["message"] = "There seems to be more than one branch existing here. Try git branch to see results."
		overall['data'][0]["status"] = "failure"
		print(json.dumps(overall, indent=4))

		with open('../evaluate.json', 'w') as f:
			json.dump(overall,f,indent=4)
		os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")      
		exit()

	# Checking for commits
	commits = list(repo.iter_commits("master"))

	if len(commits)!=3:
		overall['data'][0]["score"] = branchResult+commitResult
		overall['data'][0]["message"] = "There should be exactly 3 commits in the repository. Try git log to see the commits."
		overall['data'][0]["status"] = "failure"
		print(json.dumps(overall, indent=4))  
		
		with open('../evaluate.json', 'w') as f:
			json.dump(overall,f,indent=4)
		os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")      
		exit()

	if commits[2].message.strip("\n").strip(" ").lower() == "added readme.txt":
		commitResult = commitResult + 1
	else:
		overall['data'][0]["score"] = branchResult+commitResult
		overall['data'][0]["message"] = "First commit doesn't have message as \"Added README.txt\". Try git log to see the commits."
		overall['data'][0]["status"] = "failure"
		print(json.dumps(overall, indent=4))  
		
		with open('../evaluate.json', 'w') as f:
			json.dump(overall,f,indent=4)
		os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")      
		exit()
	if commits[1].message.strip("\n").strip(" ").lower() == "added add.h":
		commitResult = commitResult + 1
	else: 
		overall['data'][0]["score"] = branchResult+commitResult
		overall['data'][0]["message"] = "Second commit doesn't have message as \"Added add.h\". Try git log to see the commits."
		overall['data'][0]["status"] = "failure"
		print(json.dumps(overall, indent=4))  
		
		with open('../evaluate.json', 'w') as f:
			json.dump(overall,f,indent=4)
		os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")      
		exit()
	if commits[0].message.strip("\n").strip(" ").lower() == "added main.cpp":
		commitResult = commitResult + 1
	else:
		overall['data'][0]["score"] = branchResult+commitResult
		overall['data'][0]["message"] = "Third commit doesn't have message as \"Added main.cpp\". Try git log to see the commits."
		overall['data'][0]["status"] = "failure"
		print(json.dumps(overall, indent=4))  
		
		with open('../evaluate.json', 'w') as f:
			json.dump(overall,f,indent=4)
		os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")      
		exit()
	
	msg = ""

	for i in range(3):
		tree=commits[i].tree
		if len(tree.trees)>0:
			msg += "There seems to be some subdirectory in commit "+str(3-i)+". Use checkout command to see the commit."
		else: 
			if(i==2):
				if(len(tree.blobs)!=1 or tree.blobs[0].name!='README.txt'):
					msg += "The files don't seem to be correct in commit "+str(3-i)+". Use checkout command to see the commit."
				else:
					msg += "Commit "+str(3-i)+" is as expected."
					commitResult+=2
			elif(i==1):
				
				file_list = [entry.name for entry in tree]
				if(len(tree.blobs)!=2 or ('README.txt' not in file_list) or ('add.h' not in file_list)):
					msg += "The files don't seem to be correct in commit "+str(3-i)+". Use checkout command to see the commit."
				else:
					msg += "Commit "+str(3-i)+" is as expected."
					commitResult+=2

			else:
				file_list = [entry.name for entry in tree]
				if(len(tree.blobs)!=3 or ('README.txt' not in file_list) or ('add.h' not in file_list) or ('main.cpp' not in file_list)):
					msg += "The files don't seem to be correct in commit "+str(3-i)+". Use checkout command to see the commit."
				else:
					msg += "Commit "+str(3-i)+" is as expected."
					commitResult+=2

	overall['data'][0]["score"] = branchResult+commitResult
	overall['data'][0]["message"] = msg
	print(json.dumps(overall, indent=4))
	with open('../evaluate.json', 'w') as f:
		json.dump(overall,f,indent=4)
		
except Exception as e:
	print("Some error occurred", e)
	exit()

os.system("rm -rf ./working_directory/ working_directory.tar.gz 2> /dev/null")
