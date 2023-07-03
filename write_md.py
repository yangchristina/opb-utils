import os
import shutil
from utils import replace_file_line, apply_indent, write_file, apply_params_to_str, string_is_numeric
import tempfile
from constants import textbook_chapter_to_name
from pdf2image import convert_from_path

from dotenv import load_dotenv
load_dotenv()
# question What is the variance of the mean of these $n$ values: $\frac{X_1 + X_2 + \dots + X_n}{n}$?
TEXTBOOK_PATH = os.environ.get("TEXTBOOK_PATH")
# WRITE_PATH = os.environ.get("WRITE_PATH")
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
WRITE_PATH = './questions'


def md_part_lines(part, i, params=None, solution=None):
    q_type = part['info']['type']
    answer_section = ''
    if q_type == 'number-input':
        answer_section ='Please enter in a numeric value in.\n'
    elif q_type == 'multiple-choice' or q_type == 'dropdown':
        choices = part['info']['choices']
        answer_section = '\n'.join([f'- {{{{ params.part{i+1}.ans{j+1}.value }}}}' for j in range(len(choices))])
    # answer_section2 = '### pl-answer-panel\n\nEverything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.\nPlease remove this section if it is not application for this question.'
    # if part['type'] == 'multiple-choice':

    result = [
        f'## Part {i+1}', '', 
        part['question'], '', 
    ]

    result += [
        '### Answer Section\n',
        answer_section, '', 
        # answer_section2, 
        ]
    
    if solution:
        if params:
            formated_soln = apply_params_to_str(solution, params)
            result += ['### pl-answer-panel', '', f'Part {i+1}: {formated_soln}', '']
        else:
            result += ['### pl-answer-panel', '', f'Part {i+1}: {solution}', '']
    
    return result + ['']


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
            ans = ['rtol: 0.05', 'weight: 1', 'allow-blank: true', 'label: $d= $']
        if 'suffix' in info:
            ans.append(f'suffix: {info["suffix"]}')
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



def format_type_info(info: dict):
    indent = '  '
    info_type = info['type']
    list = [f'type: {info["type"]}']
    if info_type == 'longtext':
        list.append('gradingMethod: Manual')
    if info_type == 'number-input' and 'sigfigs' in info and info['sigfigs'] == 'integer':
        list.append('label: $d=$')
    return apply_indent(list, indent)


def write_code(exercise: dict):
    indent = '        '
    lines = ["data2 = pbh.create_data2()", "",]

    num_variables = exercise['num_variables']
    variables = exercise['variables']
    # Randomize Variables
    # v = random.randint(2,7)
    # t = random.randint(5,10)

    # region Handle variables
    used_by = {}
    for (var_name, value) in variables.items():
        lines.append(f"{var_name} = {value}")
        used_by[value] = var_name
    lines.append('')
    for (var_name, value) in variables.items():
        values = var_name.split('_')
        cur_var_line = f"data2['params']"
        for val in values:
            cur_var_line += f"['{val}']"
        cur_var_line += f" = {var_name}"
        lines.append(cur_var_line)
    lines.append('')

    lines.append('# Randomize Variables')
    for (key, values) in num_variables.items():
        for (i, num) in enumerate(values):
            # check if num has been used previously
            cur_var_name = f"{key}_num{i+1}"
            used = used_by[num] if (num in used_by) else ''
            if not used:
                used_by[num] = cur_var_name
            line = f"{cur_var_name} = {num}" if not used else f"{key}_num{i+1} = {used}"
            lines.append(line)
        
    lines.append('')
    lines.append('# store the variables in the dictionary "params"')
    for (key, values) in num_variables.items():
        for (i, num) in enumerate(values):
            lines.append(f"data2['params']['{key}']['num{i+1}'] = {key}_num{i+1}")
    lines.append('')

    # endregion handle variables


    for part_num, part in enumerate(exercise['parts']):
        if part['info']['type'] == 'multiple-choice' or part['info']['type'] == 'dropdown':
            lines.append(f"# Part {part_num+1} is a {part['info']['type']} question.")
            for choice_num, choice in enumerate(part['info']['choices']):
                for (key, val) in choice.items():
                    lines += [f"data2['params']['part{part_num+1}']['ans{choice_num+1}']['{key}'] = {val}"]
                lines.append('')
            lines.append('')
        if part['info']['type'] == 'number-input':
            numeric_answer = None
            if len(exercise['solutions'][part_num].strip().split(' ')) == 1 and string_is_numeric(exercise['solutions'][part_num].replace(',', '').strip()):
                numeric_answer = float(exercise['solutions'][part_num].replace(',', '').strip())
                exercise['solutions'][part_num] = f'{{{{ correct_answers.part{part_num+1}_ans }}}}'
            if len(list(filter(None, exercise['solutions'][part_num].split('\n')))) == 1 and '\\rightarrow' in exercise['solutions'][part_num]:
                numeric_answer = 1
                answer_section: str = exercise['solutions'][part_num].split('\\rightarrow')[-1].strip()
                while not answer_section[-1].isdigit():
                    answer_section = answer_section[:-1]
                while not answer_section[0].isdigit() and not answer_section[0] == '-':
                    answer_section = answer_section[1:]
                numeric_answer = (float(answer_section.strip()))
                split = exercise['solutions'][part_num].split('\\rightarrow')
                split[-1] = split[-1].replace(answer_section, f'{{{{ correct_answers.part{part_num+1}_ans }}}}')
                exercise['solutions'][part_num] = '\\rightarrow'.join(split)
            lines.append(f"# Part {part_num+1} is a {part['info']['type']} question.")
            end_note = '' if numeric_answer is not None else '# TODO: insert correct answer here'
            lines.append(f"data2['correct_answers']['part{part_num+1}_ans'] = {numeric_answer or 0}  {end_note}")
            lines.append('')


    lines += ["# Update the data object with a new dict", "data.update(data2)"]
    return apply_indent(lines, indent), used_by
        # data2["params"]["part1"]["ans1"]["value"] = pbh.roundp(42)
        # data2["params"]["part1"]["ans1"]["correct"] = False
        # data2["params"]["part1"]["ans1"]["feedback"] = "This is a random number, you probably selected this choice by mistake! Try again please!"



def write_md(exercise):
    solutions = exercise['solutions']
    chapter = exercise['chapter']
    
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
    # Do all the moving here
    for i, a in enumerate(exercise['assets']):
        if a.endswith('.html'):
            asset_lines.append(f"- {a}")
            continue
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
    code_lines, params_dict = write_code(exercise)
    lines_to_write += code_lines
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
        filename = asset_to_filename[a] if a in asset_to_filename else a
        if not filename.endswith('.jpg') and not filename.endswith('.jpeg') and not filename.endswith('.png'):
            continue
        img = f'<img src="{filename}" width=400>'
        lines_to_write.append(img)
    if len(exercise['assets']) > 0:
        lines_to_write.append('')

    has_long_text = False
    for i, part in enumerate(exercise['parts']):
        lines_to_write += md_part_lines(part, i=i, params=params_dict, solution=solutions[i])
        if part['info']['type'] == 'longtext':
            has_long_text = True

    lines_to_write += ['## Rubric', '', 'This should be hidden from students until after the deadline.', '']

    print("WRITING TO", path)
    write_file(path, lines_to_write)
    # print(''.join(exercise['path'].split('.')[:-1]))
    if has_long_text:
        shutil.copyfile('sample.html', f'{dir_path}/sample.html')
    # write_file('question-paths.txt', [path])
