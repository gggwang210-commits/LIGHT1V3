from django.contrib import admin
from .models import WeeklyReport

@admin.register(WeeklyReport)
class WeeklyReportAdmin(admin.ModelAdmin):
    list_display = ['member', 'week_start', 'week_end', 'avg_qs', 'session_count', 'reregistration_signal']
    list_filter = ['reregistration_signal']
    search_fields = ['member__name']
