import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()


conn = mysql.connector.connect(
    host="localhost",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
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
        print("Oh, it's empty here. Fill in some records!")
        return
    
    df = pd.DataFrame(records, columns=["ID", "Date", "Category", "Amount", "Description"])
    print(df.to_string(index=False))

    total = df["Amount"].sum()
    print("\nTotal expenses:", total)

def del_entry():
    view_entries()
    expense_id = int(input("Enter the ID of expense:"))
    cursor.execute("DELETE FROM expense WHERE id=%s", (expense_id,))
    conn.commit()
    print("Entry deleted successfully!")

def export_file():
    cursor.execute("SELECT * FROM expense")
    records = cursor.fetchall()

    if not records:
        print("It's empty here.")
        return

    df = pd.DataFrame(records, columns=["ID", "Date", "Category", "Amount", "Description"])

    file_name = "expenses_export.xlsx"
    df.to_excel(file_name, index=False)

    print(f"\nYour file is saved!")


while True:
    print("Expense Tracker using MySQL")
    print("\nPress (1) to add entry")
    print("\nPress (2) to view all entries")
    print("\nPress (3) to delete entry")
    print("\nPress (4) to export the records into excel file.")
    print("\nPress (5) to exit.")

    choice = int(input("Choose your option: "))

    if choice == 1:
        add_entry()
    elif choice == 2:
        view_entries()
    elif choice == 3:
        del_entry()
    elif choice == 4:
        export_file()
    elif choice == 5:
        print("Exited Program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a valid input.")

cursor.close()