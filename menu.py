from admin_dash import AdminDash
from cus_dash import CustDash
import os
from colorama import init
from colorama import Fore, Back, Style
from time import sleep
init()
class InvalidChoiceOnMainMenu(Exception):
    pass

os.system('cls')
print(Fore.MAGENTA + Back.LIGHTWHITE_EX + Style.BRIGHT)
print()
os.system('cls')
print('\n\n\n\n\n\n\n\n\n\t\t\t\t***************WELCOME********************')
sleep(0.5)
os.system('cls')
print("\n\n\n\n\n\t\t\t\t\t********************Main Menu********************\n\n\n")
while True:
    try:
        op = int(input("\t\t\t1.Admin\t\t\t2.Customer\n\n\t\t\tChoose Login Type : "))
        os.system('cls')
        if not((op == 1) or (op == 2)):
            raise InvalidChoiceOnMainMenu
        else:
            if op == 1:
                obj = AdminDash()
                print(Style.RESET_ALL + "END OF PROGRAM")
                break
            elif op == 2:
                obj = CustDash()
                print(Style.RESET_ALL + "END OF PROGRAM")
                break 
    except InvalidChoiceOnMainMenu as e:
        print("Entered an invalid choice !")
        print(e, "\nTry Again !")