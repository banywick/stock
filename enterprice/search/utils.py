import os
import sqlite3
import openpyxl
from pathlib import Path

db_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3')
media_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')




def get_doc_name():  # Функция для получения имени последнего документа
    try:
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            print("Подключен к SQLite получаем имя докуметна")
            cursor.execute("""SELECT * FROM search_document ORDER BY id DESC LIMIT 1;""")
        doc = cursor.fetchone()
        return doc[1]
    except IOError as e:
        print(f'ошибка в получении имени >>> {e}')
# print(get_doc_name())


def save_data_db():
    try:
        sp = []
        file_name = Path(media_path, get_doc_name())
        print(f'его путь ____{file_name}')
        print(f'обработал документ >>>>>>>>> {file_name}')
        book = openpyxl.load_workbook(file_name, read_only=True)
        sheet = book.active
        print(f'Добрался до книги <<<< {book}')
        for row in sheet.iter_rows(min_row=15, max_row=61900, min_col=12, max_col=19, values_only=True):
            sp.append(row)
        print('Получил список картежей всей книги')
        with sqlite3.connect(db_path) as con:
            print('Открыл соединение с базой данных')
            cursor = con.cursor()
            print('Соединение с базой данных успешн')
            cursor.executemany("""INSERT INTO search_remains(
            'comment','code','article','party','title','base_unit','project','quantity')
            VALUES (?,?,?,?,?,?,?,?)""", sp)
            print('База успешно записана соединение закрыто')
    except IOError as e:
        print(f"Ошибка в загрузге данных в базу {e}")


# save_data_db()


def delete_data_table():
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        print("Подключен к SQLite готов к удалению")
        cursor.execute("""DELETE FROM search_remains;""")
        print('Все данные удалены')


# delete_data_table()


