
from utils import unwrap_unsupported_tags, string_is_numeric, get_between_strings, find_2nd_string


def grab_latex_tag_section(lines, starting_index, target, phrases_signalling_end=None):
    cur = starting_index
    start = end = None
    # print('target', f'\\begin{{{target}}}')
    while cur < len(lines):
        line = lines[cur]
        if phrases_signalling_end is not None:
            for end_phrase in phrases_signalling_end:
                if end_phrase in line:
                    return None
        if start is None and f'\\begin{{{target}}}' in line:
            start = cur
        elif start is not None and f'\\end{{{target}}}' in line:
            end = cur
            return lines[start:end+1]
        cur += 1
    return None

def latex_table_to_md(key: str, lines, starting_index, variables, phrases_signalling_end=None)->str:
    """Converts a latex table to markdown format."""
    latex_lines = grab_latex_tag_section(lines, starting_index, 'tabular', phrases_signalling_end=phrases_signalling_end)
    # print('latex_lines')
    # print(latex_lines)
    # print(lines[starting_index:])
    if latex_lines is None:
        return None
    latex_lines = latex_lines[1:-1]
    md_lines = []
    was_empty = True
    # Need to add header | --------- | --------------------- | -------------------- | ------- | somewhere
    # TODO: turn latex table into matrix
    matrix = [[] for _ in latex_lines]
    left_border = 0
    header_label = ''
    null_value = ''
    # print('latex_lines', '\n'.join(latex_lines))
    for i, line in enumerate(latex_lines):
        if phrases_signalling_end is not None:
            for end_phrase in phrases_signalling_end:
                if end_phrase in line:
                    return None
        if not '&' in line:
            continue
        arr = []
        for col in line.split('&'):
            if '\multicolumn{' in col:
                length = int(col.split('\multicolumn{')[-1].split('}')[0]) + 1
                # extract text from \multicolumn{2}{c}{\textit{Pain free}}
                text = col[col.rfind('{')+1:].split('}')[0]
                arr.append(text)
                arr += [''] * (length - 1)
                continue
            arr.append(col)
        # if i == 0:
        #     valid_count = 0
        #     valid_value = ''
        #     for x in arr:
        #         if x.strip() != '':
        #             valid_value = x
        #             valid_count += 1
        #     print('valid count', valid_count)
        #     if valid_count == 1:
        #         matrix[i] = ['.' for x in arr]
        #         header_label = valid_value
        #         print("Valid row label", header_label)
        #         continue
        matrix[i] = [unwrap_unsupported_tags(x.strip()).strip() or null_value for x in arr]
        # print('matrix[i]', matrix[i])
        # num_cols = sum([int(col.split('\multicolumn{')[-1].split('}')[0]) + 1 if '\multicolumn{' in col else 1 for col in matrix[0]])

    columns_label = ''
    # Remove empty rows + columns
    matrix = [row for row in matrix if len(row) > 0 and any([x != null_value for x in row])]

    max_row_len = max([len(row) for row in matrix])
    for i, row in enumerate(matrix):
        if len(row) < max_row_len:
            matrix[i] = [null_value] * (max_row_len - len(row)) + row

    # print('matrix', matrix)

    # # find columns label
    # if matrix[0][0] == '.':
    #     valid_count = 0
    #     valid_value = ''
    #     for row in matrix:
    #         if row[0] != '.':
    #             valid_count += 1
    #             valid_value = row[0]
    #     if valid_count == 1:
    #         columns_label = valid_value
    #         for row in matrix:
    #             row.pop(0)
    #         matrix[0][0] = columns_label

    c = 0
    # print('matrix', matrix)
    while c < len(matrix[0]):
        if all([row[c].strip() == '' for row in matrix]):
            for row in matrix:
                row.pop(c)
        else:
            c += 1
    num_cols = sum([int(col.split('\multicolumn{')[-1].split('}')[0]) + 1 if '\multicolumn{' in col else 1 for col in matrix[0]])
    # ||           | \multicolumn{2}{c}{\textit{Pain free}} \\|
    # while True:
    #     if matrix[0][left_border].strip() == matrix[-1][left_border].strip() and matrix[0][left_border].strip() == '':
    #         left_border += 1
    #     else:
    #         break

    # variables
    # Loop through matrix
    # If a cell is a variable, add it to the variables dict
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell != null_value and string_is_numeric(cell.replace(',', '')):
                variables["{0}_r{1}_c{2}".format(key, i, j)] = float(cell.replace(',', ''))
                matrix[i][j] = f'{{{{ params.{key}.r{i}.c{j} }}}}'

    md_lines = ['| ' + ' | '.join(row) + ' |' for row in matrix]
    md_lines.insert(1, '| ' + ' | '.join(['------------'] * num_cols) + ' |')
        # for r in len(matrix):

        # if all([matrix[i][row] == '' for i in range(len(matrix))]):
        #     for i in range(len(matrix)):
        #         matrix[i].pop(row)
        # new_line = line.replace('&', '|').replace('\\\\', '')
        # if was_empty and new_line.split('|')[0].strip() != '':
        #     separator = ['| --------------------- '] * (new_line.count('|') + 1) + ['|']
        #     md_lines.append(''.join(separator))
        # md_lines.append('|' + new_line + '|')

    return '\n'.join(md_lines).replace('\\\\', '')


