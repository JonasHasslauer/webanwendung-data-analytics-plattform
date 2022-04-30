class User:

    firstname = None
    lastname = None
    birthday = None

    def __init__(self, firstname, lastname, birthday):
        """
        Constructor
        :param username: The username of the user
        :param firstname: The firstname of the user
        :param lastname: The lastname of the user
        :param birthday: The birthday of the user
        """

        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday

    def print_first_name(self):
        print("The first name of the user is: " + self.firstname)

    def print_last_name(self):
        print("The last name of the user is: " + self.lastname)

    def print_birthday(self):
        print("The birthday of the user is: " + self.birthday)

    def print_user(self):
        print(self.firstname,self.lastname,self.birthday)