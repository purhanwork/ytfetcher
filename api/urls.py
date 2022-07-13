from django.urls import path
from .api import VideoMetadata

urlpatterns = [
    path('videos/', VideoMetadata.as_view())
]