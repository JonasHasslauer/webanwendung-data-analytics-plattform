from src.accountcontroller import AccountController

ac = AccountController()
while True:
    a = input("Do you want to create a user (y/yes), login (login), search a account (searchAccount) or quit (q)?")
    if a == "yes" or a == "y":
        c = input("What is your first name?")
        d = input("What is your last name?")
        e = input("What is your birthday?")
        f = input("What is your username?")
        password = input("What is your password?")
        ac.create_account(firstname=c,lastname=d,birthday=e,username=f,password=password)
        print(ac.get_managed_accounts())
    elif a == "q":
        break
    elif a == "login":
        un = input("Your username")
        pw = input("Your password?")
        ac.login(username=un, password=pw)
    elif a == "searchAccount":
        n = input("Your username")
        pw = input("Your password?")
        account = ac.find_account(username=un,password=pw)
        # If the find_account method returns a object, then it is the same as True
        if account:
            account.print_account()
    else:
        print("Sorry, I didn't understand you.")
        break