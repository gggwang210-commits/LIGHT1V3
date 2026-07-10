from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WeeklyReport
from members.models import Member
from pt_sessions.models import MemberSession
from django.db.models import Avg


@login_required
def report_list(request):
    reports = WeeklyReport.objects.select_related('member').order_by('-week_start')[:30]
    return render(request, 'reports/report_list.html', {'reports': reports})


@login_required
def report_detail(request, pk):
    report = get_object_or_404(WeeklyReport, pk=pk)
    sessions = MemberSession.objects.filter(
        member=report.member,
        session_date__gte=report.week_start,
        session_date__lte=report.week_end,
    ).order_by('session_date')
    return render(request, 'reports/report_detail.html', {
        'report': report,
        'sessions': sessions,
        'route_summary': report.route_summary(),
    })


@login_required
def report_generate(request, member_pk):
    member = get_object_or_404(Member, pk=member_pk)
    from datetime import date, timedelta
    today = date.today()
    week_start = today - timedelta(days=28)
    sessions = MemberSession.objects.filter(
        member=member,
        session_date__gte=week_start,
        session_date__lte=today,
    )
    if not sessions.exists():
        messages.warning(request, '최근 4주 세션 데이터가 없습니다.')
        return redirect('member_detail', pk=member_pk)
    agg = sessions.aggregate(avg_qs=Avg('qs_score'), avg_pain=Avg('pain_response'), avg_rpe=Avg('rpe'))
    try:
        trainer_profile = request.user.trainer_profile
    except Exception:
        trainer_profile = None
    report = WeeklyReport.objects.create(
        member=member,
        trainer=trainer_profile,
        week_start=week_start,
        week_end=today,
        avg_qs=round(agg['avg_qs'] or 0, 1),
        avg_pain=round(agg['avg_pain'] or 0, 1),
        avg_rpe=round(agg['avg_rpe'] or 0, 1),
        session_count=sessions.count(),
        posture_score=round(sum(s.posture_summary() for s in sessions) / sessions.count(), 1),
        auto_count=sessions.filter(route='AUTO').count(),
        review_count=sessions.filter(route='REVIEW').count(),
        block_count=sessions.filter(route='BLOCK').count(),
        reregistration_signal=(sessions.filter(route='BLOCK').count() == 0 and sessions.count() >= 8),
    )
    messages.success(request, f'{member.name} 리포트가 생성되었습니다.')
    return redirect('report_detail', pk=report.pk)
