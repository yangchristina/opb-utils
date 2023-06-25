
from utils import unwrap_unsupported_tags


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

def latex_table_to_md(lines, starting_index, phrases_signalling_end=None)->str:
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
        matrix[i] = [unwrap_unsupported_tags(x.strip()).strip() or '.' for x in arr]
        # print('matrix[i]', matrix[i])
        # num_cols = sum([int(col.split('\multicolumn{')[-1].split('}')[0]) + 1 if '\multicolumn{' in col else 1 for col in matrix[0]])

    columns_label = ''
    # Remove empty rows + columns
    matrix = [row for row in matrix if len(row) > 0 and any([x != '.' for x in row])]
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

def find_all_figures(latex_lines, starting_line_index, phrases_signalling_end=None):
    """Finds all figures in a latex document/string."""
    figures = []
    # print("in figures, starting index", starting_line_index)
    for line in latex_lines[starting_line_index:]:
        # if (line.strip() != ''):
        #     print(line)
        if phrases_signalling_end is not None:
            for end_phrase in phrases_signalling_end:
                if end_phrase in line:
                    return figures
        if '\\Figures' in line:
            bracket_index = line.index(']')
            starting_index = line[bracket_index:].index('}') + 2 + bracket_index
            ending_index = line[starting_index:].index('}') + starting_index
            figures.append(line[starting_index:ending_index])
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