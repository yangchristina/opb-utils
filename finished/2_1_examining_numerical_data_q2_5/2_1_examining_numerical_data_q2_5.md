---
title: Parameters and statistics
topic: Introduction to Data
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
- sample.html
server:
  imports: |
        import random
        import pandas as pd
        import problem_bank_helpers as pbh
  generate: |
        data2 = pbh.create_data2()

        data2["params"]["vars"]["title"] = "Parameters and statistics"


        # Randomize Variables
        part1_num1 = random.randint(45,55)
        part1_num2 = 2007
        part1_num3 = 2008
        part1_num4 = random.randint(12,17) * 100  # 1500.0
        part1_num5 = random.randint(55,65)  # 58.0
        part2_num1 = 2001
        part2_num2 = round(random.uniform(2.80, 4.00), 2)  # 3.37
        part2_num3 = random.randint(150,300)  # 203.0
        part2_num4 = round(random.uniform(2.90, 4.50), 2)  # 3.59
        part1_nums = [part1_num1, part1_num2, part1_num3, part1_num4, part1_num5]
        part2_nums = [part2_num1, part2_num2, part2_num3, part2_num4]
        all_parts = [[part1_nums, 1, 5], [part2_nums, 2, 4]]

        # store the variables in the dictionary "params"
        data2['params']['part1']['num1'] = part1_num1
        data2['params']['part1']['num2'] = part1_num2
        data2['params']['part1']['num3'] = part1_num3
        data2['params']['part1']['num4'] = part1_num4
        data2['params']['part1']['num5'] = part1_num5
        data2['params']['part2']['num1'] = part2_num1
        data2['params']['part2']['num2'] = part2_num2
        data2['params']['part2']['num3'] = part2_num3
        data2['params']['part2']['num4'] = part2_num4

        matching = {
              'statements': [
                {'value': 'Claimed population mean', 'matches': 'option2' },
                {'value': 'Sample mean', 'matches': 'option1' },
              ],
            }
        for i, part in enumerate(all_parts):
          for (j, value) in enumerate(part[0]):
            data2["params"][f"part{i+1}"][f"option{j+1}"]["value"] = value
          for (s_num, statement_info) in enumerate(matching['statements']):
            data2["params"][f"part{i+1}"][f"statement{s_num+1}"]["value"] = statement_info["value"]
            data2["params"][f"part{i+1}"][f"statement{s_num+1}"]["matches"] = f"option{part[s_num+1]}"

        # Update the data object with a new dict
        data.update(data2)
  prepare: |
        pass
  parse: |
        pass
  grade: |
        pass
part1:
  type: matching
  showCorrectAnswer: true
  pl-customizations:
    weight: 1
    blank: true
part2:
  type: matching
  showCorrectAnswer: true
  pl-customizations:
    weight: 1
    blank: true
---
# {{ params.vars.title }}

Identify which value represents the sample mean and which value represents the claimed population mean.


## Part 1

American households spent an average of about \$${{ params.part1.num1 }}$ in ${{ params.part1.num2 }}$ on Halloween merchandise such as costumes, decorations and candy. To see if this number had changed, researchers conducted a new survey in ${{ params.part1.num3 }}$ before industry numbers were reported. The survey included ${{ params.part1.num4 }}$ households and found that average Halloween spending was \$${{ params.part1.num5 }}$ per household.

### Answer Section



### pl-answer-panel

Part 1: Population mean, $\mu_{2007} = {{ params.part1.num1 }}$; sample mean, $\bar{x}_{2008} = {{ params.part1.num5 }}$


## Part 2

The average GPA of students in ${{ params.part2.num1 }}$ at a private university was ${{ params.part2.num2 }}$. A survey on a sample of ${{ params.part2.num3 }}$ students from this university yielded an average GPA of ${{ params.part2.num4 }}$ a decade later.

### Answer Section



### pl-answer-panel

Part 2: Population mean, $\mu_{2001} = {{ params.part2.num2 }}$; sample mean, $\bar{x}_{2012} = {{ params.part2.num4 }}$


## Rubric

This should be hidden from students until after the deadline.