def find_all_figures(all_lines: str, phrases_signalling_end=None):
    """Finds all figures in a latex document/string."""
    figures = []
    # print("in figures, starting index", starting_line_index)
    figure_found = False

    # all_lines = ' '.join(latex_lines[starting_line_index:]).strip()
    if not all_lines.strip():
        return figures
    # print("all lines", all_lines)

    end_phrase_index = 0
    while phrases_signalling_end and end_phrase_index < len(phrases_signalling_end) and phrases_signalling_end[end_phrase_index] not in all_lines:
        end_phrase_index += 1

    text = all_lines if phrases_signalling_end is None or end_phrase_index == len(phrases_signalling_end) else all_lines[:all_lines.index(phrases_signalling_end[end_phrase_index])]

    if '\\Figure' not in text:
        return figures
    # text = '\\Figures' + get_between_strings(all_lines, '\\Figure', '}{}')
    while '\\Figure' in text:
        starting_index = text.index('\\Figure')
        text = text[starting_index + len('\\Figure'):]
        if '[' in text[:text.index(' ')]:
            if ']' not in text:
                raise Exception("No closing bracket for figure")
            text = text[text.index(']')+1:]
        if '}' not in text:
            raise Exception("No bracket for figure")
        text = text[text.index('}') + 1:]
        path = text.split(' ')[0].replace('}{', '/').replace('{', '')
        path = path[:path.index('}')].strip()
        # if '.' not in path:
        #     path += '.pdf'
        # figure_path = text.split(' ')[0].split('{')[-1].split('}')[0]
        figures.append(path)

    # for line in latex_lines[starting_line_index:]:
    #     # if (line.strip() != ''):
    #     #     print(line)
    #     if phrases_signalling_end is not None:
    #         for end_phrase in phrases_signalling_end:
    #             if end_phrase in line:
    #                 return figures
    #     if '\\Figures' in line:
    #         figure_found = True
    #     if figure_found and ']' in line:
    #         bracket_index = line.index(']') #  might be on a different line
    #         starting_index = line[bracket_index:].index('}') + 2 + bracket_index
    #         ending_index = line[starting_index:].index('}') + starting_index
    #         figures.append(line[starting_index:ending_index])
    #         figure_found = False
    print("figures", figures)
    return figures
    # \Figures[An ear is show, with an "M" shown near the front lower lobe of the ear and an "S" shown near the middle upper portion of the ear.]{0.75}{eoce/migraine_and_acupuncture_intro}{earacupuncture}


"""                                *Pain free*       
  ---------------- ----------- ------------- ---- -------
                                    Yes       No   Total
                   Treatment        10        33    43
  \[0pt\]*Group*   Control           2        44    46
                   Total            12        77    89"""


"""\begin{tabular}{ll  cc c} 
			                         		&           & \multicolumn{2}{c}{\textit{Pain free}} \\
\cline{3-4}
			                        	 	&			& Yes 	& No 	                  & Total \\
\cline{2-5}
							& Treatment 	& 10	 	& 33		                  & 43 \\
\raisebox{1.5ex}[0pt]{\emph{Group}} & Control	 	& 2	 	& 44 	 	                  & 46 \\
\cline{2-5}
							& Total		& 12		& 77		                  & 89
\end{tabular}"""