#! /bin/bash

INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
LAB_DIRECTORY="/home/labDirectory"
STUDENT_SUBMISSION="$INSTRUCTOR_SCRIPTS/student_submission"

ptcd=$(pwd)

cd "$INSTRUCTOR_SCRIPTS"
rm -rf "$STUDENT_SUBMISSION"
mkdir -p "$STUDENT_SUBMISSION"
cp -r "$LAB_DIRECTORY"/* "$STUDENT_SUBMISSION/"
chmod -R 777 "$STUDENT_SUBMISSION"
python3 "$INSTRUCTOR_SCRIPTS/autograder.py"
cd "$ptcd"
