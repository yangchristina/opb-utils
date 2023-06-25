    
def replace_file_line(file_name, line_num, text):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    lines[line_num] = text.rstrip() + '\n'
    with open(file_name, 'w') as f:
        f.writelines(lines)


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

# ISSUE: might add an extra \n
def unwrap_unsupported_tags(stringV: str):
    string = stringV.replace("\\\\", "\n").replace("``", '"').replace("''", '"')
    supported_tags = ['\\textit{', '\\$']
    unsupported_remove_entirely_tags = ['\\footfullcite', '\\noindent']
    # unsupported, \footfullcite + \noindent, \emph, '\\raisebox'
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
        if end_bracket_index+1 < len(string) and string[end_bracket_index+1] == '[':
            end_bracket_index = find_end_tag(string[end_bracket_index+1:]) + end_bracket_index
            tag_area = string[index:end_bracket_index+1]
        wrapped_text = ''
        if not any([tag_area.startswith(tag) for tag in unsupported_remove_entirely_tags]):
            wrapped_text = tag_area.split('{')[-1].split('}')[0]
        # print('tag_area:', tag_area)
        # print('wrapped_text:', wrapped_text)
        string = string[:index] + wrapped_text + string[end_bracket_index + 2:]
    return result + string


def get_between_tag(string: str, tag: str):
    index = string.index(tag)
    end_bracket_index = find_end_tag(string[index:]) + index
    also_add = 1 if string[index + len(tag)] == '{' else 0
    return string[index+len(tag)+also_add:end_bracket_index]


def get_between_strings(text: str, start_target: str, end_target: str):
    start = text.index(start_target)
    text = text[start + len(start_target):]
    end = text.index(end_target)
    text = text[:end]
    return text
