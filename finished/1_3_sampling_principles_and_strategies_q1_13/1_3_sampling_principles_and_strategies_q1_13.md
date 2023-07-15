---
title: Scope of inference
topic: Introduction to Data
author: Christina Yang
source: original
template_version: 1.4
attribution: openintro-stats
partialCredit: true
singleVariant: false
showCorrectAnswer: true
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
- sample.html
server:
  imports: |
        import random
        import pandas as pd
        import problem_bank_helpers as pbh
  generate: |
        data2 = pbh.create_data2()

        data2["params"]["vars"]["title"] = "Scope of inference"


        # Randomize Variables
        description_num1 = random.randint(128877, 157515)  #143196
        description_num2 = 1989  #1989
        description_num3 = 1993  #1993

        description2_num1 = random.randint(540, 660)  #600
        data2['params']['description2']['num1'] = description2_num1

        # store the variables in the dictionary "params"
        data2['params']['description']['num1'] = description_num1
        data2['params']['description']['num2'] = description_num2
        data2['params']['description']['num3'] = description_num3

        variants = [
          {
            'question_number': '1.13',
            'description': f'In a study, researchers collected data to examine the relationship between air pollutants and preterm births in Southern California. During the study air pollution levels were measured by air quality monitoring stations. Length of gestation data were collected on ${ description_num1 }$ births between the years ${ description_num2 }$ and ${ description_num3 }$, and air pollution exposure during gestation was calculated for each birth.',
            'part2': {
              'answer': 'If births in this time span at the geography can be considered to be representative of all births, then the results are generalizable to the population of Southern California. However, since the study is observational the findings cannot be used to establish causal relationships.'
            },
            'part1': {
              'options': [
                'All births',
                f'${ description_num1 }$ births between ${ description_num2 }$ and ${ description_num3 }$ in Southern California'
                'Air pollution exposure during gestation',
                'Air quality monitoring stations',
                'Length of gestation',
              ],
            },
          },
            {
            'question_number': '1.15',
            'description': f'As part of a study on using the Buteyko shallow breathing technique to reduce asthma symptoms and improve quality of life, ${ description2_num1 }$ asthma patients aged 18-69 who relied on medication for asthma treatment were recruited and randomly assigned to two groups: one practiced the Buteyko method and the other did not. Those in the Buteyko group experienced, on average, a significant reduction in asthma symptoms and an improvement in quality of life.',
            'part2': {
              'answer': 'If the patients in this sample, who are likely not randomly sampled, can be considered to be representative of all asthma patients aged 18-69 who rely on medication for asthma treatment, then the results are generalizable to the population defined above. Additionally, since the study is experimental, the findings can be used to establish causal relationships.'
            },
            'part1': {
              'options': [
                'All asthma patients aged 18-69 who rely on medication for asthma treatment',
                f'{ description2_num1 } asthma patients',
                'The group that practiced Buteyko',
                'The group that did not practice Buteyko',
              ],
            },
          }
        ]
        variant = variants[random.randint(0, len(variants)-1)]

        data2['params']['description']['text'] = variant['description']

        data2['params']['part2']['correct_text'] = variant["part2"]['answer']

        matching = {
              'statements': [
                {'value': 'Population of interest', 'matches': 'option1' },
                {'value': 'Sample', 'matches': 'option2' },
              ],
            }
        i = 0
        for (j, value) in enumerate(variant['part1'][f'options']):
            data2["params"][f"part{i+1}"][f"option{j+1}"]["value"] = value
        for (s_num, statement_info) in enumerate(matching['statements']):
            data2["params"][f"part{i+1}"][f"statement{s_num+1}"]["value"] = statement_info["value"]
            data2["params"][f"part{i+1}"][f"statement{s_num+1}"]["matches"] = statement_info["matches"]

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
  type: longtext
  gradingMethod: Manual
  pl-customizations:
    placeholder: "Type your answer here..."
    file-name: "answer2.html"
    quill-theme: "snow"
    directory: clientFilesQuestion
    source-file-name: sample.html
---
# {{ params.vars.title }}

{{ params.description.text }}


## Part 1

Identify the population of interest and the sample in this study.

### Answer Section


## Part 2

Comment on whether or not the results of the study can be generalized to the population, and if the findings of the study can be used to establish causal relationships.

### Answer Section



### pl-answer-panel

Part 2: {{ params.part2.correct_text }}


## Rubric

This should be hidden from students until after the deadline.
