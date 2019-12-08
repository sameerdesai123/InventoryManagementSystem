import pymysql,os
from admin_login import AdminLogin
from invoiceGenerator import InvoiceGenerator
from time import sleep
from tabUpdateRequest import UpdateRequest

class InvaildChoice(Exception):
    pass

class AdminDash:
    def __init__(self):
        try:
            self.con = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='crt_capstone_1', port=3308)
            self.cur = self.con.cursor()
            self.cart = []
        except Exception as e:
            print("Connection with Database Failed! : ", e)
            return
        admin = AdminLogin()
        c = 0
        while c < 3:
            verified = admin.verify()
            if verified == True:
                break
            else:
                c += 1
        if not verified:
            print("Wrong Credentials!!")
            return
        else:
            self.flag = 0
            numbers = ['1','2','3','4', '5','6','7','8','9','0']
            print("\t\t\t\tLogin Successful!")
            sleep(2)
            os.system('cls')
            while self.flag == 0:
                print("\n\n\n\n\n\n\t\t\t\t\t\tChoose a task :\n\n")
                menu = "\t\t\t1.Add\t2.Update\t3.Delete\t4.ProductList\t5.CustomerList\t6.InvoiceList\t7.Exit"
                print(menu)
                op = input("\t\t\t\t\t\t\t---> ")
                os.system('cls')
                if op not in numbers:
                    if op not in menu:
                        try:
                            raise InvaildChoice
                        except Exception as e:
                            print("Invalid Choice", e)
                    else:
                        eval('self.{}'.format(op))
                elif op in ['1','2','3','4', '5', '6', '7']:
                    if op == '1':
                        self.Add()
                    elif op == '2':
                        self.Update()
                    elif op == '3':
                        self.Delete()
                    elif op == '4':
                        self.ProductList()
                    elif op == '5':
                        self.CustomerList()
                    elif op == '6':
                        self.InvoiceList()
                    else:
                        self.Exit()
                else:
                    try:
                        raise InvaildChoice
                    except Exception as e:
                        print("Wrong Choice!", e)
    
    def IsPresent(self, values):
        query = "SELECT `Name`, `Category`, `MRP`, `Company`, `date_of_expiry` FROM `Product` WHERE 1"
        q = "SELECT `id` FROM `product` WHERE `Name`=%s AND `Category`=%s AND `MRP`=%s AND `Company`=%s AND `date_of_expiry`=%s"
        self.cur.execute(query)
        data = self.cur.fetchall()
        if tuple(values) in data:
            print("Entry already exists. Do you wish to update quantity? Y/N : ")
            op = input()
            if op == 'Y' or op == 'y':
                self.cur.execute(q, values)
                ID = self.cur.fetchall()
                obj = UpdateRequest()
                obj.UpdateQuantity(ID[0][0], -values[3])
                print("Quanity Updated!")
                sleep(1)
            return True
        return False
    
    def Add(self):
        # Adding row of new values into DB
        name, category, mrp = input("Enter Product Name : "), input("Enter Category : "), float(input("Enter MRP"))
        quantity,company, date_of_expiry = int(input("Enter Quantity : ")), input("Enter Company : "), input("Enter Date of Expiry: ")
        query = 'INSERT INTO PRODUCT(Name,Category,MRP,Quantity,Company,date_of_expiry) VALUES(%s,%s,%s,%s,%s,%s)'
        values = [name,category,mrp,quantity,company,date_of_expiry]
        if self.IsPresent(values):
            return
        self.cur.execute(query,values)
        self.con.commit()
        print("Product Added")
        os.system('cls')
    
    def Update(self):
        # code to update Product details ( Price or Quantity )
        q = "UPDATE `product` SET `MRP`=%s,`Quantity`=%s WHERE `id`=%s"
        os.system('cls')
        self.ProductList()
        print("\n\n\n\n\t\t\t\t\tEnter id for Updation : ", end='')
        op = int(input())
        try:
            v = [float(input("\n\tMRP : ")), int(input("\n\tEnter Quantity : ")), op]
            self.cur.execute(q,v)
            self.con.commit()
            print("Update Complete!")
            sleep(0.5)
        except Exception as e:
            print("Error oon Update : ", e)
    
    def Delete(self):
        self.ProductList()
        print("Delete based on Product - ID")
        p_id = int(input("Enter Product ID : ")) 
        query = 'DELETE FROM `Product` WHERE id=%s'
        values = [p_id]
        self.cur.execute(query, values)
        self.con.commit()
        os.system('cls')
    
    def ProductList(self):
        query = "SELECT * FROM `Product` WHERE 1"
        self.cur.execute(query)
        data = self.cur.fetchall()
        print()
        menu = "ID Product Category MRP Quantity Company Date_Of_Expiry".split(' ')
        for i in menu:
            print(i.ljust(23), end='')
        print()
        for i in data:
            for j in i:
                print(str(j).ljust(23), end='')
            print()
    
    def CustomerList(self):
        s = "SELECT `id`, `FullName`, `Email`, `Mobile` FROM `register` WHERE 1"
        self.cur.execute(s)
        cust_list = self.cur.fetchall()
        head = "ID FullName Email Mobile".split(' ')
        for i in head:
            print(i.ljust(23), end='')
        print()
        for i in cust_list:
            for j in i:
                print(str(j).ljust(23), end='')
            print()
    
    def InvoiceList(self):
        # code for retiriving and printing invoices
        try:
            q = "SELECT `id`, `Date`, `PID`, `PName`, `Quantity`, `Price`, `TotalPrice`, `Username` FROM `invoice` WHERE 1"
            self.cur.execute(q)
            data = self.cur.fetchall()
            head = "ID DATE PID PNAME QUANTITY PRICE TOTALPRICE CUSTOMER".split(' ')
            for i in head:
                print(i.ljust(20), end='')
            print()
            for i in data:
                for j in i:
                    print(str(j).ljust(20), end='')
                print()
                # print(str(total))
        except Exception as e:
            print("ERROR in InvoiceList : ", e)
    
    def Exit(self):
        self.flag = 1
        self.con.close()
        return