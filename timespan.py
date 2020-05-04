import ast
import sys
from datetime import datetime

import mysql.connector
import xlsxwriter
from mysql.connector import errorcode

workbook = xlsxwriter.Workbook('GeneratedReport.xlsm')
worksheet = workbook.add_worksheet('Exported')

merge_format_head = workbook.add_format({
    'align': 'left',
    'valign': 'vleft',
    'fg_color': 'purple',
    'font_color': 'white'})
merge_format_subhead = workbook.add_format({
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#87CEEB'})
format_subhead2 = workbook.add_format({
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#87CEEB'})
merge_format = workbook.add_format({
    'border': 1,
    'align': 'left',
    'valign': 'vleft',
    'fg_color': '#87CEEB'})


# subject_list = ['x', 'y', 'z', 'w', 't']
# department = ""
# START_DATE = ""
# END_DATE = ""


def mysql_connection():
    global department

    config = {
        'user': 'root',
        'password': 'vcvra-1002',
        'host': '127.0.0.1',
        'database': 'xstack',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**config)

        cursor = cnx.cursor()

        query = "SELECT * FROM xstack.time_table WHERE dept = %s AND sem = %s"
        cursor.execute(query, (department, 1))

        sub_pk = []
        for row in cursor:
            print(row[8])
            sub_pk.append(row[8])

        cursor.close()

        for row in sub_pk:
            looped_cursor = cnx.cursor()
            looped_query = "SELECT * FROM xstack." + str.lower(row)
            looped_cursor.execute(looped_query)
            print(looped_cursor.column_names)

            date_times = looped_cursor.column_names[2:]
            required_dates = []

            for date in date_times:
                comparand = datetime.strptime(date.split(" ")[0], "%Y-%m-%d").strftime("%Y-%m-%d")
                if START_DATE <= comparand <= END_DATE:
                    required_dates.append(date)
            print(required_dates)

            looped_cursor.fetchall()
            looped_cursor.close()

        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password!")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist!")
        else:
            print(err)


def prepare_subject_columns(alpha, subject):
    global worksheet, merge_format_subhead, format_subhead2

    worksheet.merge_range(alpha + '4:' + (chr(ord(alpha) + 3)) + '4', subject, merge_format_subhead)
    worksheet.write(alpha + '5', "Conducted Periods", format_subhead2);
    worksheet.write((chr(ord(alpha) + 1)) + '5', "Attended Periods", format_subhead2);
    worksheet.write((chr(ord(alpha) + 2)) + '5', "On Duty Periods", format_subhead2);
    worksheet.write((chr(ord(alpha) + 3)) + '5', "% Att", format_subhead2);


def prepare_workbook():
    global workbook, workbook, merge_format_head, merge_format, subject_list, START_DATE, END_DATE, department

    workbook.add_vba_project('./vbaProject.bin')

    worksheet.merge_range('A1:Z1', 'xStack: Exported Data - Loyola-ICAM College of Engineering and Technology',
                          merge_format_head)
    worksheet.merge_range('A2:Z2', 'Department of ' + department, merge_format_head)
    worksheet.merge_range('A3:Z3', 'Student attendance for the period:' + START_DATE + ' to ' + END_DATE,
                          merge_format_head)
    worksheet.merge_range('A4:A5', 'Registration #', merge_format)
    worksheet.merge_range('B4:B5', 'Name of the student', merge_format)

    alpha = 'C'
    for subject in subject_list:
        prepare_subject_columns(alpha, subject)
        alpha = chr(ord(alpha) + 4)
        print(alpha)

    workbook.close()

department = sys.argv[1]
subject_list = ast.literal_eval(sys.argv[2])
START_DATE = datetime.strptime(sys.argv[3], "%Y-%m-%d").strftime("%Y-%m-%d")
END_DATE = datetime.strptime(sys.argv[4], "%Y-%m-%d").strftime("%Y-%m-%d")

mysql_connection()

print(department, subject_list, START_DATE, END_DATE)
prepare_workbook()
