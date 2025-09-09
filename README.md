## Установка и запуск
1. Клонируем репозиторий:
git clone https://github.com/DimazKomarov/test_itk_academy.git
cd test_itk_academy

2. Создаем и запускаем контейнеры Docker:
docker-compose up --build

3. Применяем миграции базы данных (Alembic):
docker-compose exec app alembic upgrade head

Приложение доступно по адресу: http://localhost:8000
