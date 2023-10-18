import os
import sqlite3
import openpyxl
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path = BASE_DIR / 'db.sqlite3'
media_path = BASE_DIR / 'media'


def get_doc_name():  # Функция для получения имени последнего документа
    try:
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            cursor.execute("""SELECT * FROM search_document ORDER BY id DESC LIMIT 1;""")
        doc = cursor.fetchone()
        return doc[1]
    except IOError as e:
        print(f'Ошибка в получении имени >>> {e}')

def save_data_db():
    try:
        file_name = media_path / get_doc_name()
        book = openpyxl.load_workbook(file_name, read_only=True)
        sheet = book.active
        data = [row for row in sheet.iter_rows(min_row=15, max_row=61900, min_col=12, max_col=19, values_only=True)]
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            cursor.executemany("""INSERT INTO search_remains(
            'comment','code','article','party','title','base_unit','project','quantity')
            VALUES (?,?,?,?,?,?,?,?)""", data)
    except IOError as e:
        print(f"Ошибка в загрузге данных в базу {e}")


def delete_data_table():
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        cursor.execute("""DELETE FROM search_remains;""")
