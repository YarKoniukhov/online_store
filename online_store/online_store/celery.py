import os
from celery import Celery


# задать стандартный модуль настроек Django для программы 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')

# Создайте экземпляр приложения Celery.
app = Celery('online_store')

# Настройте приложение Celery для использования настроек Django и указанной переменной среды для подключения к RabbitMQ.
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.broker_url = os.environ.get('BROKER_URL')

# Автоматически обнаруживайте задачи Celery в вашем проекте.
app.autodiscover_tasks()
