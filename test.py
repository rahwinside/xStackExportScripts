#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8
import sys
from datetime import time, datetime

import mysql.connector
from mysql.connector import errorcode


def mysql_connection():
    global username, day, hour, date
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'attendance',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**config)
        response = "empty-fetch"

        cursor = cnx.cursor()
        query = "SELECT * FROM attendance.time_table_super WHERE staff_name = %s AND (week_day = %s AND hour = %s)"
        cursor.execute(query, (username, day, hour))

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
                if hour == str(find_hour(item.time())):
                    already_taken = True
                    required_timestamp = item
                    break

            if already_taken:
                response['required_timestamp'] = str(required_timestamp)
                print(str(response))
                return
            else:
                print("not-taken")
                return
        cursor.close()

        cursor = cnx.cursor()
        query = "SELECT * FROM attendance.time_table WHERE staff_name = %s AND (week_day = %s AND hour = %s)"
        cursor.execute(query, (username, day, hour))

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
                if hour == str(find_hour(item.time())):
                    already_taken = True
                    required_timestamp = item
                    break

            if already_taken:
                response['required_timestamp'] = str(required_timestamp)
                print(str(response))
                return
            else:
                print("not-taken")
                return
        cursor.close()

        print(response)

        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("db-conn-failed")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("db-critical-error")
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


username = sys.argv[1]
hour = sys.argv[2]
date = datetime.strptime("2020-05-15", "%Y-%m-%d").date()
day = 'Monday'
# day = datetime.today().strftime('%A')
# date = datetime.now().date()

if hour == "1":
    print(
        "{\"datetime\": \"15.2.2020 - Monday\", \"department\": \"DIT\", \"year\": \"I\", \"semester\": \"1\", \"subject_code\": \"CS8151\", \"subject_name\": \"Python Programming\", \"subCode_dept_sem\": \"cs8151_dit_1\", \"required_timestamp\": \"2020-05-15 09:10:12\"}")
if hour == "2":
    print(
        "{\"datetime\": \"15.2.2020 - Monday\", \"department\": \"DMEA\", \"year\": \"II\", \"semester\": \"2\", \"subject_code\": \"a\", \"subject_name\": \"C Programming\", \"subCode_dept_sem\": \"cs8151_dit_1\", \"required_timestamp\": \"2020-05-15 09:10:12\"}")
if hour == "3":
    print(
        "{\"datetime\": \"15.2.2020 - Monday\", \"department\": \"DECE\", \"year\": \"III\", \"semester\": \"4\", \"subject_code\": \"b\", \"subject_name\": \"C Programming\", \"subCode_dept_sem\": \"cs8151_dit_1\", \"required_timestamp\": \"2020-05-15 09:10:12\"}")
if hour == "4":
    print(
        "{\"datetime\": \"15.2.2020 - Monday\", \"department\": \"DMECH\", \"year\": \"IV\", \"semester\": \"1\", \"subject_code\": \"c\", \"subject_name\": \"JAVA Programming\", \"subCode_dept_sem\": \"cs8151_dit_1\", \"required_timestamp\": \"2020-05-15 09:10:12\"}")
if hour == "5":
    print(
        "{\"datetime\": \"15.2.2020 - Monday\", \"department\": \"DMECH\", \"year\": \"I\", \"semester\": \"1\", \"subject_code\": \"f\", \"subject_name\": \"Python Programming\", \"subCode_dept_sem\": \"cs8151_dit_1\", \"required_timestamp\": \"2020-05-15 09:10:12\"}")
if hour == "6":
    print(
        "{\"datetime\": \"15.2.2020 - Monday\", \"department\": \"DIT\", \"year\": \"I\", \"semester\": \"1\", \"subject_code\": \"e\", \"subject_name\": \"Python Programming\", \"subCode_dept_sem\": \"cs8151_dit_1\", \"required_timestamp\": \"2020-05-15 09:10:12\"}")
if hour == "7":
    print("\"no-class\"")
if hour == "8":
    print(
        "{\"datetime\": \"15.2.2020 - Monday\", \"department\": \"DCSE\", \"year\": \"I\", \"semester\": \"1\", \"subject_code\": \"CS8151\", \"subject_name\": \"Python Programming\", \"subCode_dept_sem\": \"cs8151_dit_1\", \"required_timestamp\": \"2020-05-15 09:10:12\"}")

# date = datetime.strptime("2020-05-15", "%Y-%m-%d").date()
# day = 'Monday'
# mysql_connection()
