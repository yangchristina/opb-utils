from github import Github
import shutil
import json
from dotenv import load_dotenv
import os
load_dotenv()

TEXTBOOK_PATH = os.environ.get("TEXTBOOK_PATH")
WRITE_PATH = os.environ.get("WRITE_PATH")
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")

textbook_chapter_to_name = {
    '1': 'ch_intro_to_data',
    '2': 'ch_summarizing_data',
    # TODO: add more chapters
}

def str_to_filename(string: str):
    return ''.join(e for e in string if e.isalnum() or e == '_')

def get_file_url(chapter: str, filename: str):
    if not filename.endswith('.tex'):
        filename += '.tex'
    return f"{TEXTBOOK_PATH}/{textbook_chapter_to_name[chapter]}/TeX/{filename}"

def read_file(path):
    with open(path, 'r') as f:
        return f.readlines()
    
def read_inputs(chapter: str):
    path = get_file_url(chapter, textbook_chapter_to_name[chapter])
    lines = read_file(path)
    inputs = []
    for i in lines:
        i = i.strip()
        if i.startswith("{\input{"):
            inputs.append(i.split('/')[-1][:-6])
    return inputs

def count_exercises(chapter: str, section: str):
    count = 0
    path = get_file_url(chapter, section)
    lines = read_file(path)
    for i in lines:
        i = i.strip()
        if i.startswith("\eoce{\qt{"):
            count += 1
    return count

def closing_bracket_index(str_list, opening_bracket_index = 0):
    stack = []
    for i, string in enumerate(str_list):
        for j, c in enumerate(string):
            if i == 0 and j < opening_bracket_index:
                continue
            if c == '{':
                stack.append(i)
            elif c == '}':
                stack.pop()
            if len(stack) == 0:
                return (i, j)
    return (-1, -1)

def remove_unmatched_closing(string: str):
    stack = []
    for i, c in enumerate(string):
        if c == '{':
            stack.append(i)
        elif c == '}':
            if len(stack) == 0:
                return string[:i]
            stack.pop()
    return string

def remove_starting_tag(string: str):
    if not string.startswith('\\'):
        return string.strip()
    stack = []
    string = string.index('{')
    for i, c in enumerate(string):
        if c == '{':
            stack.append(i)
        elif c == '}':
            stack.pop()
        if len(stack) == 0:
            return string[i+1:]
    raise Exception('Does not have ending tag')


def handle_exercise(exercise):
    pass

def guess_question_type(question: str):
    question = question.strip().lower()
    numeric_phrases = ['how many', 'what percent']
    for ph in numeric_phrases:
        if ph in question:
            return 'number-input'
    if 'which group' in question:
        return 'multiple-choice'
    return 'unknown'

def handle_parts(lines, starting_index):
    start = -1
    index = starting_index
    while index < len(lines):
        line = lines[index]
        if '\\begin{parts}' in line:
            start = index
        if start != -1 and '\\end{parts}' in line:
            end = index
            break
        index += 1
    items = ' '.join(lines[start+1:end]).split('\\item')

    parts = []
    for x in items:
        if x.strip() == '':
            continue
        question = x.replace('\\\\','\n').strip()
        parts.append({
            'question': question,
            'type': guess_question_type(question)
        })
    return parts


