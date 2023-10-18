import os


import openpyxl
from pathlib import Path

from django.db import connection

BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

media_path = BASE_DIR / 'media'


def get_doc_name():  # Функция для получения имени последнего документа
    try:
        with connection.cursor() as con:

            con.execute("""SELECT * FROM search_document ORDER BY id DESC LIMIT 1;""")
            doc = con.fetchone()
            return doc[1]
    except IOError as e:
        print(f'Ошибка в получении имени >>> {e}')


def save_data_db():
    try:
        file_name = media_path / get_doc_name()
        book = openpyxl.load_workbook(file_name, read_only=True)
        sheet = book.active
        data = [row for row in sheet.iter_rows(min_row=15, max_row=1000, min_col=12, max_col=19, values_only=True)]
        with connection.cursor() as con:

            con.executemany("""INSERT INTO search_remains(
            comment, code, article, party, title, base_unit, project, quantity)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", data)
    except IOError as e:
        print(f"Ошибка в загрузге данных в базу {e}")


def delete_data_table():
    with connection.cursor() as con:
        con.execute("""DELETE FROM search_remains;""")
