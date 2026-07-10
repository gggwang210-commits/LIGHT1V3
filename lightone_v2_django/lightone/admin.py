from django.contrib import admin
from .models import Indicator, Member, MemberSession, Session, StrategyItem

@admin.register(MemberSession)
class MemberSessionAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'trainer_name', 'qs_score', 'jatc_score', 'route', 'qc_status', 'created_at')
    list_filter = ('route', 'qc_status')


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('synthetic_id', 'display_label', 'goal', 'status', 'created_at')
    list_filter = ('status', 'consent_status')
    search_fields = ('synthetic_id', 'display_label', 'goal')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'member', 'exercise_name', 'session_date', 'rpe', 'pain_response', 'route', 'qc_status')
    list_filter = ('route', 'qc_status', 'session_date')
    search_fields = ('session_id', 'member__synthetic_id', 'member__display_label', 'exercise_name')


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('member_session', 'qs_score', 'jatc_score', 'route', 'qc_status', 'trainer_review_required', 'created_at')
    list_filter = ('route', 'qc_status', 'trainer_review_required')

@admin.register(StrategyItem)
class StrategyItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'status')
    list_filter = ('category', 'priority', 'status')
