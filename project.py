# Personal Finance Tracker
# Author: Beatriz Oliveira
# Course: LSN-0104 - Introduction to Programming with Python
# Hult International Business School - SUM1-2026
#
# AI Assistance: This project was developed with the help of Claude (Anthropic)
# as an AI coding assistant. The logic, design decisions, and understanding
# of the code are my own. Claude was used to help structure and debug the code.

import csv
import os
from datetime import datetime

DATA_FILE = "transactions.csv"
CATEGORIES = ["Food", "Transport", "Housing", "Health", "Entertainment", "Education", "Salary", "Other"]

def main():
    print("\n====================================")
    print("   💰 Personal Finance Tracker 💰   ")
    print("====================================")
    initialize_file()
    while True:
        print("\n--- MENU ---")
        print("1. Add transaction")
        print("2. View all transactions")
        print("3. View summary report")
        print("4. View spending by category")
        print("5. Exit")
        choice = input("\nChoose an option (1-5): ").strip()
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            summary_report()
        elif choice == "4":
            spending_by_category()
        elif choice == "5":
            print("\nGoodbye! Keep tracking your finances! 👋\n")
            break
        else:
            print("❌ Invalid option. Please choose between 1 and 5.")

def initialize_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "type", "category", "description", "amount"])
        print(f"📁 New finance file created: {DATA_FILE}")

def add_transaction():
    print("\n--- Add Transaction ---")
    t_type = input("Type (income/expense): ").strip().lower()
    if t_type not in ["income", "expense"]:
        print("❌ Invalid type. Please enter 'income' or 'expense'.")
        return
    print("Categories:", ", ".join(CATEGORIES))
    category = input("Category: ").strip().capitalize()
    if category not in CATEGORIES:
        print(f"❌ Invalid category. Choose from: {', '.join(CATEGORIES)}")
        return
    description = input("Description: ").strip()
    if not description:
        print("❌ Description cannot be empty.")
        return
    try:
        amount = float(input("Amount (e.g. 50.00): $").strip())
        if amount <= 0:
            print("❌ Amount must be greater than zero.")
            return
    except ValueError:
        print("❌ Invalid amount. Please enter a number.")
        return
    date = datetime.now().strftime("%Y-%m-%d")
    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, t_type, category, description, round(amount, 2)])
    print(f"✅ Transaction added: {t_type.capitalize()} of ${amount:.2f} ({category})")

def load_transactions():
    transactions = []
    if not os.path.exists(DATA_FILE):
        return transactions
    with open(DATA_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["amount"] = float(row["amount"])
            transactions.append(row)
    return transactions

def calculate_balance(transactions):
    balance = 0.0
    for t in transactions:
        if t["type"] == "income":
            balance += t["amount"]
        elif t["type"] == "expense":
            balance -= t["amount"]
    return round(balance, 2)

def calculate_total_by_type(transactions, t_type):
    total = sum(t["amount"] for t in transactions if t["type"] == t_type)
    return round(total, 2)

def calculate_average_expense(transactions):
    expenses = [t["amount"] for t in transactions if t["type"] == "expense"]
    if not expenses:
        return 0.0
    return round(sum(expenses) / len(expenses), 2)

def view_transactions():
    transactions = load_transactions()
    if not transactions:
        print("\n📭 No transactions recorded yet.")
        return
    print(f"\n{'Date':<12} {'Type':<10} {'Category':<15} {'Description':<20} {'Amount':>10}")
    print("-" * 70)
    for t in transactions:
        symbol = "+" if t["type"] == "income" else "-"
        print(f"{t['date']:<12} {t['type'].capitalize():<10} {t['category']:<15} {t['description']:<20} {symbol}${t['amount']:>8.2f}")
    print("-" * 70)
    print(f"Total transactions: {len(transactions)}")

def summary_report():
    transactions = load_transactions()
    if not transactions:
        print("\n📭 No transactions recorded yet.")
        return
    total_income = calculate_total_by_type(transactions, "income")
    total_expense = calculate_total_by_type(transactions, "expense")
    balance = calculate_balance(transactions)
    avg_expense = calculate_average_expense(transactions)
    print("\n====== 📊 Financial Summary ======")
    print(f"  Total Income:      ${total_income:>10.2f}")
    print(f"  Total Expenses:    ${total_expense:>10.2f}")
    print(f"  Current Balance:   ${balance:>10.2f}")
    print(f"  Avg. Expense:      ${avg_expense:>10.2f}")
    print("==================================")
    if balance >= 0:
        print("✅ You are in the positive! Great job.")
    else:
        print("⚠️  You are spending more than you earn. Be careful!")

def spending_by_category():
    transactions = load_transactions()
    expenses = [t for t in transactions if t["type"] == "expense"]
    if not expenses:
        print("\n📭 No expense transactions recorded yet.")
        return
    category_totals = {}
    for t in expenses:
        cat = t["category"]
        category_totals[cat] = category_totals.get(cat, 0) + t["amount"]
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    print("\n====== 🗂️  Spending by Category ======")
    for cat, total in sorted_categories:
        print(f"  {cat:<15} ${total:>10.2f}")
    print("=======================================")

if __name__ == "__main__":
    main()
