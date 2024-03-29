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

stud_att_dict = dict()
stud_name_dict = dict()
sub_code_name = []


def mysql_connection():
    global department, stud_att_dict, sub_code_name

    config = {
        'user': 'root',
        'password': 'vcvra-1002',
        'host': '127.0.0.1',
        'database': 'xstack',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**config)

        user_cursor = cnx.cursor()
        query = "SELECT reg_no, name FROM xstack.users WHERE dept = %s AND year = %s"
        user_cursor.execute(query, (department, 1))

        for row in user_cursor:
            stud_name_dict[row[0]] = row[1]
        user_cursor.close()

        cursor = cnx.cursor()

        query = "SELECT * FROM xstack.time_table WHERE dept = %s AND sem = %s"
        cursor.execute(query, (department, 1))

        sub_pk = []
        sub_code_name = []
        for row in cursor:
            if row[8] not in sub_pk:
                sub_pk.append(row[8])
            t = (row[2], row[3])
            if t not in sub_code_name:
                sub_code_name.append(t)

        cursor.close()

        for row in sub_pk:
            looped_cursor = cnx.cursor()
            looped_query = "SELECT * FROM xstack." + str.lower(row)
            looped_cursor.execute(looped_query)

            date_times = looped_cursor.column_names[2:]
            required_dates = []
            index_dates = []

            for date in date_times:
                comparand = datetime.strptime(date.split(" ")[0], "%Y-%m-%d").strftime("%Y-%m-%d")
                if START_DATE <= comparand <= END_DATE:
                    required_dates.append(date)
                    index_dates.append(date_times.index(date))

            mod_rows = []
            for row in looped_cursor:
                eval_row = []
                for index in index_dates:
                    eval_row.append(row[index + 2])
                pres = eval_row.count(1)
                abs = eval_row.count(0)
                od = eval_row.count(2)
                total_days = len(eval_row)
                att_percent = (pres + od) / total_days * 100

                insert_instance = (total_days, pres, od, abs, att_percent)

                if row[0] in stud_att_dict:
                    stud_att_dict[row[0]].append(insert_instance)
                else:
                    stud_att_dict[row[0]] = [insert_instance]
                mod_rows.append(row[0])

            na_list = []
            for reg in stud_name_dict:
                if reg not in mod_rows:
                    na_list.append(reg)

            null_tuple = ('NA', 'NA', 'NA', 'NA', 'NA')
            for reg in na_list:
                if reg in stud_att_dict:
                    stud_att_dict[reg].append(null_tuple)
                else:
                    stud_att_dict[reg] = [null_tuple]

            looped_cursor.close()

        # print(stud_name_dict)
        print(stud_att_dict)

        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password!")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist!")
        else:
            print(err)


def populate_student_names():
    global worksheet, stud_name_dict

    address = 6
    for key, value in sorted(stud_name_dict.items()):
        worksheet.write('A' + str(address), key)
        worksheet.write('B' + str(address), value)
        address += 1


def prepare_subject_columns(alpha, subject):
    global worksheet, merge_format_subhead, format_subhead2

    al = alpha
    for i in range(0, 4):
        al = increment_str(al)
    worksheet.merge_range(alpha + '4:' + al + '4', subject, merge_format_subhead)
    worksheet.write(alpha + '5', "Conducted Periods", format_subhead2)

    al = increment_str(alpha)
    worksheet.write(al + '5', "Attended Periods", format_subhead2)

    al = increment_str(al)
    worksheet.write(al + '5', "On Duty Periods", format_subhead2)

    al = increment_str(al)
    worksheet.write(al + '5', "Absent Periods", format_subhead2)

    al = increment_str(al)
    worksheet.write(al + '5', "% Att", format_subhead2)


def write_attendance():
    return


def prepare_workbook():
    global workbook, workbook, merge_format_head, merge_format, sub_code_name, START_DATE, END_DATE, department

    workbook.add_vba_project('./vbaProject.bin')

    worksheet.merge_range('A1:DD1', 'xStack: Exported Data - Loyola-ICAM College of Engineering and Technology',
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

    worksheet.merge_range('A2:DD2', 'Department of ' + dept, merge_format_head)

    worksheet.merge_range('A3:DD3', 'Student attendance for the period: ' + datetime.strptime(sys.argv[2], "%Y-%m-%d")
                          .strftime("%d %B, %Y") + ' to ' +
                          datetime.strptime(sys.argv[3], "%Y-%m-%d").strftime("%d %B, %Y"), merge_format_head)
    worksheet.merge_range('A4:A5', 'Registration #', merge_format)

    worksheet.merge_range('B4:B5', 'Name of the student', merge_format)

    populate_student_names()

    alpha = 'C'
    for tuplet in sub_code_name:
        prepare_subject_columns(alpha, tuplet[0] + " - " + tuplet[1])

        for i in range(0, 5):
            alpha = increment_str(alpha)
        # alpha = chr(ord(alpha) + 4)

    address = 6
    for key, value in sorted(stud_att_dict.items()):
        alpha = 'C'
        for val in value:
            # print(val)
            for i in val:
                # print(alpha + str(address))
                worksheet.write(alpha + str(address), i)
                alpha = increment_str(alpha)
        address += 1

    workbook.close()


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


department = sys.argv[1]
START_DATE = datetime.strptime(sys.argv[2], "%Y-%m-%d").strftime("%Y-%m-%d")
# print(datetime.strptime(sys.argv[2], "%Y-%m-%d").strftime("%d %B, %y"))
END_DATE = datetime.strptime(sys.argv[3], "%Y-%m-%d").strftime("%Y-%m-%d")

mysql_connection()

prepare_workbook()
