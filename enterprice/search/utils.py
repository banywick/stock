import os.path
import sqlite3
from openpyxl import load_workbook, workbook
import openpyxl
from pathlib import Path

menu = [{'title': 'Главная', 'url_name': 'main'},
        {'title': 'Обновить базу', 'url_name': 'update'}
        ]

db_path = Path('../my_db.sqlite3')


def get_doc_name():  # Функция для получения имени последнего документа
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        print("Подключен к SQLite получаем имя докуметна")
        cursor.execute("""SELECT * FROM maxfind_document ORDER BY id DESC LIMIT 1;""")
        doc = cursor.fetchone()
        return doc[1]


def save_data_db():
    file_name = Path('../media', get_doc_name())
    print(file_name)
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        print('Соединение с базой данных')
        book = openpyxl.load_workbook(file_name, read_only=True)
        sheet = book.active
        for row in sheet.iter_rows(min_row=15, max_row=20, min_col=12, max_col=19, values_only=True):
            comment = row[0]
            code = row[1]
            article = row[2]
            party = row[3]
            title = row[4]
            base_unit = row[5]
            project = row[6]
            quantity = row[7]
            print(comment)
            cursor.execute(
                f"INSERT INTO maxfind_remains(comment,code,article,party,title,base_unit,project,quantity)"
                f" VALUES  ('{comment}', '{code}','{article}',"
                f"'{party}','{title}','{base_unit}','{project}','{quantity}')")
        print('База успешно записана')
        cursor.close()


def delete_data_table():
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        print("Подключен к SQLite готов к удалению")
        cursor.execute("""DELETE FROM maxfind_remains;""")
        print('Все данные удалены')