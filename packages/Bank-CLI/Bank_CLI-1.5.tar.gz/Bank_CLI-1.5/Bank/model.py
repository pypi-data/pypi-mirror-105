import json
from chequing import Chequing
from savings import Savings

import random

class Model():

    _NEXT_ACC_NUM = 1000000

    def __init__(self):
        self.filename = 'accounts.json'
        self.accounts = {}
        self.tellers = {}


    def write_file(self):
        with open(self.filename, 'w') as open_f:
            json.dump(self.accounts, open_f)

    def read_file(self):
        try:
            with open(self.filename, 'r') as open_f:
                self.accounts = {}
                self.accounts = json.load(open_f)
        except FileNotFoundError:
            self.write_file()

    def read_tellers_file(self):
        with open('tellers.json', 'r') as open_f:
            self.tellers = json.load(open_f)


    def add_account(self, f_name, l_name, pin):
        self.read_file()
        if len(self.accounts) == 0:
            n = 1
            acc_num = n
        else:
            n = 0
            for user in self.accounts:
                if n < int(user):
                    n = int(user)
            acc_num = n + 1
        keys = self._encrypt(pin)
        self.accounts[acc_num] = {'PIN': keys[0], 'First Name': f_name.title(), 'Last Name': l_name.title(), 'Type': {'Chequing': {'Balance': 0, 'Transaction Log': []}, 'Savings': {'Balance':0, 'Transaction Log': []}}, 'key': keys[1]}
        self.write_file()
        return acc_num

    def del_account(self, acc_num):
        self.read_file()
        del self.accounts[str(acc_num)]
        self.write_file()


    def pin_check(self, acc_num, pin):
        self.read_file()
        if int(pin) == int(self.accounts[acc_num]['PIN'])/int(self.accounts[acc_num]['key']):
            return True

    def no_user_check(self, acc_num):
        self.read_file()
        if str(acc_num) in self.accounts:
            return True

    def no_teller_check(self, teller):
        self.read_tellers_file()
        if teller in self.tellers:
            return True

    def teller_password_check(self, teller, password):
        self.read_tellers_file()
        if str(password) == str(self.tellers[teller]['Password']):
            return True


    def pin_value_check(self, pin1, pin2):
        try:
            pin1 = int(pin1)
            pin2 = int(pin2)
            if self.check_length(4, len(str(pin1)), 6) != True or self.check_length(4, len(str(pin2)), 6) != True:
                return 0
            else:
                if pin1 == pin2:
                    return 3
                else:
                    return 2
        except ValueError:
            return 1

    def check_length(self, expected_length, actual_length, expected_length2=None):
        if actual_length == expected_length or actual_length == expected_length2:
            return True

    def pin_acc_num_check(self, acc_num, pin):
        self.read_file()
        if int(pin) == int(self.accounts[acc_num]['PIN'])/int(self.accounts[acc_num]['key']):
            return True

    def deposit_chequing(self, acc_num, amount, name):
        self.read_file()
        account = Chequing(name)
        account.acc_bal = self.accounts[acc_num]['Type']['Chequing']['Balance']
        if account.deposit(amount) == True:
            self.accounts[acc_num]['Type']['Chequing']['Balance'] = account.acc_bal
            one_log = '{} ${} on {}'.format(account.transaction_log[0][0][0], account.transaction_log[0][0][1], account.transaction_log[0][1])
            self.accounts[acc_num]['Type']['Chequing']['Transaction Log'].append(one_log)
            self.write_file()
            return True


    def deposit_savings(self, acc_num, amount, name):
        self.read_file()
        account = Savings(name)
        account.acc_bal = self.accounts[acc_num]['Type']['Savings']['Balance']
        if account.deposit(amount) == True:
            self.accounts[acc_num]['Type']['Savings']['Balance'] = account.acc_bal
            one_log = '{} ${} on {}'.format(account.transaction_log[0][0][0], account.transaction_log[0][0][1], account.transaction_log[0][1])
            self.accounts[acc_num]['Type']['Savings']['Transaction Log'].append(one_log)
            self.write_file()
            return True


    def withdraw_chequing(self, acc_num, amount, name):
        self.read_file()
        account = Chequing(name)
        account.acc_bal = self.accounts[acc_num]['Type']['Chequing']['Balance']
        if account.withdraw(amount) == True:
            self.accounts[acc_num]['Type']['Chequing']['Balance'] = account.acc_bal
            one_log = '{} ${} on {}'.format(account.transaction_log[0][0][0], account.transaction_log[0][0][1], account.transaction_log[0][1])
            self.accounts[acc_num]['Type']['Chequing']['Transaction Log'].append(one_log)
            self.write_file()
            return True


    def withdraw_savings(self, acc_num, amount, name):
        self.read_file()
        account = Savings(name)
        account.acc_bal = self.accounts[acc_num]['Type']['Chequing']['Balance']
        if account.withdraw(amount) == True:
            self.accounts[acc_num]['Type']['Savings']['Balance'] = account.acc_bal
            one_log = '{} ${} on {}'.format(account.transaction_log[0][0][0], account.transaction_log[0][0][1], account.transaction_log[0][1])
            self.accounts[acc_num]['Type']['Savings']['Transaction Log'].append(one_log)
            self.write_file()
            return True

    def no_account_check(self):
        self.read_file()
        if len(self.accounts) == 0:
            return True

    def get_balance(self, acc_num, type):
        self.read_file()
        return self.accounts[acc_num]['Type'][type]['Balance']

    def get_transaction(self, acc_num, type):
        self.read_file()
        return self.accounts[acc_num]['Type'][type]['Transaction Log']

    def _encrypt(self, pin):
        rand = random.randint(17,42)
        hashed_pin = int(pin)*rand
        return (hashed_pin, rand)

    # def _decrypt(self, hashed_pin, key):
    #     pin = int(hashed_pin)/int(key)
    #     return int(pin)


if __name__ == '__main__':
    m = Model()
    the_tuple = m._encrypt(1234)
    print("The hashed password is", the_tuple)

