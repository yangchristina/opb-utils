---
title: Variance of a mean, Part III
topic: Probability
author: Christina Yang
source: original
template_version: 1.4
attribution: openintro-stats
partialCredit: true
singleVariant: false
showCorrectAnswer: true
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
        import sympy as sp
        import prairielearn as pl
        import problem_bank_helpers as pbh
  generate: |
        data2 = pbh.create_data2()

        data2["params"]["vars"]["title"] = "Variance of a mean, Part III"


        # Randomize Variables

        # store the variables in the dictionary "params"

        # Part 1 is a number-input question.
        data2['correct_answers']['part1_ans'] = 0  # TODO: insert correct answer here

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

Suppose we have $n$ independent observations $X_1$, $X_2$, ..., $X_n$ from a distribution with mean $\mu$ and standard deviation $\sigma$.

| For  | Use   |
|----------|-------|
| $\mu$  | mu  |
| $\sigma$  | sg  |
| $n$  | n  |
| $X_1$  | x1  |
| $X_n$  | xn  |

## Part 1

What is the variance of the mean of these $n$ values: $\frac{X_1 + X_2 + \dots + X_n}{n}$? .

### Answer Section

Please enter a numeric value in.


### pl-answer-panel

Part 1: $Var\left(\frac{X_1 + X_2 + \dots + X_n}{n}\right)$
  $= Var\left(\frac{X_1}{n} + \frac{X_2}{n} + \dots +
      \frac{X_n}{n}\right)$
  $= \frac{Var(X_1)}{n^2} + \frac{Var(X_2)}{n^2} + \dots +
      \frac{Var(X_n)}{n^2}$
  $= \frac{\sigma^2}{n^2} + \frac{\sigma^2}{n^2} + \dots +
      \frac{\sigma^2}{n^2}$ (there are $n$ of these terms)
  $= n \frac{\sigma^2}{n^2}$
  $= \sigma^2 / n$


## Rubric

This should be hidden from students until after the deadline.
