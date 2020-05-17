import sys
from datetime import time, datetime

import mysql.connector
from mysql.connector import errorcode


def mysql_connection():
    global username, auth_token, day, hour, date
    config = {
        'user': 'root',
        'password': 'vcvra-1002',
        'host': '127.0.0.1',
        'database': 'xstack',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**config)
        response = "empty-fetch"

        cursor = cnx.cursor()
        query = "SELECT * FROM xstack.super_time_table WHERE staff_email = %s AND (weekday = %s AND hour = %s)"
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
            response = {"department": row[4], "year": year, "semester": str(row[5]), "sub_code": row[2],
                        "sub_name": row[3], "subCode_dept_sem": row[8].lower()}

            pk_table = str(row[8]).lower()
            cursor.close()
            cursor = cnx.cursor()
            query = "SHOW COLUMNS FROM xstack." + pk_table
            cursor.execute(query)

            col_schema = []
            for col in cursor:
                col_schema.append(col)

            col_schema = col_schema[2:]

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
        query = "SELECT * FROM xstack.time_table WHERE staff_email = %s AND (weekday = %s AND hour = %s)"
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
            response = {"department": row[4], "year": year, "semester": str(row[5]), "sub_code": row[2],
                        "sub_name": row[3], "subCode_dept_sem": row[8].lower()}

            pk_table = str(row[8]).lower()
            cursor.close()
            cursor = cnx.cursor()
            query = "SHOW COLUMNS FROM xstack." + pk_table
            cursor.execute(query)

            col_schema = []
            for col in cursor:
                col_schema.append(col)

            col_schema = col_schema[2:]

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
            print("Something is wrong with your user name or password!")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist!")
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
# day = datetime.today().strftime('%A')
# date = datetime.now().date()
date = datetime.strptime("2020-05-15", "%Y-%m-%d").date()
day = 'Monday'
mysql_connection()
