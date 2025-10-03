Микросервис для загрузки, просмотра и удаления изображений на Django с Docker и PostgreSQL.

Для Windows :

Просто запусти батник, но должен быть установлен Docker Desktop и запущен и гит для виндовс


Через setup.sh :

# 1. Скачай проект
git clone https://github.com/gajethatredddd/django_image_service_itm.git

cd django_image_service

# 2. Запусти автоматическую установку
./setup.sh

Руками: 

# 1. Скачай проект
git clone https://github.com/gajethatredddd/django_image_service_itm.git

cd django_image_service

# 2. Настрой окружение
cp .env.example .env

# 3. Запусти проект
docker compose up -d --build

# 4. Настрой базу данных
docker compose exec web python django_app/manage.py migrate

# 5. Создай администратора (опционально)
docker compose exec web python django_app/manage.py createsuperuser

# 6. Открой в браузере
     Приложение: http://localhost:8000

     Админка: http://localhost:8000/admin

     Через Nginx: http://localhost

# 🛠 Команды для управления
1. Остановить проект
docker compose down
2. Просмотреть логи
docker compose logs web
docker compose logs db
3. Перезапустить
docker compose restart
4. Посмотреть статус контейнеров
docker compose ps
5. Выполнить команду в контейнере
docker compose exec web bash
6. Запуск тестов
docker compose exec web python django_app/manage.py test
7. Создание миграций
docker compose exec web python django_app/manage.py makemigrations
