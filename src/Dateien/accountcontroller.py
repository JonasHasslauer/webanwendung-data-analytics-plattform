from src.account import Account
from datetime import date


class AccountController:
    accounts = []

    def create_account(self, firstname, lastname, birthday, username, password):
        account = Account(firstname=firstname, lastname=lastname, birthday=birthday, username=username, password=password)
        self.accounts.append(account)

    def get_managed_accounts(self):
        return len(self.accounts)

    def login(self, username, password):
        for a in self.accounts:
            if a.username == username and a.password == password:
                print("Login was successful")
                today = date.today()
                a.set_login_date(str(today))
                return a

    def print_accounts(self):
        for a in self.accounts:
            a.print_account()

    def find_account(self, username, password):
        for a in self.accounts:
            if a.username == username and a.password == password:
                return a
        return False