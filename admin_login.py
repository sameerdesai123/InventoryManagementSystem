import getpass, sys

class AdminLogin:
    def __init__(self):
        print("\n\n\n\n\n\n\t\t\t\t\t\t#############Entering Admin Login#############\n\n")
    def verify(self):
        self.username = input("\t\tUsername : ")
        try:
            self.password = getpass.getpass(prompt=("\t\tPassword : "), stream=sys.__stderr__)
            if self.username == "admin" and self.password == "pass#":
                return True
            else:
                return False
        except Exception as e:
            print("Error Occured : ", e)            