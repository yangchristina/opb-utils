def get_file_url(chapter: str, filename: str):
    if not filename.endswith('.tex'):
        filename += '.tex'
    return f"{TEXTBOOK_PATH}/{textbook_chapter_to_name[chapter]}/TeX/{filename}"

def get_exercises(chapter: str, section: str, questions, solutions_dict):
    path = get_file_url(chapter, section)
    lines = [x.strip() for x in read_file(path)]

    # print(path)
    # print(questions)
    exercises = []
    table_num = 0

    cur_question = 0
    for i, line in enumerate(lines):
        if cur_question >= len(questions):
            break
        question = questions[cur_question]['question_number']

        line = line.strip()
        if line.startswith("% ") and lines[i + 2].strip().startswith('\eoce{'):
            if int(line.split(' ')[-1]) != question:
                continue
            else:
                variables = {}
                solutions = [x.replace("\\\\", "").strip().lstrip('`').lstrip('\\`').rstrip("'").rstrip('"').rstrip('".').strip() for x in re.split('\([a-z]+\)~|\([a-z]+\)\\\\|\([a-z]+-i+\)~', solutions_dict[question]) if x.strip() != '']

                #region title
                title_end_index = i + 1
                closing_line = -1
                bracket_start_index = find_2nd_string(lines[i + 2], '{')
                while closing_line == -1:
                    title_end_index += 1
                    (closing_line, closing_line_index) = closing_bracket_index(lines[i+2:title_end_index+1], bracket_start_index)
                closing_line += i+2
                title_lines = lines[i+2:closing_line+1]
                if len(title_lines) == 1:
                    title_lines[0] = title_lines[0][bracket_start_index+1:closing_line_index]
                else:
                    title_lines[0] = title_lines[0][bracket_start_index+1:]
                    title_lines[-1] = title_lines[-1][:closing_line_index]
                title = ' '.join(title_lines)
                title = remove_tags(title)
                #endregion

                #region description
                target = '\\begin{parts'
                description_end_index = closing_line
                started = False
                while description_end_index < len(lines):
                    cur_line = lines[description_end_index]
                    if description_end_index == closing_line:
                        cur_line = cur_line[closing_line_index+1:]
                    if (target in cur_line and '\\begin{align' not in cur_line and '\\begin{center' not in cur_line) or '}{}' in cur_line:
                        print('chapter', chapter, 'section', section, 'question', question)
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

                # print("END CUR DESCRIPTION", lines[description_end_index], lines[description_end_index+1])
                non_text_description_lines = []
                # print(f'i: {i}, Question: {question}')
                table = latex_table_to_md(f'table{table_num}', lines, description_end_index+1, variables=variables, phrases_signalling_end=['\\begin{parts}', '}{}'])
                figures = []
                # try:
                figures = find_all_figures(' '.join(lines[description_end_index+1:]).strip(), phrases_signalling_end=['}{}'])
                # except Exception as e:
                #     print("\nERROR FINDING FIGURES", chapter, section, question)
                #     print(e)
                if table is not None:
                    non_text_description_lines.append(table)
                    table_num += 1

                description, question_numbers = format_description(description, non_text_description_lines)
                #endregion


                # after adding parameters, description_end_index may have to be changed
                #region parts
                parts, number_variables, additional_assets = handle_parts(lines, description_end_index, description, solutions)
                number_variables['description'] = question_numbers
                #endregion
                if len(parts) == 1:
                    description = '. '.join([sentence for sentence in description.split('. ') if sentence.strip() != ''][:-1]) + '.'


                filename = str_to_filename(questions[cur_question]['issue_title'], '_')
                exercises.append({
                    "title": title,
                    "description": description,
                    "parts": parts,
                    "chapter": chapter,
                    "path": f"{filename}.md",
                    "assets": figures + list(additional_assets),
                    "issue": questions[cur_question]['issue_title'],
                    "num_variables": number_variables,
                    "variables": variables,
                    "solutions": solutions,
                })
                cur_question += 1
    if cur_question < len(questions):
        print("Looping again: CUR QUESTION", cur_question, questions[cur_question])
        print("chapter", chapter, "section", section, "questions", [question['question_number'] for question in questions], len(questions))
        raise Exception("Looping again")

    # print("CHAPTER", chapter)
    # print(json.dumps(exercises, indent=4))
    # print(len(exercises))
    return exercises


def read_chapter(chapter: str, questions: list): # questions is int list
    questions.sort(key=lambda x: x['question_number'])
    chapter_info = read_chapter_info(chapter)
    all_sections = chapter_info['inputs']
    exercise_counts = [count_exercises(chapter, cur_section) for cur_section in all_sections]
    summed_counts = [sum(exercise_counts[:i]) for i in range(len(exercise_counts))]
    title = chapter_info['title']
    # return
    sections = {}
    for question in questions:
        section_index = bisect.bisect_left(summed_counts, question['question_number'])
        section = all_sections[section_index-1]
        if section not in sections:
            sections[section] = []
        sections[section].append(question)

        # print("SECTIONS", json.dumps(sections, indent=2))
    results = []
    # print(all_sections)
    # for (section, questions) in sections.items():
        # question_numbers = [x['questions'] for x in questions]
    # section_index = all_sections.index(section)
    # file_questions = [q - summed_counts[section_index] for q in questions]
    question_solutions_dict = find_solutions(title, questions)
    for (section, questions) in sections.items():
        print("SECTION", section, "count", len(questions))
        print([question['question_number'] for question in questions])
        results += get_exercises(chapter, section, questions, question_solutions_dict)

    with open('completed.txt', 'r') as reader:
        lines = reader.readlines()
        lines = [line.strip() for line in lines]
        results = [exercise for exercise in results if exercise['path'].strip() not in lines]
        # ex. exercise['path'] = '1_2_data_basics_q1_9.md'
        for line in lines:
            line.strip()
    for exercise in results:
        # if (exercise['path'] == ''):
        write_md(exercise)
        # try:
        #     write_md(exercise)
        # except Exception as e:
        #     print(f'Error writing {exercise["path"]}')
        #     print(e)
        #     continue
    # print(json.dumps(results, indent=4))
# endregion read textbook
