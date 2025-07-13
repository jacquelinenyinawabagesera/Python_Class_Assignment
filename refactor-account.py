import datetime

class Transaction:
    def __init__(self, trans_type, amount, narration=""):
        self.date_time = datetime.datetime.now()
        self.trans_type = trans_type  
        self.amount = amount
        self.narration = narration

    def __str__(self):
        return f"{self.date_time.strftime('%Y-%m-%d %H:%M:%S')} - {self.narration}: {self.trans_type} ${self.amount:.2f}"

class Account:
    def __init__(self, name):
        self._name = name
        self._balance = 0
        self._deposits = []
        self._withdrawals = []
        self._loan = 0
        self._frozen = False
        self._minimum_balance = 0
        self._closed = False
        self._transactions = [] 

    def deposit(self, amount):
        if self._closed:
            return "Account is closed. Cannot deposit."
        if self._frozen:
            return "Account is frozen. Cannot deposit."
        if amount <= 0:
            return "Deposit amount must be positive."
        self._deposits.append(amount)
        self._balance += amount
        self._transactions.append(Transaction('deposit', amount, "Deposit"))
        return f"Deposited {amount}. New balance is {self._balance}."

    def withdraw(self, amount):
        if self._closed:
            return "Account is closed. Cannot withdraw."
        if self._frozen:
            return "Account is frozen. Cannot withdraw."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        if amount > self._balance:
            return "Insufficient funds."
        if self._balance - amount < self._minimum_balance:
            return f"Cannot withdraw. Balance would fall below minimum balance of {self._minimum_balance}."
        self._withdrawals.append(amount)
        self._balance -= amount
        self._transactions.append(Transaction('withdrawal', amount, "Withdrawal"))
        return f"Withdrew {amount}. New balance is {self._balance}."

    def transfer_funds(self, amount, target_account):
        if self._closed:
            return "Account is closed. Cannot transfer funds."
        if self._frozen:
            return "Account is frozen. Cannot transfer funds."
        if not isinstance(target_account, Account):
            return "Target must be an Account instance."
        if amount <= 0:
            return "Transfer amount must be positive."
        if amount > self._balance:
            return "Insufficient funds to transfer."
        if self._balance - amount < self._minimum_balance:
            return f"Cannot transfer. Balance would fall below minimum balance of {self._minimum_balance}."
        
        withdraw_msg = self.withdraw(amount)
        if "Withdrew" in withdraw_msg:
            deposit_msg = target_account.deposit(amount)
            return f"Transferred {amount} to {target_account.get_name()}. {withdraw_msg} | {deposit_msg}"
        else:
            return f"Transfer failed. {withdraw_msg}"

    def get_balance(self):
        return self._balance

    def request_loan(self, amount):
        if self._closed:
            return "Account is closed. Cannot request loan."
        if amount <= 0:
            return "Loan amount must be positive."
        self._loan += amount
        self._balance += amount
        self._transactions.append(Transaction('loan', amount, "Loan granted"))
        return f"Loan of {amount} granted. Total loan is now {self._loan}. Current balance is {self._balance}."

    def repay_loan(self, amount):
        if self._closed:
            return "Account is closed. Cannot repay loan."
        if amount <= 0:
            return "Repayment amount must be positive."
        if self._loan == 0:
            return "No outstanding loan to repay."
        if amount > self._loan:
            amount = self._loan
            msg = f"Repaying full loan amount of {amount}."
        else:
            msg = ""
        if amount > self._balance:
            return "Insufficient funds to repay loan."
        self._loan -= amount
        self._balance -= amount
        self._transactions.append(Transaction('repayment', amount, "Loan repayment"))
        return f"{msg} Repaid {amount}. Remaining loan balance is {self._loan}. Current balance is {self._balance}."

    def view_account_details(self):
        return (f"Account owner: {self._name} Current balance: {self._balance} Outstanding loan: {self._loan} "
                f"Account frozen: {self._frozen} Minimum balance: {self._minimum_balance} Account closed: {self._closed}")

    def change_account_owner(self, new_name):
        if self._closed:
            return "Account is closed. Cannot change owner."
        if not new_name:
            return "New owner name cannot be empty."
        self._name = new_name
        return f"Account owner changed to {self._name}."

    def get_account_statement(self):
        print(f"Hello {self._name}, here is your account statement.")
        for transaction in self._transactions:
            print(transaction)
        print(f"Current balance: {self.get_balance()}")

    def calculate_interest(self):
        if self._closed:
            return "Account is closed. Cannot calculate interest."
        if self._frozen:
            return "Account is frozen. Cannot calculate interest."
        interest = self._balance * 0.05
        if interest > 0:
            self._deposits.append(interest)
            self._balance += interest
            self._transactions.append(Transaction('interest', interest, "Interest applied"))
            return f"Interest of {interest} applied. New balance is {self._balance}."
        else:
            return "No interest applied because balance is zero or negative."

    def freeze_account(self):
        if self._closed:
            return "Account is closed. Cannot freeze."
        self._frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        if self._closed:
            return "Account is closed. Cannot unfreeze."
        self._frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        if self._closed:
            return "Account is closed. Cannot set minimum balance."
        if amount < 0:
            return "Minimum balance cannot be negative."
        self._minimum_balance = amount
        return f"Minimum balance set to {self._minimum_balance}."

    def close_account(self):
        self._balance = 0
        self._deposits.clear()
        self._withdrawals.clear()
        self._loan = 0
        self._frozen = False
        self._minimum_balance = 0
        self._closed = True
        self._transactions.append(Transaction('closure', 0, "Account closed"))
        return f"Account for {self._name} has been closed. All balances and transactions cleared."
account1 = Account("Jacky")
account2 = Account("Jane")

print(account1.deposit(1000))
print(account1.withdraw(200))
print(account1.transfer_funds(300, account2))
print(f"Jacky's balance: {account1.get_balance()}")
print(f"Jane's balance: {account2.get_balance()}")
print(account2.request_loan(500))
print(account2.repay_loan(200))
print(account1.view_account_details())
account1.get_account_statement()
print(account1.calculate_interest())
print(account1.freeze_account())
print(account1.deposit(100))
print(account1.unfreeze_account())
print(account1.deposit(100))
print(account1.set_minimum_balance(200))
print(account1.withdraw(500))
print(account1.close_account())
print(account1.deposit(50))
