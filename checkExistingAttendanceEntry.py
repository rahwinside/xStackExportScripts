import sys
from datetime import datetime, time

import mysql.connector
from mysql.connector import errorcode


def mysql_connection():
    global timestamp, pk_table
    config = {
        'user': 'root',
        'password': '',
        'host': '127.0.0.1',
        'database': 'xstack',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**config)

        cursor = cnx.cursor()
        query = "SELECT * FROM xstack." + pk_table
        cursor.execute(query)

        date_times = cursor.column_names[2:]
        datetime_array = []
        for item in date_times:
            datetime_array.append(
                datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
            )

        # date to be checked from argv
        date = timestamp.date()

        # contains timestamps with the same date
        filtered_datetimes = []
        # filter dates from datetime_array
        for item in datetime_array:
            if item.date() == date:
                filtered_datetimes.append(item)

        # hour to be checked from timestamp
        time_from_timestamp = timestamp.time()
        hour_from_timestamp = find_hour(time_from_timestamp)

        hours_from_datetimearray = []
        for item in filtered_datetimes:
            hours_from_datetimearray.append(find_hour(item.time()))

        if hour_from_timestamp in hours_from_datetimearray:
            print("true")
        else:
            print("false")

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


timestamp = datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M:%S")
pk_table = sys.argv[2]
mysql_connection()
