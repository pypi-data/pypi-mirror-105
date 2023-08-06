from account import Account
from transaction_log import TransactionLog

class Chequing(Account):

    """This class is a subclass of Account: A Chequing account"""

    def __init__(self, name, acc_bal=0):
        super().__init__(name, acc_bal)

    def withdraw(self, amount):
        global checker
        try:
            if float(amount) < 0:
                print('Error: Amount has to be larger than 0')
            else:
                if self.acc_bal - float(amount) >= -500:
                    self.acc_bal -= float(amount)
                    one_log = TransactionLog('Withdraw', amount)
                    self.transaction_log.append((one_log.action, one_log.date))
                    checker = True
                    return checker
                else:
                    print('Insufficient funds')
                    checker = False
        except TypeError:
            print('Error: Amount has to be a float or an integer')

    def pay_charge(self):
        if self.acc_bal < 0:
            one_log = TransactionLog('Charge fee', -(self.acc_bal * (3 / 100)))
            self.acc_bal += self.acc_bal*(3/100)
            self.transaction_log.append((one_log.action, one_log.date))
        else:
            print("There's no overdraft amount")

    def post_cheque(self, amount):
        self.withdraw(amount)
        if checker == True:
            print('Your cheque has ${}'.format(amount))
        elif checker == False:
            self.acc_bal -= 25
        return checker

if __name__ == "__main__":
    acc = Chequing('Nam')
    print(acc.acc_bal)
    acc.acc_bal = 100
    print(acc.acc_bal)