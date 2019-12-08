import pymysql, os
from datetime import date
from cus_login import CustLogin
from signup import Signup
from tabUpdateRequest import UpdateRequest
from invoiceGenerator import InvoiceGenerator
from colorama import Fore, Back, Style
from time import sleep

class InvaildChoice(Exception):
    pass

class CustDash:
    def __init__(self):
        try:
            self.con = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='crt_capstone_1', port=3308)
            self.cur = self.con.cursor()
            self.cart = []
        except Exception as e:
            print("Connection with Database Failed! : ", e)
        print("\n\n\n\n\t\t\t\t############ WELCOME #############\n\n\t\t1.Signup\t\t2.Login")
        op = input("\n\t\t\t--> ")
        if(op == '1' or op == 'Signup'):
            Signup()
        os.system('cls')
        self.mainDashboard()
    def mainDashboard(self):
        cust = CustLogin()
        numbers = ['1','2','3','4', '5','6','7','8','9','0']
        c = 0
        while c < 3:
            verified = cust.verify()
            if verified == True:
                break
            else:
                c += 1
        if not verified:
            print( Style.BRIGHT + "Wrong Credentials!!")
            return
        else:
            self.flag = 0
            print("Login Successful!")
            sleep(1)
            self.session_user = cust.getUser()
            cust = None
            os.system('cls')
            while self.flag == 0:
                print("\n\n\n\n\t\t\t\tChoose a task :\n")
                menu = "\t\t\t0.MyAccount\t1.ProductList\t2.MyCart\t3.Checkout\t4.Exit"
                print(menu)
                op = input("\n\t\t\t\t--->")
                os.system('cls')
                if op not in numbers:
                    if op not in menu:
                        try:
                            raise InvaildChoice
                        except Exception as e:
                            print("Invalid Choice", e)
                    else:
                        eval('self.{}'.format(op))
                elif op in ['0','1','2','3','4']:
                    if op == '1':
                        self.ProductList()
                    elif op == '2':
                        self.MyCart()
                    elif op == '3':
                        self.Checkout()
                    elif op == '0':
                        # code for MyAccount
                        self.MyAccount()
                        pass
                    else:
                        self.Exit()    
                else:
                    try:
                        raise InvaildChoice
                    except Exception as e:
                        print("Wrong Choice!", e)
    
    def MyAccount(self):
        q_get_details = "SELECT `FullName`, `Email`, `DOB`, `Address`, `Mobile` FROM `register` WHERE `id`=%s"
        q_get_id = "SELECT `id` FROM `cust_login` WHERE `username`=%s"
        v_user = [self.session_user]
        try:
            self.cur.execute(q_get_id, v_user)
            ID = self.cur.fetchall()
            self.cur.execute(q_get_details, [ID[0]])
            data = self.cur.fetchall()
            head = "FullName Email DOB Address Mobile".split(' ')
            for i in head:
                print(i.ljust(23), end='')
            print()
            for i in data:
                for j in i:
                    print(str(j).ljust(23), end='')
                print()
            op = input("\n\n\t\tDo you wish to update your Profile ? Y/N : ")
            if op == 'Y' or op == 'y':
                while op != 'n' and op!='N':
                    attr = input("\n\tEnter attribute Name to be updated : (as in table header ) : ")
                    if attr == 'Email':
                        q_update = "UPDATE `register` SET Email=%s WHERE `id`=%s"
                    elif attr == 'DOB':
                        q_update = "UPDATE `register` SET DOB=%s WHERE `id`=%s"
                    elif attr == 'Address':
                        q_update = "UPDATE `register` SET Address=%s WHERE `id`=%s"
                    elif attr == 'Mobile':
                        q_update = "UPDATE `register` SET Mobile=%s WHERE `id`=%s"
                    else:
                        print("You are not allowed to change this !!")
                        sleep(1)
                        break
                    v_update = [input("\tEnter attr Value : "), ID[0][0]]
                    self.cur.execute(q_update, v_update)
                    self.con.commit()
                    op = input("\n\tUpdate Complete ..\n\nDo you wish to alter other details ? Y/N :")
                    os.system('cls')
        except Exception as e:
            print("Error ! ", e)

    def ProductList(self):
        q = "SELECT `id`, `Name`, `Category`,`MRP`, `Quantity` FROM `product` WHERE 1"
        self.cur.execute(q)
        self.prodList = self.cur.fetchall()
        data = self.prodList
        while True:
            head = "ID NAME CATEGORY MRP QUANTITY".split(' ')
            print("\n\n")
            for i in head:
                print(i.ljust(23), end='')
            print()
            for row in self.prodList:
                for val in row:
                    print(str(val).ljust(23), end='')
                print()
            l = None
            sub_op = input("\n\tWould you like to add items to cart ? Y/N : ")
            if sub_op == 'N' or sub_op == 'n':
                return
            new_prod = int(input("Enter Product ID :"))
            for i in data:
                if i[0] == new_prod:
                    q1 = int(input("Enter Quantity: "))
                    if q1 > i[4]:
                        print("Sorry request exceeds stock!")
                        continue
                    l = [i[0],i[1], i[3],q1]
            if l == None:
                print("Wrong ID")
                continue
            self.cart.append(l)
            contOp = input("\n\tDo you want to continue? Y/N : ")
            if (contOp == 'N' or contOp == 'n'):
                os.system('cls')
                break
            os.system('cls')
    def MyCart(self):
        while True:
            os.system('cls')
            print("\n\n\n\t\t\t\t1.Your Orders\t\t 2.Current Cart")
            op = int(input("\n\t\t\t\tEnter Choice : "))
            if op == 1:
                q = "SELECT `id`, `Date`, `PID`, `PName`, `Quantity`, `Price`, `TotalPrice` FROM `cart` WHERE Username=%s"
                v = [self.session_user]
                self.cur.execute(q, v)
                cartData = self.cur.fetchall()
                os.system('cls')
                l, l1 = [], []
                head = "ID DATE PID PName Quantity Price TotalPrice".split(' ')
                if len(cartData) == 0:
                    print("\n\n\t\t\t\t\tNo Previous Orders")
                    sleep(0.5)
                    continue
                for i in head:
                    print(i.ljust(23), end='')
                print()
                for i in cartData:
                    l1.append(i[0])
                    l.append([i[2],i[3],i[5],int(i[4])])
                    for j in i:
                        print(str(j).ljust(23), end='')
                    print()
                f = 0
                while f == 0:
                    rep_choice = input("Select id of cart to add : {q to skip}")
                    if rep_choice == 'q':
                        l = []
                        print("Old Order not included in current cart")
                        break
                    for i in l1:
                        if i == int(rep_choice):
                            l = l[l1.index(i)]
                            f = -1
                            ch = input("\nDo You want to add these to your Current Cart? (Y/N)")
                            if ch == 'Y' or ch == 'y':
                                print(l)
                                self.cart.extend([l])
                                print(self.cart)
                    if f == 0:
                        print("Wrong Choice!:")
            elif op == 2:
                if self.cart == []:
                    print('\t\t\tEMPTY')
                    sleep(0.5)
                    self.ProductList()
                    break
                head1 = "ID NAME MRP QUANTITY".split(' ')
                for i in head1:
                    print(i.ljust(23), end='')
                print()
                for i in self.cart:
                    for j in i:
                        print(str(j).ljust(23), end='')
                    print()
                break
        else:
            try:
                raise InvaildChoice
            except:
                print("Wrong Choice : Try Again!")
    
    def Checkout(self):
        # Confirm buying cart
        cnf = input("\n\tDO YOU WANT TO PROCEED TO BILLING ? (Y?N)")
        if cnf == 'N' or cnf == 'n':
            os.system('cls')
            return
        # Update Product Table
        secret = UpdateRequest()
        for row in self.cart:
            secret.UpdateQuantity(row[0], row[3])
        secret = None
        print("\n\n\t\t\t\tPURCHASE COMPLETE\n\n")
        # Update Cart Table
        self.SaveCart()
        self.SaveInvoice()
        self.displayInvoice()
        self.cart = []
        input("Enter any key to continue....")
        os.system('cls')

    def SaveCart(self):
        try:
            q = "INSERT INTO `cart`(`Date`, `PID`, `PName`, `Quantity`, `Price`, `TotalPrice`, `Username`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            today, username = date.today(), self.session_user
            for i in self.cart:
                val = [str(today), i[0], i[1], i[3], i[2], i[2]*int(i[3]), username]
                self.cur.execute(q, val)
            self.con.commit()
        except Exception as e:
            print("ERROR occured in Save Cart", e)

    def SaveInvoice(self):
        try:
            q = "INSERT INTO `invoice`(`Date`, `PID`, `PName`, `Quantity`, `Price`, `TotalPrice`, `Username`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            today, username = date.today(), self.session_user
            for i in self.cart:
                val = [str(today), i[0], i[1], i[3], i[2], i[2]*int(i[3]), username]
                self.cur.execute(q, val)
            self.con.commit()
        except Exception as e:
            print("ERROR occured in Save Cart", e)
    
    def displayInvoice(self):
        obj = InvoiceGenerator()
        invoice = obj.generateInvoice(self.session_user)
        print("\t\t\t\t\tINVOICE\n\n\t\t")
        print("\tInvoice ID", invoice['id'], "\n")
        print("\tDATE : ", invoice['date'], "\n")
        head = "PID PName Price Quantity SubTotal".split(' ')
        for i in head:
            print(i.ljust(23), end='')
        print()
        for i in invoice['lines']:
            for j in i:
                print(str(j).ljust(23), end='')
            print()
        print("\n\t\t\tTotal : ", invoice['total'])

    def Exit(self):
        os.system('cls')
        self.con.close()
        self.flag = 1
        print("Exiting")