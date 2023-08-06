from transaction_log import TransactionLog

class Account:

    """This class includes methods to manage accounts"""

    __NEXT_ACC_NUM = 10000

    def __init__(self, name, acc_bal=0):
        self.name = str(name)
        try:
            if acc_bal < 0:
                print('Error: Account Balance needs to be a positive float or integer')
            else:
                self.acc_bal = float(acc_bal)
        except TypeError:
            print('Error: Account Balance needs to be a float or an integer')
        self.acc_num = Account.__NEXT_ACC_NUM
        self.transaction_log = []
        Account.__NEXT_ACC_NUM += 1

    def withdraw(self, amount):
        try:
            if amount < 0:
                print('Error: Amount has to be larger than 0')
            else:
                if self.acc_bal >= float(amount):
                    self.acc_bal -= float(amount)
                    one_log = TransactionLog('Withdraw', amount)
                    self.transaction_log.append((one_log.action, one_log.date))
                    return True
                else:
                    print('Insufficient funds')
        except TypeError:
            print('Error: Amount has to be a float or an integer')

    def deposit(self, amount):
        try:
            if amount <= 0:
                print('Error: Amount has to be larger than 0')
            else:
                self.acc_bal += float(amount)
                one_log = TransactionLog('Deposit', amount)
                self.transaction_log.append((one_log.action, one_log.date))
                return True
        except TypeError:
            print('Error: Amount has to be a float or an integer')


    @property
    def balance(self):
        return self.acc_bal

    def __str__(self):
        return 'Name: {0}\nAccount Number: {1}\nAccount Balance: ${2}'.format(self.name, self.acc_num, self.acc_bal)

    # def change_name(self, new_name):
    #     self.name = str(new_name)
    #     return

    def show_transaction(self):
        print('\nAccount name: {}\nAccount number: {}'.format(self.name, self.acc_num))
        for items in self.transaction_log:
            print('Date: {}\nActivity: {}\nAmount: {}'.format(items[1], items[0][0], items[0][1]))
        return

if __name__ == "__main__":
    acc = Account('Nam', 1000)
    acc2 = Account('Jakob', 1000)
    acc2.deposit(200)
    acc2.withdraw(12)
    print(acc)
    print(acc2)
    acc2.show_transaction()