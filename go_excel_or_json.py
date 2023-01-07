import json

import openpyxl


def write_date(date):
    with open('res.json', 'w') as f:
        json.dump(date, f, indent=4, ensure_ascii=False)


def write_to_table(row_num, date):
    wb = openpyxl.load_workbook(filename='openpyxl.xlsx')
    sheet = wb['Лист1']
    print(row_num)
    sheet[f'A{row_num}'] = date[0]
    sheet[f'B{row_num}'] = date[1]
    sheet[f'C{row_num}'] = date[2]
    sheet[f'D{row_num}'] = date[3]
    sheet[f'E{row_num}'] = date[4]
    sheet[f'F{row_num}'] = date[5]
    wb.save('openpyxl.xlsx')
