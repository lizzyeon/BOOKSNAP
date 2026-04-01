from django.contrib import admin
from django.utils.html import format_html
from content.models import Follow
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_login', 'profile_preview', 'email', 'nickname', 'name', 'follower_count', 'following_count', 'is_staff', 'is_superuser')
    search_fields = ('email', 'nickname', 'name')
    list_filter = ('is_staff', 'is_superuser')
    ordering = ('id',)
    readonly_fields = ('password',)

    fieldsets = (
        ('기본 정보', {
            'fields': ('email', 'password')
        }),
        ('사용자 정보', {
            'fields': ('nickname', 'name', 'profile_image', 'last_login')
        }),
        ('권한', {
            'fields': ('is_staff', 'is_superuser', 'is_admin')
        }),
    )

    def profile_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="/media/{}" width="60" height="60" style="object-fit:cover;" />',
                obj.profile_image
            )
        return "-"

    profile_preview.short_description = 'Profile'


    def follower_count(self, obj):
        return Follow.objects.filter(to_user=obj, is_followed=True).count()

    def following_count(self, obj):
        return Follow.objects.filter(from_user=obj, is_followed=True).count()