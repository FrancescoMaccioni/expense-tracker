# Personal Expense Tracker - command-line application.


from decimal import Decimal, InvalidOperation
from pathlib import Path
import json
import os


# Keep the data file beside this script, regardless of the working directory.
EXPENSES_FILE = str(Path(__file__).resolve().parent / "expenses.json")


def menu(expenses):
    """Run the menu and save expenses after additions, edits, and deletions."""
    open_menu = True
    while open_menu:
        print(
            "\nMenu of the program:\n"
            "1 - Add expenses\n"
            "2 - Display existing expenses\n"
            "3 - Total of all expenses\n"
            "4 - Totals by category\n"
            "5 - Expenses by category\n"
            "6 - Delete expense\n"
            "7 - Edit expense\n"
            "8 - Search by description\n"
            "9 - Statistics about your expenses\n"
            "10 - Filter expenses by amount\n"
            "0 - Exit program\n"
        )
        selector = input("Please select an option: ").strip()
        if selector == "1":
            add_expense(expenses)
            save_expenses_with_feedback(expenses, EXPENSES_FILE) 
        elif selector == "2":
            display_expenses(expenses)
        elif selector == "3":
            print(f"Total of all expenses is: {calculate_total(expenses):.2f} EUR")
        elif selector == "4":
            totals = calculate_totals_by_category(expenses)
            if totals:
                for key in totals.keys():
                    print(f"{key}: {totals[key]:.2f} EUR")
            else: print("No expenses recorded")
        elif selector == "5":
            category = read_non_empty_text("Enter the category: ")
            expenses_by_category = filter_expenses_by_category(expenses, category)
            if expenses_by_category:
                display_expenses(expenses_by_category)
            else: print("No expenses found for this category!")
        elif selector == "6":
            outcome = delete_expense(expenses)
            if outcome:
                save_expenses_with_feedback(expenses, EXPENSES_FILE)
        elif selector == "7":
            outcome = edit_expense(expenses)
            if outcome:
                save_expenses_with_feedback(expenses, EXPENSES_FILE)           
        elif selector == "8":
            search_by_description(expenses)
        elif selector == "9":
            statistics(expenses)
        elif selector == "10":
            filter_by_amount(expenses)
        elif selector == "0":
            open_menu = False
        else:
            print("Please provide a valid option!")


def add_expense(expenses):
    """Read a valid expense and append it to the list in memory."""
    amount = read_positive_amount()
    category = read_non_empty_text("Insert expense category: ")
    description = read_non_empty_text("Insert expense description: ")
    expense = {"amount":amount, "category":category, "description":description}
    expenses.append(expense)
    print("Your expense is added!")


def display_expenses(expenses):
    """Display numbered expenses, or a message when the list is empty."""
    i = 1
    if expenses:
        for expense in expenses:
            print(
                f'{i} | Amount: {expense["amount"]:.2f} EUR'
                f' | Category: {expense["category"]}'
                f' | Description: {expense["description"]}'
            )
            i += 1
    else: 
        print("No expenses recorded.")


def calculate_total(expenses):
    """Return the total amount as a Decimal; return zero for an empty list."""
    total = Decimal("0.00")
    for expense in expenses:
        total += expense["amount"]
    return total


def calculate_totals_by_category(expenses):
    """Return a dictionary mapping each category to its total amount."""
    totals = {}
    for expense in expenses:
        if expense["category"] in totals:
            totals[expense["category"]] += expense["amount"]
        else:
            totals[expense["category"]] = expense["amount"]
    return totals     


def filter_expenses_by_category(expenses, category):
    """Return matching expenses using an exact, case-sensitive category comparison."""
    expenses_by_category = []
    for expense in expenses:
        if expense["category"] == category:
            expenses_by_category.append(expense)   
    return expenses_by_category


def delete_expense(expenses):
    """Delete a selected expense; return True on deletion or False if canceled or empty."""
    while True:
        if expenses:
            print("0 | Back to menu")
            display_expenses(expenses)
            try:
                selector = int(input("Select the expense you want to delete: "))
            except ValueError:
                print("Please insert a valid number!\n")
                continue
            if selector > len(expenses) or selector < 0:
                print("Please insert a valid number!\n")
            elif selector == 0:
                break
            else:
                del expenses[selector-1]
                return True
        else:
            print("No expenses recorded!")
            break
    return False
        

