import sqlite3


def create_db():
    con = sqlite3.connect(database=r'zstore.db')
    cur = con.cursor()

    # Tables
    cur.execute("CREATE TABLE IF NOT EXISTS Employee(ID INTEGER PRIMARY KEY AUTOINCREMENT, Gender text, Contact text, Name text, DateofBirth text, DateofJoining text, Email text, Password text, UserType text, Address text, Salary text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Supplier(Invoice INTEGER PRIMARY KEY AUTOINCREMENT, Name text, Contact text, Description text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL, supplier TEXT NOT NULL, price REAL NOT NULL, qty INTEGER NOT NULL)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS sales(id INTEGER PRIMARY KEY AUTOINCREMENT, customer_name TEXT, customer_contact TEXT, product_id INTEGER, product_name TEXT, quantity INTEGER, price REAL, total REAL, sale_date TEXT)")
    con.commit()

    con.close()

create_db()
