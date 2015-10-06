#encoding=UTF-8
__author__ = 'Hao'

import sys
import MySQLdb
import csv

reload(sys)
sys.setdefaultencoding('utf-8')

conn = MySQLdb.connect(host='localhost',user='root',passwd='',db ='workshop',port = 3306,charset="utf8")
cur = conn.cursor()
cur.execute("SET NAMES utf8")
cur.execute("use workshop")

cur.execute("select * from forthcomingworkshop")
result=cur.fetchall()
#这样做的目的是为了输出 每一个tuple里面的每一个元素，这样就可以看到汉字了
c = csv.writer(open("temp.csv","wb"))
for row in result:
    c.writerow(row)
cur.close()
conn.commit()
conn.close()
