---
title: Variance of a mean, Part I + Part III
topic: Probability
author: Christina Yang
source: original
template_version: 1.4
attribution: openintro-stats
partialCredit: true
singleVariant: false
showCorrectAnswer: true
outcomes:
- 3.1.1.14
- 3.1.1.15
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
        import sympy as sp
        import prairielearn as pl
        import problem_bank_helpers as pbh
  generate: |
        data2 = pbh.create_data2()

        data2["params"]["vars"]["title"] = "Variance of a mean, Part I + Part III"

        variants = [
            {
                  'description': 'Suppose we have independent observations $X_1$ and $X_2$ from a distribution with mean $\mu$ and standard deviation $\sigma$.',
                  'question': r'What is the variance of the mean of the two values: $\frac{X_1 + X_2}{2}$?',
                  'answer': r'$Var\left(\frac{X_1 + X_2}{2}\right)$  $= Var\left(\frac{X_1}{2} + \frac{X_2}{2}\right)$  $= \frac{Var(X_1)}{2^2} + \frac{Var(X_2)}{2^2}$  $= \frac{\sigma^2}{4} + \frac{\sigma^2}{4}$  $= \sigma^2 / 2$',
            },
            {
                  'description': 'Suppose we have $n$ independent observations $X_1$, $X_2$, ..., $X_n$ from a distribution with mean $\mu$ and standard deviation $\sigma$.',
                  'question': r'What is the variance of the mean of these $n$ values: $\frac{X_1 + X_2 + \dots + X_n}{n}$?',
                  'answer': r'$Var\left(\frac{X_1 + X_2 + \dots + X_n}{n}\right)$  $= Var\left(\frac{X_1}{n} + \frac{X_2}{n} + \dots + \frac{X_n}{n}\right)$  $= \frac{Var(X_1)}{n^2} + \frac{Var(X_2)}{n^2} + \dots + \frac{Var(X_n)}{n^2}$  $= \frac{\sigma^2}{n^2} + \frac{\sigma^2}{n^2} + \dots + \frac{\sigma^2}{n^2}$ (there are $n$ of these terms)  $= n \frac{\sigma^2}{n^2}$  $= \sigma^2 / n$'
            }
        ]

        variant = variants[random.randint(0, len(variants)-1)]

        data2['params']['description']['text'] = variant['description']
        data2['params']['part1']['question'] = variant['question']
        data2['params']['part1']['correct_text'] = variant['answer']

        # Randomize Variables

        # store the variables in the dictionary "params"

        mu, sg, n = sp.symbols('mu sg n')

        # Describe the solution equation
        F = sg**2/n

        # Answer to fill in the blank input stored as JSON.
        data2['correct_answers']['part1_ans'] = pl.to_json(F)

        # Update the data object with a new dict
        data.update(data2)
  prepare: |
        pass
  parse: |
        pass
  grade: |
        pass
part1:
  type: symbolic-input
  pl-customizations:
    label: $\sigma^2 = $
    variables: "mu, sg, n"
    weight: 1
    allow-blank: false
---
# {{ params.vars.title }}

{{ params.description.text }}


| For  | Use   |
|----------|-------|
| $\mu$  | mu  |
| $\sigma$  | sg  |
| $n$  | n  |
| $X_i$  | xi  |

## Part 1

{{ params.part1.question }}

### Answer Section

Please enter a numeric value in.


### pl-answer-panel

Part 1: {{ params.part1.correct_text }}


## Rubric

This should be hidden from students until after the deadline.
