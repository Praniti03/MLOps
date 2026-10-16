import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.bank_account import (
    deposit, withdraw, calculate_interest, apply_overdraft_fee,
    transfer_funds, calculate_monthly_loan_payment,
    convert_currency, check_minimum_balance
)

@pytest.mark.parametrize("balance, amount, expected", [
    (100, 50, 150),
    (0, 200, 200),
    (500, 0.01, 500.01),
])
def test_deposit(balance, amount, expected):
    assert deposit(balance, amount) == expected

def test_deposit_negative_raises():
    with pytest.raises(ValueError):
        deposit(100, -10)

def test_deposit_invalid_type_raises():
    with pytest.raises(ValueError):
        deposit(100, "fifty")

@pytest.mark.parametrize("balance, amount, overdraft, expected", [
    (100, 50, 0, 50),
    (50, 100, 100, -50),
])
def test_withdraw(balance, amount, overdraft, expected):
    assert withdraw(balance, amount, overdraft) == expected

def test_withdraw_insufficient_funds():
    with pytest.raises(ValueError):
        withdraw(50, 100)

def test_calculate_interest():
    assert calculate_interest(1000, 0.05, 1) == 50.0

def test_apply_overdraft_fee():
    assert apply_overdraft_fee(-20) == -55
    assert apply_overdraft_fee(20) == 20

def test_transfer_funds():
    assert transfer_funds(200, 50, 100) == (100, 150)

def test_transfer_insufficient_funds():
    with pytest.raises(ValueError):
        transfer_funds(50, 100, 200)

def test_calculate_monthly_loan_payment():
    payment = calculate_monthly_loan_payment(10000, 0.06, 12)
    assert payment > 0

def test_convert_currency():
    assert convert_currency(100, 1.1) == 110.0

def test_convert_currency_invalid_rate():
    with pytest.raises(ValueError):
        convert_currency(100, -1)

def test_check_minimum_balance():
    assert check_minimum_balance(150) is True
    assert check_minimum_balance(50) is False