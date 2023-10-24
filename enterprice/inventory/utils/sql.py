import pandas as pd
from sqlalchemy import create_engine

new_doc = r'G:\Адресное хранение склад\Свалка\тест\03.10.23.xlsx'
old_stability = r'G:\Адресное хранение склад\Свалка\25.05.22.Большой.xlsx'


def load_db_inventory_doc():  # Чтение данных из Excel
    df = pd.read_excel(new_doc, usecols=[13, 15, 16, 18])
    df = df.iloc[10:]  # Начинаем с 10 строки
    df = df.where(pd.notnull(df), None)  # Замена NULL значений на None
    engine = create_engine('postgresql://postgres:19377@127.0.0.1:5432/postgres')  # Создание подключения к базе данных
    df.columns = ['article', 'title', 'base_unit', 'quantity']  # Замена  на желаемые названия столбцов
    # df['quantity'] = df['quantity'].astype(float).round(2)
    df.to_sql('inventory_inventorystatic', engine, if_exists='replace', index_label='id')  # Запись данных в базу данных
load_db_inventory_doc()