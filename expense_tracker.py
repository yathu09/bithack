import sqlite3

#to create the sqlite database
def create_database():
    conn = sqlite3.connect('expense_tracker.db')  
    cursor = conn.cursor()

    #budget table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            category TEXT PRIMARY KEY,  -- Category name as the primary key
            amount REAL                -- Budget amount for the category
        )
    ''')

    #expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each expense
            category TEXT,                         -- Category of the expense
            amount REAL,                           -- Amount spent
            date TEXT                              -- Date of the expense
        )
    ''')

    #constant budget 
    budget_data = [
        ('food', 5000),         
        ('dress', 3000),        
        ('healthcare', 2000),   
        ('transport', 1500),    
        ('entertainment', 2500),
        ('housekeeping', 1000)  
    ]

    #for const budget amounts
    cursor.executemany('INSERT OR IGNORE INTO budget (category, amount) VALUES (?, ?)', budget_data)
    
    conn.commit() 
    conn.close()  

#to insert expenses
def insert_expense(category, amount, date):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)', (category, amount, date))
    conn.commit()
    conn.close()

#to get total expenses
def get_total_expenses(category):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM expenses WHERE category = ?', (category,))
    result = cursor.fetchone()
    conn.close()

    # Ensure the result is returned as a float or 0 if no expenses exist
    return float(result[0]) if result[0] is not None else 0.0

#to get the budget 
def get_budget(category):
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT amount FROM budget WHERE category = ?', (category,))
    result = cursor.fetchone()
    conn.close()

    #for float result
    return float(result[0]) if result else 0.0

#to calculate remaining budget
def calculate_remaining_budget(category):
    budget = get_budget(category)
    total_expenses = get_total_expenses(category)
    if budget is not None:
        return budget - total_expenses
    else:
        return None

#to check if the budget is exceeded
def check_budget_exceeded(category):
    remaining = calculate_remaining_budget(category)
    if remaining is not None and remaining < 0:
        print(f"Alert! You have exceeded your budget for {category}.")
    else:
        print(f"You are within budget for {category}.")

#to display budget summary
def display_budget_summary():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category, amount FROM budget')
    budgets = cursor.fetchall()

    for category, amount in budgets:
        total_expenses = get_total_expenses(category)
        remaining = amount - total_expenses
        print(f"{category.capitalize()}: Budget = Rs {amount}, Spent = Rs {total_expenses}, Remaining = Rs {remaining}")

    conn.close()

#to create the database and tables
create_database()

#  usage
insert_expense('food', 50, '2024-09-25')
insert_expense('dress', 3000, '2024-09-26')
insert_expense('healthcare', 100, '2024-09-26')
insert_expense('transport', 200, '2024-09-27')
insert_expense('entertainment', 300, '2024-09-28')
insert_expense('housekeeping', 200, '2024-09-29')

# show budget summary
display_budget_summary()

#budget check
check_budget_exceeded('food')
check_budget_exceeded('dress')
check_budget_exceeded('healthcare')
check_budget_exceeded('transport')
check_budget_exceeded('entertainment')
check_budget_exceeded('housekeeping')
