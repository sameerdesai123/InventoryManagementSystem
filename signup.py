import pymysql, sys, getpass, os
from time import sleep

def Signup():
    try:
        f = 0
        con = pymysql.connect(host='127.0.0.1',user='root',passwd='',db='crt_capstone_1',port=3308)
        cur = con.cursor()
        Fname,Lname,username,email,dob,address,mobile = input("\n\t\tFirst Name : "), input("\t\tLast Name : "),input("\t\tUserName : "), input("\t\tEmail : "), input("\t\tDOB: "), input("\t\tAddress : "), input("\t\tMobile : ")
        full_name = ' '.join([Fname,Lname])
        try:
            while f == 0 :
                password = getpass.getpass(prompt=("\t\tEnter Password : "), stream=sys.__stderr__)
                cnfPassword = getpass.getpass(prompt=("\t\tConfirm Password : "), stream=sys.__stderr__)
                if password == cnfPassword:
                    f = 1
                else:
                    print("Passwords don't Match!")
                os.system('cls')
            q1 = "INSERT INTO `register`(`FullName`, `Email`, `DOB`, `Address`, `Mobile`, `FirstName`, `LastName`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            v1 = [full_name, email, dob, address, mobile, Fname, Lname]
            q2 = "INSERT INTO `cust_login`(`username`, `password`) VALUES (%s,%s)"
            v2 = [username, password]
            cur.execute(q1,v1)
            con.commit()
            cur.execute(q2,v2)
            con.commit()
            print("SUCCESS")
            sleep(1)
            os.system('cls')
            con.close()
        except Exception as e:
            print("Failed Registration", e)
    except Exception as e:
        print("Failed Connection!", e)