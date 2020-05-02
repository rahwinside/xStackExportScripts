import xlsxwriter

workbook = xlsxwriter.Workbook('GeneratedReport.xlsx')
worksheet = workbook.add_worksheet('Exported')

merge_format_head = workbook.add_format({
    'align': 'left',
    'valign': 'vleft',
    'fg_color': 'yellow'})
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

subject_list = ['x', 'y', 'z']


def prepare_subject_columns(alpha, subject):
    global worksheet, merge_format_subhead, format_subhead2
    worksheet.merge_range(alpha + '4:' + (chr(ord(alpha) + 3)) + '4', subject, merge_format_subhead)
    worksheet.write(alpha + '5', "Conducted Periods", format_subhead2);
    worksheet.write((chr(ord(alpha) + 1)) + '5', "Attended Periods", format_subhead2);
    worksheet.write((chr(ord(alpha) + 2)) + '5', "On Duty Periods", format_subhead2);
    worksheet.write((chr(ord(alpha) + 3)) + '5', "% Att", format_subhead2);


def prepare_workbook():
    global workbook, workbook, merge_format_head, merge_format, subject_list

    worksheet.merge_range('A1:Z1', 'xStack: Exported Data - Loyola-ICAM College of Engineering and Technology',
                          merge_format_head)
    worksheet.merge_range('A2:Z2', 'Department of Information Technology', merge_format_head)
    worksheet.merge_range('A3:Z3', 'Student attendance for the period: Apr 1, 2020 to May 1, 2020', merge_format_head)
    worksheet.merge_range('A4:A5', 'Registration #', merge_format)
    worksheet.merge_range('B4:B5', 'Name of the student', merge_format)

    alpha = 'C'
    for subject in subject_list:
        prepare_subject_columns(alpha, subject)
        alpha = chr(ord(alpha) + 4)
        print(alpha)

    workbook.close()


prepare_workbook()
