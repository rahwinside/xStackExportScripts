#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8
import sys

import mysql.connector
from mysql.connector import errorcode


def mysql_connection():
    global pk_table, required_timestamp
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'attendance',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**config)
        response = "\"null\""

        cursor = cnx.cursor()
        query = "SELECT register_no, `{required_timestamp}` FROM attendance.{pk_table}".format(
            required_timestamp=required_timestamp, pk_table=pk_table)
        cursor.execute(query)
        json = {}
        for row in cursor:
            json[str(row[0])] = str(row[1])
            response = str(json)
        cursor.close()

        print(response.replace("'", '"'))

        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("\"db-fetch-error\"")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("\"db-fetch-error\"")
        else:
            print(err)


pk_table = str(sys.argv[1]).lower()
required_timestamp = sys.argv[2]
mysql_connection()
