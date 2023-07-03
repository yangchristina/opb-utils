import os
from utils import get_between_strings, get_between_tag

from dotenv import load_dotenv
load_dotenv()
# question What is the variance of the mean of these $n$ values: $\frac{X_1 + X_2 + \dots + X_n}{n}$?
TEXTBOOK_PATH = os.environ.get("TEXTBOOK_PATH")
# WRITE_PATH = os.environ.get("WRITE_PATH")
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
WRITE_PATH = './questions'

def find_solutions(chapter_title: str, questions: list):
    path = f"{TEXTBOOK_PATH}/extraTeX/eoceSolutions/eoceSolutions.tex"
    # print("SOLUTIONS", chapter_title)
    # print(questions)
    res = {}
    # questions.sort()
    with open(path) as reader:
        file = reader.read()
        file = get_between_strings(file, f'\\eocesolch{{{chapter_title}}}', [f'\\eocesolch', '%_______________'])
    for question in questions:
        question_num = question['question_number']
        # print(chapter_title, "QUESTION NUM", question_num)
        question = get_between_strings(file, f'% {question_num}\n\n', [f'\n% ', '%_______________'])
        question = get_between_tag(question, '\\eocesol{').strip()
        res[question_num] = question

    return res
