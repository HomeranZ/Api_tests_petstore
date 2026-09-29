# API Tests — jsonplaceholder

[![Tests](https://github.com/HomeranZ/Api_tests_petstore/actions/workflows/tests.yml/badge.svg)](https://github.com/HomeranZ/Api_tests_petstore/actions/workflows/tests.yml)

Автотесты для публичного API [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com/).

## Стек
- Python 3.14
- pytest 8.3.3
- requests 2.32.3

## Что тестируется
- **GET /posts/{id}** — получение поста по ID
- **GET /posts** — список всех постов
- **POST /posts** — создание поста
- **Негативные сценарии** — невалидные ID, 404


## Структура
```
api-tests-petstore/
├── tests/
│ ├── init.py
│ ├── conftest.py # fixtures: api_client, base_url, created_post
│ └── test_posts.py # 16 тестов
├── pytest.ini # конфигурация pytest
├── requirements.txt # зависимости
└── README.md
```


## Особенности
- **Fixtures** в `conftest.py` — общий `api_client`, `base_url`, подготовка данных
- **Параметризация** — один тест, много кейсов
- **Маркеры:** `smoke`, `api`, `negative`
- **CI** через GitHub Actions — запуск на каждый push

## Как запустить

### 1. Клонировать
````bash
git clone https://github.com/HomeranZ/Api_tests_petstore.git
cd Api_tests_petstore
````

### 2. Установить зависимости
````bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

### 3. Запустить тесты
````bash
# всё
python -m pytest

# только smoke
python -m pytest -m smoke

# только негативные
python -m pytest -m negative
````

## Результат
````
16 passed in 2.36s
````
