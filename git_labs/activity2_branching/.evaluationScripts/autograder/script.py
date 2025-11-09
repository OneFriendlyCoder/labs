# pip install GitPython

import git
import json
import tarfile
import os

overall = {"data":[
	{
		"testid": "1",
		"status": "success",
		"score": 0,
		"maximum marks" : 25,
		"message": ""
	}
]
}

my_tar = tarfile.open('./big_repo.tar.gz')
my_tar.extractall("./")
my_tar.close()
os.system('clear')

try:
	repo = git.Repo("./big_repo/")
except:
	overall['data'][0]["score"] = 0
	overall['data'][0]["message"] = "Could not find project folder"
	overall['data'][0]["status"] = "failure"
	print(json.dumps(overall, indent=4))

	with open('../evaluate.json', 'w') as f:
		json.dump(overall,f,indent=4)
	os.system("rm -rf ./big_repo big_repo.tar.gz")      
	exit()

branchResult = 0

# Task that must be present in the assignment 
try:
	# Checking for branches
	msg=""
 
	branch_objects=[head.name for head in repo.heads]

	if len(branch_objects)!=6:
		overall['data'][0]["score"] = 0
		overall['data'][0]["message"] = "The number of branches in the repository seems incorrect. Only six branches, master, correct_dfs, correct_bfs, correct_binary_search, correct_matrixmul and correct_sieve must exist. Use git branch to see all branches."
		overall['data'][0]["status"] = "failure"
		print(json.dumps(overall, indent=4))

		with open('../evaluate.json', 'w') as f:
			json.dump(overall,f,indent=4)
		os.system("rm -rf ./big_repo big_repo.tar.gz")      
		exit()

	if 'master' not in branch_objects:
		overall['data'][0]["score"] = 0
		overall['data'][0]["message"] = "The \"master\" branch does not seem to exist here. Try git branch to see results."
		overall['data'][0]["status"] = "failure"
		print(json.dumps(overall, indent=4))

		with open('../evaluate.json', 'w') as f:
			json.dump(overall,f,indent=4)
		os.system("rm -rf ./big_repo big_repo.tar.gz")      
		exit()
	
	master_commit_list = list(repo.iter_commits("master"))
 
	hashes = ['3d510c3b236bb38b77d273d000f578712c955d76','ff203994750a1b799a7a1118962035039f786ecd','0c3be9740504e915ceb370a50eed9d8c81496d55','2a07d132e99dc4d397c0a8bd625c0435f33bc528'\
     		  '260451cfb0925260e77bd096af33c09655581f6e','5fcb6a5dac8cf43e752d97b3f41c18f752cde2ad','280327bc7455ac6fc8bc69559c835bab6c2a8ca6']
 
	if len(master_commit_list)!=7 or \
    	master_commit_list[0].hexsha!='3d510c3b236bb38b77d273d000f578712c955d76' or \
    	master_commit_list[1].hexsha!='ff203994750a1b799a7a1118962035039f786ecd' or \
    	master_commit_list[2].hexsha!='0c3be9740504e915ceb370a50eed9d8c81496d55' or \
    	master_commit_list[3].hexsha!='2a07d132e99dc4d397c0a8bd625c0435f33bc528' or \
		master_commit_list[4].hexsha!='260451cfb0925260e77bd096af33c09655581f6e' or \
		master_commit_list[5].hexsha!='5fcb6a5dac8cf43e752d97b3f41c18f752cde2ad' or \
		master_commit_list[6].hexsha!='280327bc7455ac6fc8bc69559c835bab6c2a8ca6' :
		overall['data'][0]["score"] = 0
		overall['data'][0]["status"] = 'failure'
		overall['data'][0]["message"] = "The master branch seems to have been modified in some way. Run the reset.sh script and try again."
		print(json.dumps(overall, indent=4))
		with open('../evaluate.json', 'w') as f:
			json.dump(overall,f,indent=4)
		os.system("rm -rf ./big_repo big_repo.tar.gz")
		exit()

	temp=0

	# correct_dfs
	if 'correct_dfs' not in branch_objects:
		msg+='"correct_dfs" branch does not exist. '
	else:
		commit_list = list(repo.iter_commits('correct_dfs'))
		temp+=1
		if len(commit_list)<2 or ((commit_list[1].hexsha!='2a07d132e99dc4d397c0a8bd625c0435f33bc528' or commit_list[0].hexsha in hashes) and commit_list[0].hexsha!='2a07d132e99dc4d397c0a8bd625c0435f33bc528'):
			msg+='"correct_dfs" branch not branched out at the right commit from master. Try git branch and git log for further information. '
		else:
			temp+=2
		if len(commit_list[0].tree.blobs)!=1 or len(commit_list[0].tree.trees)!=0 or commit_list[0].tree.blobs[0].name != 'dfs.cpp' or commit_list[0].message.strip("\n").strip(" ").lower()!='saved dfs.cpp':
			msg+=' "correct_dfs" branch HEAD does not have the correct directory structure or commit message. Try git checkout to see the directory. '
		else:
			temp+=2

		if temp==5:
			msg+=' "correct_dfs" branch done perfectly!'
	branchResult+=temp
	temp=0

	# correct_bfs
	if 'correct_bfs' not in branch_objects:
		msg+='"correct_bfs" branch does not exist. '
	else:
		commit_list = list(repo.iter_commits('correct_bfs'))
		temp+=1
		if len(commit_list)<2 or ((commit_list[1].hexsha!='0c3be9740504e915ceb370a50eed9d8c81496d55' or commit_list[0].hexsha in hashes) and commit_list[0].hexsha!='0c3be9740504e915ceb370a50eed9d8c81496d55'):
			msg+=' "correct_bfs" branch not branched out at the right commit from master commit. Try git branch and git log for further information. '
		else:
			temp+=2
		if len(commit_list[0].tree.blobs)!=1 or len(commit_list[0].tree.trees)!=0 or commit_list[0].tree.blobs[0].name != 'bfs.cpp' or commit_list[0].message.strip("\n").strip(" ").lower()!='saved bfs.cpp':
			msg+=' "correct_bfs" branch HEAD does not have the correct directory structure or commit message. Try git checkout to see the directory. '
		else:
			temp+=2
   
		if temp==5:
			msg+=' "correct_bfs" branch done perfectly!'
	branchResult+=temp
	temp=0
	
	# correct_binary_search
	if 'correct_binary_search' not in branch_objects:
		msg+='"correct_binary_search" branch does not exist. '
	else:
		commit_list = list(repo.iter_commits('correct_binary_search'))
		temp+=1
		if len(commit_list)<2 or ((commit_list[1].hexsha!='ff203994750a1b799a7a1118962035039f786ecd' or commit_list[0].hexsha in hashes) and commit_list[0].hexsha!='ff203994750a1b799a7a1118962035039f786ecd'):
			msg+=' "correct_binary_search" branch not branched out at the right commit from master. Try git branch and git log for further information. '
		else:
			temp+=2
		if len(commit_list[0].tree.blobs)!=1 or len(commit_list[0].tree.trees)!=0 or commit_list[0].tree.blobs[0].name != 'binary_search.cpp' or commit_list[0].message.strip("\n").strip(" ").lower()!='saved binary_search.cpp':
			msg+=' "correct_binary_search" branch HEAD does not have the correct directory structure or commit message. Try git checkout to see the directory. '
		else:
			temp+=2
   
		if temp==5:
			msg+=' "correct_binary_search" branch done perfectly!'
	branchResult+=temp
	temp=0

	# correct_matrixmul
	if 'correct_matrixmul' not in branch_objects:
		msg+='"correct_matrixmul" branch does not exist. '
	else:
		commit_list = list(repo.iter_commits('correct_matrixmul'))
		temp+=1
		if len(commit_list)<2 or ((commit_list[1].hexsha!='ff203994750a1b799a7a1118962035039f786ecd' or commit_list[0].hexsha in hashes) and commit_list[0].hexsha!='ff203994750a1b799a7a1118962035039f786ecd'):
			msg+=' "correct_matrixmul" branch not branched out at the right commit from master. Try git branch and git log for further information. '
		else:
			temp+=2
		if len(commit_list[0].tree.blobs)!=1 or len(commit_list[0].tree.trees)!=0 or commit_list[0].tree.blobs[0].name != 'matrixmul.cpp' or commit_list[0].message.strip("\n").strip(" ").lower()!='saved matrixmul.cpp':
			msg+=' "correct_matrixmul" branch HEAD does not have the correct directory structure or commit message. Try git checkout to see the directory. '
		else:
			temp+=2
   
		if temp==5:
			msg+=' "correct_matrixmul" branch done perfectly!'
	branchResult+=temp
	temp=0

	# correct_sieve
	if 'correct_sieve' not in branch_objects:
		msg+=' "correct_sieve " branch does not exist. '
	else:
		commit_list = list(repo.iter_commits('correct_sieve'))
		temp+=1
		if len(commit_list)<2 or ((commit_list[1].hexsha!='3d510c3b236bb38b77d273d000f578712c955d76' or commit_list[0].hexsha in hashes) and commit_list[0].hexsha!='3d510c3b236bb38b77d273d000f578712c955d76'):
			msg+=' "correct_sieve" branch not branched out at the right commit from master. Try git branch and git log for further information. '
		else:
			temp+=2
		if len(commit_list[0].tree.blobs)!=1 or len(commit_list[0].tree.trees)!=0 or commit_list[0].tree.blobs[0].name != 'sieve.cpp' or commit_list[0].message.strip("\n").strip(" ").lower()!='saved sieve.cpp':
			msg+=' "correct_sieve" branch HEAD does not have the correct directory structure or commit message. Try git checkout to see the directory. '
		else:
			temp+=2
   
		if temp==5:
			msg+=' "correct_sieve" branch done perfectly!'
	branchResult+=temp
	temp=0
	
	overall['data'][0]["score"] = branchResult
	overall['data'][0]["message"] = msg
	print(json.dumps(overall, indent=4))
	with open('../evaluate.json', 'w') as f:
		json.dump(overall,f,indent=4)
		
except Exception as e:
	print("Some error occurred", e)
	exit()

os.system("rm -rf ./big_repo big_repo.tar.gz")