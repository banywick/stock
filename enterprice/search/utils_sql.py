import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from openpyxl import load_workbook
import psycopg2


# import numpy as np

def connect_to_db():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='19377',
        host='127.0.0.1',
        port='5432')
    return conn


BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
media_path = BASE_DIR / 'media'


def get_doc_name():  # Функция для получения имени последнего документа
    engine = create_engine('postgresql://postgres:19377@127.0.0.1:5432/postgres')
    query = "SELECT * FROM search_document ORDER BY id DESC LIMIT 1"
    df = pd.read_sql_query(query, con=engine)
    try:
        return df.values[0][1]
    except:
        return '         Не загружена!'


def save_data_db():  # Чтение данных из Excel
    df = pd.read_excel(f'{media_path}/{get_doc_name()}', usecols=[11, 12, 13, 14, 15, 16, 17, 18])
    df = df.iloc[10:]  # Начинаем с 10 строки
    df = df.where(pd.notnull(df), None)  # Замена NULL значений на None
    engine = create_engine('postgresql://postgres:19377@127.0.0.1:5432/postgres')  # Создание подключения к базе данных
    df.columns = ['comment', 'code', 'article', 'party', 'title', 'base_unit', 'project',
                  'quantity']  # Замена  на желаемые названия столбцов
    df['quantity'] = df['quantity'].astype(float).round(2)
    df.to_sql('search_remains', engine, if_exists='replace', index_label='id')  # Запись данных в базу данных


# r'G:\Адресное хранение склад\Свалка\тест\03.10.23.xlsx'


def load_inventory_doc():
    df = pd.read_excel(f'{media_path}/{get_doc_name()}', usecols=[13, 15, 16, 18])
    df = df.iloc[10:]  # Начинаем с 10 строки
    df = df.where(pd.notnull(df), None)  # Замена NULL значений на None
    engine = create_engine('postgresql://postgres:19377@127.0.0.1:5432/postgres')  # Создание подключения к базе данных
    with engine.connect() as con:
        con.execute(text("DELETE from search_remainsinventory"))  # отчищаем паблицу перед APPEND
        con.commit()
    df.columns = ['article', 'title', 'base_unit', 'quantity']  # Замена  на желаемые названия столбцов
    df['quantity'] = df['quantity'].astype(float).round(2)
    df['status'] = ''
    df.to_sql('search_remainsinventory', engine, if_exists='append', index_label='id')  # Запись данных в базу данных


# load_inventory_doc()
