from datetime import datetime
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from rest_framework import generics
from .models import VideoMeta

class VideoMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoMeta
        fields = '__all__'

class VideoMetadataPagination(PageNumberPagination):
    page_size = 10

class VideoMetadata(generics.ListAPIView):
    serializer_class = VideoMetadataSerializer
    pagination_class = VideoMetadataPagination
    queryset = VideoMeta.objects.all().order_by('-publishedAt')
    search_fields = ('title', 'description',)
    filter_backends = (filters.SearchFilter,)