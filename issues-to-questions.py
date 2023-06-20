import random
from github import Github
import shutil
import json
import os
from table import latex_table_to_md, find_all_figures
import pandoc
from pdf2image import convert_from_path
from utils import replace_file_line
import tempfile
import re
from dotenv import load_dotenv
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
def str_to_filename(string: str, delimiter='_'):
    return ''.join(e for e in string.lower().replace(' ', delimiter).replace(".", delimiter) if e.isalnum() or e == delimiter)

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
        # print("INDEX:", string[index:])
        end_bracket_index = find_end_tag(string[index:])
        # print("BEFORE:", string)
        string = string[:index] + string[index+end_bracket_index+1:]
        # print("AFTER:", string)
    return string

def unwrap_tags(string: str):
    while '\\' in string:
        index = string.index('\\')
        end_bracket_index = find_end_tag(string[index:])
        tag_area = string[index:index+end_bracket_index+1]
        wrapped_text = tag_area.split('{')[1].split('}')[0]
        string = string[:index] + wrapped_text + string[index+end_bracket_index+1:]
    return string

def unwrap_unsupported_tags(stringV: str):
    string = stringV.replace("\\\\", "\n").replace("``", '"').replace("''", '"')
    supported_tags = ['\\textit{', '\\$']
    unsupported_remove_entirely_tags = ['\\footfullcite', '\noindent']
    # unsupported, \footfullcite + \noindent
    result = ''
    while '\\' in string:
        index = string.index('\\')
        matching_tags = [tag for tag in supported_tags if string[index:].startswith(tag)]
        if len(matching_tags) > 0:
            end_tag_index = find_end_tag(string[index:])+index if matching_tags[0].endswith("{") else index + len(matching_tags[0])-1
            result += string[:index]
            result += f'${string[index:end_tag_index+1]}$'
            string = string[end_tag_index+1:]
            continue
        if '{' not in string[index+1:].split(' ')[0].split('}')[0]:
            end_bracket_index = index + len(string[index+1:].split(' ')[0])
            string = string[:index] + string[end_bracket_index+1:]
            continue
        end_bracket_index = find_end_tag(string[index:]) + index
        tag_area = string[index:end_bracket_index+1]
        wrapped_text = ''
        if not any([tag_area.startswith(tag) for tag in unsupported_remove_entirely_tags]):
            wrapped_text = tag_area.split('{')[1].split('}')[0]

        string = string[:index] + wrapped_text + string[end_bracket_index+1:]
    return result + string

def write_file(path, lines, mode='a'):
    lines = '\n'.join(lines).split('\n')
    while lines[-1].strip() == '':
        lines.pop()
    with open(path, mode) as f:
        f.writelines([line.rstrip()+ '\n' for line in lines])
# endregion


def latex_to_markdown(latex_lines: list):
    # write_file('latex.tex', latex_lines)
    doc = pandoc.read(file='latex.tex')
    md = pandoc.write(doc, format='markdown')
    pandoc.write(doc, file='md.md')
    return md
    # pandoc.write('markdown', format='markdown')
    # write_file('latex.tex', latex)
    # doc = pandoc.Document()
    # doc.latex = latex
    # webConverted = doc.markdown

# region latex helpers

# use unwrap_unsupported_tags instead
# def handle_latex_tags_in_text(paragraph: str, key: str):
#     paragraph = paragraph.replace('\\\\', '\n')
#     supported_tags = ['\\textit']
#     tags = []

#     chunks = paragraph.split('\\')
#     res = ''
#     for i, chunk in enumerate(chunks):
#         is_supported = False
#         for supported_tag in supported_tags:
#             # ex. /textit{hello}, Bob
#             if chunk.startswith(supported_tag):
#                 chunks[i] = chunk[len(supported_tag):]
#                 tags.append(supported_tag)
#                 is_supported = True
#                 break
#         if not is_supported:
#             remove_tags

def string_is_numeric(s: str):
    return s.lstrip("-").replace('.','',1).isdigit()

