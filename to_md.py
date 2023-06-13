from github import Github
import shutil
import json
from dotenv import load_dotenv
import os
from utils import replace_file_line

load_dotenv()

TEXTBOOK_PATH = os.environ.get("TEXTBOOK_PATH")
WRITE_PATH = os.environ.get("WRITE_PATH")
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")

def write_file(path, lines):
    with open(path, 'a') as f:
        f.writelines([line + '\n' for line in lines])

def write_question_md(exercise):
    path = WRITE_PATH + '/' + exercise['path']
    shutil.copyfile('q11_multi-part.md', path)
    replace_file_line(path, 1, f"title: {exercise['title']}")

    lines_to_write = []
    asset_lines = ["assets:"]
    for a in exercise['assets']:
        asset_lines.append(f"- {a}")
    lines_to_write += asset_lines
    
    lines_to_write += [
        "server:\n  imports: |\n        import random\n        import pandas as pd\n        import problem_bank_helpers as pbh",
        "  generate: |\n        data2 = pbh.create_data2()\n        data.update(data2)",
        "  prepare: |\n        pass\n  parse: |\n        pass\n  grade: |\n        pass"
    ]
    question_part_lines = []
    for (i, e) in enumerate(exercise['parts']):
        question_lines = [
            f'part{i+1}:',
            f'  type: {e["type"]}',
            '  pl-customizations:',
        ]
        question_part_lines += question_lines
    lines_to_write += question_part_lines
    lines_to_write += ['---', '# {{ params.vars.title }}', '', exercise['description'], '']
    
    # TODO: ADD ASSETS HERE, how should assets be formatted?, since parts assets + main assets
    for a in exercise['assets']:
        img = f'<img src="{a}" width=400>'
        lines_to_write.append(img)
    if len(exercise['assets']) > 0:
        lines_to_write.append('')

    for i, part in enumerate(exercise['parts']):
        answer_section = '### Answer Section\n\nPlease enter in a numeric value in {{ params.vars.units }}.\n\n### pl-submission-panel\n\nEverything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.\nPlease remove this section if it is not application for this question.'
        answer_section2 = '### pl-answer-panel\n\nEverything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.\nPlease remove this section if it is not application for this question.'
        part_lines = [f'## Part{i+1}', '']
        part_lines.append(part['question']) 
        part_lines.append('')
        # TODO: ADD ASSETS HERE
        part_lines.append(answer_section)
        part_lines.append('')
        part_lines.append(answer_section2)
        part_lines.append('')
        lines_to_write += part_lines

    write_file(path, lines_to_write)
