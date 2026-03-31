from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_login', 'email', 'nickname', 'name', 'is_staff', 'is_superuser')
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