def numbers_to_latex_equations(paragraph: str, key: str):
    numbers = []
    # TODO: handle negative numbers

    words = paragraph.split(' ')
    for i, word in enumerate(words):
        if len(word) == 0:
            continue
        possible_prefixes = ['(', '[', '{', "\\$"]
        possible_suffixes = ['.', ',', '?', '!', ':', ';', ')', ']', '}']
        prefix = ''
        suffix = ''

        for pre in possible_prefixes:
            if word.startswith(pre):
                word = word[len(pre):]
                prefix = pre
                break
        for suf in possible_suffixes:
            if word.endswith(suf):
                word = word[:-len(suf)]
                suffix = suf
                break
        word = word.replace(',', '')  # ex. 1,000,000

        if string_is_numeric(word):
            numbers.append(float(word))
            words[i] = f'{prefix}${{{{ params.{key}.num{len(numbers)} }}}}${suffix}'
    return ' '.join(words), numbers
# i = re.sub(r"\d+", r"[\g<0>]", i)
# endregion

def generate_random_choices(num_choices: int):
    choices = [{"value": f"'{i}'", "correct": False, "feedback": '"This is a random number, you probably selected this choice by mistake! Try again please!"'} for i in range(num_choices)]
    # TODO: add actual choices
    correct = random.randint(0, num_choices-1)
    choices[correct]["correct"] = True
    choices[correct]["feedback"] = '"Correct!"'
    return choices

# region read textbook
def guess_question_type(question: str):
    question = question.strip().lower()
    numeric_phrases = ['what percent', 'calculate']
    integer_phrases = ['how many']
    multiple_choice_phrases = ['what is', 'which group', 'identify', 'each variable', 'what are']
    long_text_phrases = ['describe', 'explain', 'why', 'comment on']
    drop_down_phrases = ['determine which of']

    for ph in long_text_phrases:
        if ph in question:
            return {'type': 'longtext'}
    for ph in drop_down_phrases:
        if ph in question:
            return {'type': 'dropdown', 'choices': generate_random_choices(4)}
    for ph in numeric_phrases:
        if ph in question:
            return {'type': 'number-input'}
    for ph in integer_phrases:
        if ph in question:
            return {'type': 'number-input', 'sigfigs': 'integer'}
    for ph in multiple_choice_phrases:
        if ph in question:
            choices = [{"value": f"'{i}'", "correct": False, "feedback": '"This is a random number, you probably selected this choice by mistake! Try again please!"'} for i in range(4)]
            # TODO: add actual choices
            correct = random.randint(0, 3)
            choices[correct]["correct"] = True
            choices[correct]["feedback"] = '"Correct!"'
            return {'type': 'multiple-choice', 'choices': generate_random_choices(4)}
    return {'type': 'unknown'}

def handle_parts(lines, starting_index, title: str):
    start = -1
    index = starting_index
    number_variables = {}
    while index < len(lines):
        line = lines[index]
        if '\\begin{parts}' in line:
            start = index
        if ('\\end{parts}' in line or '}{}' in line or '%' in line):
            if start == -1:
                break
            end = index
            break
        index += 1

    parts = []
    items = []
    if start == -1:
        sentences = [sentence for sentence in title.split('.') if sentence.strip() != '']
        split_index = -1
        # for i, sent in enumerate(sentences.reverse()):
        #     if '?' in sent:
        #         split_index = len(sentences) - i
        #         break
        # if split_index == -1:
        # info = guess_question_type(title)
        items = [sentences[-1]]
        # else:
        #     return [{
        #         'question': numbers_to_latex_equations('.'.join(sentences[split_index-1:])),
        #     }]
    else:
        items = ' '.join(lines[start+1:end]).split('\\item')

    for x in items:
        if x.strip() == '':
            continue
        question = x.replace('\\\\','\n').strip()
        info = guess_question_type(question)
        if info['type'] == 'unknown':
            info = guess_question_type(title)
        
        num_key = f'part{len(parts)+1}'
        extracted_question, question_numbers = numbers_to_latex_equations(unwrap_unsupported_tags(question), num_key)
        parts.append({
            'question': extracted_question,
            'info': info,
        })
        number_variables[num_key] = question_numbers
    return parts, number_variables


def format_description(description: str, non_text_lines: list):
    non_text = '\n\n' + '\n'.join(non_text_lines) if len(non_text_lines) > 0 else ''
    extracted_question, question_numbers = numbers_to_latex_equations(unwrap_unsupported_tags(description), 'description')
    text = extracted_question + non_text
    return text, question_numbers

