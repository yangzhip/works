import pymysql

db = pymysql.connect("172.17.0.2", "root", "123456", "mydb", charset='utf8' )

cursor = db.cursor()
sql = """CREATE TABLE SPORTNEWS(
         Link  CHAR(100) primary key ,    
         tittle char (50) )"""
cursor.execute(sql)
db.close()