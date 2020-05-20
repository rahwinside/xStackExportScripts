#!C:/Users/danie/AppData/Local/Programs/Python/Python38-32/python.exe
import sys
from datetime import time

import mysql.connector
from mysql.connector import errorcode


def mysql_connection():
    global department, semester, hour, date, day
    config = {
        'user': 'root',
        'password': 'vcvra-1002',
        'host': 'localhost',
        'database': 'attendance',
        'raise_on_warnings': True
    }

    try:
        # check in super time table
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT * FROM attendance.time_table_super WHERE department = {department} AND semester = {semester} AND override_date = {date} AND hour = {hour}".format(
            department=department, semester=semester, date=str(date), hour=hour)
        cursor.execute(query)

        # block if super time table is true
        # todo
        cursor.close()
        # return

        # check in super time table
        cursor = cnx.cursor()
        query = "SELECT * FROM attendance.time_table WHERE department = {department} AND semester = {semester} AND week_day = {day} AND hour = {hour}".format(
            department=department, semester=semester, day=str(day), hour=hour)
        cursor.execute(query)

        # block if super time table is true
        # todo
        cursor.close()
        # return
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("\"db-fetch-error\"")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("\"db-fetch-error\"")
        else:
            print(err)


def find_hour(param):
    if time(8, 0, 0) <= param < time(8, 55, 0):
        return 1
    elif time(8, 55, 0) <= param < time(9, 50, 0):
        return 2
    elif time(10, 10, 0) <= param < time(11, 0, 0):
        return 3
    elif time(11, 0, 0) <= param < time(11, 50, 0):
        return 4
    elif time(11, 50, 0) <= param < time(12, 40, 0):
        return 5
    elif time(1, 30, 0) <= param < time(2, 20, 0):
        return 6
    elif time(2, 20, 0) <= param < time(3, 10, 0):
        return 7
    elif time(3, 10, 0) <= param < time(4, 10, 0):
        return 8


department = str(sys.argv[1])
semester = int(sys.argv[2])
date = int(sys.argv[3])
hour = int(sys.argv[4])
day = "mon"
mysql_connection()
