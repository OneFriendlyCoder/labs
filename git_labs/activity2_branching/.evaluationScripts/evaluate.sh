#! /bin/bash

# For Testing
INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
LAB_DIRECTORY="/home/labDirectory"


cd $INSTRUCTOR_SCRIPTS

cp -r $LAB_DIRECTORY/big_repo.tar.gz autograder/

cd ./autograder/

chmod -R 777 big_repo.tar.gz

./grader.sh

rm -r big_repo.tar.gz