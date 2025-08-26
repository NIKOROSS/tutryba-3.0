#!/usr/bin/env python3
"""
WSGI конфигурация для проекта ТУТРЫБА.
"""

import os
import sys

# Путь к проекту (замените на реальный путь на сервере)
# Например: /var/www/tutryba или /home/user/public_html
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# Добавляем путь к проекту в sys.path
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# Путь к виртуальному окружению (если используется)
# VENV_PATH = os.path.join(PROJECT_PATH, 'venv')
# if os.path.exists(VENV_PATH):
#     activate_this = os.path.join(VENV_PATH, 'bin', 'activate_this.py')
#     if os.path.exists(activate_this):
#         with open(activate_this) as file_:
#             exec(file_.read(), dict(__file__=activate_this))

# Настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

# Приложение Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
