from models.savings import Savings
from datetime import datetime, timedelta

class TermSavings(Savings):

    """This class is a subclass of Account: A term savings account"""

    def __init__(self, name, acc_bal=0):
        super().__init__(name, acc_bal)
        self.day_created = datetime.today()

    def withdraw(self, amount):
        if datetime.today() - timedelta(days=60) < self.day_created:
            print('You need at least 60 days after creating the account in oder to withdraw')
        else:
            super().withdraw(amount)

if __name__ == "__main__":
    acc = TermSavings('Nam', 1000)
    acc.pay_interest()
    acc.withdraw(100)
    print(acc.acc_bal)
    print(acc.day_created)