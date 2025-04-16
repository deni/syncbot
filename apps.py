from django.apps import AppConfig
from cron import runCronTasks

class SyncbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'syncbot'

    def ready(self):
        runCronTasks()
