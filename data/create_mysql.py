import pymysql

# Создать соединение
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='your_password',
                       database='site_db')  # TODO change passowrd

cur = conn.cursor()

cur.close()
# Закрыть соединение
conn.close()
