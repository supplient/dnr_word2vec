import pymysql
from db_config import *

class readBasicData:

    def __init__(self):
        self.db = pymysql.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.db.cursor()
        self.cur_start = 0
        self.step = 10000
        #调整step，每次读入多少行数据
        self.sum = 1060676

    def search(self):
        all_tables = ", ".join(table_list)
        sql_select = "select keyword_cn from " + all_tables + " limit " + str(self.cur_start) + "," + str(self.step)
        self.cursor.execute(sql_select)

    def readOneData(self):
        result = self.cursor.fetchone()
        if result is None:
            self.cur_start = self.cur_start+self.step
            if self.cur_start > self.sum:
                return None

            self.search()
            return self.cursor.fetchone()
        else:
            return result

    def readManyData(self, size):
        result = self.cursor.fetchmany(size)
        if result == ():
            self.cur_start = self.cur_start + self.step
            if self.cur_start > self.sum:
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
