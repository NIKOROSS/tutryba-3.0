# Инструкция по развертыванию ТУТРЫБА на Apache

## 🚀 Развертывание на Apache сервере

### Вариант 1: Shared Hosting (cPanel, ISPmanager и т.д.)

#### 1. Загрузка файлов
```bash
# Загрузите все файлы проекта в корневую папку сайта
# Обычно это public_html/ или www/
```

#### 2. Настройка Python
```bash
# Создайте виртуальное окружение
python3 -m venv venv

# Активируйте его
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

#### 3. Настройка .htaccess
Создайте файл `.htaccess` в корне сайта:

```apache
# .htaccess для Django на Apache
RewriteEngine On

# Перенаправление на HTTPS (опционально)
# RewriteCond %{HTTPS} off
# RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Статические файлы
RewriteCond %{REQUEST_URI} !^/static/
RewriteCond %{REQUEST_URI} !^/media/

# Перенаправление всех запросов на Django
RewriteRule ^(.*)$ /tutryba.wsgi/$1 [QSA,L]

# Настройки для Python
AddHandler wsgi-script .wsgi
Options ExecCGI

# Безопасность
<Files "*.py">
    Require all denied
</Files>

<Files "*.pyc">
    Require all denied
</Files>

<Files ".env">
    Require all denied
</Files>
```

#### 4. Создание WSGI файла
Создайте файл `tutryba.wsgi` в корне сайта:

```python
#!/usr/bin/env python3
import os
import sys

# Путь к проекту
path = '/path/to/your/project'  # Замените на реальный путь
if path not in sys.path:
    sys.path.append(path)

# Путь к виртуальному окружению
activate_this = '/path/to/your/project/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

# Приложение Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### 5. Настройка базы данных
```bash
# Создайте миграции
python manage.py makemigrations

# Примените миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Соберите статические файлы
python manage.py collectstatic --noinput
```

### Вариант 2: VPS/Выделенный сервер с Apache

#### 1. Установка Apache и mod_wsgi
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install apache2 libapache2-mod-wsgi-py3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install httpd mod_wsgi python3-pip python3-venv
```

#### 2. Настройка виртуального хоста
Создайте файл `/etc/apache2/sites-available/tutryba.conf`:

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    ServerAlias www.your-domain.com
    DocumentRoot /var/www/tutryba

    # WSGI настройки
    WSGIDaemonProcess tutryba python-path=/var/www/tutryba:/var/www/tutryba/venv/lib/python3.x/site-packages
    WSGIProcessGroup tutryba
    WSGIScriptAlias / /var/www/tutryba/tutryba.wsgi

    # Статические файлы
    Alias /static/ /var/www/tutryba/staticfiles/
    <Directory /var/www/tutryba/staticfiles>
        Require all granted
    </Directory>

    # Медиа файлы
    Alias /media/ /var/www/tutryba/media/
    <Directory /var/www/tutryba/media>
        Require all granted
    </Directory>

    # Основная директория
    <Directory /var/www/tutryba>
        <Files tutryba.wsgi>
            Require all granted
        </Files>
    </Directory>

    # Логи
    ErrorLog ${APACHE_LOG_DIR}/tutryba_error.log
    CustomLog ${APACHE_LOG_DIR}/tutryba_access.log combined
</VirtualHost>
```

#### 3. Активация сайта
```bash
# Ubuntu/Debian
sudo a2ensite tutryba
sudo a2enmod wsgi
sudo systemctl restart apache2

# CentOS/RHEL
sudo systemctl enable httpd
sudo systemctl restart httpd
```

### Вариант 3: Простой запуск через Python

Если у вас есть доступ к Python, но нет mod_wsgi:

#### 1. Установка Gunicorn
```bash
pip install gunicorn
```

#### 2. Запуск через Gunicorn
```bash
# В папке проекта
gunicorn --bind 0.0.0.0:8000 market.wsgi:application
```

#### 3. Настройка Apache как прокси
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```

## 🔧 Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# База данных
DATABASE_URL=sqlite:///db.sqlite3

# Email (опционально)
EMAIL_HOST=smtp.your-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password

# Yandex API (опционально)
YANDEX_DELIVERY_API_KEY=your-api-key
YANDEX_GEOCODER_API_KEY=your-api-key
```

## 📝 Проверка работоспособности

1. Откройте сайт в браузере
2. Проверьте работу корзины
3. Проверьте оформление заказов
4. Проверьте админ-панель
5. Проверьте расчет доставки

## 🆘 Устранение неполадок

### Логи Apache
```bash
# Ubuntu/Debian
sudo tail -f /var/log/apache2/error.log

# CentOS/RHEL
sudo tail -f /var/log/httpd/error_log
```

### Права доступа
```bash
sudo chown -R www-data:www-data /var/www/tutryba
sudo chmod -R 755 /var/www/tutryba
```

### Перезапуск Apache
```bash
# Ubuntu/Debian
sudo systemctl restart apache2

# CentOS/RHEL
sudo systemctl restart httpd
```

## 📞 Поддержка

Если что-то не работает:

1. Проверьте логи Apache
2. Убедитесь, что mod_wsgi установлен
3. Проверьте права доступа к файлам
4. Убедитесь, что виртуальное окружение активировано
