import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
# import numpy as np


BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
media_path = BASE_DIR / 'media'


def get_doc_name():  # Функция для получения имени последнего документа
    engine = create_engine('postgresql://postgres:19377@127.0.0.1:5432/postgres')
    query = "SELECT * FROM search_document ORDER BY id DESC LIMIT 1"
    df = pd.read_sql_query(query, con=engine)
    return df.values[0][1]


def save_data_db():  # Чтение данных из Excel
    df = pd.read_excel(f'{media_path}/{get_doc_name()}', usecols=[11, 12, 13, 14, 15, 16, 17, 18])
    df = df.iloc[10:]  # Начинаем с 10 строки
    df = df.where(pd.notnull(df), None)  # Замена NULL значений на None
    engine = create_engine('postgresql://postgres:19377@127.0.0.1:5432/postgres')  # Создание подключения к базе данных
    df.columns = ['comment', 'code', 'article', 'party', 'title', 'base_unit', 'project', 'quantity']  # Замена  на желаемые названия столбцов
    # df['quantity'] = np.where(df['quantity'] % 1 == 0, df['column_name'].astype(int), round(df['column_name'], 2))
    df['quantity'] = df['quantity'].astype(float).round(2)
    df.to_sql('search_remains', engine, if_exists='replace',  index_label='id')  # Запись данных в базу данных




