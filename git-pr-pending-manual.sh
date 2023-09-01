#!/bin/bash

PL_QUESTION_PATH=/Users/christinayang/Documents/GitHub/OPB/pl-opb-ind100/questions/FM
WRITE_PATH=/Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank/source/unsorted

# array[0]="sophivar"
# array[1]="alebuiles"
# array[2]="IRIDIXVdt"
array[0]="camirr"
array[1]="SamuelStreet"

size=${#array[@]}
LINK=https://ca.prairielearn.com/pl/course_instance/4024/instructor/course_admin/questions

DIR=w-pending
for FILE in $DIR/*/*.md;
do
    echo $FILE
    cd /Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank
    echo $FILE
    git reset --hard origin/main
    echo $FILE
    out="$(basename $FILE .md)"
    BRANCH_NAME="$(basename $FILE .md)"
    INFO_PATH=/Users/christinayang/Documents/GitHub/OPB/opb-utils/info/$out
    ASSIGN=$(cat $INFO_PATH/assign.txt)
    ISSUE_NUMBER=$(cat $INFO_PATH/issue_number.txt)
    TITLE=$(cat $INFO_PATH/title.txt)
    index=$(($RANDOM % $size))
    echo $ASSIGN
    echo $TITLE
    echo $ISSUE_NUMBER
    echo $BRANCH_NAME
    git checkout main
    git pull origin main
    git checkout -B $BRANCH_NAME
    git pull origin $BRANCH_NAME
    cp -R /Users/christinayang/Documents/GitHub/OPB/opb-utils/$DIR/$out $WRITE_PATH
    echo "ADDING $WRITE_PATH/$out"
    git add $WRITE_PATH/$out
    git commit -m "user_code to student"
    git push -u origin $BRANCH_NAME
    echo "PUSHED $FILE SUCCESSFULLY"

    # hub pull-request -m "$BRANCH_NAME" -m "This resolves #$ISSUE_NUMBER
    # OPB 000: $LINK, Title: $TITLE" --assign $ASSIGN
    # # gh pr reopen $BRANCH_NAME
    # gh pr edit $BRANCH_NAME --add-label "check_syntax" # --add-reviewer $REVIEWER
    # # gh pr ready $BRANCH_NAME
    sleep 60
done
