import openpyxl
from openpyxl.drawing.image import Image
import os
import sys


def get_cell_coordinate(row, column):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letter = letters[column]
    number = str(row)
    return f'{letter}{number}'


def create_column(table, property_name_list):
    if not os.path.isfile(table):
        workbook = openpyxl.Workbook()
    else:
        workbook = openpyxl.load_workbook(table)
    sheet = workbook.active

    column = 0
    for value in property_name_list:
        sheet.cell(row=1, column=column + 1, value=value)
        sheet[1][column].value = value
        column += 1

    workbook.save(table)


def import_xl(table):
    workbook = openpyxl.load_workbook(table)
    sheet = workbook.active

    property_ = []

    for row in sheet.rows:
        for cell in row:
            if cell.value is not None:
                property_.append(cell.value)
    workbook.save(table)

    return property_


def property_export(row, table, site_prop_list):
    workbook = openpyxl.load_workbook(table)
    sheet = workbook.active

    table_prop_list = import_xl(table)
    for prop in site_prop_list:
        if prop[0] in table_prop_list:
            sheet.cell(row=row, column=table_prop_list.index(prop[0]) + 1).value = prop[1]

    img = Image(fr'C:\Users\User\PycharmProjects\Freelans_1\фото\{site_prop_list[0][1]}.jpg')
    cell = get_cell_coordinate(row=row, column=table_prop_list.index('Фото'))
    sheet.add_image(img, cell)
    sheet.row_dimensions[row].height = 135

    workbook.save(table)
    return


if __name__ == "__main__":
    property_name = import_xl('Каталог.xlsx')
    print(property_name)
