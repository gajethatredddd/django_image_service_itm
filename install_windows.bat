@echo off
chcp 65001 >nul
echo Установка для Windows
echo ==============================================
echo.

REM Проверка Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker не установлен
    echo    Скачай с: https://docs.docker.com/desktop/install/windows-install/
    echo.
    pause
    exit /b 1
)

REM Проверка Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git не установлен
    echo    Скачай с: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

REM Проверка что Docker запущен
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker не запущен
    echo    Запусти Docker Desktop и дождись "Docker is running"
    echo.
    pause
    exit /b 1
)

echo ✅ Система проверена
echo  Клонируем проект...
echo.

REM Клонирование
git clone https://github.com/gajethatredddd/django_image_service.git
if %errorlevel% neq 0 (
    echo ❌ Ошибка клонирования
    echo.
    pause
    exit /b 1
)

cd django_image_service

echo  Настраиваем окружение...
copy .env.example .env >nul

echo  Запускаем контейнеры...
docker compose up -d --build

echo  Ожидаем запуск (30 секунд)...
timeout /t 30 /nobreak >nul

echo  Применяем миграции...
docker compose exec web python django_app/manage.py migrate

echo.
echo  УСТАНОВКА ЗАВЕРШЕНА!
echo.
echo 📍 Доступные адреса:
echo    - Приложение: http://localhost:8000
echo    - Админка:    http://localhost:8000/admin  
echo    - Через Nginx: http://localhost
echo.
echo 🛠  Команды управления:
echo    - Остановка: docker compose down
echo    - Логи:      docker compose logs web
echo    - Перезапуск: docker compose restart
echo.
pause
