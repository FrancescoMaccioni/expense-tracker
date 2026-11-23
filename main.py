# Personal Expense Tracker - command-line application.

from decimal import Decimal, InvalidOperation

def menu(expenses):
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
            delete_expense(expenses)
        elif selector == "7":
            edit_expense(expenses)
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
    amount = read_positive_amount()
    category = read_non_empty_text("Insert expense category: ")
    description = read_non_empty_text("Insert expense description: ")
    expense = {"amount":amount, "category":category, "description":description}
    expenses.append(expense)
    print("Your expense is added!")


def display_expenses(expenses):
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
    total = Decimal("0.00")
    for expense in expenses:
        total += expense["amount"]
    return total


def calculate_totals_by_category(expenses):
    totals = {}
    for expense in expenses:
        if expense["category"] in totals:
            totals[expense["category"]] += expense["amount"]
        else:
            totals[expense["category"]] = expense["amount"]
    return totals     


def filter_expenses_by_category(expenses, category):
    expenses_by_category = []
    for expense in expenses:
        if expense["category"] == category:
            expenses_by_category.append(expense)   
    return expenses_by_category


def delete_expense(expenses):
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
                break
        else:
            print("No expenses recorded!")
            break
        

def edit_expense(expenses):
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
                break
        else:
            print("No expenses recorded!")
            break


def read_positive_amount(allow_zero=False):
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
        rounded_amount = amount.quantize(Decimal("0.01"))
        if amount != rounded_amount:
            print("Please insert an amount with at most two decimal places!")
            continue
        return rounded_amount


def read_non_empty_text(prompt):
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Please insert a non-empty value!")


def search_by_description(expenses):
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


def main():
    expenses_list = []

    try:
        menu(expenses_list)
    except (EOFError, KeyboardInterrupt):
        print("\nProgram closed.")


if __name__ == "__main__": 
    main()