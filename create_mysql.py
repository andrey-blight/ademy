import pymysql

conn = pymysql.connect(host='127.0.0.1', user='USER', passwd='PASSWORD')
cur = conn.cursor()
cur.execute("CREATE DATABASE site_database")
cur.close()
conn.close()
