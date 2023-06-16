#!/bin/bash
PL_QUESTION_PATH=/Users/christinayang/Documents/GitHub/OPB/pl-opb-ind100/questions/FM
CHECKQ=/Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank/scripts/checkq.py
WRITE_PATH=/Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank/source/unsorted

# opb-utils/questions/q03_data_basics/q03_data_basics.md
# git clone https://github.com/open-resources/instructor_physics_bank.git
for FILE in questions/*/*.md; 
do
    echo $FILE
    cd /Users/christinayang/Documents/GitHub/OPB/instructor_stats_bank
    echo "HII"
    echo $FILE
    git checkout main
    git reset --hard origin/main
    # python $CHECKQ $FILE --output_root $PL_QUESTION_PATH
    echo $FILE;
    out="$(basename $FILE .md)"
    git switch -c $out
    mv /Users/christinayang/Documents/GitHub/OPB/opb-utils/questions/$out $WRITE_PATH
    git add source/unsorted/$out
    # git commit -m "First draft of $out"
    # git push
    # do echo $FILE; 
    cd /Users/christinayang/Documents/GitHub/OPB/opb-utils
done
