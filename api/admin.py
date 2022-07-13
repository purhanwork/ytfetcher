from django.contrib import admin
from django.contrib.auth.models import User, Group
from api.models import VideoMeta

admin.site.unregister(User)
admin.site.unregister(Group)

class VideMetaAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'title_preview', 'publishedAt')
    readonly_fields = ('video_url', 'thumbnail_preview', 'title_preview',)
    list_filter = ('publishedAt',)
    ordering = ('-publishedAt',)
    search_fields = ('title', 'description',)
    list_per_page = 10
    actions = None

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    def title_preview(self, obj):
        return obj.title_preview

    thumbnail_preview.short_description = ''
    thumbnail_preview.allow_tags = True
    title_preview.short_description = ''
    title_preview.allow_tags = True

admin.site.register(VideoMeta, VideMetaAdmin)
