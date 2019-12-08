import pymysql, os

class UpdateRequest:
    def __init__(self):
        try:
            self.con = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='crt_capstone_1', port=3308)
            self.cur = self.con.cursor()
        except Exception as e:
            print("Connection with Database Failed! : ", e)
    def UpdateQuantity(self, pid, quantity):
        q = "UPDATE `product` SET `Quantity`=%s WHERE `id`=%s"
        q1 = "SELECT `Quantity` FROM `product` WHERE `id`=%s"
        self.cur.execute(q1, [pid])
        fct_q = self.cur.fetchall()
        os.system('cls')
        quantity_left = fct_q[0][0] - int(quantity)
        v = [quantity_left,pid]
        try:
            self.cur.execute(q, v)
            self.con.commit()
        except Exception as e:
            print("ERROR occured!!!", e)