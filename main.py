from abc import ABC, abstractmethod


class Transaction:
    def __init__(self, t_type, amount, target_acc="Self"):
        self.t_type = t_type  # Deposit, Withdraw, Transfer
        self.amount = amount
        self.target_acc = target_acc

    def __str__(self):
        return f"-> {self.t_type}: Rs.{self.amount} (To/From: {self.target_acc})"


class Account(ABC):
    def __init__(self, account_number, holder_name, initial_balance):
        self._account_number = account_number  
        self._holder_name = holder_name
        self._balance = initial_balance
        self.is_frozen = False
        self.transaction_history = []

    @property
    def account_number(self):
        return self._account_number

    @property
    def holder_name(self):
        return self._holder_name

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if self.is_frozen:
            print("❌ Transaction Failed! Account is frozen.")
            return False
        if amount > 0:
            self._balance += amount
            self.transaction_history.append(Transaction("Deposit", amount))
            print(f"✅ Rs.{amount} deposited successfully.")
            return True
        return False

    @abstractmethod
    def withdraw(self, amount):
        """Har account type isko apne mutabiq implement karega (Polymorphism)"""
        pass

    def show_history(self):
        print(f"\n--- Transaction History for Acc: {self._account_number} ---")
        if not self.transaction_history:
            print("Koi transactions nahi hain.")
        for t in self.transaction_history:
            print(t)


class SavingsAccount(Account):
    def __init__(self, account_number, holder_name, initial_balance, min_balance=2000, interest_rate=0.05):
        super().__init__(account_number, holder_name, initial_balance)
        self.min_balance = min_balance
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        if self.is_frozen:
            print("❌ Account frozen hai!")
            return False
        if self._balance - amount >= self.min_balance:
            self._balance -= amount
            self.transaction_history.append(Transaction("Withdrawal", amount))
            print(f"✅ Rs.{amount} withdrawn successfully.")
            return True
        else:
            print("❌ Transaction Failed! Minimum balance requirement limit cross ho rahi hai.")
            return False

    def apply_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        self.transaction_history.append(Transaction("Interest Added", interest))
        print(f"💰 Interest of Rs.{interest} applied.")

class CurrentAccount(Account):
    def __init__(self, account_number, holder_name, initial_balance, overdraft_limit=10000):
        super().__init__(account_number, holder_name, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if self.is_frozen:
            print("❌ Account frozen hai!")
            return False
        if self._balance + self.overdraft_limit >= amount:
            self._balance -= amount
            self.transaction_history.append(Transaction("Withdrawal (with Overdraft)", amount))
            print(f"✅ Rs.{amount} withdrawn successfully.")
            return True
        else:
            print("❌ Transaction Failed! Overdraft limit exceeded.")
            return False


class Bank:
    def __init__(self):
        self.accounts = {}  

    def add_account(self, account):
        self.accounts[account.account_number] = account
        print(f"🏦 Account created for {account.holder_name} (Acc No: {account.account_number})")

    def find_account(self, account_number):
        return self.accounts.get(account_number, None)

    def transfer_funds(self, sender_num, receiver_num, amount):
        sender = self.find_account(sender_num)
        receiver = self.find_account(receiver_num)

        if not sender or not receiver:
            print("❌ Sender ya Receiver account nahi mila.")
            return

        if sender.withdraw(amount):
            receiver.deposit(amount)
            # Transfer tracking tags override
            sender.transaction_history[-1].t_type = "Transfer Sent"
            sender.transaction_history[-1].target_acc = receiver_num
            receiver.transaction_history[-1].t_type = "Transfer Received"
            receiver.transaction_history[-1].target_acc = sender_num
            print(f"💸 Rs.{amount} transferred from {sender_num} to {receiver_num}.")

# ==========================================
# 5. ADMIN ROLE
# ==========================================
class Admin:
    def __init__(self, bank_instance):
        self.bank = bank_instance

    def freeze_account(self, acc_num):
        acc = self.bank.find_account(acc_num)
        if acc:
            acc.is_frozen = True
            print(f"🔒 Account {acc_num} has been FROZEN.")

    def view_total_assets(self):
        total = sum(acc.balance for acc in self.bank.accounts.values())
        print(f"📈 Bank's Total Assets: Rs.{total}")