def get_exercises(chapter: str, section: str, questions):
    path = get_file_url(chapter, section)
    lines = [x.strip() for x in read_file(path)]
    # print(path)
    # print(questions)
    exercises = []
    cur_question = 0
    for i, line in enumerate(lines):
        if cur_question >= len(questions):
            break
        question = questions[cur_question]['question_number']
        line = line.strip()
        if line.startswith("% ") and lines[i + 2].strip().startswith('\eoce{\qt{'):
            if int(line.split(' ')[-1]) != question:
                continue
            else:
                print()
                print(f'Question {question}, num: {int(line.split(" ")[-1])}, line: {i}')
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
                # print("CUR DESCRIPTION")
                # print(description)
                # print("END CUR DESCRIPTION", lines[description_end_index], lines[description_end_index+1])
                non_text_description_lines = []
                # print(f'i: {i}, Question: {question}')
                table = latex_table_to_md(lines, description_end_index+1, phrases_signalling_end=['\\begin{parts}', '}{}', '%'])
                figures = find_all_figures(lines, description_end_index+1, phrases_signalling_end=['\\begin{parts}', '%'])
                if table is not None:
                    non_text_description_lines.append(table)

                description, question_numbers = format_description(description, non_text_description_lines)
                #endregion

                #region parts
                parts, number_variables = handle_parts(lines, description_end_index, description)
                number_variables['description'] = question_numbers
                #endregion
                if len(parts) == 1:
                    description = '.'.join([sentence for sentence in description.split('.') if sentence.strip() != ''][:-1]) + '.'

                filename = str_to_filename(questions[cur_question]['issue_title'], '_')
                exercises.append({
                    "title": title,
                    "description": description,
                    "parts": parts,
                    "chapter": chapter,
                    "path": f"{filename}.md",
                    "assets": figures,
                    "issue": questions[cur_question]['issue_title'],
                    "variables": number_variables,
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
    # print(all_sections)
    for (section, questions) in sections.items():
        # question_numbers = [x['questions'] for x in questions]
        questions.sort(key=lambda x: x['question_number'])
        section_index = all_sections.index(section)
        # file_questions = [q - summed_counts[section_index] for q in questions]
        results += get_exercises(chapter, section, questions)

    for exercise in results:
        write_md(exercise)
    # print(json.dumps(results, indent=4))
# endregion read textbook

def md_part_lines(part, i):
    q_type = part['info']['type']
    answer_section = ''
    if q_type == 'number-input':
        answer_section ='Please enter in a numeric value.\n'
    elif q_type == 'multiple-choice' or q_type == 'dropdown':
        choices = part['info']['choices']
        answer_section = '\n'.join([f'- {{{{ params.part{i+1}.ans{j+1}.value }}}}' for j in range(len(choices))])
    # answer_section2 = '### pl-answer-panel\n\nEverything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.\nPlease remove this section if it is not application for this question.'
    # if part['type'] == 'multiple-choice':

    return [
        f'## Part {i+1}', '', 
        part['question'], '', 
        '### Answer Section\n',
        answer_section, '', 
        # answer_section2, 
        '']


def apply_indent(lines, indent):
    return [indent + x for x in lines]

def format_type_info(info: dict):
    indent = '  '
    info_type = info['type']
    list = [f'type: {info["type"]}']
    if info_type == 'longtext':
        list.append('gradingMethod: Manual')
    if info_type == 'number-input' and 'sigfigs' in info and info['sigfigs'] == 'integer':
        list.append('label: $d=$')
    return apply_indent(list, indent)

def get_pl_customizations(info: dict = {}, index: int = 0):
    type = info['type']
    pl_indent = '    '
    ans = []
    if type == 'multiple-choice':
        ans = ['weight: 1']
    elif type == 'number-input':
        # TODO: need to know if integer or not
        if 'sigfigs' in info and info['sigfigs'] == 'integer':
            ans = ['weight: 1', 'allow-blank: true'] #'label: $d= $', 
        else:
            ans = ['rtol: 0.05', 'weight: 1', 'allow-blank: true', 'label: $d= $', 'suffix: m']
        # ans = ['weight: 1', 'allow-blank: true'] # for integer
    elif type == 'dropdown':
        ans = ['weight: 1', 'blank: true']
    elif type == 'checkbox':
        ans = ['weight: 1', 'partial-credit: true', 'partial-credit-method: EDC']
    elif type == 'symbolic-input':
        ans = ['label: $F_r = $', 'variables: "m, v, r"', 'weight: 1', 'allow-blank: false']
    elif type == 'longtext':
        ans = ['placeholder: "Type your answer here..."', f'file-name: "answer{index+1}.html"', 'quill-theme: "snow"', 'directory: clientFilesQuestion', 'source-file-name: sample.html']
    return ['  pl-customizations:'] + apply_indent(lines=ans, indent=pl_indent)


def write_code(exercise: dict):
    indent = '        '
    lines = ["data2 = pbh.create_data2()", "",]

    variables = exercise['variables']
    # Randomize Variables
    v = random.randint(2,7)
    t = random.randint(5,10)
    used_by = {}
    for (key, values) in variables.items():
        for (i, num) in enumerate(values):
            # check if num has been used previously
            cur_var_name = f"{key}_num{i+1}"
            used = used_by[num] if (num in used_by) else ''
            if not used:
                used_by[num] = cur_var_name
            line = f"{cur_var_name} = {num}" if not used else f"{key}_num{i+1} = {used}"
            lines.append(line)
    lines.append('')
    for (key, values) in variables.items():
        for (i, num) in enumerate(values):
            lines.append(f"data2['params']['{key}']['num{i+1}'] = {key}_num{i+1}")
    lines.append('')

    for part_num, part in enumerate(exercise['parts']):
        if part['info']['type'] == 'multiple-choice' or part['info']['type'] == 'dropdown':
            lines.append(f"# Part {part_num+1} is a {part['info']['type']} question.")
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
    dir_path = WRITE_PATH + '/' + ''.join(exercise['path'].split('.')[:-1])
    path = dir_path + '/' + exercise['path'] 
    if not os.path.exists('questions'):
        os.mkdir('questions')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    shutil.copyfile('q11_multi-part.md', path)
    replace_file_line(path, 1, f"title: {exercise['title']}")

    # TODO: write expression
    lines_to_write = []
    asset_lines = ["assets:"]
    asset_to_filename = {}
    for a in exercise['assets']:
        figure_dir_path = f"{TEXTBOOK_PATH}/{textbook_chapter_to_name[chapter]}/figures/{a}"
        figure_name = os.listdir(figure_dir_path)[0]
        figure_no_extension_name, ext = figure_name.split('.')
        if ext == 'pdf':
            images = None
            with tempfile.TemporaryDirectory() as tmp_path:
                images = convert_from_path(f'{figure_dir_path}/{figure_name}', output_folder=tmp_path, use_cropbox=True)
                figure_name = f'{figure_no_extension_name}.jpg'
                if len(images) > 0:
                    images[0].save(f'{dir_path}/{figure_name}', 'JPEG')
        asset_to_filename[a] = figure_name
        asset_lines.append(f"- {figure_name}")
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
        question_lines = [f'part{i+1}:'] + format_type_info(e['info']) + get_pl_customizations(e['info'], i)
        question_part_lines += question_lines
    lines_to_write += question_part_lines
    lines_to_write += ['---', '# {{ params.vars.title }}', '', exercise['description'], '']
    
    # TODO: ADD ASSETS HERE, how should assets be formatted?, since parts assets + main assets
    for a in exercise['assets']:
        filename = asset_to_filename[a]
        img = f'<img src="{filename}" width=400>'
        lines_to_write.append(img)
    if len(exercise['assets']) > 0:
        lines_to_write.append('')

    has_long_text = False
    for i, part in enumerate(exercise['parts']):
        lines_to_write += md_part_lines(part, i=i)
        if part['info']['type'] == 'longtext':
            has_long_text = True
    print("WRITING TO", path)
    write_file(path, lines_to_write)
    # print(''.join(exercise['path'].split('.')[:-1]))
    if has_long_text:
        shutil.copyfile('sample.html', f'{dir_path}/sample.html')
    # write_file('question-paths.txt', [path])
# endregion

if __name__ == "__main__":
    print('hi')
    # latex_to_markdown('')
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
        sections_by_chapter[chapter][section_name].append({"question_number": question, 'issue_title': item.title})
    # print(sections_by_chapter)
    for (chapter, sections) in sections_by_chapter.items():
        read_chapter(chapter, sections)
    # NOT IN CORRECT ORDER from .items
