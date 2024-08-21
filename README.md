# Market API

## Описание

Market API — это REST API для управления продуктами на торговой площадке. API позволяет пользователям:

- Регистрироваться и авторизовываться
- Добавлять продукты
- Обновлять информацию о продуктах
- Удалять продукты
- Получать информацию о продуктах
- Получать информацию о категориях
- Фильтровать продукты по различным параметрам


## Установка
1. Клонируйте репозиторий:  
git clone https://github.com/Mike-swingman/market_app_fast_api.git  
cd <имя репозитория>

2. Установите зависимости с помощью Poetry:
`poetry install`

3. Настройте переменные окружения на основе _.env-example_.  


## Запуск приложения
**Локально
Вы можете запустить приложение локально с использованием Uvicorn:**

Запустите сервер 
_uvicorn app.main:app --reload_

**Использование Docker
Сборка и запуск приложения через Docker Compose:**

_docker-compose up --build_

Это создаст и запустит контейнеры для вашего приложения и базы данных, а также запустит миграцию.


## Использование API  
После запуска приложения API будет доступен по адресу http://localhost:8000  
Вы можете взаимодействовать с ним через любой HTTP-клиент, такой как Postman, или через Swagger UI по адресу http://localhost:8000/docs