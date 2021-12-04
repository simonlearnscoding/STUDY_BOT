import mysql.connector
import pymysql
"""
class db():
    mydb = mysql.connector.connect(
    host="134.122.105.194",
    user="sinon",
    password="12345678",
    #database="test",
    #auth_plugin='mysql_native_password'
    )
    #cur = mydb.cursor(buffered=True)   
    #def drop_tables():
     #   drop_tables()  
"""

class db():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="users")
    cur = mydb.cursor(buffered=True)   
    def drop_tables(self):
        pass
        #drop_tables(self)

# class db():

#     def __init__(self):
#         self.host = "127.0.0.1"
#         self.user = "root"
#         self.password = "unknown072"
#         self.db = "users"

#     def __connect__(self):
#         self.con = pymysql.connect(host="127.0.0.1", user="root", password="unknown072", db="users", cursorclass=pymysql.cursors.                               DictCursor)
#         self.cur = self.con.cursor()

#     def __disconnect__(self):
#         self.con.close()

#     def fetch(self, sql):
#         self.__connect__()
#         self.cur.execute(sql)
#         result = self.cur.fetchall()
#         self.__disconnect__()
#         return result

#     def fetchone(self, sql):
#         self.__connect__(self)
#         self.cur.execute(sql)
#         result = self.cur.fetchone()
#         self.__disconnect__()
#         return result

#     def execute(self, sql):
#         self.__connect__(self)
#         self.cur.execute(sql)
#         self.__disconnect__(self)
 
"""

def drop_tables(self):
        sql = ("DROP TABLE IF EXISTS User;")
        db.cur.execute(sql, )
        sql = ("DROP TABLE IF EXISTS Goal;")
        db.cur.execute(sql, )
        sql = ("DROP TABLE IF EXISTS Daily;")
        db.cur.execute(sql, )
        sql = ("DROP TABLE IF EXISTS Weekly;")
        db.cur.execute(sql, )
        sql = ("DROP TABLE IF EXISTS Monthly;")
        db.cur.execute(sql, )
        sql = ("DROP TABLE IF EXISTS Streaks;")
        db.cur.execute(sql, )
        sql = ("DROP TABLE IF EXISTS Week;")
        db.cur.execute(sql, )
        sql = ("DROP TABLE IF EXISTS Achievements;")
        db.cur.execute(sql, )
        
            # Create every Table
        sql = ("CREATE TABLE IF NOT EXISTS user (ID bigint, Bot Bool, Name varchar(50), NickName varchar(50), XP int);")
        db.cur.execute(sql, )
        sql = ("CREATE TABLE IF NOT EXISTS goal (ID bigint, Goal int, Current int, NickName varchar(50), measuredMin int, Won Bool);")
        db.cur.execute(sql, )
        sql = ("CREATE TABLE IF NOT EXISTS daily (ID bigint, Study int, Workout int, Yoga int, Reading int, Meditation int, Chores int, Creative int, Total int);")
        db.cur.execute(sql, )
        sql = ("CREATE TABLE IF NOT EXISTS weekly (ID bigint, Study int, Workout int, Yoga int, Reading int, Meditation int, Chores int, Creative int, Total int);")
        db.cur.execute(sql, )
        sql = ("CREATE TABLE IF NOT EXISTS monthly (ID bigint, Study int, Workout int, Yoga int, Reading int, Meditation int, Chores int, Creative int, Total int);")
        db.cur.execute(sql, )
        sql = ("CREATE TABLE IF NOT EXISTS streaks (ID bigint, Study int, Workout int, Yoga int, Reading int, Meditation int, Chores int, Creative int, Boots int, LongestSession int);")
        db.cur.execute(sql, )
        sql = ("CREATE TABLE IF NOT EXISTS week (ID bigint, Study int, Workout int, Yoga int, Reading int, Meditation int, Creative int, Chores int);")
        db.cur.execute(sql, )
        sql = ("CREATE TABLE IF NOT EXISTS achievements (ID bigint, Cage int, Won int, Lost int);")
        db.cur.execute(sql, )

"""

#cur = db.cursor()


