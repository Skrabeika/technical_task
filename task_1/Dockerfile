# Берем образ на основе debian, более подходит для python зависимостей
FROM python:3.9-slim

LABEL maintainer="ps.devnetops@gmail.com"

# Устанавливаем рабочую директорию 
WORKDIR /app
# Копируем зависимость по заданию
COPY requirements.txt .
# Устанавливаем зависимости 
RUN pip install --no-cache-dir -r requirements.txt
# Копируем файл выполнения программы app.py  
COPY app.py .

# Открываем требуемый порт
EXPOSE 5000
# Запускаем приложение из файла
CMD ["python", "app.py"]
