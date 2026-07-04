from transaction import Transaction

class Account:
    def __init__(
        self,
        account_no,
        name,
        balance=0,
        phone="",
        address="",
        photo_path="",
        kyc_status="Pending",
        kyc_document="",
        aadhaar_number="",
        pan_number="",
        aadhaar_document="",
        pan_document="",
        otp_verified=False,
        face_verified=False,
    ):
        self.account_no = account_no
        self.name = name
        self.__balance = float(balance or 0)

        self.phone = phone
        self.address = address
        self.photo_path = photo_path

        self.kyc_status = kyc_status
        self.kyc_document = kyc_document

        self.aadhaar_number = aadhaar_number
        self.pan_number = pan_number
        self.aadhaar_document = aadhaar_document
        self.pan_document = pan_document

        self.otp_verified = otp_verified
        self.face_verified = face_verified

        self.transactions = []
        self.loans = []
        self.fixed_deposits = []
        self.credit_cards = []

    def _ensure_balance(self):
        if self.__balance is None:
            self.__balance = 0

    def ensure_profile_fields(self):
        defaults = {
            "phone": "",
            "address": "",
            "photo_path": "",
            "kyc_status": "Pending",
            "kyc_document": "",
            "aadhaar_number": "",
            "pan_number": "",
            "aadhaar_document": "",
            "pan_document": "",
            "otp_verified": False,
            "face_verified": False,
            "loans": [],
            "fixed_deposits": [],
            "credit_cards": [],
        }

        for field, default in defaults.items():
            if not hasattr(self, field):
                setattr(
                    self,
                    field,
                    default.copy() if isinstance(default, list) else default,
                )

    @staticmethod
    def _valid_amount(amount):
        return isinstance(amount, (int, float)) and amount > 0

    def deposit(self, amount):
        if self._valid_amount(amount):
            self._ensure_balance()
            self.__balance += amount

            transaction = Transaction(
                "Deposit",
                amount
            )

            self.transactions.append(transaction)
            return True

        return False
    
    def withdraw(self, amount):
        self._ensure_balance()

        if self._valid_amount(amount) and amount <= self.__balance:
           self.__balance -= amount

           transaction = Transaction(
                "Withdraw",
                amount
           )

           self.transactions.append(transaction)
           return True

        return False

    def get_balance(self):
        self._ensure_balance()
        return self.__balance

    @staticmethod
    def search_account(account_list, acc_no):
        for acc in account_list:
            if acc.account_no == acc_no:
                return acc
        return None

    def delete_account(self, account_list, acc_no):
        account = self.search_account(account_list, acc_no)

        if account:
            account_list.remove(account)
            return True

        return False

    def transfer(self, target_account, amount):
        if target_account is self:
            return False

        if self.withdraw(amount):
            target_account.deposit(amount)
            return True

        return False

    def to_dict(self):
        self.ensure_profile_fields()

        return {
            "account_no": self.account_no,
            "name": self.name,
            "balance": self.get_balance(),
            "phone": self.phone,
            "address": self.address,
            "photo_path": self.photo_path,
            "kyc_status": self.kyc_status,
            "kyc_document": self.kyc_document,

            "aadhaar_number": self.aadhaar_number,
            "pan_number": self.pan_number,
            "aadhaar_document": self.aadhaar_document,
            "pan_document": self.pan_document,

            "otp_verified": self.otp_verified,
            "face_verified": self.face_verified,

            "transactions": [
                t if isinstance(t, dict) else t.to_dict()
                for t in self.transactions
            ],

            "loans": self.loans,
            "fixed_deposits": self.fixed_deposits,
            "credit_cards": self.credit_cards,
        }


class SavingAccount(Account):
    def __init__(self, account_no, name, balance=0, **kwargs):
        super().__init__(
            account_no,
            name,
            balance,
            **kwargs
        )
        self.transactions = [] 


class CurrentAccount(Account):
    def __init__(self, account_no, name, balance=0, **kwargs):
        super().__init__(
            account_no,
            name,
            balance,
            **kwargs
        )
        self.transactions = []