from gpt import create_template_json
from utils import write_json, read_json, split_comma, write_file
import questionary

def create_chapter_template(chapter: int, index: int):
    """
    chapter is 1-indexed, index is 0-indexed
    """
    textbook_file = read_json('./questions.json')
    question = textbook_file["questions"][str(chapter)][index]
    all_solutions = textbook_file["solutions"][str(chapter)]
    question_numbers = [q["questionNumber"] for q in question["parts"] if str(q["questionNumber"]) in all_solutions]
    question["parts"] = [x for x in question["parts"] if x["questionNumber"] in question_numbers]
    question["parts"] = [{**part, "solution": all_solutions[str(part["questionNumber"])]} for part in question["parts"]]
    print(question_numbers)
    is_good = questionary.confirm("are these the right question numbers? No if this is too much", default=len(question_numbers) < 10).ask()
    if not is_good:
        question_numbers_str = split_comma(questionary.text("paste in the list you want then (comma separated, numbers only) ex. 1, 2, 3").ask())
        new_question_numbers = [int(s) for s in question_numbers_str]
        if not (question_numbers[0] in new_question_numbers):
            question["description"] = ""
        question_numbers = new_question_numbers
    question["parts"] = [x for x in question["parts"] if x["questionNumber"] in question_numbers]

    solutions = {str(key): all_solutions[str(key)] for key in question_numbers if str(key) in all_solutions}

    instructions = questionary.text('Give question context, ex: "This question has 1 part, which is "matching""').ask()
    exercise = create_template_json(question, solutions, instructions)
    exercise["chapter"] = str(chapter)
    exercise["question_numbers"] = question_numbers
    branch_name = f"openstax_C{chapter}_Q{'_Q'.join([str(x) for x in question_numbers])}"
    exercise["branch_name"] = branch_name
    exercise["path"] = f"{branch_name}.md"
    exercise["solutions"] = [all_solutions[str(key)]  if str(key) in all_solutions else "" for key in question_numbers]
    exercise["issues"] = split_comma(questionary.text("What issues does this resolve (comma separated, numbers only)").ask())
    write_json(exercise, 'saved.json')
    print(f"Index {index} of CH {chapter} done!")

create_chapter_template(6, 0)