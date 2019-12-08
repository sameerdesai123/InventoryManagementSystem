import pymysql

class LoginDetailsFromDB:
    def __init__(self):
        try:
            self.con = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='crt_capstone_1', port=3308)
            self.cur = self.con.cursor()
        except Exception as e:
            print("Connection with Database Failed! : ", e)
            return
    def getValues(self):
        # return a list of usernames and passwords
        query = 'SELECT `username`, `password` FROM `cust_login` WHERE 1'
        self.cur.execute(query)
        data = self.cur.fetchall()
        return data