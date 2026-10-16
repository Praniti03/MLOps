import sys, os, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bank_account import (
    deposit, withdraw, calculate_interest, apply_overdraft_fee,
    transfer_funds, calculate_monthly_loan_payment,
    convert_currency, check_minimum_balance
)

class TestBankAccount(unittest.TestCase):

    def test_deposit(self):
        self.assertEqual(deposit(100, 50), 150)

    def test_deposit_negative_raises(self):
        with self.assertRaises(ValueError):
            deposit(100, -10)

    def test_withdraw(self):
        self.assertEqual(withdraw(100, 50), 50)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            withdraw(50, 100)

    def test_calculate_interest(self):
        self.assertEqual(calculate_interest(1000, 0.05, 1), 50.0)

    def test_apply_overdraft_fee(self):
        self.assertEqual(apply_overdraft_fee(-20), -55)

    def test_transfer_funds(self):
        self.assertEqual(transfer_funds(200, 50, 100), (100, 150))

    def test_convert_currency(self):
        self.assertEqual(convert_currency(100, 1.1), 110.0)

    def test_check_minimum_balance(self):
        self.assertTrue(check_minimum_balance(150))
        self.assertFalse(check_minimum_balance(50))

if __name__ == '__main__':
    unittest.main()