#!/bin/bash
echo "Мой Django проект для itm"
echo "============================="

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен"
    exit 1
fi

echo "✅ Docker установлен"

# Создание .env файла
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Создан .env файл"
else
    echo "✅ .env файл уже существует"
fi

# Запуск проекта
echo "Запуск проекта..."
docker compose up -d --build

echo "Ожидание запуска..."
sleep 10

# Миграции
echo "Применение миграций..."
docker compose exec web python django_app/manage.py migrate

echo "Готово!"
echo ""
echo "Доступные адреса:"
echo "  - Приложение: http://localhost:8000"
echo "  - Админка:    http://localhost:8000/admin"
echo "  - Через Nginx: http://localhost"
echo ""
echo "Команды управления:"
echo "  - Остановка: docker compose down"
echo "  - Логи:      docker compose logs web"
echo "  - Перезапуск: docker compose restart"