def edit_expense(expenses):
    """Replace a selected expense; return True on update or False if canceled or empty."""
    while True:
        if expenses:
            print("0 | Back to menu")
            display_expenses(expenses)
            try:
                selector = int(input("Select the expense you want to edit: "))
            except ValueError:
                print("Please insert a valid number!\n")
                continue
            if selector > len(expenses) or selector < 0:
                print("Please insert a valid number!\n")
            elif selector == 0:
                break
            else:
                amount = read_positive_amount()
                category = read_non_empty_text("Insert expense new category: ")
                description = read_non_empty_text("Insert expense new description: ")
                new_expense = {"amount":amount, "category":category, "description":description}
                expenses[selector-1] = new_expense
                print("Your expense is updated!")
                return True
        else:
            print("No expenses recorded!")
            break
    return False


def read_positive_amount(allow_zero=False):
    """Read a finite amount within the allowed range, rejecting fractions below one cent. Allow zero only when requested."""
    while True:
        try:
            amount = Decimal(input("Insert expense amount: ").strip())
        except InvalidOperation:
            print("This is not a valid amount, please insert a numeric value!")
            continue
        if not amount.is_finite():
            print("Please insert a finite amount!")
            continue
        if amount < 0 or (amount == 0 and not allow_zero):
            if allow_zero:
                print("This is not a valid amount, please insert a non-negative value!")
            else:
                print("This is not a valid amount, please insert a positive value!")
            continue
        if amount > Decimal("999999999.99"):
            print("Maximum allowed amount: 999999999.99 EUR")
            continue
        # Normalize to cents, then reject any amount whose value would change.
        rounded_amount = amount.quantize(Decimal("0.01"))
        if amount != rounded_amount:
            print("Please insert an amount with at most two decimal places!")
            continue
        return rounded_amount


