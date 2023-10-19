import os
import openpyxl
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from django.db import connection

BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


#
# media_path = BASE_DIR / 'media'


def base_append():
    # Чтение данных из Excel
    df = pd.read_excel(r'G:\Адресное хранение склад\Свалка\25.05.22.Большой.xlsx',
                       usecols=[11, 12, 13, 14, 15, 16, 17, 18])
    df = df.iloc[10:]  # Начинаем с 15 строки

    # Замена NULL значений на None
    df = df.where(pd.notnull(df), None)

    # Создание подключения к базе данных
    engine = create_engine('postgresql://postgres:19377@127.0.0.1:5432/postgres')

    # Запись данных в базу данных
    df.to_sql('search_remains', engine, if_exists='replace')


# base_append()


# def null_del():
#
#
# null_del()

def get_doc_name():  # Функция для получения имени последнего документа

    engine = create_engine('postgresql://postgres:19377@127.0.0.1:5432/postgres')
    query = "SELECT * FROM search_document ORDER BY id DESC LIMIT 1"
    df = pd.read_sql_query(query, con=engine)
    print(df.values[0][1][9:])


get_doc_name()
#
# def save_data_db():
#     try:
#         file_name = media_path / get_doc_name()
#         book = openpyxl.load_workbook(file_name, read_only=True)
#         sheet = book.active
#         data = [row for row in sheet.iter_rows(min_row=15, max_row=65000, min_col=12, max_col=19, values_only=True)]
#         with connection.cursor() as con:
#
#             con.executemany("""INSERT INTO search_remains(
#             comment, code, article, party, title, base_unit, project, quantity)
#             VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", data)
#     except IOError as e:
#         print(f"Ошибка в загрузге данных в базу {e}")


# def delete_data_table():
#     with connection.cursor() as con:
#         con.execute("""DELETE FROM search_remains;""")
