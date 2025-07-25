from django.contrib import admin
from .models import Game, GameImage, GameVideo, Platform

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'release_date', 'has_images', 'has_videos')
    list_filter = ('status', 'platforms')
    search_fields = ('title', 'description')

    filter_horizontal = ('platforms',)
    readonly_fields = ('created_at', 'updated_at')

    def has_images(self, obj):
        return obj.images.exists()
    has_images.boolean = True
    has_images.short_description = 'Images'

    def has_videos(self, obj):
        return obj.videos.exists()
    has_videos.boolean = True
    has_videos.short_description = 'Videos'

@admin.register(GameImage)
class GameImageAdmin(admin.ModelAdmin):
    list_display = ('game', 'is_main_image', 'has_image_or_url')
    list_filter = ('game', 'is_main_image')
    readonly_fields = ('image_preview',)

    def has_image_or_url(self, obj):
        return bool(obj.image or obj.image_url)
    has_image_or_url.boolean = True
    has_image_or_url.short_description = 'Has Media'

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        elif obj.image_url:
            return f'<img src="{obj.image_url}" width="100" height="100" />'
        return ''
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'

@admin.register(GameVideo)
class GameVideoAdmin(admin.ModelAdmin):
    list_display = ('game', 'video_url')
    list_filter = ('game',)

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name',)
