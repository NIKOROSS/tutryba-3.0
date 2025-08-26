#!/bin/bash

# Скрипт для развертывания ТУТРЫБА на сервере
# Использование: ./deploy.sh

echo "🚀 Начинаем развертывание ТУТРЫБА..."

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен. Установите Python3 и попробуйте снова."
    exit 1
fi

# Проверка наличия pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не установлен. Установите pip3 и попробуйте снова."
    exit 1
fi

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
python3 -m venv venv

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Обновление pip
echo "⬆️ Обновление pip..."
pip install --upgrade pip

# Установка зависимостей
echo "📚 Установка зависимостей..."
pip install -r requirements.txt

# Создание директории для логов
echo "📁 Создание директории для логов..."
mkdir -p logs

# Создание миграций
echo "🗄️ Создание миграций..."
python manage.py makemigrations

# Применение миграций
echo "🔄 Применение миграций..."
python manage.py migrate

# Сбор статических файлов
echo "📦 Сбор статических файлов..."
python manage.py collectstatic --noinput

# Создание суперпользователя (если не существует)
echo "👤 Создание суперпользователя..."
echo "Введите данные для суперпользователя (или нажмите Enter для пропуска):"
python manage.py createsuperuser --noinput || echo "Суперпользователь уже существует или создание пропущено"

echo "✅ Развертывание завершено!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Настройте файл .env с вашими переменными окружения"
echo "2. Настройте Nginx (см. DEPLOYMENT.md)"
echo "3. Настройте Gunicorn (см. DEPLOYMENT.md)"
echo "4. Запустите сервер: python manage.py runserver"
echo ""
echo "🌐 Для запуска в продакшене используйте Gunicorn:"
echo "gunicorn --workers 3 --bind 0.0.0.0:8000 market.wsgi:application"
