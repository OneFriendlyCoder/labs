Please go through the README in labDirectory folder before attempting this activity. It describes how to setup the directory and submit your work.


Navigate to the scripts/ directory and run :- bash reset.sh.


***PLEASE USE RESET.SH CAREFULLY, IT CAN RESET YOUR WHOLE WORK WITH NO WAY OF RECOVERING IF IT HASNT BEEN COMMITTED***


Now navigate to merge_repo/. All the git commands have to be run inside this directory.


The repository merge_repo has a commit history with two branches master and development. 


The repo had an initial commit where 4 empty files were added :- file_1.cpp, file_2.cpp, file_3.cpp, file_4.cpp


At this commit the development branch was created, which modified these 4 files. In the meantime, these 4 files were also modified in the master branch. This can be seen in the commit history.


Now, we wish to merge these two branches.


Remember to merge the development branch into the master, and not the other way around.


However, since the files were modified differently, there are bound to be some merge conflicts.


Resolve the merge conflicts in the following manner :-


file_1.cpp Modify the file so that it becomes identical to the file in the master branch.


file_2.cpp Modify the file so that it becomes identical to the file in the development branch.


file_3.cpp Take all the changes in the files in both the branches.


file_4.cpp Replace the original file with two files :- file_4_master.cpp (that contains the file contents of the master branch) and file_4_development.cpp (that contains the file contents of the development branch).


The above is a basic idea of what is to be done, more specifics on the functionality of the merged file can be found in the README.


Though a basic functionality of the files is outlined in the README, you guys are encouraged to go through the code on a superficial level, and run the programs a few times to get acquainted with it.


*********A basic knowledge of the code will be needed for merging (especially file_3.cpp).*********


Rest assured you dont have to match the file content exactly. As long as the C++ code compiles and behaviour of the code is as expected on a few basic tests, you shall receive full marks for merging.


You may take as many commits as you need for merging, just make sure that the latest commit in the master branch contains the expected merged files. Be sure that the commit does not contain any executable or other files. Only 5 .cpp files should be present in the final commit in the master branch. You can add anything in the commit message.


Finally, submit this modified repo with the merged branches.


To create the solution file, navigate to the scripts/ directory and run:- bash submit.sh


Note: Edit the merge conflicts using nano/vim/vscode
