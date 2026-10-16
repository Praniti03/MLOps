def deposit(balance, amount):
    """Add funds to the account balance."""
    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number.")
    if amount <= 0:
        raise ValueError("Deposit amount must be positive.")
    return balance + amount


def withdraw(balance, amount, overdraft_limit=0):
    """Withdraw funds, allowing an optional overdraft limit."""
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive.")
    if balance - amount < -overdraft_limit:
        raise ValueError("Insufficient funds.")
    return balance - amount


def calculate_interest(balance, annual_rate, years=1):
    """Calculate compound interest earned over a number of years."""
    if balance < 0:
        raise ValueError("Balance cannot be negative.")
    if annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")
    return round(balance * (1 + annual_rate) ** years - balance, 2)


def apply_overdraft_fee(balance, fee=35):
    """Apply a flat fee if the account balance is negative."""
    return balance - fee if balance < 0 else balance


def transfer_funds(from_balance, to_balance, amount):
    """Transfer funds from one account balance to another."""
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if from_balance < amount:
        raise ValueError("Insufficient funds for transfer.")
    return from_balance - amount, to_balance + amount


def calculate_monthly_loan_payment(principal, annual_rate, months):
    """Calculate a fixed monthly loan payment."""
    if months <= 0:
        raise ValueError("Months must be positive.")
    monthly_rate = annual_rate / 12
    if monthly_rate == 0:
        return round(principal / months, 2)
    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
    return round(payment, 2)


def convert_currency(amount, exchange_rate):
    """Convert an amount using a given exchange rate."""
    if exchange_rate <= 0:
        raise ValueError("Exchange rate must be positive.")
    return round(amount * exchange_rate, 2)


def check_minimum_balance(balance, minimum=100):
    """Check whether the account meets a minimum balance requirement."""
    return balance >= minimum