import random
import tkinter as tk
from tkinter import messagebox

class InvalidInputError(Exception):
    """Raised when user input is invalid."""
    pass

class InvalidTransferError(Exception):
    """Raised when a transfer attempt is invalid."""
    pass

class BankAccount:
    """A class representing a bank account."""

    def __init__(self, account_id, passcode, account_category, funds=0):
        self.account_id = account_id
        self.passcode = passcode
        self.account_category = account_category
        self.funds = funds

    def deposit(self, amount):
        """Deposit amount to the account."""
        if amount > 0:
            self.funds += amount
            return "Deposit completed."
        raise InvalidInputError("Invalid deposit amount.")

    def withdraw(self, amount):
        """Withdraw amount from the account."""
        if 0 < amount <= self.funds:
            self.funds -= amount
            return "Withdrawal completed."
        raise InvalidInputError("Insufficient funds or invalid amount.")

    def transfer(self, amount, recipient_account):
        """Transfer funds to another account."""
        self.withdraw(amount)
        recipient_account.deposit(amount)
        return "Transfer completed."

    def mobile_top_up(self, phone_number, amount):
        """Top up a mobile number."""
        if len(phone_number) < 10 or not phone_number.isdigit():
            raise InvalidInputError("Invalid phone number.")
        self.withdraw(amount)
        return f"Mobile number {phone_number} recharged with {amount}."

class PersonalAccount(BankAccount):
    def __init__(self, account_id, passcode, funds=0):
        super().__init__(account_id, passcode, "Personal", funds)

class BusinessAccount(BankAccount):
    def __init__(self, account_id, passcode, funds=0):
        super().__init__(account_id, passcode, "Business", funds)

class BankingSystem:
    """Class to manage the bank system."""

    def __init__(self, filename="accounts.txt"):
        self.filename = filename
        self.accounts = self.load_accounts()

    def load_accounts(self):
        """Load account data from file."""
        accounts = {}
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    account_id, passcode, account_category, funds = line.strip().split(",")
                    funds = float(funds)
                    account = PersonalAccount(account_id, passcode, funds) if account_category == "Personal" else BusinessAccount(account_id, passcode, funds)
                    accounts[account_id] = account
        except FileNotFoundError:
            pass
        return accounts

    def save_accounts(self):
        """Save accounts to file."""
        with open(self.filename, "w") as file:
            for account in self.accounts.values():
                file.write(f"{account.account_id},{account.passcode},{account.account_category},{account.funds}\n")

    def create_account(self, account_type):
        """Create a new bank account."""
        account_id = str(random.randint(10000, 99999))
        passcode = str(random.randint(1000, 9999))
        account = PersonalAccount(account_id, passcode) if account_type == "Personal" else BusinessAccount(account_id, passcode)
        self.accounts[account_id] = account
        self.save_accounts()
        return account

    def login(self, account_id, passcode):
        """Login using credentials."""
        account = self.accounts.get(account_id)
        if account and account.passcode == passcode:
            return account
        raise InvalidInputError("Invalid account ID or passcode.")

    def delete_account(self, account_id):
        """Delete an account."""
        if account_id in self.accounts:
            del self.accounts[account_id]
            self.save_accounts()
        else:
            raise InvalidInputError("Account does not exist.")


def process_user_input(account, bank):
    """Handle user commands after login."""
    while True:
        print("\n1. Check funds\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Mobile Top-up\n6. Delete Account\n7. Logout")
        action = input("Enter your choice: ")
        try:
            if action == "1":
                print(f"Your funds: {account.funds}")
            elif action == "2":
                amount = float(input("Enter deposit amount: "))
                print(account.deposit(amount))
                bank.save_accounts()
            elif action == "3":
                amount = float(input("Enter withdrawal amount: "))
                print(account.withdraw(amount))
                bank.save_accounts()
            elif action == "4":
                recipient_id = input("Recipient ID: ")
                amount = float(input("Amount to transfer: "))
                recipient = bank.accounts.get(recipient_id)
                if not recipient:
                    raise InvalidTransferError("Recipient does not exist.")
                print(account.transfer(amount, recipient))
                bank.save_accounts()
            elif action == "5":
                phone = input("Mobile number: ")
                amount = float(input("Amount: "))
                print(account.mobile_top_up(phone, amount))
                bank.save_accounts()
            elif action == "6":
                bank.delete_account(account.account_id)
                print("Account deleted.")
                break
            elif action == "7":
                break
            else:
                raise InvalidInputError("Invalid selection.")
        except Exception as e:
            print(f"Error: {e}")


