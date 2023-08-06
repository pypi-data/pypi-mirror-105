from view import View
from model import Model
import sys


class Controller:
    def __init__(self):
        self.view = View()
        self.model = Model()

    def pin_value_check(self):
        pin = self.view.get_pin_msg()
        pin2 = self.view.pin_confirm_msg()
        pin_value_check = self.model.pin_value_check(pin, pin2)
        while pin_value_check != 3:
            if pin_value_check == 1:
                self.view.value_error_msg()
                pin = self.view.get_pin_msg()
                pin2 = self.view.pin_confirm_msg()
                pin_value_check = self.model.pin_value_check(pin, pin2)
            elif pin_value_check == 0:
                self.view.pin_length_check_msg()
                pin = self.view.get_pin_msg()
                pin2 = self.view.pin_confirm_msg()
                pin_value_check = self.model.pin_value_check(pin, pin2)
            elif pin_value_check == 2:
                self.view.pin_not_match()
                pin = self.view.get_pin_msg()
                pin2 = self.view.pin_confirm_msg()
                pin_value_check = self.model.pin_value_check(pin, pin2)
        return pin

    def user_check(self):
        acc_num = self.view.get_acc_num()
        acc_num_check = self.model.no_user_check(acc_num)
        while acc_num_check != True:
            self.view.no_user_msg()
            acc_num = self.view.get_acc_num()
            acc_num_check = self.model.no_user_check(acc_num)
        return acc_num

    def pin_user_check(self, acc_num, pin):
        while self.model.pin_acc_num_check(acc_num, pin) != True:
            self.view.inc_pin_msg()
            pin = self.pin_value_check()

    def get_amount(self):
        try:
            amount = float(self.view.get_amount_msg())
            return amount
        except ValueError:
            self.view.value_error_msg()

    def run(self):
        teller_cred = self.view.get_teller_cred_msg().title()
        while teller_cred != 'q' or teller_cred != 'quit':
            while self.model.no_teller_check(teller_cred) != True:
                self.view.wrong_username_msg()
                teller_cred = self.view.get_teller_cred_msg().title()
            teller_pass = self.view.get_teller_pass_msg()
            while self.model.teller_password_check(teller_cred, teller_pass) != True:
                self.view.wrong_pass_msg()
                teller_pass = self.view.get_teller_pass_msg()
            self.view.main_menu()
            inp = self.view.choice_msg()
            while inp != '-q':
                if inp == '-c':
                    self.view.welcome_create_acc_msg()
                    fname = self.view.get_fname_msg()
                    lname = self.view.get_lname_msg()
                    pin = self.pin_value_check()
                    self.view.add_success_msg(self.model.add_account(fname, lname, pin))
                elif inp == '-d':
                    self.view.welcome_delete_acc_msg()
                    acc_num = self.user_check()
                    pin = self.pin_value_check()
                    self.pin_user_check(acc_num, pin)
                    self.model.del_account(acc_num)
                    self.view.del_success_msg()
                elif inp == '-m':
                    if self.model.no_account_check() == True:
                        self.view.no_account_msg()
                    else:
                        self.view.welcome_manage_acc_msg()
                        acc_num = self.user_check()
                        pin = self.pin_value_check()
                        self.pin_user_check(acc_num, pin)
                        self.view.manage_acc_menu()
                        inp2 = self.view.get_acc_mng()
                        while inp2 != '-q':
                            if inp2 == '-d':
                                self.view.cheq_save_menu()
                                inp3 = self.view.cheq_or_save_msg().title()
                                if inp3 == '1' or inp3 == 'Chequing':
                                    amount = self.get_amount()
                                    if self.model.deposit_chequing(acc_num, amount, '') == True:
                                        self.view.depos_success_msg(amount, 'Chequing')
                                elif inp3 == '2' or inp3 == 'Savings':
                                    amount = self.get_amount()
                                    if self.model.deposit_savings(acc_num, amount, '') == True:
                                        self.view.depos_success_msg(amount, 'Savings')
                            elif inp2 == '-w':
                                self.view.cheq_save_menu()
                                inp3 = self.view.cheq_or_save_msg().title()
                                if inp3 == '1' or inp3 == 'Chequing':
                                    amount = self.get_amount()
                                    if self.model.withdraw_chequing(acc_num, amount, '') == True:
                                        self.view.withdr_success_msg(amount, 'Chequing')
                                elif inp3 == '2' or inp3 == 'Savings':
                                    amount = self.get_amount()
                                    if self.model.withdraw_savings(acc_num, amount, ''):
                                        self.view.withdr_success_msg(amount, 'Savings')
                            elif inp2 == '-sb':
                                self.view.cheq_save_menu()
                                inp3 = self.view.cheq_or_save_msg().title()
                                if inp3 == '1' or inp3 == 'Chequing':
                                    self.view.show_balance(self.model.get_balance(acc_num, 'Chequing'))
                                elif inp3 == '2' or inp3 == 'Savings':
                                    self.view.show_balance(self.model.get_balance(acc_num, 'Savings'))
                            elif inp2 == '-st':
                                self.view.cheq_save_menu()
                                inp3 = self.view.cheq_or_save_msg()
                                if inp3 == '1' or inp3 == 'Chequing':
                                    self.view.show_transaction(self.model.get_transaction(acc_num, 'Chequing'))
                                elif inp3 == '2' or inp3 == 'Savings':
                                    self.view.show_transaction(self.model.get_transaction(acc_num, 'Savings'))
                            elif inp2 == '-h':
                                self.view.help_mng_acc_menu()
                            else:
                                self.view.invalid_choice_msg()
                            self.view.manage_acc_menu()
                            inp2 = self.view.get_acc_mng()
                elif inp == '-h':
                    self.view.help_main_menu()
                else:
                    self.view.invalid_choice_msg()
                self.view.main_menu()
                inp = self.view.choice_msg()
            sys.exit(0)




if __name__ == '__main__':
    controller = Controller()
    controller.run()
