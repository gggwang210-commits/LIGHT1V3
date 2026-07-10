from django.contrib import admin
from .models import MemberSession

@admin.register(MemberSession)
class MemberSessionAdmin(admin.ModelAdmin):
    list_display = ['member', 'session_date', 'qs_score', 'route', 'pain_response', 'rpe', 'qc_status', 'created_at']
    list_filter = ['route', 'qc_status']
    search_fields = ['member__name']
    readonly_fields = ['qs_score', 'route']
