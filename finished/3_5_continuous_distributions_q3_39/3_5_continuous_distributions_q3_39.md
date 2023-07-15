---
title: Grade distributions
topic: Probability
author: Christina Yang
source: original
template_version: 1.4
attribution: openintro-stats
partialCredit: true
singleVariant: false
showCorrectAnswer: true
outcomes:
- 3.1.1.4
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
  generate: |
        data2 = pbh.create_data2()

        data2["params"]["vars"]["title"] = "Grade distributions"

        # Randomize Variables
        description_num1 = round(random.uniform(0.1, 0.3), 1)  # 0.3
        description_num2 = description_num1
        description_num3 = description_num1
        description_num4 = round(random.uniform(0.1, 0.5), 1)  # 0.2
        description_ra_cf = round(1.2 - (description_num1 * 3 + description_num4), 1)  # 0.1
        description_num5 = 0  # 0
        description_num6 = description_num5
        description_num7 = 1  # 1
        description_num8 = description_num5
        description_num9 = description_num5

        description_num10 = description_num1
        description_num11 = description_num1
        description_num12 = description_num1
        description_num13 = description_num5
        description_num14 = description_num5

        description_num15 = description_num1
        description_num16 = round(random.uniform(0, 0.3), 1)  # 0.5
        description_num17 = description_num4
        description_num18 = round(random.uniform(0.1, 0.2), 1)  # 0.1
        description_num19 = round(random.uniform(-0.5, -0.1), 1)  # -0.1

        description_num20 = round(random.uniform(0.1, 0.2), 1)  # 0.2
        description_num21 = round(random.uniform(0.1, 0.3), 1)  # 0.4
        description_num22 = round(random.uniform(0.1, 0.3), 1)
        description_num23 = round(random.uniform(0.1, 0.2), 1)
        description_num24 = round(1 - description_num20 - description_num21 - description_num22 - description_num23, 1)

        description_num25 = description_num5
        description_num26 = description_num19
        description_num27 = round(random.uniform(1.0, 1.2), 1)  # 1.1
        description_num28 = description_num5
        description_num29 = description_num5

        # store the variables in the dictionary "params"
        data2['params']['description']['ra_cf'] = description_ra_cf
        data2['params']['description']['num1'] = description_num1
        data2['params']['description']['num2'] = description_num2
        data2['params']['description']['num3'] = description_num3
        data2['params']['description']['num4'] = description_num4
        data2['params']['description']['num5'] = description_num5
        data2['params']['description']['num6'] = description_num6
        data2['params']['description']['num7'] = description_num7
        data2['params']['description']['num8'] = description_num8
        data2['params']['description']['num9'] = description_num9

        data2['params']['description']['num10'] = description_num10
        data2['params']['description']['num11'] = description_num11
        data2['params']['description']['num12'] = description_num12
        data2['params']['description']['num13'] = description_num13
        data2['params']['description']['num14'] = description_num14

        data2['params']['description']['num15'] = description_num15
        data2['params']['description']['num16'] = description_num16
        data2['params']['description']['num17'] = description_num17
        data2['params']['description']['num18'] = description_num18
        data2['params']['description']['num19'] = description_num19
        data2['params']['description']['num20'] = description_num20
        data2['params']['description']['num21'] = description_num21
        data2['params']['description']['num22'] = description_num22
        data2['params']['description']['num23'] = description_num23
        data2['params']['description']['num24'] = description_num24
        data2['params']['description']['num25'] = description_num25
        data2['params']['description']['num26'] = description_num26
        data2['params']['description']['num27'] = description_num27
        data2['params']['description']['num28'] = description_num28
        data2['params']['description']['num29'] = description_num29

        # Part 1 is a multiple-choice question.
        data2['params']['part1']['ans1']['value'] = "Valid"
        data2['params']['part1']['ans1']['correct'] = False
        data2['params']['part1']['ans1']['feedback'] = "Incorrect!"

        data2['params']['part1']['ans2']['value'] = "Invalid"
        data2['params']['part1']['ans2']['correct'] = True
        data2['params']['part1']['ans2']['feedback'] = "Correct!"

        # Part 2 is a multiple-choice question.
        data2['params']['part2']['ans1']['value'] = "Valid"
        data2['params']['part2']['ans1']['correct'] = True
        data2['params']['part2']['ans1']['feedback'] = "Correct!"

        data2['params']['part2']['ans2']['value'] = "Invalid"
        data2['params']['part2']['ans2']['correct'] = False
        data2['params']['part2']['ans2']['feedback'] = "Try again please!"


        # Part 3 is a multiple-choice question.
        data2['params']['part3']['ans1']['value'] = "Valid"
        data2['params']['part3']['ans1']['correct'] = False
        data2['params']['part3']['ans1']['feedback'] = "Try again please!"

        data2['params']['part3']['ans2']['value'] = "Invalid"
        data2['params']['part3']['ans2']['correct'] = True
        data2['params']['part3']['ans2']['feedback'] = "Correct!"


        # Part 4 is a multiple-choice question.
        data2['params']['part4']['ans1']['value'] = "Valid"
        data2['params']['part4']['ans1']['correct'] = False
        data2['params']['part4']['ans1']['feedback'] = "Try again please!"

        data2['params']['part4']['ans2']['value'] = "Invalid"
        data2['params']['part4']['ans2']['correct'] = True
        data2['params']['part4']['ans2']['feedback'] = "Correct!"


        # Part 5 is a multiple-choice question.
        data2['params']['part5']['ans1']['value'] = "Valid"
        data2['params']['part5']['ans1']['correct'] = True
        data2['params']['part5']['ans1']['feedback'] = "Correct!"

        data2['params']['part5']['ans2']['value'] = "Invalid"
        data2['params']['part5']['ans2']['correct'] = False
        data2['params']['part5']['ans2']['feedback'] = "Try again please!"


        # Part 6 is a multiple-choice question.
        data2['params']['part6']['ans1']['value'] = "Valid"
        data2['params']['part6']['ans1']['correct'] = False
        data2['params']['part6']['ans1']['feedback'] = "Try again please!"

        data2['params']['part6']['ans2']['value'] = "Invalid"
        data2['params']['part6']['ans2']['correct'] = True
        data2['params']['part6']['ans2']['feedback'] = "Correct!"


        # Update the data object with a new dict
        data.update(data2)
  prepare: |
        pass
  parse: |
        pass
  grade: |
        pass
