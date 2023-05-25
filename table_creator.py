# THIS FILE WILL RECREATE THE ENTIRE DATABASE DO NOT JUST RUN IT!!
import mysql.connector


class db():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="users")
    cur = mydb.cursor(buffered=True)

    def create_db():
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
        sql = (
            "CREATE TABLE IF NOT EXISTS goal (ID bigint, Goal int, Current int, NickName varchar(50), measuredMin int, Won Bool);")
        db.cur.execute(sql, )
        sql = (
            "CREATE TABLE IF NOT EXISTS daily (ID bigint, Study int, Workout int, Yoga int, Reading int, Meditation int, Chores int, Creative int, Total int);")
        db.cur.execute(sql, )
        sql = (
            "CREATE TABLE IF NOT EXISTS weekly (ID bigint, Study int, Workout int, Yoga int, Reading int, Meditation int, Chores int, Creative int, Total int);")
        db.cur.execute(sql, )
        sql = (
            "CREATE TABLE IF NOT EXISTS monthly (ID bigint, Study int, Workout int, Yoga int, Reading int, Meditation int, Chores int, Creative int, Total int);")
        db.cur.execute(sql, )
        sql = (
            "CREATE TABLE IF NOT EXISTS streaks (ID bigint, Study int, Workout int, Yoga int, Reading int, Meditation int, Chores int, Creative int, Boots int, LongestSession int);")
        db.cur.execute(sql, )
        sql = (
            "CREATE TABLE IF NOT EXISTS week (ID bigint, Study int, Workout int, Yoga int, Reading int, Meditation int, Creative int, Chores int);")
        db.cur.execute(sql, )
        sql = ("CREATE TABLE IF NOT EXISTS achievements (ID bigint, Cage int, Won int, Lost int);")
        db.cur.execute(sql, )

db.create_db()