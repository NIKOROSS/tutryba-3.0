# 🐟 ТУТРЫБА - Интернет-магазин рыбы

Онлайн-магазин рыбы и морепродуктов с автоматическим расчетом доставки.

## ✨ Основные возможности

- 🛒 **Корзина покупок** с сессионным хранением
- 📦 **Автоматический расчет доставки** через Yandex Delivery API
- 🗺️ **Геокодирование адресов** через Yandex Geocoder API
- 👤 **Система пользователей** с регистрацией и авторизацией
- 📋 **История заказов** для пользователей
- 💳 **Онлайн оплата** и оплата при получении
- 📱 **Адаптивный дизайн** для всех устройств
- 🔧 **Админ-панель** для управления товарами и заказами

## 🛠️ Технологии

- **Backend**: Django 5.0.2
- **Frontend**: Bootstrap 5, jQuery
- **База данных**: SQLite (разработка) / PostgreSQL (продакшен)
- **Аутентификация**: django-allauth
- **Формы**: django-crispy-forms
- **API**: Yandex Delivery, Yandex Geocoder

## 🚀 Быстрый старт

### Локальная разработка

1. **Клонирование репозитория**
   ```bash
   git clone <repository-url>
   cd tutryba-3.0
   ```

2. **Создание виртуального окружения**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установка зависимостей**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройка переменных окружения**
   Создайте файл `.env` в корне проекта:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   YANDEX_DELIVERY_API_KEY=your-api-key
   YANDEX_GEOCODER_API_KEY=your-api-key
   ```

5. **Миграции базы данных**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Создание суперпользователя**
   ```bash
   python manage.py createsuperuser
   ```

7. **Запуск сервера**
   ```bash
   python manage.py runserver
   ```

### Развертывание на сервере

См. файл `DEPLOYMENT.md` для подробных инструкций.

## 📁 Структура проекта

```
tutryba-3.0/
├── accounts/          # Пользователи и профили
├── cart/             # Корзина и заказы
├── products/         # Товары и категории
├── market/           # Основные настройки Django
├── templates/        # HTML шаблоны
├── static/           # Статические файлы (CSS, JS, изображения)
├── media/            # Загруженные файлы
├── requirements.txt  # Зависимости Python
├── DEPLOYMENT.md     # Инструкции по развертыванию
└── deploy.sh         # Скрипт автоматического развертывания
```

## 🔧 Настройка API

### Yandex Delivery API

1. Получите API ключ на [Yandex Delivery](https://delivery.yandex.ru/)
2. Добавьте ключ в переменную окружения `YANDEX_DELIVERY_API_KEY`

### Yandex Geocoder API

1. Получите API ключ на [Yandex Geocoder](https://yandex.ru/dev/geocoder/)
2. Добавьте ключ в переменную окружения `YANDEX_GEOCODER_API_KEY`

## 📊 База данных

### Основные модели

- **Product**: Товары с категориями
- **Order**: Заказы с адресами доставки
- **OrderItem**: Товары в заказах
- **CustomUser**: Пользователи с дополнительными полями

### Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🎨 Кастомизация

### Добавление новых категорий товаров

1. Создайте категорию через админ-панель
2. Добавьте товары в категорию
3. Категория автоматически появится в навигации

### Изменение дизайна

- CSS файлы: `static/css/style.css`
- Шаблоны: `templates/`
- JavaScript: `static/js/`

## 🔒 Безопасность

- CSRF защита включена
- XSS фильтрация
- Безопасные настройки сессий
- Валидация форм

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи в `logs/django.log`
2. Убедитесь, что все зависимости установлены
3. Проверьте настройки в файле `.env`

## 📄 Лицензия

© 2025 Магазин ТУТРЫБА. Все права защищены.
