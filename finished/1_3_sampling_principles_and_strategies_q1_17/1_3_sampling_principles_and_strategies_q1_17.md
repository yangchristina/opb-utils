---
title: Relaxing after work
topic: Introduction to Data
author: Christina Yang
source: original
template_version: 1.4
attribution: openintro-stats
partialCredit: true
singleVariant: false
showCorrectAnswer: false
outcomes:
- 1.1.1.4
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

        data2["params"]["vars"]["title"] = "Relaxing after work"

        # Randomize Variables
        part3_num1 = round(random.uniform(1.00, 2.50), 2)  # 1.65
        description_num1 = random.randint(1000, 1500)
        description_num2 = part3_num1

        # store the variables in the dictionary "params"
        data2['params']['part3']['num1'] = part3_num1
        data2['params']['description']['num1'] = description_num1
        data2['params']['description']['num2'] = description_num2

        matching = {
              'options': {
                'option1': 'Observation',
                'option2': 'Variable',
                'option3': 'Sample statistic',
                'option4': 'Population parameter',
              },
              'statements': [
                {'value': 'An American in the sample.', 'matches': 'option1' },
                {'value': 'Number of hours spent relaxing after an average work day.', 'matches': 'option2' },
                {'value': part3_num1, 'matches': 'option3' },
                {'value': 'Average number of hours all Americans spend relaxing after an average work day.', 'matches': 'option4' },
              ],
            }
        for (key, value) in matching["options"].items():
          data2["params"]["part1"][key]["value"] = value

        for (s_num, statement_info) in enumerate(matching['statements']):
          data2["params"]["part1"][f"statement{s_num+1}"]["value"] = statement_info["value"]
          data2["params"]["part1"][f"statement{s_num+1}"]["matches"] = statement_info["matches"]


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
---
# {{ params.vars.title }}

The General Social Survey asked the question, "After an average work day, about how many hours do you have to relax or pursue activities that you enjoy?" to a random sample of ${{ params.description.num1 }}$ Americans. The average relaxing time was found to be ${{ params.description.num2 }}$ hours. Determine which of the following is an observation, a variable, a sample statistic (value calculated based on the observed sample), or a population parameter.

## Part 1


### Answer Section


## Rubric

This should be hidden from students until after the deadline.
