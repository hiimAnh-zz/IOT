__author__ = 'NA'

import pymysql


#khoi tao mysql
class PyMySQL():
    def __init__(self,host="localhost",user="root",password="1234",database="data_sensors"): #password = linh1999
        self.host = host
        self.db = pymysql.connect(host,user,password,database)
        self.cursor = self.db.cursor()
        self.tableName = "sensors"
        print("[MySQL][Connect]")
    
    def version(self):
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        print("[MySQL][Version] Database version: %s" %data)
    
    def close(self):
        self.db.close()
        print("[MySQL][Close]")
#ham thuc thi
    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        data = self.cursor.fetchall()
        print("[MySQL][Execute] %s" %sql)
        return data

    
    def createTable(self, tableName="sensors"):
        print("[MySQL][CreateTable]")
        self.tableName = tableName;
        sql = "CREATE TABLE IF NOT EXISTS " + str(tableName) + \
            """(id INT PRIMARY KEY AUTO_INCREMENT,
            temperature INT NOT NULL,
            humidity INT NOT NULL,
            light INT NOT NULL,
            time DATETIME NOT NULL
            )
            """
        self.execute(sql)

    def insertData(self, temp, humi, light, time):
        print("[MySQL][InsertData] ")
        sql = "INSERT INTO " + str(self.tableName) + "(temperature, humidity, light, time) VALUES (" \
            + str(temp) + ", " \
            + str(humi) + ", " \
            + str(light) + ", " \
            + "\"" + str(time) + "\")"
        self.execute(sql)

    # def selectData(self, select="*"):
    #     print("[MySQL][SelectData]")
    #     sql = "SELECT " + str(select) + " FROM " + str(self.tableName);
    #     for i in self.execute(sql):
    #         print(i)