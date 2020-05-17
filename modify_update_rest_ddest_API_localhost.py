#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8
import json
import sys

import mysql.connector
from mysql.connector import errorcode


def mysql_connection():
    global pk_table, required_timestamp, req_json
    config = {
        'user': 'root',
        'password': 'vcvra-1002',
        'host': 'localhost',
        'database': 'attendance',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**config)

        try:
            for key, value in req_json.items():
                cursor = cnx.cursor()

                query = "UPDATE attendance.{pk_table} SET `{required_timestamp}` = {value} WHERE register_no = {key}".format(
                    pk_table=pk_table, required_timestamp=required_timestamp, value=value, key=key)

                cursor.execute(query)
                cursor.close()

            cnx.commit()
            print('\"update-success\"')
            return

        except:
            cnx.rollback()
            print("\"modify-failed\"")

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
req_json = json.loads(sys.argv[3])

# print(req_json)
mysql_connection()
