import random
import string
import sys
from datetime import datetime

import mysql.connector
import xlsxwriter
from mysql.connector import errorcode

from local_config import config

stud_name_dict = dict()


def random_string(string_length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


workbook = xlsxwriter.Workbook('GeneratedCourseReport_' + random_string(8) + '.xlsm')
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


def mysql_connection():
    global pk_table, start_date, end_date, department, year

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        user_cursor = cnx.cursor()
        query = "SELECT register_no, full_name FROM attendance.users WHERE department = %s AND semester = %s"
        user_cursor.execute(query, (department.lower(), semester))

        for row in user_cursor:
            stud_name_dict[row[0]] = row[1]
        user_cursor.close()

        query = "SHOW COLUMNS FROM attendance." + pk_table
        cursor.execute(query)

        col_schema = []
        for col in cursor:
            col_schema.append(col)

        col_schema = col_schema[1:]

        datetimes = []
        for col in col_schema:
            if start_date <= datetime.strptime(col[0], "%Y-%m-%d %H:%M:%S").date() <= end_date:
                datetimes.append(col[0])

        cursor = cnx.cursor()
        query = "SELECT register_no,"
        for stamp in datetimes:
            query += "`" + stamp + "`,"

        query = query[:-1] + " "
        query += "FROM attendance." + pk_table

        cursor.execute(query)

        # prepare report template here
        prepare_workbook()

        # resume general execution
        alpha = 'C'
        for stamp in datetimes:
            worksheet.write(alpha + '5', stamp, merge_format)
            alpha = increment_str(alpha)

        alpha = 'C'
        i = 6
        for row in cursor:
            for j in range(1, len(row)):
                worksheet.write(alpha + str(i), row[j])
                alpha = increment_str(alpha)
            alpha = 'C'
            i += 1

        workbook.close()

        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("\"db-fetch-error\"")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("\"db-fetch-error\"")
        else:
            print(err)


def prepare_workbook():
    global workbook, workbook, merge_format_head, merge_format, start_date, end_date, department, subject_code

    workbook.add_vba_project('./vbaProject.bin')

    worksheet.merge_range('A1:DD1', 'xStack: Exported Data - Loyola-ICAM College of Engineering and Technology',
                          merge_format_head)

    local_sem = int(semester)
    if local_sem == 1 or local_sem == 2:
        year = 'I'
    elif local_sem == 3 or local_sem == 4:
        year = 'II'
    elif local_sem == 5 or local_sem == 6:
        year = 'III'
    elif local_sem == 7 or local_sem == 8:
        year = 'IV'

    worksheet.merge_range('A2:DD2', "Subject Code: " + subject_code + " Year: " + year + " Semester: " + str(semester),
                          merge_format_head)

    if department == "DIT":
        dept = "Information Technology"
    elif department == "DCSE":
        dept = "Computer Science and Engineering"
    elif department == "DEEE":
        dept = "Electrical and Electronics Engineering"
    elif department == "DECE":
        dept = "Electronics and Communication Engineering"
    elif department == "DMEA":
        dept = "Mechanical Engineering - A"
    elif department == "DMEB":
        dept = "Mechanical Engineering - B"
    else:
        dept = "Unknown"

    worksheet.merge_range('A3:DD3', 'Department of ' + dept, merge_format_head)

    worksheet.merge_range('A4:DD4', 'Student attendance for the period: ' + datetime.strptime(sys.argv[2], "%Y-%m-%d")
                          .strftime("%d %B, %Y") + ' to ' +
                          datetime.strptime(sys.argv[3], "%Y-%m-%d").strftime("%d %B, %Y"), merge_format_head)
    worksheet.write('A5', 'Registration #', merge_format)

    worksheet.write('B5', 'Name of the student', merge_format)

    populate_student_names()


def populate_student_names():
    global worksheet, stud_name_dict

    address = 6
    for key, value in sorted(stud_name_dict.items()):
        worksheet.write('A' + str(address), key)
        worksheet.write('B' + str(address), value)
        address += 1


def increment_char(c):
    """
    Increment an uppercase character, returning 'A' if 'Z' is given
    """
    return chr(ord(c) + 1) if c != 'Z' else 'A'


def increment_str(s):
    lpart = s.rstrip('Z')
    if not lpart:  # s contains only 'Z'
        new_s = 'A' * (len(s) + 1)
    else:
        num_replacements = len(s) - len(lpart)
        new_s = lpart[:-1] + increment_char(lpart[-1])
        new_s += 'A' * num_replacements
    return new_s


pk_table = str(sys.argv[1])
start_date = datetime.strptime(str(sys.argv[2]), "%Y-%m-%d").date()
end_date = datetime.strptime(str(sys.argv[3]), "%Y-%m-%d").date()

subject_code = pk_table.split('_')[0].upper()
department = pk_table.split('_')[1].upper()
semester = pk_table.split('_')[2]

local_sem = int(semester)
if local_sem == 1 or local_sem == 2:
    year = 1
elif local_sem == 3 or local_sem == 4:
    year = 2
elif local_sem == 5 or local_sem == 6:
    year = 3
elif local_sem == 7 or local_sem == 8:
    year = 4

mysql_connection()
