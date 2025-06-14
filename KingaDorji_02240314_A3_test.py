import unittest
import tkinter as tk
from tkinter import messagebox
import os
import tempfile
from KIngaDorji_02240314_A3 import (
    BankingSystem, PersonalAccount, BusinessAccount, 
    BankingAppGUI, InvalidInputError, InvalidTransferError
)

class TestBankingAppEdgeCases(unittest.TestCase):
    """
    Test class for comprehensive testing of banking application edge cases and functionality.
    Tests various scenarios including invalid inputs, boundary conditions, and normal operations.
    """
    
    def setUp(self):
        """
        Set up test environment before each test method.
        Creates temporary file for data persistence and initializes test accounts.
        """
        # Create a temporary file for testing data persistence without affecting real data
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        self.temp_file.close()
        
        # Initialize banking system with temporary file
        self.banking_system = BankingSystem(self.temp_file.name)
        
        # Create test accounts with known values for predictable testing
        self.personal_account = PersonalAccount("12345", "1234", 1000.0)  # Personal account with $1000
        self.business_account = BusinessAccount("54321", "5678", 2000.0)  # Business account with $2000
        
        # Add accounts to banking system and save to file
        self.banking_system.accounts["12345"] = self.personal_account
        self.banking_system.accounts["54321"] = self.business_account
        self.banking_system.save_accounts()

    def test_deposit_invalid_input(self):
        """
        Test deposit functionality with invalid inputs.
        Should raise InvalidInputError for negative amounts and zero amounts.
        """
        # Test negative deposit amount - should raise exception
        with self.assertRaises(InvalidInputError):
            self.personal_account.deposit(-100)
        
        # Test zero deposit amount - should raise exception  
        with self.assertRaises(InvalidInputError):
            self.personal_account.deposit(0)

    def test_deposit_valid_input(self):
        """
        Test deposit functionality with valid positive amount.
        Should successfully add amount to account balance.
        """
        initial_balance = self.personal_account.funds
        result = self.personal_account.deposit(500.0)
        
        # Verify successful deposit message and updated balance
        self.assertEqual(result, "Deposit completed.")
        self.assertEqual(self.personal_account.funds, initial_balance + 500.0)

    def test_withdraw_insufficient_funds(self):
        """
        Test withdrawal with amount exceeding account balance.
        Should raise InvalidInputError when trying to withdraw more than available funds.
        """
        # Attempt to withdraw $2000 from account with $1000 balance
        with self.assertRaises(InvalidInputError):
            self.personal_account.withdraw(2000.0) 

    def test_withdraw_negative_amount(self):
        """
        Test withdrawal with negative amount.
        Should raise InvalidInputError for negative withdrawal amounts.
        """
        with self.assertRaises(InvalidInputError):
            self.personal_account.withdraw(-100)

    def test_withdraw_zero_amount(self):
        """
        Test withdrawal with zero amount.
        Should raise InvalidInputError for zero withdrawal amounts.
        """
        with self.assertRaises(InvalidInputError):
            self.personal_account.withdraw(0)

    def test_withdraw_valid_amount(self):
        """
        Test withdrawal with valid amount within account balance.
        Should successfully deduct amount from account balance.
        """
        initial_balance = self.personal_account.funds
        result = self.personal_account.withdraw(500.0)
        
        # Verify successful withdrawal message and updated balance
        self.assertEqual(result, "Withdrawal completed.")
        self.assertEqual(self.personal_account.funds, initial_balance - 500.0)

    def test_transfer_insufficient_funds(self):
        """
        Test transfer with amount exceeding sender's account balance.
        Should raise InvalidInputError when transfer amount > available funds.
        """
        # Attempt to transfer $2000 from account with $1000 balance
        with self.assertRaises(InvalidInputError):
            self.personal_account.transfer(2000.0, self.business_account)

    def test_transfer_valid(self):
        """
        Test valid transfer between accounts.
        Should deduct from sender and add to recipient account.
        """
        initial_sender_balance = self.personal_account.funds
        initial_recipient_balance = self.business_account.funds
        
        result = self.personal_account.transfer(500.0, self.business_account)
        
        # Verify successful transfer and correct balance updates for both accounts
        self.assertEqual(result, "Transfer completed.")
        self.assertEqual(self.personal_account.funds, initial_sender_balance - 500.0)
        self.assertEqual(self.business_account.funds, initial_recipient_balance + 500.0)

    def test_mobile_topup_invalid_phone(self):
        """
        Test mobile top-up with invalid phone number formats.
        Should raise InvalidInputError for phone numbers that don't meet validation criteria.
        """
        # Test phone number too short
        with self.assertRaises(InvalidInputError):
            self.personal_account.mobile_top_up("123", 50.0)
        
        # Test non-numeric phone number
        with self.assertRaises(InvalidInputError):
            self.personal_account.mobile_top_up("invalid_phone", 50.0)
        
        # Test phone number with letters mixed with digits
        with self.assertRaises(InvalidInputError):
            self.personal_account.mobile_top_up("12345abcde", 50.0)

    def test_mobile_topup_insufficient_funds(self):
        """
        Test mobile top-up with amount exceeding account balance.
        Should raise InvalidInputError when top-up amount > available funds.
        """
        # Attempt to top-up $2000 from account with $1000 balance
        with self.assertRaises(InvalidInputError):
            self.personal_account.mobile_top_up("1234567890", 2000.0)

    def test_mobile_topup_valid(self):
        """
        Test valid mobile top-up with correct phone number and sufficient funds.
        Should successfully deduct amount and return confirmation message.
        """
        initial_balance = self.personal_account.funds
        result = self.personal_account.mobile_top_up("1234567890", 100.0)
        
        # Verify successful top-up message and updated balance
        self.assertEqual(result, "Mobile number 1234567890 recharged with 100.0.")
        self.assertEqual(self.personal_account.funds, initial_balance - 100.0)

    def test_login_invalid_credentials(self):
        """
        Test login functionality with invalid credentials.
        Should raise InvalidInputError for non-existent accounts or wrong passcodes.
        """
        # Test with non-existent account ID
        with self.assertRaises(InvalidInputError):
            self.banking_system.login("99999", "0000")
        
        # Test with correct account ID but wrong passcode
        with self.assertRaises(InvalidInputError):
            self.banking_system.login("12345", "0000")

    def test_login_valid_credentials(self):
        """
        Test login functionality with valid credentials.
        Should return the correct account object when credentials match.
        """
        account = self.banking_system.login("12345", "1234")
        
        # Verify returned account has correct credentials
        self.assertEqual(account.account_id, "12345")
        self.assertEqual(account.passcode, "1234")

    def test_delete_existing_account(self):
        """
        Test deletion of existing account.
        Should successfully remove account from banking system.
        """
        # Verify account exists before deletion
        self.assertIn("12345", self.banking_system.accounts)
        
        # Delete account and verify it's removed
        self.banking_system.delete_account("12345")
        self.assertNotIn("12345", self.banking_system.accounts)

    def test_delete_nonexistent_account(self):
        """
        Test deletion of non-existent account.
        Should raise InvalidInputError when trying to delete account that doesn't exist.
        """
        with self.assertRaises(InvalidInputError):
            self.banking_system.delete_account("99999")

    def test_create_personal_account(self):
        """
        Test creation of new personal account.
        Should create PersonalAccount instance and add to banking system.
        """
        initial_count = len(self.banking_system.accounts)
        account = self.banking_system.create_account("Personal")
        
        # Verify account type, category, and that it was added to system
        self.assertIsInstance(account, PersonalAccount)
        self.assertEqual(account.account_category, "Personal")
        self.assertEqual(len(self.banking_system.accounts), initial_count + 1)

    def test_create_business_account(self):
        """
        Test creation of new business account.
        Should create BusinessAccount instance and add to banking system.
        """
        initial_count = len(self.banking_system.accounts)
        account = self.banking_system.create_account("Business")
        
        # Verify account type, category, and that it was added to system
        self.assertIsInstance(account, BusinessAccount)
        self.assertEqual(account.account_category, "Business")
        self.assertEqual(len(self.banking_system.accounts), initial_count + 1)

    def test_account_persistence(self):
        """
        Test data persistence functionality.
        Should save and load account data correctly from file storage.
        """
        # Create new banking system instance using same file
        new_banking_system = BankingSystem(self.temp_file.name)
        
        # Verify accounts were loaded from file
        self.assertIn("12345", new_banking_system.accounts)
        self.assertIn("54321", new_banking_system.accounts)
        
        # Verify loaded account data integrity
        loaded_account = new_banking_system.accounts["12345"]
        self.assertEqual(loaded_account.account_id, "12345")
        self.assertEqual(loaded_account.passcode, "1234")
        self.assertEqual(loaded_account.funds, 1000.0)

    def test_edge_case_empty_strings(self):
        """
        Test login with empty string credentials.
        Should raise InvalidInputError for empty account ID or passcode.
        """
        with self.assertRaises(InvalidInputError):
            self.banking_system.login("", "")

    def test_boundary_values(self):
        """
        Test boundary value conditions.
        Tests minimum deposit amount and complete balance withdrawal.
        """
        # Test minimum valid deposit (0.01) - skip if deposit(0) raises exception
        try:
            result = self.personal_account.deposit(0.01)
            self.assertEqual(result, "Deposit completed.")
        except InvalidInputError:
            # If small deposits are not allowed, test with 1.0 instead
            result = self.personal_account.deposit(1.0)
            self.assertEqual(result, "Deposit completed.")
        
        # Test withdrawing entire account balance
        current_funds = self.personal_account.funds
        result = self.personal_account.withdraw(current_funds)
        self.assertEqual(result, "Withdrawal completed.")
        self.assertAlmostEqual(self.personal_account.funds, 0.0, places=2)

    def tearDown(self):
        """
        Clean up test environment after each test method.
        Removes temporary file to prevent accumulation of test files.
        """
        try:
            # Remove temporary file created during setUp
            os.unlink(self.temp_file.name)
        except (FileNotFoundError, OSError):
            # Handle case where file was already deleted or permission issues
            pass

# Run tests with verbose output when script is executed directly
if __name__ == '__main__':
    unittest.main(verbosity=2)
