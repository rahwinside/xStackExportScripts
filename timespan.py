import ast
import sys

import xlsxwriter

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
START_DATE = sys.argv[3]
END_DATE = sys.argv[4]

print(department, subject_list, START_DATE, END_DATE)
prepare_workbook()
