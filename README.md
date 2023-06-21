# opb-utils
 helpers for creating questions for opb stats

issues-to-questions.py: takes issues from github repo and turns them into questions in the (temporary) /questions directory
pl.sh: moves questions in /questions into prairelearn
git-pr.sh: pushes questions in /questions to github (different branch for each question)

To use: create .env file, and copy .env.example there, and fill in