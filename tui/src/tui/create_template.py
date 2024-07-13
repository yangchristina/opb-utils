from gpt import create_template_json
from utils import write_json, read_json, split_comma
import questionary

def create_chapter_template(*, chapter: int, index: int):
    """
    chapter is 1-indexed, index is 0-indexed
    """
    textbook_file = read_json('./questions.json')
    question = textbook_file["questions"][str(chapter)][index]
    all_solutions = textbook_file["solutions"][str(chapter)]
    question_numbers = [q["questionNumber"] for q in question["parts"]]
    solutions = {[str(key)]: all_solutions[str(key)] for key in question_numbers}
    exercise = create_template_json(question, solutions)
    exercise["chapter"] = str(chapter)
    exercise["question_numbers"] = question_numbers
    branch_name = f"openstax_C{chapter}_Q{'_Q'.join([str(x) for x in question_numbers])}"
    exercise["branch_name"] = branch_name
    exercise["path"] = f"{branch_name}.md"
    print("question numbers are", question_numbers)
    exercise["issues"] = split_comma(questionary.text(question="What issues does this resolve (comma separated, numbers only)").ask())
    write_json('saved.json')
    print(f"Part {index} of CH {chapter} done!")

create_chapter_template(6, 0)