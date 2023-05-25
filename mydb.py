import mysql.connector

class db():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="users")
    cur = mydb.cursor(buffered=True)   
    def drop_tables(self):
        pass



