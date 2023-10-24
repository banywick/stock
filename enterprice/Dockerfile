FROM python:3.8

# Установите рабочую директорию в контейнере
WORKDIR /usr/src/app

# Установите зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте текущий каталог в рабочую директорию контейнера
COPY . .
# Запустите приложение
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]