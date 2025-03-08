## Установка

### 1. Клонируйте репозиторий
```bash
git clone git@github.com:SanyaAlm/orders_test.git
cd orders_test
```

### 2. Установка зависимостей:
Создайте файл `.env` в папке `orders_test` с следующими данными.
Пример данных:
```
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=4342
POSTGRES_DB=orders

SECRET_KEY=80aec31db155016928db203f3af4b56cba5f2e4f27d0aa5b7607715dcf8be127

REDIS_HOST=redis
REDIS_PORT=6379
```
Для установки зависимостей используйте [Poetry](https://python-poetry.org/). Выполните следующую команду:

```bash
poetry install
```
### 3. Запуск Docker контейнеров:
Для поднятия Docker контейнеров выполните команду:
```bash
docker compose up -d --build
```
### 4. Запуск тестов
Для запуска тестов проваливаемся в докер контейнер с помощью команды:
```bash
docker exec -it fastapi_app /bin/bash
```
После этого можем запустить тесты командой:
```bash
pytest -v
```

### 5. Доступ к API
API эндпоинты будут доступны по адресу: (http://localhost:8000/docs)
