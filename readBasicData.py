import pymysql
from db_config import *

class readBasicData:

    def __init__(self):
        self.db = pymysql.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.db.cursor()
        self.table_list = table_list
        self.table_cnt = 0

        if len(table_list) < 1:
            raise Exception("Too few tables to search")
        self.table = table_list[0]


    def search(self):
        sql_select = "select " + column_keyword + " from " + self.table
        self.cursor.execute(sql_select)

    def readOneData(self):
        if self.table == None:
            return None

        result = self.cursor.fetchone()
        if result is None:
            # Change to next table
            self.table_cnt += 1 
            if self.table_cnt >= len(self.table_list):
                self.table = None
                return None
            self.table = self.table_list[self.table_cnt]
            self.search()
            return self.cursor.fetchone()
        else:
            return result

    def readManyData(self, size):
        result = self.cursor.fetchmany(size)
        if result == ():
            # Change to next table
            self.table_cnt += 1 
            if self.table_cnt >= len(self.table_list):
                self.table = None
                return None
            self.table = self.table_list[self.table_cnt]
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
        a= x.readManyData(1000)
