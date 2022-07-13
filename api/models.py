from django.db import models
from django.utils.html import mark_safe


class VideoMeta(models.Model):
    title = models.CharField(blank=False, max_length=100)
    description = models.TextField()
    publishedAt = models.DateTimeField(blank=False)
    thumbnailURL = models.URLField()
    videoId = models.CharField(max_length=256, primary_key=True)

    @property
    def video_url(self):
        return mark_safe(f'https://youtu.be/{self.videoId}')

    @property
    def thumbnail_preview(self):
        return mark_safe(f'<img src="{self.thumbnailURL}" width="120" height="90" />')

    @property
    def title_preview(self):
        return mark_safe(f'<a style="color: inherit;" href="{self.video_url}">' +
                         f'<h style="font-weight: bold;">{self.title}</h><br/><p>{self.description}</p></a>'
                         )

    class Meta:
        verbose_name = "Video Metadata"
        verbose_name_plural = "Videos Metadata"
        ordering = ['-publishedAt']
        default_permissions = ('view',)
        indexes = [
            models.Index(fields=['videoId']),
            models.Index(fields=['publishedAt'])
        ]
        get_latest_by = "publishedAt"

class ApiSettings(models.Model):
    baseTime = models.DateTimeField(blank=False)
