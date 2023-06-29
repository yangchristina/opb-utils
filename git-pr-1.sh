#!/bin/bash
/Users/christinayang/miniconda3/bin/python /Users/christinayang/Documents/GitHub/OPB/opb-utils/issues-to-questions.py

PL_QUESTION_PATH=/Users/christinayang/Documents/GitHub/OPB/pl-opb-ind100/questions/FM
CHECKQ=/Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank/scripts/checkq.py
WRITE_PATH=/Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank/source/unsorted

# opb-utils/questions/q03_data_basics/q03_data_basics.md
# git clone https://github.com/open-resources/instructor_physics_bank.git

# TODO: Change this to file you would like to commit
BRANCH_NAME=1_1_case_study_using_stents_to_prevent_strokes_q1_1
ISSUE_NUMBER=12
# ex. BRANCH_NAME=1_1_case_study_using_stents_to_prevent_strokes_q1_1
FILE=questions/$BRANCH_NAME/$BRANCH_NAME.md

cd /Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank
echo "HII"
echo $FILE
# git pull origin main
# git merge origin main
git reset --hard origin/main
# python $CHECKQ $FILE --output_root $PL_QUESTION_PATH
echo $FILE
out="$(basename $FILE .md)"
# git checkout master
# git pull origin master
git checkout -B $out
git pull origin $out
git merge $out
# git switch $out
# rm -R /Users/christinayang/Documents/GitHub/OPB/opb-utils/questions/$out/*
cp -R /Users/christinayang/Documents/GitHub/OPB/opb-utils/questions/$out $WRITE_PATH
# mv -f /Users/christinayang/Documents/GitHub/OPB/opb-utils/questions/$out $WRITE_PATH
echo "ADDING $WRITE_PATH/$out"
ls
git add $WRITE_PATH/$out
git commit -m "ready for review"
# "First draft of $out"
# git push
git push -f -u origin $out
echo "PUSHED $FILE SUCCESSFULLY"


hub pull-request -m "This resolves #$ISSUE_NUMBER"
# cd /Users/christinayang/Documents/GitHub/OPB/opb-utils
# break
