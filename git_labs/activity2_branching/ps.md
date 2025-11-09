Please go through the README in labDirectory folder before attempting this activity. It describes how to setup the directory and submit your work.


Navigate to the scripts/ directory and run :- bash reset.sh.


***PLEASE USE RESET.SH CAREFULLY, IT CAN RESET YOUR WHOLE WORK WITH NO WAY OF RECOVERING IF IT HASNT BEEN COMMITTED***


Now navigate to working_directory/big_repo/. All the git commands have to be run inside this directory.


The repository big_repo has a commit history with a single branch master. Each commit adds a new file with a function implemented in it. However, sometimes, in a commit some previously uploaded files are incorrectly modified. Your job is to identify the "last" commit where each of the files bfs.cpp, binary_search.cpp, dfs.cpp, matrixmul.cpp and sieve.cpp were functioning correctly.


(You dont need to test out the functions to check their correctness, assume that when the function was first added it was working correctly. 

If and when it is modified in any later commit, assume that causes the function to work incorrectly.

If any function is only added, and never modified, assume that it works correctly even in the last commit. 

To check the changes that were done from one commit to another, try the git diff command.

The main.cpp file is modified at each commit but assume that it works correctly at each of them).


After identification of the commits for each of these files, navigate to each of these commits and create a new branch from the commit with the name correct_<function_name>. In this branch, (remember to checkout to the branch first) delete all files except the file that contains the last version of the correct function, add the changes and commit them with the message :- Saved <file_name> (without quotes).


Finally, you should have 6 branches :- 


master

correct_bfs

correct_binary_search

correct_dfs

correct_matrixmul

correct_sieve


Each of these branches (except master) should have exactly one commit not in the master branch with the corresponding message :- 


correct_bfs -> Saved bfs.cpp 

correct_binary_search -> Saved binary_search.cpp

correct_dfs -> Saved dfs.cpp

correct_matrixmul -> Saved matrixmul.cpp

correct_sieve -> Saved sieve.cpp


The latest commit in each of these would have exactly one file :- 


correct_bfs -> bfs.cpp 

correct_binary_search -> binary_search.cpp

correct_dfs -> dfs.cpp

correct_matrixmul -> matrixmul.cpp

correct_sieve -> sieve.cpp


Each of these branches has to be created at the right commit which you have to find out. You can manually check the files for changes (which can be tedious) or you can use the git diff command (figure out how one can use this)

Finally, submit this modified repo with the new branches.


To create solution file, navigate to the scripts/ directory and run:- bash submit.sh
