import sqlite3
from datetime import datetime

class ExpenseTracker:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect_to_db()

    def connect_to_db(self):
        """initialize connection to the sqlite"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """create necessary tables"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget (
                category TEXT PRIMARY KEY,
                amount REAL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                amount REAL,
                date TEXT
            )
        ''')
        self.conn.commit()

    def add_budget(self, category, amount):
        """insert or update the budget for a category."""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO budget (category, amount)
                VALUES (?, ?)
            ''', (category.lower(), amount))
            self.conn.commit()
            print(f"Budget for {category} set to Rs {amount}.")
        except sqlite3.Error as e:
            print(f"Error setting budget: {e}")

    def add_expense(self, category, amount, date=None):
        """add an expense to a category."""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        try:
            self.cursor.execute('''
                INSERT INTO expenses (category, amount, date)
                VALUES (?, ?, ?)
            ''', (category.lower(), amount, date))
            self.conn.commit()
            print(f"Expense of Rs {amount} added to {category}.")
        except sqlite3.Error as e:
            print(f"Error adding expense: {e}")

    def display_budget_summary(self):
        """display the budget summary with remaining amounts."""
        self.cursor.execute('SELECT category, amount FROM budget')
        budgets = self.cursor.fetchall()

        for category, budget_amount in budgets:
            self.cursor.execute('SELECT SUM(amount) FROM expenses WHERE category = ?', (category,))
            result = self.cursor.fetchone()
            total_expenses = result[0] if result[0] else 0
            remaining = budget_amount - total_expenses
            print(f"{category.capitalize()}: Budget = Rs {budget_amount}, Spent = Rs {total_expenses}, Remaining = Rs {remaining}")

    def close_connection(self):
        """close the sqlite database connection."""
        if self.conn:
            self.conn.close()



def main():
    #create or select database
    db_name = input("Enter the name of the database (or create a new one): ")
    tracker = ExpenseTracker(db_name)

    while True:
        print("\n1. Add/Update Budget")
        print("2. Add Expense")
        print("3. Display Budget Summary")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            category = input("Enter the budget category: ")
            amount = float(input("Enter the budget amount: "))
            tracker.add_budget(category, amount)

        elif choice == '2':
            category = input("Enter the expense category: ")
            amount = float(input("Enter the expense amount: "))
            date = input("Enter the date (YYYY-MM-DD) or press Enter for today: ")
            tracker.add_expense(category, amount, date)

        elif choice == '3':
            tracker.display_budget_summary()

        elif choice == '4':
            tracker.close_connection()
            print("Exiting the application.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