def read_non_empty_text(prompt):
    """Read text, strip surrounding whitespace, and retry until it is non-empty."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Please insert a non-empty value!")


def search_by_description(expenses):
    """Display expenses whose descriptions contain the search text, ignoring case."""
    expenses_by_description = []
    while True:
        description = read_non_empty_text("Enter the words or descriptions to search for: ")
        find = False
        if description:
            for expense in expenses:
                current_description = expense["description"]
                if description.lower() in current_description.lower():
                    find = True
                    expenses_by_description.append(expense)
            if find:
                print("Here the list of corresponding expenses:")
                display_expenses(expenses_by_description)
                break
            else:
                print("No corresponding expense found!")
                break
        else:
            print("Please provide a valid string to be searched!")
            continue


def calculate_statistics(expenses):
    """Return expense count, total, mean, minimum, and maximum; return None if empty."""
    if not expenses:
        return None
    number_of_expenses = len(expenses)
    total = Decimal("0.00")
    min_expense = expenses[0]["amount"]
    max_expense = expenses[0]["amount"]
    for expense in expenses:
        total += expense["amount"]
        if expense["amount"] < min_expense:
            min_expense = expense["amount"]
        if expense["amount"] > max_expense:
            max_expense = expense["amount"]
    mean = total / number_of_expenses
    return {
        "number": number_of_expenses,
        "total": total,
        "min": min_expense,
        "max": max_expense,
        "mean": mean,
    }


def statistics(expenses):
    """Display expense statistics, or a message when no expenses are recorded."""
    expense_statistics = calculate_statistics(expenses)
    if expense_statistics is None:
        print("No expenses recorded! Add some expenses to have statistics!")
        return
    print("Here are some statistics about your expenses:")
    print("Number of expenses:", expense_statistics["number"])
    print(f'Total amount of expenses: {expense_statistics["total"]:.2f} EUR')
    print(f'Mean expense: {expense_statistics["mean"]:.2f} EUR')
    print(f'Minimum expense: {expense_statistics["min"]:.2f} EUR')
    print(f'Maximum expense: {expense_statistics["max"]:.2f} EUR')


def filter_by_amount(expenses):
    """Read an inclusive amount range and display matching expenses."""
    expenses_by_amount = []
    while True:
        print("Insert minimum expense amount")
        minimum = read_positive_amount(allow_zero=True)
        print("Insert maximum expense amount")
        maximum = read_positive_amount(allow_zero=True)
        if maximum < minimum:
            print("Minimum value can't be greater than maximum value!")
            continue
        for expense in expenses:
            if minimum <= expense["amount"] <= maximum:
                expenses_by_amount.append(expense)
        if expenses_by_amount:
            display_expenses(expenses_by_amount)
        else:
            print("No expenses with this filter!")
        return
    

def expenses_for_json(expenses):
    """Return new expense dictionaries with amounts converted to strings for JSON storage."""
    json_expenses = []
    for expense in expenses:
        # Store monetary amounts as strings to preserve their exact decimal values.
        new_amount = str(expense["amount"])
        new_dictionary = {"amount": new_amount,
                          "category": expense["category"],
                          "description": expense["description"]}
        json_expenses.append(new_dictionary)
    return json_expenses


def validate_and_convert_expenses(loaded_data):
    """Validate loaded data and return new expense dictionaries.
    
    Convert amount strings to Decimal values normalized to cents.
    Leave the input unchanged and raise ValueError for invalid data.
    """
    validated_expenses = []
    if not isinstance(loaded_data, list):
        raise ValueError("Expenses must be a list.")
    for expense_data in loaded_data:
        if not isinstance(expense_data, dict):
            raise ValueError("Each expense must be a dictionary.")
        if "amount" not in expense_data or "category" not in expense_data or "description" not in expense_data:
            raise ValueError("Each expense must contain all necessary keys.")
        if not isinstance(expense_data["amount"], str) or not isinstance(expense_data["category"], str) or not isinstance(expense_data["description"], str):
            raise ValueError("Each expense key must contain a string value.")
        if expense_data["category"].strip() == "" or expense_data["description"].strip() == "":
            raise ValueError("Expense category and description can't be empty or only a space.")
        try:
            new_amount = Decimal(expense_data["amount"])
        except InvalidOperation:
            raise ValueError("Amount must contain a valid numeric value.")
        # Decimal accepts NaN and infinity, so reject them before numeric comparisons.
        if not new_amount.is_finite():
            raise ValueError("Amount must contain a finite value.")
        if new_amount <= 0 or new_amount > Decimal("999999999.99"):
            raise ValueError("The amount must be greater than zero and less or equal to 999999999.99.")
        # Normalize to cents, then reject any amount whose value would change.
        rounded_amount = new_amount.quantize(Decimal("0.01"))
        if new_amount != rounded_amount:
            raise ValueError("Amount must be at most two decimal places.")
        new_dictionary = {"amount": rounded_amount,
                          "category": expense_data["category"],
                          "description": expense_data["description"]}
        validated_expenses.append(new_dictionary)
    return validated_expenses


def load_expenses(filename):
    """Load and validate expenses from a UTF-8 JSON file.

    Return an empty list if the file does not exist.
    Propagate other read, JSON decoding, and validation errors to the caller.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            expense_data = json.load(file)
    except FileNotFoundError:
        expense_data = []
    validated_expenses = validate_and_convert_expenses(expense_data)
    return validated_expenses


def save_expenses(expenses, filename):
    """Write expenses to a temporary file, then replace the destination.

    Keep the previous destination intact if writing the temporary file fails.
    Propagate save errors and attempt to clean up the temporary file.
    """
    temp_file = filename + ".tmp"
    loaded_data = expenses_for_json(expenses)
    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(loaded_data, file, indent=4, ensure_ascii=False)
        # Replace the destination only after the temporary file has been written and closed.
        os.replace(temp_file, filename)
    finally:
        # Cleanup is best effort: it must not hide the original save error.
        try:
            os.remove(temp_file)
        except OSError:
            pass


def save_expenses_with_feedback(expenses, filename):
    """Save expenses and report success or an OSError; failed saves leave changes in memory."""
    try:
        save_expenses(expenses, filename)
    except OSError:
        print("Save failed. Changes are available in memory but have not been saved to disk.")
    else:
        print("Changes saved.")


def main():
    """Load expenses and start the menu only if loading succeeds. Handle user interruptions during menu execution."""
    try:
        # Stop on load errors rather than risk overwriting existing data with an empty list.
        loaded_expenses = load_expenses(EXPENSES_FILE)
    except json.JSONDecodeError:
        print("Cannot load expenses: the file contains invalid JSON.")
    except ValueError:
        print("Cannot load expenses: the file contains invalid values.")
    except OSError:
        print("Cannot load expenses: unable to read the file.")
    else:
        try:
            menu(loaded_expenses)
        except (EOFError, KeyboardInterrupt):
            print("\nProgram closed.")


if __name__ == "__main__": 
    main()