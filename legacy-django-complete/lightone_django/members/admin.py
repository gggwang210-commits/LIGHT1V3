from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'sex', 'goal', 'discomfort_area', 'is_active', 'registered_at']
    list_filter = ['goal', 'sex', 'is_active']
    search_fields = ['name', 'discomfort_area']
