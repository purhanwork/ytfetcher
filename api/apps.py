import threading
from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    def ready(self):
        from api.daemon import fetchVideoData
        threading.Thread(target=fetchVideoData,daemon=True).start()
