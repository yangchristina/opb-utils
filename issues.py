import random
from github import Github
import shutil
import json
from dotenv import load_dotenv
import os
load_dotenv()

# region settings
TEXTBOOK_PATH = os.environ.get("TEXTBOOK_PATH")
WRITE_PATH = os.environ.get("WRITE_PATH")
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")

# TESTING PURPOSES, comment out when ready to actually write
WRITE_PATH = './questions'

textbook_chapter_to_name = {
    '1': 'ch_intro_to_data',
    '2': 'ch_summarizing_data',
    # TODO: add more chapters
}
# endregion

# region general helpers
def str_to_filename(string: str):
    return ''.join(e for e in string if e.isalnum() or e == '_')

def get_file_url(chapter: str, filename: str):
    if not filename.endswith('.tex'):
        filename += '.tex'
    return f"{TEXTBOOK_PATH}/{textbook_chapter_to_name[chapter]}/TeX/{filename}"

def read_file(path):
    with open(path, 'r') as f:
        return f.readlines()
    
def replace_file_line(file_name, line_num, text):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    lines[line_num] = text + '\n'
    with open(file_name, 'w') as f:
        f.writelines(lines)
    
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

def find_end_tag(string: str):
    stack = []
    is_started = False
    for i, c in enumerate(string):
        if c == '{':
            is_started = True
            stack.append(i)
        elif c == '}':
            stack.pop()
        if is_started and len(stack) == 0:
            return i
    raise Exception('Does not have ending tag')

def remove_tags(string: str):
    while '\\' in string:
        index = string.index('\\')
        print("INDEX:", string[index:])
        end_bracket_index = find_end_tag(string[index:])
        print("BEFORE:", string)
        string = string[:index] + string[index+end_bracket_index+1:]
        print("AFTER:", string)
    return string

def write_file(path, lines):
    with open(path, 'a') as f:
        f.writelines([line + '\n' for line in lines])
# endregion

# region read textbook
def guess_question_type(question: str):
    question = question.strip().lower()
    numeric_phrases = ['how many', 'what percent']
    multiple_choice_phrases = ['what is', 'which group']
    for ph in numeric_phrases:
        if ph in question:
            return {'type': 'number-input'}
    for ph in multiple_choice_phrases:
        if ph in question:
            choices = [{"value": f"'{i}'", "correct": False, "feedback": '"This is a random number, you probably selected this choice by mistake! Try again please!"'} for i in range(4)]
            # TODO: add actual choices
            correct = random.randint(0, 3)
            choices[correct]["correct"] = True
            choices[correct]["feedback"] = '"Correct!"'
            return {'type': 'multiple-choice', 'choices': choices}
            # data2["params"]["part1"]["ans1"]["value"] = pbh.roundp(42)
            # data2["params"]["part1"]["ans1"]["correct"] = False
            # data2["params"]["part1"]["ans1"]["feedback"] = "This is a random number, you probably selected this choice by mistake! Try again please!"
    return {'type': 'unknown'}

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
            'info': guess_question_type(question),
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
                title = remove_tags(title)
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
                    "path": f"q{str(question).zfill(2)}_{section}.md",
                    "assets": [],
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

    for exercise in results:
        write_md(exercise)
    print(json.dumps(results, indent=4))
# endregion read textbook

def md_part_lines(part, i):
    q_type = part['info']['type']
    answer_section = ''
    if q_type == 'number-input':
        answer_section ='Please enter in a numeric value.\n\n### pl-submission-panel\n\nEverything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.\nPlease remove this section if it is not application for this question.'
    elif q_type == 'multiple-choice':
        choices = part['info']['choices']
        answer_section = '\n'.join([f'- {{{{ params.part{i+1}.ans{j+1}.value }}}}' for j in range(len(choices))])
    answer_section2 = '### pl-answer-panel\n\nEverything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.\nPlease remove this section if it is not application for this question.'
    # if part['type'] == 'multiple-choice':

    return [
        f'## Part {i+1}', '', 
        part['question'], '', 
        '### Answer Section\n',
        answer_section, '', 
        answer_section2, '']


def apply_indent(lines, indent):
    return [indent + x for x in lines]

def get_pl_customizations(info: dict = {}):
    type = info['type']
    pl_indent = '    '
    ans = []
    if type == 'multiple-choice':
        ans = ['weight: 1']
    elif type == 'number-input':
        # TODO: need to know if integer or not
        if 'sigfigs' in info and info['sigfigs'] == 'integer':
            ans = ['label: $d= $', 'weight: 1', 'allow-blank: true']
        else:
            ans = ['rtol: 0.05', 'weight: 1', 'allow-blank: true', 'label: $d= $', 'suffix: m']
        # ans = ['weight: 1', 'allow-blank: true'] # for integer
    elif type == 'dropdown':
        ans = ['weight: 1', 'blank: true']
    elif type == 'checkbox':
        ans = ['weight: 1', 'partial-credit: true', 'partial-credit-method: EDC']
    elif type == 'symbolic-input':
        ans = ['label: $F_r = $', 'variables: "m, v, r"', 'weight: 1', 'allow-blank: false']
    return ['  pl-customizations:'] + apply_indent(lines=ans, indent=pl_indent)


def write_code(exercise: dict):
    indent = '        '
    lines = ["data2 = pbh.create_data2()", "",]
    for part_num, part in enumerate(exercise['parts']):
        if part['info']['type'] == 'multiple-choice':
            lines.append(f"# Part {part_num+1} is a multiple choice question.")
            for choice_num, choice in enumerate(part['info']['choices']):
                for (key, val) in choice.items():
                    lines += [f"data2['params']['part{part_num+1}']['ans{choice_num+1}']['{key}'] = {val}"]
                lines.append('')
            lines.append('')

    lines += ["# Update the data object with a new dict", "data.update(data2)"]
    return apply_indent(lines, indent)
        # data2["params"]["part1"]["ans1"]["value"] = pbh.roundp(42)
        # data2["params"]["part1"]["ans1"]["correct"] = False
        # data2["params"]["part1"]["ans1"]["feedback"] = "This is a random number, you probably selected this choice by mistake! Try again please!"

# region write_md
def write_md(exercise):
    path = WRITE_PATH + '/' + exercise['path']
    shutil.copyfile('q11_multi-part.md', path)
    replace_file_line(path, 1, f"title: {exercise['title']}")

    lines_to_write = []
    asset_lines = ["assets:"]
    for a in exercise['assets']:
        asset_lines.append(f"- {a}")
    lines_to_write += asset_lines
    lines_to_write.append("server:\n  imports: |\n        import random\n        import pandas as pd\n        import problem_bank_helpers as pbh")
    lines_to_write.append("  generate: |")
    lines_to_write += write_code(exercise)
    lines_to_write.append("  prepare: |\n        pass\n  parse: |\n        pass\n  grade: |\n        pass")
    # lines_to_write += [
    #     "        data2 = pbh.create_data2()\n        data.update(data2)",
    #     "  prepare: |\n        pass\n  parse: |\n        pass\n  grade: |\n        pass"
    # ]
    question_part_lines = []
    for (i, e) in enumerate(exercise['parts']):
        question_lines = [f'part{i+1}:', f'  type: {e["info"]["type"]}'] + get_pl_customizations(e['info'])
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
        lines_to_write += md_part_lines(part, i=i)

    write_file(path, lines_to_write)
# endregion


if __name__ == "__main__":
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
