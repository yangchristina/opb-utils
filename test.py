data2 = {}
import random
data2["params"]["vars"]["title"] = "Study components"


# Randomize Variables
description_num1 = 160.0

variants = [{
    'description': f'Researchers studying the relationship between honesty, age and self-control conducted an experiment on {description_num1} children between the ages of 5 and 15. Participants reported their age, sex, and whether they were an only child or not. The researchers asked each child to toss a fair coin in private and to record the outcome (white or black) on a paper sheet, and said they would only reward children who report white. The study\'s findings can be summarized as follows: "Half the students were explicitly told not to cheat and the others were not given any explicit instructions. In the no instruction group probability of cheating was found to be uniform across groups based on child\'s characteristics. In the group that was explicitly told to not cheat, girls were less likely to cheat, and while rate of cheating didn\'t vary by age for boys, it decreased with age for girls."',
    'part2': { 
        'choices': [
            {
            "value": 'Children between the ages of 5 and 15',
            "correct": True,
            "feedback": 'Correct',
            },
            {
            "value": '"Children who cheated"',
            "correct": False,
            "feedback": 'Incorrect',
            },
            {
            "value": 'Students who were explicitly told not to cheat',
            "correct": False,
            "feedback": 'Incorrect',
            },
            {
            "value": 'Children who did not cheat',
            "correct": False,
            "feedback": 'Incorrect',
            }
        ]
    },
    'part3': description_num1,
    'part4': {
        'options': {
            'option1': '"Not a variable in the study"',
            'option2': '"Numerical and discrete variable"',
            'option3': '"Numerical and continuous variable"',
            'option4': '"Categorical"',
            # 'option4': 'Categorical and not ordinal variable',
        },
        'statements': [
            {'value': '"Age"', 'matches': 'option3' },
            {'value': '"Sex"', 'matches': 'option4' },
            {'value': '"Whether they were an only child or not"', 'matches': 'option4' },
            {'value': '"whether they cheated or not"', 'matches': 'option4' },
        ],
    },
    }
]

variant = variants[random.randint(0, len(variants)-1)] 

data2['params']['description']['text'] = variant['description']


# Part 2 is a multiple-choice question.
for i, choice in enumerate(variant["part2"]["choices"]):
    data2['params']['part2'][f'ans{i+1}']['value'] = choice['value']
    data2['params']['part2'][f'ans{i+1}']['correct'] = choice['correct']
    data2['params']['part2'][f'ans{i+1}']['feedback'] = f'"{choice["feedback"]}"'
    if choice['correct']:
        data2['part2']['correct_ans'] = choice['value']

# Part 3 is a number-input question.
data2['correct_answers']['part3_ans'] = variant["part3"]

# Part 4 is a matching question.
for (key, value) in variant["part4"]["options"].items():
    data2["params"]["part4"][key]["value"] = value

for s_num, statement_info in enumerate(variant["part4"]['statements']):
    data2["params"]["part4"][f"statement{s_num+1}"]["value"] = f'"{statement_info["value"]}"'
    data2["params"]["part4"][f"statement{s_num+1}"]["matches"] = f'"{statement_info["matches"]}"'

# Update the data object with a new dict
data.update(data2)