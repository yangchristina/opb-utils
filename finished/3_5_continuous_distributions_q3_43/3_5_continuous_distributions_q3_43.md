---
title: Cost of breakfast
topic: Probability
author: Christina Yang
source: original
template_version: 1.4
attribution: openintro-stats
partialCredit: true
singleVariant: false
showCorrectAnswer: false
outcomes:
difficulty:
- undefined
randomization:
- undefined
taxonomy:
- undefined
span:
- undefined
length:
- undefined
tags:
- CY
assets:
server:
  imports: |
        import random
        import pandas as pd
        import problem_bank_helpers as pbh
        import math
  generate: |
        data2 = pbh.create_data2()

        data2["params"]["vars"]["title"] = "Cost of breakfast"


        # Randomize Variables
        description_num1 = round(random.uniform(1.26, 1.54), 2)  #1.4
        description_num2 = round(random.uniform(2.25, 2.75), 2)  #2.5
        description_num3 = random.randint(10, 20) / 100  #15
        description_std = random.randint(description_num3 * 100 + 5, 40) / 100  #30

        # store the variables in the dictionary "params"
        data2['params']['description']['num1'] = description_num1
        data2['params']['description']['num2'] = description_num2
        data2['params']['description']['num3'] = description_num3
        data2['params']['description']['std'] = description_std

        ans1 = description_num1 + description_num2
        ans2 = math.sqrt(description_num3**2 + description_std**2)
        ans3 = ans1 * 7
        ans4 = ans2 * math.sqrt(7)

        # Part 1 is a number-input question.
        data2['correct_answers']['part1_ans'] = ans1  # E = \$3.90.

        # Part 2 is a number-input question.
        data2['correct_answers']['part2_ans'] = ans2  # SD = \$0.34

        # Part 3 is a number-input question.
        data2['correct_answers']['part3_ans'] = ans3  # E = \$27.30.

        # Part 4 is a number-input question.
        data2['correct_answers']['part4_ans'] = ans4  # SD = \$0.89

        # Update the data object with a new dict
        data.update(data2)
  prepare: |
        pass
  parse: |
        pass
  grade: |
        pass
part1:
  type: number-input
  pl-customizations:
    rtol: 0.0001
    weight: 1
    allow-blank: true
    label: $E= \$$
part2:
  type: number-input
  pl-customizations:
    rtol: 0.02
    weight: 1
    allow-blank: true
    label: $SD= \$$
part3:
  type: number-input
  pl-customizations:
    rtol: 0.01
    weight: 1
    allow-blank: true
    label: $E= \$$
part4:
  type: number-input
  pl-customizations:
    rtol: 0.02
    weight: 1
    allow-blank: true
    label: $SD= \$$
---
# {{ params.vars.title }}

Sally gets a cup of coffee and a muffin every day for breakfast from one of the many coffee shops in her neighborhood. She picks a coffee shop each morning at random and independently of previous days. The average price of a cup of coffee is \$${{ params.description.num1 }}$ with a standard deviation of \${{ params.description.std }}, the average price of a muffin is \$${{ params.description.num2 }}$ with a standard deviation of ${{ params.description.num3 }}$ and the two prices are independent of each other. (Round the following to 2 decimal places)

## Part 1

What is the mean she spends on breakfast daily?

### Answer Section

Please enter a numeric value in.


## Part 2

What is the standard deviation of the amount she spends on breakfast daily?

### Answer Section

Please enter a numeric value in.


## Part 3

What is the mean of the amount she spends on breakfast weekly (7~days)?

### Answer Section

Please enter a numeric value in.


## Part 3

What is the standard deviation of the amount she spends on breakfast weekly (7~days)?

### Answer Section

Please enter a numeric value in.


## Rubric

This should be hidden from students until after the deadline.
