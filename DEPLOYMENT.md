# Инструкция по развертыванию ТУТРЫБА

## 🚀 Быстрое развертывание

### 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Установка Nginx
sudo apt install nginx -y

# Установка PostgreSQL (опционально, можно использовать SQLite)
sudo apt install postgresql postgresql-contrib -y
```

### 2. Загрузка проекта

```bash
# Создание директории для проекта
sudo mkdir -p /var/www/tutryba
sudo chown $USER:$USER /var/www/tutryba

# Загрузка файлов проекта в /var/www/tutryba/
# (скопируйте все файлы проекта в эту папку)
```

### 3. Настройка виртуального окружения

```bash
cd /var/www/tutryba

# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 4. Настройка базы данных

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Сбор статических файлов
python manage.py collectstatic --noinput
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# База данных (если используете PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost/tutryba

# Email
EMAIL_HOST=smtp.your-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@domain.com

# Yandex API (опционально)
YANDEX_DELIVERY_API_KEY=your-yandex-delivery-api-key
YANDEX_GEOCODER_API_KEY=your-yandex-geocoder-api-key
```

### 6. Настройка Gunicorn

```bash
# Установка Gunicorn
pip install gunicorn

# Создание systemd сервиса
sudo nano /etc/systemd/system/tutryba.service
```

Содержимое файла `/etc/systemd/system/tutryba.service`:

```ini
[Unit]
Description=Tutryba Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/tutryba
Environment="PATH=/var/www/tutryba/venv/bin"
ExecStart=/var/www/tutryba/venv/bin/gunicorn --workers 3 --bind unix:/var/www/tutryba/tutryba.sock market.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 7. Настройка Nginx

```bash
sudo nano /etc/nginx/sites-available/tutryba
```

Содержимое файла конфигурации Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/tutryba;
    }

    location /media/ {
        root /var/www/tutryba;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/tutryba/tutryba.sock;
    }
}
```

```bash
# Активация сайта
sudo ln -s /etc/nginx/sites-available/tutryba /etc/nginx/sites-enabled

# Проверка конфигурации Nginx
sudo nginx -t

# Перезапуск Nginx
sudo systemctl restart nginx
```

### 8. Запуск сервисов

```bash
# Запуск Django приложения
sudo systemctl start tutryba
sudo systemctl enable tutryba

# Проверка статуса
sudo systemctl status tutryba
```

### 9. Настройка SSL (HTTPS)

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx -y

# Получение SSL сертификата
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 🔧 Дополнительные настройки

### Настройка для продакшена

В `settings.py` измените:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Настройки безопасности
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Резервное копирование

```bash
# Создание бэкапа базы данных
python manage.py dumpdata > backup.json

# Восстановление из бэкапа
python manage.py loaddata backup.json
```

## 📝 Проверка работоспособности

1. Откройте сайт в браузере
2. Проверьте работу корзины
3. Проверьте оформление заказов
4. Проверьте админ-панель
5. Проверьте расчет доставки

## 🆘 Устранение неполадок

### Логи

```bash
# Логи Django
sudo journalctl -u tutryba

# Логи Nginx
sudo tail -f /var/log/nginx/error.log
```

### Права доступа

```bash
# Установка правильных прав
sudo chown -R www-data:www-data /var/www/tutryba
sudo chmod -R 755 /var/www/tutryba
```

### Перезапуск сервисов

```bash
sudo systemctl restart tutryba
sudo systemctl restart nginx
```
