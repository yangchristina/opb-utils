#!/bin/bash
# /Users/christinayang/miniconda3/bin/python /Users/christinayang/Documents/GitHub/OPB/opb-utils/issues-to-questions.py

PL_QUESTION_PATH=/Users/christinayang/Documents/GitHub/OPB/pl-opb-ind100/questions/FM
CHECKQ=/Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank/scripts/checkq.py
WRITE_PATH=/Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank/source/unsorted

LINK=https://ca.prairielearn.com/pl/course_instance/4024/instructor/course_admin/questions

# opb-utils/questions/q03_data_basics/q03_data_basics.md
# git clone https://github.com/open-resources/instructor_physics_bank.git
for FILE in questions/*/*.md;
do
    echo $FILE
    cd /Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank
    echo $FILE
    # git pull origin main
    # git merge origin main
    git reset --hard origin/main
    # python $CHECKQ $FILE --output_root $PL_QUESTION_PATH
    echo $FILE
    out="$(basename $FILE .md)"
    BRANCH_NAME="auto_$(basename $FILE .md)"
    INFO_PATH=/Users/christinayang/Documents/GitHub/OPB/opb-utils/info/$out
    ASSIGN=$(cat $INFO_PATH/assign.txt)
    ISSUE_NUMBER=$(cat $INFO_PATH/issue_number.txt)
    TITLE=$(cat $INFO_PATH/title.txt)
    echo $ASSIGN
    echo $ISSUE_NUMBER
    echo $BRANCH_NAME
    # git checkout master
    # git pull origin master
    git checkout -B $BRANCH_NAME
    # git pull origin $out
    # git merge $out
    # rm -R /Users/christinayang/Documents/GitHub/OPB/opb-utils/questions/$out/*
    cp -R /Users/christinayang/Documents/GitHub/OPB/opb-utils/questions/$out $WRITE_PATH
    echo "ADDING $WRITE_PATH/$out"
    git add $WRITE_PATH/$out
    git commit -m "Autogenerated template"
    git push --force-with-lease -u origin $BRANCH_NAME
    echo "PUSHED $FILE SUCCESSFULLY"
    gh pr comment $BRANCH_NAME --body "OPB 000: $LINK, Title: $TITLE"
    # if [ -z "$ASSIGN" ]
    # then
    #     hub pull-request -d -m "$BRANCH_NAME" -m "This resolves #$ISSUE_NUMBER"
    #     echo "\$var is empty"
    # else
    #     echo "\$var is NOT empty"
    #     hub pull-request -d -m "$BRANCH_NAME" -m "This resolves #$ISSUE_NUMBER" --assign $ASSIGN
    # fi
    sleep 2
done
