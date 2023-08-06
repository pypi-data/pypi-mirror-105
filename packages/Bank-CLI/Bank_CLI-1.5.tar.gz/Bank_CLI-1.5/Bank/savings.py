from account import Account
from transaction_log import TransactionLog

class Savings(Account):

    """This class is a subclass of Account: A Savings account"""

    def __init__(self, name, acc_bal=0):
        try:
            super().__init__(name, acc_bal)
        except TypeError:
            print('Error: Account Balance needs to be a float or an integer')


    def pay_charge(self):
        if self.acc_bal < 1000:
            self.acc_bal -= 10
            one_log = TransactionLog('Charge fee', 10)
            self.transaction_log.append((one_log.action, one_log.date))
            print('Account Balance below minimum fee $1000.00. A charge of $10.00 was issued.')

    def pay_interest(self):
        if self.acc_bal >= 1000:
            one_log = TransactionLog('Interests', self.acc_bal * (2 / 100))
            self.acc_bal += self.acc_bal*(2/100)
            self.transaction_log.append((one_log.action, one_log.date))
        else:
            print('Not enough balance in account for interest.')

if __name__ == "__main__":
    acc = Savings('Nam', 1000)
    acc2 = Savings('Nam', 2000)
    acc.withdraw(50)
    print(acc)
    print(acc.transaction_log)