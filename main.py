import sqlite3

# database connection
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# make table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT
)
""")

conn.commit()


# expense class
class Expense:
    def __init__(self, amount, category):
        self.amount = amount
        self.category = category

    def __str__(self):
        return str(self.amount) + " - " + self.category


# child class
class FoodExpense(Expense):
    def __str__(self):
        return "Food: " + str(self.amount) + " - " + self.category


# menu
def menu():
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Update Expense")
    print("4. Delete Expense")
    print("5. Exit")


# main loop
running = True

while running:
    menu()

    choice = input("Choose option: ")

    # add expense
    if choice == "1":

        try:
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")

            # object example
            if category.lower() == "food":
                expense = FoodExpense(amount, category)
            else:
                expense = Expense(amount, category)

            # save to database
            cursor.execute(
                "INSERT INTO expenses (amount, category) VALUES (?, ?)",
                (expense.amount, expense.category)
            )

            conn.commit()

            print("Expense added")

        except:
            print("Invalid input")

    # show expenses
    elif choice == "2":

        cursor.execute("SELECT * FROM expenses")

        expenses = cursor.fetchall()

        print("\nExpenses:")

        for item in expenses:
            print(
                "ID:",
                item[0],
                "| Amount:",
                item[1],
                "| Category:",
                item[2]
            )

    # update
    elif choice == "3":

        try:
            expense_id = int(input("Enter ID: "))
            new_amount = float(input("New amount: "))
            new_category = input("New category: ")

            cursor.execute(
                "UPDATE expenses SET amount=?, category=? WHERE id=?",
                (new_amount, new_category, expense_id)
            )

            conn.commit()

            print("Expense updated")

        except:
            print("Could not update")

    # delete
    elif choice == "4":

        try:
            expense_id = int(input("Enter ID to delete: "))

            cursor.execute(
                "DELETE FROM expenses WHERE id=?",
                (expense_id,)
            )

            conn.commit()

            print("Expense deleted")

        except:
            print("Could not delete")

    # exit
    elif choice == "5":

        print("Program ended")
        running = False

    else:
        print("Invalid option")


conn.close()
