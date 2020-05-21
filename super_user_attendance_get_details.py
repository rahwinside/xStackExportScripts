#!C:/Users/danie/AppData/Local/Programs/Python/Python38-32/python.exe
import sys
from datetime import time, datetime

import mysql.connector
from mysql.connector import errorcode


def mysql_connection():
    global department, semester, hour, date, day
    config = {
        'user': 'root',
        'password': '',
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

        # run block if super time table is true

        for row in cursor:
            year = "NA"
            if row[5] == 1 or row[5] == 2:
                year = "I"
            if row[5] == 3 or row[5] == 4:
                year = "II"
            if row[5] == 5 or row[5] == 6:
                year = "III"
            if row[5] == 7 or row[5] == 8:
                year = "IV"
            response = {"department": row[4], "year": year, "semester": str(row[5]), "subject_code": row[3],
                        "subject_name": row[2], "subCode_dept_sem": row[8].lower()}

            pk_table = str(row[8]).lower()
            cursor.close()
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
                response['required_timestamp'] = str(required_timestamp)
                response['datetime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response['displaydate'] = str(datetime.now().strftime("%d.%m.%Y - %A"))
                print(str(response).replace("'", '"'))
                return
            else:
                response['required_timestamp'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response['datetime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response['displaydate'] = str(datetime.now().strftime("%d.%m.%Y - %A"))
                print(str(response).replace("'", '"'))
                return
        cursor.close()

        # check in regular time table
        cursor = cnx.cursor()
        query = "SELECT * FROM attendance.time_table WHERE department = {department} AND semester = {semester} AND week_day = '{day}' AND hour = {hour}".format(
            department=department, semester=semester, day=str(day), hour=hour)
        cursor.execute(query)

        for row in cursor:
            year = "NA"
            if row[5] == 1 or row[5] == 2:
                year = "I"
            if row[5] == 3 or row[5] == 4:
                year = "II"
            if row[5] == 5 or row[5] == 6:
                year = "III"
            if row[5] == 7 or row[5] == 8:
                year = "IV"
            response = {"department": row[4], "year": year, "semester": str(row[5]), "subject_code": row[3],
                        "subject_name": row[2], "subCode_dept_sem": row[8].lower()}

            pk_table = str(row[8]).lower()
            cursor.close()
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
                response['required_timestamp'] = str(required_timestamp)
                response['datetime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response['displaydate'] = str(datetime.now().strftime("%d.%m.%Y - %A"))
                print(str(response).replace("'", '"'))
                return
            else:
                response['required_timestamp'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response['datetime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response['displaydate'] = str(datetime.now().strftime("%d.%m.%Y - %A"))
                print(str(response).replace("'", '"'))
                return

        cursor.close()

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

date = datetime.strptime(sys.argv[3], "%Y-%m-%d").date()
day = str(date.day)
hour = int(sys.argv[4])
mysql_connection()
