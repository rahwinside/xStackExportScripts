#!C:/Users/danie/AppData/Local/Programs/Python/Python38-32/python.exe
import sys
from datetime import time, datetime

import mysql.connector
from mysql.connector import errorcode

from config import config


def mysql_connection():
    global department, semester, hour, date, day, response_list, pk_table_list

    try:
        # check in super time table
        cnx = mysql.connector.connect(**config)
        response = "\"no-class\""
        cursor = cnx.cursor()
        query = "SELECT * FROM attendance.time_table_super WHERE department = {department} AND semester = {semester} AND override_date = '{date}' AND hour = {hour}".format(
            department=department, semester=semester, date=str(date), hour=hour)
        cursor.execute(query)

        # run block if super time table is true

        count = 0
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

            response_list.append(response)

            count += 1

            pk_table = str(row[6]).lower()
            pk_table_list.append(pk_table)
            cursor.close()

        for i in range(0, count):
            cursor = cnx.cursor()
            query = "SHOW COLUMNS FROM attendance." + pk_table_list[i]
            cursor.execute(query)

            col_schema = []
            for col in cursor:
                col_schema.append(col)

            cursor.close()

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
                response_list[i]['required_timestamp'] = str(required_timestamp)
                response_list[i]['datetime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response_list[i]['displaydate'] = str(datetime.now().strftime("%d.%m.%Y - %A"))

            else:
                response_list[i]['required_timestamp'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response_list[i]['datetime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response_list[i]['displaydate'] = str(datetime.now().strftime("%d.%m.%Y - %A"))

        # check in regular time table
        cursor = cnx.cursor()
        query = "SELECT DISTINCT `subject_name`, `subject_code`, `department`, `semester`, `week_day`, `hour`, `subCode_dept_sem` FROM attendance.time_table WHERE department = {department} AND semester = {semester} AND week_day = '{day}' AND hour = {hour}".format(
            department=department, semester=semester, day=str(day), hour=hour)
        cursor.execute(query)
        # print(query)

        # run block if regular time table is true
        for row in cursor:
            year = "NA"
            if row[3] == 1 or row[3] == 2:
                year = "I"
            if row[3] == 3 or row[3] == 4:
                year = "II"
            if row[3] == 5 or row[3] == 6:
                year = "III"
            if row[3] == 7 or row[3] == 8:
                year = "IV"
            response = {"department": row[2], "year": year, "semester": str(row[3]), "subject_code": row[1],
                        "subject_name": row[0], "subCode_dept_sem": row[6].lower()}
            response_list.append(response)

            pk_table = str(row[6]).lower()
            pk_table_list.append(pk_table)
            cursor.close()

        for i in range(count, len(response_list)):
            cursor = cnx.cursor()
            query = "SHOW COLUMNS FROM attendance." + pk_table_list[i]
            cursor.execute(query)

            col_schema = []
            for col in cursor:
                col_schema.append(col)

            cursor.close()

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
                response_list[i]['required_timestamp'] = str(required_timestamp)
                response_list[i]['datetime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response_list[i]['displaydate'] = str(datetime.now().strftime("%d.%m.%Y - %A"))

            else:
                response_list[i]['required_timestamp'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response_list[i]['datetime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                response_list[i]['displaydate'] = str(datetime.now().strftime("%d.%m.%Y - %A"))

        if len(response_list) == 0:
            print(response)

        else:
            print(str(response_list))

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
day = str(datetime.strptime(sys.argv[3], "%Y-%m-%d").date().strftime("%a")).lower()
# day = "fri"
hour = int(sys.argv[4])

response_list = []
pk_table_list = []

mysql_connection()
