import json
import os
from datetime import datetime
from transaction import Transaction

# Agar account.py me koi galti hogi to ye error pakad lega
try:
    from account import SavingAccount
except Exception as e:
    print(f"Error importing SavingAccount: {e}")

class Bank:
    FILE_NAME = "data.json"
    ACCOUNT_PREFIX = "SBI"

    def __init__(self):
        # Pehle list initialize hogi har haal me
        self.accounts = []
        
        # Fir load karne ki koshish karenge, agar crash hua to pata chal jayega
        try:
            self.load_accounts()
        except Exception as e:
            print(f"Error while loading accounts: {e}")

    def load_accounts(self):
        if os.path.exists(self.FILE_NAME):
            # Check karein agar file khali to nahi hai
            if os.path.getsize(self.FILE_NAME) == 0:
                return
                
            with open(self.FILE_NAME, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    print("data.json file corrupt hai ya khali hai.")
                    return

                if data and isinstance(data, list):
                    for item in data:
                        try:
                            account_no = str(item.get("account_no", "")).strip()
                            name = str(item.get("name", "")).strip()
                            if not account_no or not name:
                                continue

                            account = SavingAccount(
                                account_no,
                                name,
                                item.get("balance", 0),
                                phone=item.get("phone", ""),
                                address=item.get("address", ""),
                                photo_path=item.get("photo_path", ""),
                                kyc_status=item.get("kyc_status", "Pending"),
                                kyc_document=item.get("kyc_document", ""),
                            )
                            for t in item.get("transactions", []):
                                if isinstance(t, dict):
                                    account.transactions.append(Transaction.from_dict(t))
                            account.loans = item.get("loans", [])
                            account.fixed_deposits = item.get("fixed_deposits", [])
                            account.credit_cards = item.get("credit_cards", [])
                            account.ensure_profile_fields()
                            self.accounts.append(account)
                        except Exception as e:
                            print(f"Error parsing item {item}: {e}")

    def save_accounts(self):
        data = []
        for account in self.accounts:
            data.append(account.to_dict())
        with open(self.FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)

    def create_account(self, account):
        if self.find_account(account.account_no):
            return False
        self.accounts.append(account)
        self.save_accounts()
        return True

    def generate_account_no(self):
        max_number = 1000
        for account in self.accounts:
            account_no = str(account.account_no)
            if account_no.startswith(self.ACCOUNT_PREFIX):
                number_part = account_no.replace(self.ACCOUNT_PREFIX, "", 1)
                if number_part.isdigit():
                    max_number = max(max_number, int(number_part))
        return f"{self.ACCOUNT_PREFIX}{max_number + 1}"

    def find_account(self, account_no):
        for account in self.accounts:
            if account.account_no == account_no:
                account.ensure_profile_fields()
                return account
        return None
    def delete_account(self, account_no):
        account = self.find_account(account_no)
        if account:
             self.accounts.remove(account)
             self.save_accounts()
             return True
        return False

    def transfer_money(self, sender_no, receiver_no, amount):

        sender = self.find_account(sender_no)
        receiver = self.find_account(receiver_no)
        if sender and receiver and sender is not receiver and amount > 0 and sender.get_balance() >= amount:
            sender.withdraw(amount)
            receiver.deposit(amount)
            self.save_accounts()
            return True
        return False

    def update_kyc(self, account_no, phone, address, kyc_document, kyc_status, photo_path=""):
        account = self.find_account(account_no)
        if not account:
            return False
        account.phone = phone
        account.address = address
        account.kyc_document = kyc_document
        account.kyc_status = kyc_status
        if photo_path:
            account.photo_path = photo_path
        self.save_accounts()
        return True

    def add_loan(self, account_no, loan_type, amount, interest_rate, tenure_months):
        account = self.find_account(account_no)
        if not account or amount <= 0 or interest_rate <= 0 or tenure_months <= 0:
            return False
        account.loans.append({
            "loan_type": loan_type,
            "amount": amount,
            "interest_rate": interest_rate,
            "tenure_months": tenure_months,
            "status": "Active",
            "created_on": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })
        self.save_accounts()
        return True

    def add_fixed_deposit(self, account_no, amount, interest_rate, tenure_months):
        account = self.find_account(account_no)
        if not account or amount <= 0 or interest_rate <= 0 or tenure_months <= 0:
            return False
        account.fixed_deposits.append({
            "amount": amount,
            "interest_rate": interest_rate,
            "tenure_months": tenure_months,
            "maturity_amount": round(amount + (amount * interest_rate * tenure_months / 1200), 2),
            "status": "Active",
            "created_on": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })
        self.save_accounts()
        return True

    def add_credit_card(self, account_no, card_type, credit_limit):
        account = self.find_account(account_no)
        if not account or credit_limit <= 0:
            return False
        account.credit_cards.append({
            "card_type": card_type,
            "credit_limit": credit_limit,
            "used_limit": 0,
            "status": "Active",
            "created_on": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })
        self.save_accounts()
        return True
    
