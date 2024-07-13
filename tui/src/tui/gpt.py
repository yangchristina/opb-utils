import ast
import json
from openai import OpenAI
from utils import write_json

client = OpenAI()


def ask_number_code(question: str, answer: str | float | int, additional_info="") -> str:
    extra_info = f"Additional context: {additional_info}" if additional_info else ""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""I am creating a number-input question. The question is: "{question}"

                {extra_info}

                The correct answer is "{answer}".
                Write me the python code to solve the question. Use variables when possible.
                Answer with only the python code.""",
            }
        ],
        model="gpt-3.5-turbo",
    )
    for choice in chat_completion.choices:
        print(choice.message.content)
    res = chat_completion.choices[0].message.content
    # check that res is a list of strings
    assert isinstance(res, str)
    return res


def ask_mc_options(options: list[str], answer: str, question: str, num_to_generate: int):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""I am creating a multiple choice question. The question is: "{question}"
                Here are the options: {options}. The correct answer is "{answer}". Generate me {num_to_generate} incorrect options.
                Answer with only a python list of strings.""",
            }
        ],
        model="gpt-3.5-turbo",
    )
    for choice in chat_completion.choices:
        print(choice.message.content)
    try:
        res = ast.literal_eval(chat_completion.choices[0].message.content)  # pyright: ignore[reportArgumentType]
    except Exception as e:
        print(e)
        res = "\n".split(chat_completion.choices[0].message.content)
    # check that res is a list of strings
    assert isinstance(res, list)
    assert all(isinstance(x, str) for x in res)
    return res


def dict_to_string(dict: dict):
    return json.dumps(dict, indent=2)

def create_template_json(question: dict, solutions: dict, instructions: str):
    """
    example instructions: This question has 1 part, which is "matching".
    """

    prompt = f"{dict_to_string(question)}\n${dict_to_string(solutions)}" + f"""
Instructions:
Try to avoid long-text questions, can convert most long-text to multiple-choice, by generating possible wrong answers. It is possible for multiple questions to go into a single part (ie. for matching) and possible to split one question in to multiple parts.
Turn numbers in the question text into variables. Replace variables in the question with {{{{ params.VARIABLE_NAME }}}}
{instructions}
Create the question in the following format (not all parts have solutions):\n"""
    + """
interface LargeQuestion {
    variables: Record<string, string>;
    question_numbers: number[];
    title: string; // generate a title for the entire question
    parts: {
        solution: string;
        question: string;
        info: {
            type:
                | "multiple-choice"
                | "checkbox"
                | "number-input"
                | "longtext"
                | "dropdown"
                | "matrix"
                | "matching"
                | "true-false"
                | "yes-no"
                | "file-upload"
                | "integer-input"
                | "symbolic-input";
            choices?: { value: string; correct: boolean; feedback: string }[]; // for multiple-choice | checkbox | dropdown | yes-no | true-false
            digits: number; // for number-input
            label?: string; // for number-input | integer-input | symbolic-input (ex. "$p=$")
            suffix?: string; // for number-input
            code?: string; // python code to solve question as a string
            statements?: { value: string; matches: string }[]; // for matching
            options?: string[] // for matching: generate around 2 extra statements with no matches. These should not overlap with those in "statements"
        };
    }[];
}"""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    write_json(chat_completion.choices[0], 'gpt-template.json')
    return chat_completion.choices[0]