def get_exercises(chapter: str, section: str, questions):
    path = get_file_url(chapter, section)
    lines = [x.strip() for x in read_file(path)]
    print(path)
    print(questions)
    exercises = []
    cur_question = 0
    for i, line in enumerate(lines):
        if cur_question >= len(questions):
            break
        question = questions[cur_question]
        line = line.strip()
        if line.startswith("% ") and lines[i + 2].strip().startswith('\eoce{\qt{'):
            if int(line.split(' ')[-1]) != question:
                continue
            else:
                #region title
                title_end_index = i + 1
                closing_line = -1
                while closing_line == -1:
                    title_end_index += 1
                    (closing_line, closing_line_index) = closing_bracket_index(lines[i+2:title_end_index+1], 9)
                closing_line += i+2
                title_lines = lines[i+2:closing_line+1]
                if len(title_lines) == 1:
                    title_lines[0] = title_lines[0][10:closing_line_index]
                else:
                    title_lines[0] = title_lines[0][10:]
                    title_lines[-1] = title_lines[-1][:closing_line_index]
                title = ' '.join(title_lines)
                #endregion

                #region description
                target = '\\begin'
                description_end_index = closing_line
                started = False
                while True:
                    cur_line = lines[description_end_index]
                    if description_end_index == closing_line:
                        cur_line = cur_line[closing_line_index+1:]
                    if target in cur_line:
                        break
                    if cur_line.strip() == '':
                        if started:
                            break
                    else:
                        started = True
                    description_end_index += 1
                # Look for closing bracket without opening
                description_lines = [x.strip() for x in lines[closing_line:description_end_index+1]]
                description_lines[0] = description_lines[0][closing_line_index+1:]
                description_lines[-1] = description_lines[-1].split(target)[0]
                description = ' '.join(description_lines).strip()
                description = remove_unmatched_closing(description)
                #endregion

                #region parts
                parts = handle_parts(lines, description_end_index)
                #endregion

                exercises.append({
                    "title": title,
                    "description": description,
                    "parts": parts,
                    "path": f"q{str(question).zfill(2)}_{section}.md"
                })
                cur_question += 1

    # print(json.dumps(exercises, indent=4))
    # print(len(exercises))
    return exercises

def read_chapter(chapter: str, sections):
    all_sections = read_inputs(chapter)
    exercise_counts = [count_exercises(chapter, cur_section) for cur_section in all_sections]
    summed_counts = [sum(exercise_counts[:i]) for i in range(len(exercise_counts))]
    
    results = []
    print(all_sections)
    for (section, questions) in sections.items():
        questions.sort()
        section_index = all_sections.index(section)
        # file_questions = [q - summed_counts[section_index] for q in questions]
        
        results += get_exercises(chapter, section, questions)

    print(json.dumps(results, indent=4))


def write_file(path, lines):
    with open(path, 'a') as f:
        f.writelines([line + '\n' for line in lines])

def write_md(new_file_name, assets, exercises):
    path = f'{WRITE_PATH}/{new_file_name}.md'
    shutil.copyfile('q11_multi-part.md', path)
    asset_lines = ["assets:"]
    for a in assets:
        asset_lines.append(f"- {a}")
    
    lines_to_write = [
        "server:\nimports: |\n\t  import random\n\t  import pandas as pd\n\t  import problem_bank_helpers as pbh",
        "  generate: |\n\t  data2 = pbh.create_data2()\n\t  data.update(data2)",
        "  prepare: |        pass\n  parse: |\n        pass\n  grade: |\n        pass"
    ]
    question_part_lines = []
    for (i, e) in enumerate(exercises):
        question_lines = [
            f'part{i+1}:',
            f'  type: {e["type"]}',
            '  pl-customizations:',
        ]
        question_part_lines += question_lines
    
    end_lines = ['---']
    write_file(path, asset_lines + lines_to_write + question_part_lines + end_lines)

# Public Web Github
g = Github(login_or_token=GITHUB_ACCESS_TOKEN)

# Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", auth=auth)

repo = g.get_repo("open-resources/instructor_stats_bank")

issues = repo.get_issues(state="open", assignee=GITHUB_USERNAME)
print(issues.totalCount)

sections_by_chapter = {}
for item in issues:
    print(item.title)
    chapter = item.title.split(' ')[0].split('.')[0]
    split = item.title.split(' ')
    section_name = '_'.join(split[1:-1]).lower()
    section_name = str_to_filename(section_name)
    question = int(split[-1][1:].split('.')[-1])
    if chapter not in sections_by_chapter:
        sections_by_chapter[chapter] = {}
    if section_name not in sections_by_chapter[chapter]:
        sections_by_chapter[chapter][section_name] = []
    sections_by_chapter[chapter][section_name].append(question)
print(sections_by_chapter)
for (chapter, sections) in sections_by_chapter.items():
    read_chapter(chapter, sections)
