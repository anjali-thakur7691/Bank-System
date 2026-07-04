from datetime import datetime

class Transaction:
    def __init__(self, transaction_type, amount, date=None):
        self.transaction_type = transaction_type
        self.amount = amount
        self.date = date or datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return {
            "type": self.transaction_type,
            "amount": self.amount,
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Transaction(
            data.get("type", "Unknown"),
            data.get("amount", 0),
            data.get("date")
        )
