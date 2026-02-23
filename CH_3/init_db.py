import sqlite3

conn = sqlite3.connect('SalesDB/salesdb.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    sale_date TEXT NOT NULL
)''')

sales_data = [
    ('Laptop', 2, 1200.00, '2024-01-15'),
    ('Smartphone', 5, 800.00, '2024-01-16'),
    ('Headphones', 10, 150.00, '2024-01-17'),
    ('Monitor', 3, 300.00, '2024-01-18'),
    ('Keyboard', 7, 100.00, '2024-01-19')
]

cursor.executemany('INSERT INTO sales (product_name, quantity, price, sale_date) VALUES (?, ?, ?, ?)', sales_data)

conn.commit()
conn.close()