import pymysql
from datetime import date

class InvoiceGenerator:
    def __init__(self):
        try:
            self.con = pymysql.connect(host='127.0.0.1',user='root',passwd='',db='crt_capstone_1',port=3308)
            self.cur = self.con.cursor()
        except Exception as e:
            print("Error in db connection : ", e)
    def generateInvoice(self,user):
        q = 'SELECT `id`, `PID`, `PName`, `Price`, `Quantity`,`TotalPrice` FROM `invoice` WHERE `Date`=%s AND `Username`=%s'
        val = [date.today(), user]
        invoice = dict()
        try:
            self.cur.execute(q,val)
            data = self.cur.fetchall()
            invoice['id'] = data[0][0]
            invoice['date'] = date.today()
            invoice['lines'] = []
            total = 0
            for i in data:
                total += i[5]
                invoice['lines'].append(list(i[1:]))
            invoice['total'] = total
            return invoice
        except Exception as e:
            print("Error occured! ", e)