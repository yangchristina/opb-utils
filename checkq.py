# Author: Firas Moosvi
# Date: 2023-05-14

"""Syntax check on an individual question.

Usage:
    checkq.py <md_file> [options]

Arguments:
    md_file              Path to the source md file.

Options:
    --output_root=<str>          Location where the question folder should export [default: ../../pl-opb-ind100/questions].
"""

from docopt import docopt
import problem_bank_scripts as pbs
import pathlib
import os

def main():
    args = docopt(__doc__)
    output_root = args["--output_root"]
    question = args["<md_file>"]

    output_dir = os.path.join(output_root,pathlib.Path(question).parts[-2], \
                                          pathlib.Path(question).parts[-1])

    assert 'md' in question, f"You must provide a path to an .md file - '{question}' is not an md file!"

    # Process md file
    try:
        print(f"Processing question: {question}")
        pbs.process_question_pl(question, output_path=output_dir)

        print(f"\t Moved file to location: {output_dir}")

    except FileNotFoundError:
        print(
            f"This question's file was not found. \n\tSkipping question: {question}."
        )

    except Exception as e:
        print(f"There is an error in this problem: \n\t- File path: {question}\n\t- Error: {e}")
        raise e


if __name__ == "__main__":
    main()
