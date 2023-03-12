import db as db

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="unknown072",
  database="users"
)
cur = db.cursor(buffered= True)
print(mydb)

