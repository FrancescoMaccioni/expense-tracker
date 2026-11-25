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

## Usage example

Select `1` to add an expense and enter:

- Amount: `12.50`
- Category: `Transport`
- Description: `Train ticket`

Select `2` to display recorded expenses, or `3` to calculate the total.

## Input validation

- Expense amounts must be positive and have at most two decimal places.
- The maximum accepted amount is 999999999.99 EUR.

# Data storage

Expenses are loaded from `expenses.json` at startup and saved automatically
after adding, editing, or deleting an expense.

The data file is stored beside `main.py`, regardless of the directory
from which the application is started. It is excluded from Git.

Amounts are stored as strings and converted to Python Decimal values
when loaded. Invalid files stop startup without being overwritten.

Saving uses a temporary file before replacing the previous data file.
If saving fails, changes remain in memory but may be lost when the
application closes.

## Limitations

- Category matching is case-sensitive.
- Concurrent use by multiple application instances is not supported.

