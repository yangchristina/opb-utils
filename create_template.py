# from gpt import create_template_json
# from utils import write_json, read_json, split_comma, write_file
# import questionary
# from dotenv import load_dotenv
# load_dotenv()

# def create_chapter_template():
#     """
#     chapter is 1-indexed, index is 0-indexed
#     """
#     textbook_file = read_json('./questions.json')

#     chapter = int(questionary.text("what chapter (integer)").ask())
#     one_question_number = int(questionary.text("name just one question number you want in your range (integer)").ask())
#     index = next(i for i,v in enumerate(textbook_file["questions"][str(chapter)]) if next((True for x in v["parts"] if x["questionNumber"]==one_question_number), False))
#     question = textbook_file["questions"][str(chapter)][index]
#     print("here is a link to the question section\n", question["sectionHref"])

#     all_solutions = textbook_file["solutions"][str(chapter)]
#     question_numbers = [q["questionNumber"] for q in question["parts"] if str(q["questionNumber"]) in all_solutions]
#     question["parts"] = [x for x in question["parts"] if x["questionNumber"] in question_numbers]
#     question["parts"] = [{**part, "solution": all_solutions[str(part["questionNumber"])]} for part in question["parts"]]
#     print(question_numbers)
#     if ("tables" in question):
#         print(f'this question has {len(question["tables"])} table(s)')
#     # description
#     is_good = questionary.confirm("are these the right question numbers? No if this is too much", default=len(question_numbers) < 10).ask()

#     if not is_good:
#         question_numbers_str = split_comma(questionary.text("paste in the list you want then (comma separated, numbers only) ex. 1, 2, 3").ask())
#         question_numbers = [int(s) for s in question_numbers_str]
#         print(question["description"])
#         should_keep = questionary.confirm("keep this description?").ask()
#         if not should_keep:
#             question["description"] = ""
#     question["parts"] = [x for x in question["parts"] if x["questionNumber"] in question_numbers]

#     solutions = {str(key): all_solutions[str(key)] for key in question_numbers if str(key) in all_solutions}

#     instructions = questionary.text('Give question context, ex: "This question has 1 part, which is "matching""').ask()
#     exercise = create_template_json(question, solutions, instructions)
#     exercise["chapter"] = str(chapter)
#     exercise["question_numbers"] = question_numbers
#     branch_name = f"openstax_C{chapter}_Q{'_Q'.join([str(x) for x in question_numbers])}"
#     exercise["branch_name"] = branch_name
#     exercise["path"] = f"{branch_name}.md"
#     exercise["solutions"] = [part["solution"] for part in exercise["parts"]]
#     exercise["issues"] = split_comma(questionary.text("What issues does this resolve (comma separated, numbers only)").ask())
#     exercise["tables"] = question["tables"]
#     write_json(exercise, 'saved.json')
#     print(f"Index {index} of CH {chapter} done!")

# # create_chapter_template(2, 9)
# create_chapter_template()