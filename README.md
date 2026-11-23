# Personal Expense Tracker

A command-line application for managing personal expenses.

## Features

The program allows you to:
- Add expenses with an amount, category, and description
- Display recorded expenses
- Calculate the overall total and totals by category
- Filter expenses by category or amount range
- Search descriptions without case sensitivity
- Delete or edit an expense
- Calculate the expense count, total, average, minimum, and maximum

## Requirements

Python 3. No external packages required

## How to run 

Open the terminal in the project folder and run `python main.py`

## Input validation

- Expense amounts must be positive and have at most two decimal places.
- The maximum accepted amount is 999999999.99 EUR.

## Limitations

- Data is stored in memory and lost when the program closes.
- Category matching is case-sensitive.