part1:
  type: multiple-choice
  pl-customizations:
    weight: 1
part2:
  type: multiple-choice
  pl-customizations:
    weight: 1
part3:
  type: multiple-choice
  pl-customizations:
    weight: 1
part4:
  type: multiple-choice
  pl-customizations:
    weight: 1
part5:
  type: multiple-choice
  pl-customizations:
    weight: 1
part6:
  type: multiple-choice
  pl-customizations:
    weight: 1
---
# {{ params.vars.title }}

Each row in the table below is a proposed grade distribution for a class. Identify each as a valid or invalid probability distribution.
|  |  A ------   |  B ------  |  C ------  |  D ------  |  F |
| --- | ------------ | ------------ | ------------ | ------------ | ------------ |
| (a) | ${{ params.description.num1 }}$   | ${{ params.description.num2 }}$   | ${{ params.description.num3 }}$   | ${{ params.description.num4 }}$   | ${{ params.description.ra_cf }}$
| (b) | ${{ params.description.num5 }}$     | ${{ params.description.num6 }}$     | ${{ params.description.num7 }}$     | ${{ params.description.num8 }}$     | ${{ params.description.num9 }}$
| (c) | ${{ params.description.num10 }}$   | ${{ params.description.num11 }}$   | ${{ params.description.num12 }}$   | ${{ params.description.num13 }}$     | ${{ params.description.num14 }}$
| (d) | ${{ params.description.num15 }}$   | ${{ params.description.num16 }}$   | ${{ params.description.num17 }}$   | ${{ params.description.num18 }}$   | ${{ params.description.num19 }}$
| (e) | ${{ params.description.num20 }}$   | ${{ params.description.num21 }}$   | ${{ params.description.num22 }}$   | ${{ params.description.num23 }}$   | ${{ params.description.num24 }}$
| (f) | ${{ params.description.num25 }}$     | ${{ params.description.num26 }}$  | ${{ params.description.num27 }}$   | ${{ params.description.num28 }}$     | ${{ params.description.num29 }}$


## Part 1

(a)

### Answer Section

- {{ params.part1.ans1.value }}
- {{ params.part1.ans2.value }}

### pl-answer-panel

Part 1: Invalid. Sum is greater than~1


## Part 2

(b)

### Answer Section

- {{ params.part2.ans1.value }}
- {{ params.part2.ans2.value }}

### pl-answer-panel

Part 2: Valid. Probabilities are between ${{ params.description.num5 }}$ and ${{ params.description.num7 }}$, and they sum to ${{ params.description.num7 }}$.


## Part 3

(c)

### Answer Section

- {{ params.part3.ans1.value }}
- {{ params.part3.ans2.value }}

### pl-answer-panel

Part 3: Invalid. Sum is less than~1


## Part 4

(d)

### Answer Section

- {{ params.part4.ans1.value }}
- {{ params.part4.ans2.value }}

### pl-answer-panel

Part 4: Invalid. There is a negative probability


## Part 5

(e)

### Answer Section

- {{ params.part5.ans1.value }}
- {{ params.part5.ans2.value }}

### pl-answer-panel

Part 5: Valid. Probabilities are between ${{ params.description.num5 }}$ and ${{ params.description.num7 }}$, and they sum to~1


## Part 6

(f)

### Answer Section

- {{ params.part6.ans1.value }}
- {{ params.part6.ans2.value }}

### pl-answer-panel

Part 6: Invalid. There is a negative probability


## Rubric

This should be hidden from students until after the deadline.
