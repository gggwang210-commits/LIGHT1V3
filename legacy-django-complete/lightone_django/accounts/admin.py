from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TrainerProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'display_name', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('LIGHT ONE 정보', {'fields': ('role', 'display_name')}),
    )


@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'center_name', 'specialty']
