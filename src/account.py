from src.user import User


class Account:
    user = None
    username = None
    password = None
    last_login_date = None
    preferences = {
        "language": "EN"
    }

    def __init__(self, firstname, lastname, birthday, username, password):
        """
        asdf
        :param user:
        :param username:
        :param password:
        :param preferences:
        """

        self.user = User(firstname=firstname, lastname=lastname, birthday=birthday)
        self.username = username
        self.password = password

    def print_account(self):
        print("The username is: " + self.username)
        print("The password is: " + self.password)
        print(self.last_login_date)
        print(self.preferences)
        self.user.print_user()

    def set_login_date(self, date):
        self.last_login_date = date

    def change_preferences(self, preference_key, new_value):
        self.preferences[preference_key] = new_value

    def add_preferences(self, preference_key, value):
        self.preferences[preference_key] = value
