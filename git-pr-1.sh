#!/bin/bash

PL_QUESTION_PATH=/Users/christinayang/Documents/GitHub/OPB/pl-opb-ind100/questions/FM
CHECKQ=/Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank/scripts/checkq.py
WRITE_PATH=/Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank/source/unsorted

# opb-utils/questions/q03_data_basics/q03_data_basics.md
# git clone https://github.com/open-resources/instructor_physics_bank.git

# TODO: Change this to file you would like to commit
BRANCH_NAME=1_2_data_basics_q1_7
ISSUE_NUMBER=3

# ex. BRANCH_NAME=1_1_case_study_using_stents_to_prevent_strokes_q1_1
FILE=questions/$BRANCH_NAME/$BRANCH_NAME.md

cd /Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank
echo "HII"
echo $FILE
git reset --hard origin/main
echo $FILE
out="$(basename $FILE .md)"
AUTO_BRANCH_NAME="auto_$(basename $FILE .md)"
git checkout -B $AUTO_BRANCH_NAME
# git pull origin $out
# git merge $out
# git merge main
cp -R /Users/christinayang/Documents/GitHub/OPB/opb-utils/questions/$out $WRITE_PATH
echo "ADDING $WRITE_PATH/$out"
git add $WRITE_PATH/$out
git commit -m "ready for review"
git push --force-with-lease origin $AUTO_BRANCH_NAME
echo "PUSHED $FILE SUCCESSFULLY"
# hub pull-request -m "$BRANCH_NAME" -m "This resolves #$ISSUE_NUMBER"
