from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserGame

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_picture', 'is_subscribed', 'subscription_end_date')
        }),
    )

@admin.register(UserGame)
class UserGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'purchase_date', 'last_played', 'play_time')
    list_filter = ('user', 'game')
    readonly_fields = ('purchase_date',)
