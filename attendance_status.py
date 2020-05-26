#!C:/Users/danie/AppData/Local/Programs/Python/Python38-32/python.exe
import sys
from datetime import time, datetime

import mysql.connector
from mysql.connector import errorcode


def mysql_connection():
    global pk_table, hour, date
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'attendance',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SHOW COLUMNS FROM attendance." + pk_table
        cursor.execute(query)

        col_schema = []
        for col in cursor:
            col_schema.append(col)

        col_schema = col_schema[1:]

        datetimes = []
        for col in col_schema:
            if datetime.strptime(col[0], "%Y-%m-%d %H:%M:%S").date() == date:
                datetimes.append(
                    datetime.strptime(col[0], "%Y-%m-%d %H:%M:%S")
                )

        already_taken = False
        for item in datetimes:
            if str(hour) == str(find_hour(item.time())):
                already_taken = True
                required_timestamp = item
                break

        if already_taken:
            print("\"taken\"")
            return
        else:
            print("\"not-taken\"")
            return

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


pk_table = str(sys.argv[1])
hour = int(sys.argv[2])
# day = datetime.today().strftime('%A')
date = datetime.strptime("2020-05-15", "%Y-%m-%d").date()
mysql_connection()
