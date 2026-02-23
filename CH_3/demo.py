import sqlite3

conn = sqlite3.connect('SalesDB/salesdb.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM sales')
sales_records = cursor.fetchall()
for record in sales_records:
    print(record)