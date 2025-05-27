class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.deposits = []
        self.withdrawals = []
        self.loan = 0
        self.frozen = False
        self.minimum_balance = 0
        self.closed = False

    def deposit(self, amount):
        if self.closed:
            return "Account is closed. Cannot deposit."
        if self.frozen:
            return "Account is frozen. Cannot deposit."
        if amount <= 0:
            return "Deposit amount must be positive."
        self.deposits.append(amount)
        self.balance += amount
        return f"Deposited {amount}. New balance is {self.balance}."

    def withdraw(self, amount):
        if self.closed:
            return "Account is closed. Cannot withdraw."
        if self.frozen:
            return "Account is frozen. Cannot withdraw."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        if amount > self.balance:
            return "Insufficient funds."
        if self.balance - amount < self.minimum_balance:
            return f"Cannot withdraw. Balance would fall below minimum balance of {self.minimum_balance}."
        self.withdrawals.append(amount)
        self.balance -= amount
        return f"Withdrew {amount}. New balance is {self.balance}."

    def transfer_funds(self, amount, target_account):
        if self.closed:
            return "Account is closed. Cannot transfer funds."
        if self.frozen:
            return "Account is frozen. Cannot transfer funds."
        if not isinstance(target_account, Account):
            return "Target must be an Account instance."
        if amount <= 0:
            return "Transfer amount must be positive."
        if amount > self.balance:
            return "Insufficient funds to transfer."
        if self.balance - amount < self.minimum_balance:
            return f"Cannot transfer. Balance would fall below minimum balance of {self.minimum_balance}."
        withdraw_msg = self.withdraw(amount)
        if "Withdrew" in withdraw_msg:
            deposit_msg = target_account.deposit(amount)
            return f"Transferred {amount} to {target_account.name}. {withdraw_msg} | {deposit_msg}"
        else:
            return f"Transfer failed. {withdraw_msg}"

    def get_balance(self):
        return self.balance

    def request_loan(self, amount):
        if self.closed:
            return "Account is closed. Cannot request loan."
        if amount <= 0:
            return "Loan amount must be positive."
        self.loan += amount
        self.balance += amount
        return f"Loan of {amount} granted. Total loan is now {self.loan}. Current balance is {self.balance}."

    def repay_loan(self, amount):
        if self.closed:
            return "Account is closed. Cannot repay loan."
        if amount <= 0:
            return "Repayment amount must be positive."
        if self.loan == 0:
            return "No outstanding loan to repay."
        if amount > self.loan:
            amount = self.loan
            msg = f"Repaying full loan amount of {amount}."
        else:
            msg = ""
        if amount > self.balance:
            return "Insufficient funds to repay loan."
        self.loan -= amount
        self.balance -= amount
        return f"{msg} Repaid {amount}. Remaining loan balance is {self.loan}. Current balance is {self.balance}."

    def view_account_details(self):
        return (f"Account owner: {self.name} Current balance: {self.balance} Outstanding loan: {self.loan} "
                f"Account frozen: {self.frozen} Minimum balance: {self.minimum_balance} Account closed: {self.closed}")

    def change_account_owner(self, new_name):
        if self.closed:
            return "Account is closed. Cannot change owner."
        if not new_name:
            return "New owner name cannot be empty."
        self.name = new_name
        return f"Account owner changed to {self.name}."

    def account_statement(self):
        statement = f"Account statement for {self.name}: Deposits: "
        for i, amount in enumerate(self.deposits, 1):
            statement += f"{i}. +{amount} "
        statement += "Withdrawals: "
        for i, amount in enumerate(self.withdrawals, 1):
            statement += f"{i}. {amount} "
        statement += f"Current balance: {self.balance} Outstanding loan: {self.loan}"
        return statement

    def calculate_interest(self):
        if self.closed:
            return "Account is closed. Cannot calculate interest."
        if self.frozen:
            return "Account is frozen. Cannot calculate interest."
        interest = self.balance * 0.05
        if interest > 0:
            self.deposits.append(interest)
            self.balance += interest
            return f"Interest of {interest} applied. New balance is {self.balance}."
        else:
            return "No interest applied because balance is zero or negative."

    def freeze_account(self):
        if self.closed:
            return "Account is closed. Cannot freeze."
        self.frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        if self.closed:
            return "Account is closed. Cannot unfreeze."
        self.frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        if self.closed:
            return "Account is closed. Cannot set minimum balance."
        if amount < 0:
            return "Minimum balance cannot be negative."
        self.minimum_balance = amount
        return f"Minimum balance set to {self.minimum_balance}."

    def close_account(self):
        self.balance = 0
        self.deposits.clear()
        self.withdrawals.clear()
        self.loan = 0
        self.frozen = False
        self.minimum_balance = 0
        self.closed = True
        return f"Account for {self.name} has been closed. All balances and transactions cleared."


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
print(account1.account_statement())
print(account1.calculate_interest())
print(account1.freeze_account())
print(account1.deposit(100))
print(account1.unfreeze_account())
print(account1.deposit(100))
print(account1.set_minimum_balance(200))
print(account1.withdraw(500))
print(account1.close_account())
print(account1.deposit(50))
