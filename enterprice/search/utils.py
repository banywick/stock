import os.path
import sqlite3
from openpyxl import load_workbook, workbook
import openpyxl
from pathlib import Path

menu = [{'title': 'Главная', 'url_name': 'main'},
        {'title': 'Обновить базу', 'url_name': 'update'}
        ]

db_path = Path('../db.sqlite3')


def get_doc_name():  # Функция для получения имени последнего документа
    try:
        with sqlite3.connect('/home/banywick/projects/stock/enterprice/db.sqlite3') as con:
            cursor = con.cursor()
            print("Подключен к SQLite получаем имя докуметна")
            cursor.execute("""SELECT * FROM search_document ORDER BY id DESC LIMIT 1;""")
        doc = cursor.fetchone()
        return doc[1]
    except:
        print(f'ошибка в получении имени >>> ')
#print(get_doc_name())


def save_data_db():
    try:
        file_name = Path('/home/banywick/projects/stock/enterprice/media/', get_doc_name())
        print(f'обработал документ >>>>>>>>> {file_name}')
        book = openpyxl.load_workbook(file_name, read_only=True)
        sheet = book.active
        print(f'Добрался до книги <<<< {book}')
        with sqlite3.connect('/home/banywick/projects/stock/enterprice/db.sqlite3') as con:
            print('Открыл соединение с базой данных')
            cursor = con.cursor()
            print('Соединение с базой данных успешн')
            for row in sheet.iter_rows(min_row=15, max_row=200, min_col=12, max_col=19, values_only=True):
                comment = row[0]
                code = row[1]
                article = row[2]
                party = row[3]
                title = row[4]
                base_unit = row[5]
                project = row[6]
                quantity = row[7]
                cursor.execute(
                    f"INSERT INTO search_remains(comment,code,article,party,title,base_unit,project,quantity)"
                    f" VALUES  ('{comment}','{code}','{article}',"
                    f"'{party}','{title}','{base_unit}','{project}','{quantity}')")
        print('База успешно записана соединение закрыто')
    except IOError as e:
        print(f"Ошибка в загрузге данных в базу {e}")


#save_data_db()

def delete_data_table():
    with sqlite3.connect('/home/banywick/projects/stock/enterprice/db.sqlite3') as con:
        cursor = con.cursor()
        print("Подключен к SQLite готов к удалению")
        cursor.execute("""DELETE FROM search_remains;""")
        print('Все данные удалены')
# delete_data_table()
