from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MemberProfile, TrainerProfile

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'name', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('역할 정보', {'fields': ('role', 'name')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(MemberProfile)
admin.site.register(TrainerProfile)
