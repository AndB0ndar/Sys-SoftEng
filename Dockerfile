# Используем базовый образ Python
FROM python:3.9
LABEL authors="micro-soft kittens"

# Установка переменной окружения для Python в режиме неинтерактивного вывода
ENV PYTHONUNBUFFERED 1

# Создание и переключение на рабочий каталог /app
WORKDIR /app

# Копирование зависимостей файла requirements.txt в рабочий каталог
COPY requirements.txt /app/

# Установка зависимостей проекта
RUN pip install -r requirements.txt

# Копирование текущего каталога в рабочий каталог контейнера
COPY . /app/

# Открытие порта 8000
EXPOSE 8000

# Запуск команды для запуска Django сервера
CMD ["python", "web_queue/manage.py", "runserver", "0.0.0.0:8000"]
