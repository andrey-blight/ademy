import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='your_password!?',
                       database='site_db')  # TODO change passowrd
cur = conn.cursor()
cur.execute("CREATE DATABASE site_db")
cur.close()
conn.close()