class BankingAppGUI:
    """GUI for banking app using tkinter."""

    def __init__(self, master):
        self.bank = BankingSystem()
        self.master = master
        self.master.title("Banking System")
        self.build_login_screen()

    def build_login_screen(self):
        self.clear()
        tk.Label(self.master, text="Account ID:").grid(row=0, column=0)
        tk.Label(self.master, text="Passcode:").grid(row=1, column=0)

        self.account_entry = tk.Entry(self.master)
        self.passcode_entry = tk.Entry(self.master)
        self.account_entry.grid(row=0, column=1)
        self.passcode_entry.grid(row=1, column=1)

        tk.Button(self.master, text="Login", command=self.login).grid(row=2, column=0)
        tk.Button(self.master, text="Create Account", command=self.create_account_screen).grid(row=2, column=1)

    def create_account_screen(self):
        self.clear()
        tk.Label(self.master, text="Choose account type:").grid(row=0, column=0)
        self.type_var = tk.StringVar(value="Personal")
        tk.Radiobutton(self.master, text="Personal", variable=self.type_var, value="Personal").grid(row=1, column=0)
        tk.Radiobutton(self.master, text="Business", variable=self.type_var, value="Business").grid(row=2, column=0)
        tk.Button(self.master, text="Create", command=self.create_account).grid(row=3, column=0)

    def create_account(self):
        account = self.bank.create_account(self.type_var.get())
        messagebox.showinfo("Account Created", f"ID: {account.account_id}, Passcode: {account.passcode}")
        self.build_login_screen()

    def login(self):
        try:
            account_id = self.account_entry.get()
            passcode = self.passcode_entry.get()
            self.account = self.bank.login(account_id, passcode)
            self.build_dashboard()
        except InvalidInputError as e:
            messagebox.showerror("Login Failed", str(e))

    def build_dashboard(self):
        self.clear()
        tk.Label(self.master, text=f"Welcome {self.account.account_id} ({self.account.account_category})").grid(row=0, column=0, columnspan=2)
        tk.Button(self.master, text="Check Funds", command=lambda: messagebox.showinfo("Funds", f"{self.account.funds}"), width=20).grid(row=1, column=0)
        tk.Button(self.master, text="Deposit", command=self.deposit_screen, width=20).grid(row=1, column=1)
        tk.Button(self.master, text="Withdraw", command=self.withdraw_screen, width=20).grid(row=2, column=0)
        tk.Button(self.master, text="Transfer", command=self.transfer_screen, width=20).grid(row=2, column=1)
        tk.Button(self.master, text="Top-up", command=self.topup_screen, width=20).grid(row=3, column=0)
        tk.Button(self.master, text="Delete Account", command=self.delete_account, width=20).grid(row=3, column=1)
        tk.Button(self.master, text="Logout", command=self.build_login_screen, width=20).grid(row=4, column=0, columnspan=2)

    def deposit_screen(self):
        self.transaction_popup("Deposit Amount:", lambda amount: self.account.deposit(amount))

    def withdraw_screen(self):
        self.transaction_popup("Withdraw Amount:", lambda amount: self.account.withdraw(amount))

    def transfer_screen(self):
        self.clear()
        tk.Label(self.master, text="Recipient ID:").grid(row=0, column=0)
        tk.Label(self.master, text="Amount:").grid(row=1, column=0)
        rid = tk.Entry(self.master)
        amt = tk.Entry(self.master)
        rid.grid(row=0, column=1)
        amt.grid(row=1, column=1)
        def transfer_action():
            try:
                recipient = self.bank.accounts.get(rid.get())
                if not recipient:
                    raise InvalidTransferError("Recipient not found.")
                self.account.transfer(float(amt.get()), recipient)
                self.bank.save_accounts()
                messagebox.showinfo("Success", "Transfer successful.")
                self.build_dashboard()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(self.master, text="Transfer", command=transfer_action).grid(row=2, column=0, columnspan=2)

    def topup_screen(self):
        self.clear()
        tk.Label(self.master, text="Phone Number:").grid(row=0, column=0)
        tk.Label(self.master, text="Amount:").grid(row=1, column=0)
        phone = tk.Entry(self.master)
        amt = tk.Entry(self.master)
        phone.grid(row=0, column=1)
        amt.grid(row=1, column=1)
        def topup_action():
            try:
                self.account.mobile_top_up(phone.get(), float(amt.get()))
                self.bank.save_accounts()
                messagebox.showinfo("Success", "Top-up successful.")
                self.build_dashboard()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(self.master, text="Top-up", command=topup_action).grid(row=2, column=0, columnspan=2)

    def transaction_popup(self, label, action):
        self.clear()
        tk.Label(self.master, text=label).grid(row=0, column=0)
        amt = tk.Entry(self.master)
        amt.grid(row=0, column=1)
        def perform():
            try:
                action(float(amt.get()))
                self.bank.save_accounts()
                messagebox.showinfo("Success", "Transaction completed.")
                self.build_dashboard()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(self.master, text="Submit", command=perform).grid(row=1, column=0, columnspan=2)

    def delete_account(self):
        self.bank.delete_account(self.account.account_id)
        messagebox.showinfo("Deleted", "Account successfully deleted.")
        self.build_login_screen()

    def clear(self):
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingAppGUI(root)
    root.mainloop()
