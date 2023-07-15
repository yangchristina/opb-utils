---
title: American roulette
topic: Probability
author: Christina Yang
source: original
template_version: 1.4
attribution: openintro-stats
partialCredit: true
singleVariant: false
showCorrectAnswer: false
outcomes:
- 3.1.1.14  # Expected value and variance of a discrete random variable, X, can be calculated.
- 3.1.1.15  # Standard deviation is the square root of variance. We use standard deviation also as a measure of the variability of the random variable. Standard deviation is often easier to interpret since it's in the same units of the random variable.
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

        data2["params"]["vars"]["title"] = "American roulette"


        # Randomize Variables
        description_num1 = 38  # 38
        description_num2 = 18  # 18
        description_num3 = description_num2
        description_num4 = 2  # 2
        description_num5 = random.randint(1, 10)  # 1

        # store the variables in the dictionary "params"
        data2['params']['description']['num1'] = description_num1
        data2['params']['description']['num2'] = description_num2
        data2['params']['description']['num3'] = description_num3
        data2['params']['description']['num4'] = description_num4
        data2['params']['description']['num5'] = description_num5

        bet_amount = description_num5
        profit = bet_amount
        loss = -1 * bet_amount
        expected_value = profit * 18/38 + loss * 20 / 38
        std = math.sqrt((profit-expected_value)**2*18/38+(loss-expected_value)**2*20/38)
        # Part 1 is a number-input question.
        data2['correct_answers']['part1_ans'] = expected_value  # TODO: insert correct answer here
        data2['params']['part1']['correct'] = round(expected_value, 4)

        # Part 2 is a number-input question.
        data2['correct_answers']['part2_ans'] = std  # TODO: insert correct answer here
        data2['params']['part2']['correct'] = round(std, 4)

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
    rtol: 0.001
    weight: 1
    allow-blank: true
    label: $E = \$$
part2:
  type: number-input
  pl-customizations:
    rtol: 0.001
    weight: 1
    allow-blank: true
    label: $SD = \$$
---
# {{ params.vars.title }}

The game of American roulette involves spinning a wheel with ${{ params.description.num1 }}$ slots: ${{ params.description.num2 }}$ red, ${{ params.description.num3 }}$ black, and ${{ params.description.num4 }}$ green. A ball is spun onto the wheel and will eventually land in a slot, where each slot has an equal chance of capturing the ball. Gamblers can place bets on red or black. If the ball lands on their color, they double their money. If it lands on another color, they lose their money. Suppose you bet \${{ params.description.num5 }} on red.

## Part 1

What's the expected value of your winnings? Round to 4 decimal places.

### Answer Section

Please enter a numeric value in.


### pl-answer-panel

Part 1: E = {{ params.part1.correct }}


## Part 2

What's the standard deviation of your winnings? Round to 4 decimal places.

### Answer Section

Please enter a numeric value in.


### pl-answer-panel

Part 2: SD = {{ params.part2.correct }}


## Rubric

This should be hidden from students until after the deadline.
