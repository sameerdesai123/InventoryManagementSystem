import getpass, sys, pymysql
from cust_details import LoginDetailsFromDB

class CustLogin:
    def __init__(self):
        print("\n\n\n\n\n\t\t\t\t\t############Entering Customer Login###############")
        self.loginCred = LoginDetailsFromDB()
    def verify(self):
        self.username = input("\t\t\tUsername : ")
        try:
            self.password = getpass.getpass(prompt=("\t\t\tPassword : "), stream=sys.__stderr__)
            cred = (self.username, self.password)
            data = self.loginCred.getValues()
            if cred in data:
                self.session_user = self.username 
                return True
            else:
                return False
        except Exception as e:
            print("Error Occured : ", e)
    def getUser(self):
        return self.session_user