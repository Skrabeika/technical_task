# ТЗ для стажировки

Для прохождения отбора на стажировку, требуется выполнить 2 задания и сдать на проверку для оценки и возможности попасть в гурппу! 
Перед выполенение нужно проверить установлены ли тулы для выполнение или нужно установить зависимости, а именно docker compose и python

## Задания

Задание 1: Docker image
Создайте Dockerfile, который:
• Используется python3.9 как базовый образ.
• Копирует локальный файл app.py в контейнер.
• Устанавливает зависимости из requirements.txt.
• Запускает Flask-приложение при старте контейнера.
Необходимо создать app.py - простое Flask api с 1 эндпоинтом /ping, который возвращает {"status":
"ok"}.
Контейнер должен запуститься на порту 5000. Проверка работы контейнера производится путем
отправки curl запроса http://localhost:5000/ping

###############################################################################

Задание 2: Docker compose
Создайте docker-compose.yaml, который поднимет 2 контейнера:
• Собирает Flask приложение из первой части.
• Redis из образа redis:alpine как кеш.
Необходимо обновить app.py, чтобы он использовал Redis.
При запросе к /count увеличивал счетчик посещений и возвращал его.
Запустите docker-compose и убедитесь, что сервисы работают корректно.

## Технологии

- [Docker](https://docs.docker.com/)
- [Dockerhub](https://docs.docker.com/)
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Redis](https://redis.io/)
- ...

## Выполнение задания №1

Для начала переходим в удобную директорию и создаем еще одну для проекта и 2 папки для заданий, так как в последствии, 
нужно менять python скрипт и адаптировать его под использование redis контейнера

```sh
mkdir -p games/{task_1,task_2}
cd games/task_1
```

Создадим и открываем файл программы app.py, Flask api с 1 эндпоинтом /ping, который возвращает {"status":"ok"}.

```sh
nano app.py
```
В открывшемся файле пишем следующий код и сохраняем:

```python
# Импорт модуля flask по заданию
from flask import Flask, jsonify
# Создание экземпляра приложение
app = Flask(name)
# Определение маршрута ping 
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})
# Запуск сервера
if name == 'main':
    app.run(host='0.0.0.0', port=5000)
```

Создадим и открываем файл программы для зависимостей  requirements.txt:

```sh
nano requirements.txt
```

Прописываем зависимости исходя из версии использования Werkzeug с Flask, они могут отличаться и не подходить друг к другу, нужно подбирать:

```sh
# Указываем минимальные зависимости
flask==2.0.3
werkzeug==2.0.3
```
Создаем Dockerfile и описываем для сборки и запуска контейнера:

```dockerfile
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
```

Собираем образ на основании вашего выбора, иногда выбранный образ для билда не будет иметь нужных зависимостей,
рекомендую отталкиватся на количество использований, это гововрит о качестве образа и его использования, выбор пал на rrequero/flask-app с 1M скачиваний

```sh
build -t rrequero/flask-app -f Dockerfile .
```

Далее запускаем контейнер из собранного образа rrequero/flask-app:

```sh
docker run -d -p 5000:5000 --name flask-service rrequero/flask-app
```

Затем проверяем работу запущенного контейнера исходя из задания, отправляем в консоли:

```sh
curl http://localhost:5000/ping
```

И видим, что консоль возвращает:

```sh
{"status":"ok"}
```

## Выполнение задания №2

На основании задания 1 копируем файлы в папку 2
Затем начинаем обновлять файл app.py, и адаптировать под redis, в гугле можно посмотреть, что redis работает на 6379 порту, его и прописываем: 

```python

from flask import Flask, jsonify
# Добавляем клиент редиса и работы с переменными из задания 
import redis
import os

app = Flask(__name__)

# Добавляем блок для настройки редиса на его стандартном порту и подключение к нему
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port, db=0)

# Добавлем блок 
@app.route('/count')
def count():
    try:
        visits = r.incr('counter')
        return jsonify({
            "counter": visits,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Обновляем файл зависимостей nano requirements.txt, путем добавления следующей строки зависимостий для redis,
тут смотрим на версию использования python и поддержкой redis:

```sh
# Указываем минимальные зависимости
flask==2.0.3
werkzeug==2.0.3
# Добавляем запсимость для redis
redis==4.5.5
```

Далее создаем docker-compose.yml файл для наших контейнеров, flask-service который будет билдится и redis, с образа redis:alpine

```sh
nano docker-compose.yml
```

Затем описываем docker-copose.yml файл на основании наших требований

```docker-compose
services:
  flask-service:
    build: .
    container_name: flask-service
    ports:
      - "5000:5000"
    environment:
      - REDIS_HOST=redis
    networks:
      - games-network
    depends_on:
      - redis

  redis:
    image: redis:alpine
    container_name: redis
    volumes:
      - redis_data:/data
    networks:
      - games-network

volumes:
  redis_data:

networks:
  games-network:
    name: games-network
    driver: bridge
```

Запускаем docker-compose.yml для билда и поднятия 2-х контейнеров

```sh
docker compose -f docker-compose.yml up -d
```

Для проверки работы контейнеров нужно посылать запросы, отправим через /ping и /count как описано в задании следующим образом:

```sh
curl http://localhost:5000/ping
```

Видим вывод:

```sh
{"status":"ok"}
```

Затем несколько раз командную строку отправляем следующий запрос:

```sh
curl http://localhost:5000/count
```

После каждого запроса в выводе повышается counter:

```sh
{"counter":9,"status":"success"}
```

После заверешение работы, можно остановить и удалить контейнеры с сохранением томов как добавили в redis, следующей командой:

```sh
docker compose -f docker-compose.yml down -v
```
