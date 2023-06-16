    
def replace_file_line(file_name, line_num, text):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    lines[line_num] = text.rstrip() + '\n'
    with open(file_name, 'w') as f:
        f.writelines(lines)