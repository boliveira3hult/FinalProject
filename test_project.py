import pytest
from project import calculate_balance, calculate_total_by_type, calculate_average_expense

@pytest.fixture
def sample_transactions():
    return [
        {"date": "2026-06-01", "type": "income",  "category": "Salary",        "description": "Monthly salary", "amount": 3000.00},
        {"date": "2026-06-02", "type": "expense", "category": "Food",          "description": "Groceries",      "amount": 150.00},
        {"date": "2026-06-03", "type": "expense", "category": "Transport",     "description": "Uber",           "amount": 25.00},
        {"date": "2026-06-04", "type": "expense", "category": "Entertainment", "description": "Netflix",        "amount": 15.00},
        {"date": "2026-06-05", "type": "income",  "category": "Other",         "description": "Freelance",      "amount": 500.00},
    ]

@pytest.fixture
def empty_transactions():
    return []

@pytest.fixture
def only_expenses():
    return [
        {"date": "2026-06-01", "type": "expense", "category": "Food",      "description": "Pizza", "amount": 30.00},
        {"date": "2026-06-02", "type": "expense", "category": "Transport", "description": "Bus",   "amount": 10.00},
        {"date": "2026-06-03", "type": "expense", "category": "Health",    "description": "Gym",   "amount": 60.00},
    ]

def test_calculate_balance_normal(sample_transactions):
    assert calculate_balance(sample_transactions) == 3310.00

def test_calculate_balance_empty(empty_transactions):
    assert calculate_balance(empty_transactions) == 0.0

def test_calculate_balance_only_expenses(only_expenses):
    assert calculate_balance(only_expenses) == -100.00

def test_calculate_balance_only_income():
    transactions = [{"type": "income", "amount": 1000.00}, {"type": "income", "amount": 500.00}]
    assert calculate_balance(transactions) == 1500.00

def test_calculate_total_income(sample_transactions):
    assert calculate_total_by_type(sample_transactions, "income") == 3500.00

def test_calculate_total_expense(sample_transactions):
    assert calculate_total_by_type(sample_transactions, "expense") == 190.00

def test_calculate_total_empty(empty_transactions):
    assert calculate_total_by_type(empty_transactions, "income") == 0.0
    assert calculate_total_by_type(empty_transactions, "expense") == 0.0

def test_calculate_total_no_income(only_expenses):
    assert calculate_total_by_type(only_expenses, "income") == 0.0

def test_calculate_total_expense_only(only_expenses):
    assert calculate_total_by_type(only_expenses, "expense") == 100.00

def test_calculate_average_expense_normal(sample_transactions):
    assert calculate_average_expense(sample_transactions) == 63.33

def test_calculate_average_expense_empty(empty_transactions):
    assert calculate_average_expense(empty_transactions) == 0.0

def test_calculate_average_expense_no_expenses():
    transactions = [{"type": "income", "amount": 2000.00}]
    assert calculate_average_expense(transactions) == 0.0

def test_calculate_average_expense_single():
    transactions = [{"type": "expense", "amount": 75.00}]
    assert calculate_average_expense(transactions) == 75.00

def test_calculate_average_expense_only(only_expenses):
    assert calculate_average_expense(only_expenses) == 33.33
