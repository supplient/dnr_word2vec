import pymysql
from db_config import *

class readBasicData:

    def __init__(self):
        self.db = pymysql.connect(host=host, user=user, password=password, database=databse);
        self.cursor = self.db.cursor()
        self.table = "id_keyword_1"
        self.table_cnt =0


    def search(self):
        sql_select = "select keyword_cn from "+self.table
        self.cursor.execute(sql_select)


    def readOneData(self):
        result = self.cursor.fetchone()
        if result is None:
            if self.table_cnt==0:
                self.table = "id_keyword_2"
            else:
                if self.table_cnt==1:
                    self.table = "id_keyword_3"
                else:
                    return None
            self.search()
            return self.cursor.fetchone()
        else:
            return result

    def readManyData(self, size):
        result = self.cursor.fetchmany(size)
        if result == ():
            if self.table_cnt == 0:
                self.table = "id_keyword_2"

            else:
                if self.table_cnt == 1:
                    self.table = "id_keyword_3"
                else:
                    return None
            self.search()
            return self.cursor.fetchmany(size)
        else:
            return result

    def end(self):
        self.cursor.close()


if __name__ == "__main__":
    sum = 0
    x = readBasicData()
    x.search()
    a = x.readManyData(1000)

    while a is not None:
        sum = sum + 1000
        print("sum:",sum)
        print("cur_start:",x.cur_start)
        a= x.readManyData(1000)
