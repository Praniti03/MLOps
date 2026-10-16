from src.bank_account import (
    deposit, withdraw, calculate_interest, apply_overdraft_fee,
    transfer_funds, calculate_monthly_loan_payment,
    convert_currency, check_minimum_balance
)

def main():
    lines = []
    lines.append("=== Bank Account System — Example Output ===\n")

    bal = deposit(1000, 500)
    lines.append(f"1. Deposit 500 into 1000 -> {bal}")

    bal2 = withdraw(bal, 300)
    lines.append(f"2. Withdraw 300 -> {bal2}")

    interest = calculate_interest(bal2, 0.05, 2)
    lines.append(f"3. Interest on {bal2} at 5% for 2 years -> {interest}")

    fee_applied = apply_overdraft_fee(-20)
    lines.append(f"4. Overdraft fee applied to -20 balance -> {fee_applied}")

    from_acc, to_acc = transfer_funds(bal2, 200, 150)
    lines.append(f"5. Transfer 150 from account A to B -> A: {from_acc}, B: {to_acc}")

    payment = calculate_monthly_loan_payment(10000, 0.06, 12)
    lines.append(f"6. Monthly loan payment on $10,000 at 6% for 12 months -> {payment}")

    converted = convert_currency(100, 1.1)
    lines.append(f"7. Convert $100 at rate 1.1 -> {converted}")

    meets_min = check_minimum_balance(bal2)
    lines.append(f"8. Does balance {bal2} meet minimum? -> {meets_min}")

    with open("OUTPUT.txt", "w") as f:
        f.write("\n".join(lines))

    print("OUTPUT.txt generated successfully.")

if __name__ == "__main__":
    main()