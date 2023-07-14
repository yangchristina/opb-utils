#!/bin/bash

PL_QUESTION_PATH=/Users/christinayang/Documents/GitHub/OPB/pl-opb-ind100/questions/FM
CHECKQ=/Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank/scripts/checkq.py
WRITE_PATH=/Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank/source/unsorted

# opb-utils/questions/q03_data_basics/q03_data_basics.md
# git clone https://github.com/open-resources/instructor_physics_bank.git

# TODO: Change this to file you would like to commit
BRANCH_NAME=1_3_sampling_principles_and_strategies_q1_13
# ISSUE_NUMBER=7

# ex. BRANCH_NAME=1_1_case_study_using_stents_to_prevent_strokes_q1_1
FILE=questions/$BRANCH_NAME/$BRANCH_NAME.md

array[0]="sophivar"
array[1]="SamuelStreet"
array[2]="IRIDIXVdt"
array[3]="camirr"
array[4]="alebuiles"

size=${#array[@]}
index=$(($RANDOM % $size))
REVIEWER=${array[$index]}
echo "REVIEWER: $REVIEWER"

cd /Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank
echo "HII"
echo $FILE
git reset --hard origin/main
echo $FILE
out="$(basename $FILE .md)"
AUTO_BRANCH_NAME="auto_$(basename $FILE .md)"
git checkout -B $AUTO_BRANCH_NAME
INFO_PATH=/Users/christinayang/Documents/GitHub/OPB/opb-utils/info/$out
ASSIGN=$(cat $INFO_PATH/assign.txt)
ISSUE_NUMBER=$(cat $INFO_PATH/issue_number.txt)
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
gh pr edit $AUTO_BRANCH_NAME --add-label "check_syntax" #--add-reviewer $REVIEWER
gh pr reopen $AUTO_BRANCH_NAME
gh pr ready $AUTO_BRANCH_NAME
