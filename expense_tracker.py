import mysql.connector
from tabulate import tabulate

conn = mysql.connector.connect(
    host="localhost", user=" root", password="shreya3112", database="expense_tracker"
)
cursor = conn.cursor()

def add_entry():
    date = input("Enter date (YYYY-MM-DD):")
    category = input("Enter category of expense:")
    amount = float(input("Enter amount spent:"))
    description = input("Enter description")
    
    if description.strip():
        cursor.execute("INSERT INTO expense(Date, Category, Amount, Description) VALUES (%s, %s, %s, %s)", (date, category, amount, description))
    else:
        cursor.execute("INSERT INTO expense(Date, Category, Amount) VALUES (%s, %s, %s)", (date, category, amount))

    conn.commit()
    print("Expense entry added!")

def view_entries():
    cursor.execute("SELECT * FROM expense")
    records = cursor.fetchall()

    if not records:
        print("No expenses recorded yet.")
        return
    
    print(tabulate(records, headers=["ID", "Date", "Category", "Amount", "Description"], tablefmt="grid"))

def del_entry():
    view_entries()
    expense_id = int(input("Enter the ID of expense:"))
    cursor.execute("DELETE FROM expense WHERE id=%s", (expense_id,))
    conn.commit()
    print("Entry deleted successfully!")

while True:
    print("Expense Tracker using MySQL")
    print("\nPress (1) to add entry")
    print("\nPress (2) to view all entries")
    print("\nPress (3) to delete entry")
    print("\nPress (4) to exit.")

    choice = int(input("Choose your option: "))

    if choice == 1:
        add_entry()
    elif choice == 2:
        view_entries()
    elif choice == 3:
        del_entry()
    elif choice == 4:
        print("Exited Program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a valid input.")

cursor.close()