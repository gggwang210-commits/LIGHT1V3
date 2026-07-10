from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import MemberSession
from members.models import Member


@login_required
def session_list(request):
    sessions = MemberSession.objects.select_related('member').order_by('-created_at')[:50]
    return render(request, 'sessions/session_list.html', {'sessions': sessions})


@login_required
def session_detail(request, pk):
    session = get_object_or_404(MemberSession, pk=pk)
    return render(request, 'sessions/session_detail.html', {'session': session})


@login_required
def session_create(request):
    members = Member.objects.filter(is_active=True)
    if request.method == 'POST':
        member_id = request.POST.get('member')
        member = get_object_or_404(Member, pk=member_id)
        try:
            trainer_profile = request.user.trainer_profile
        except Exception:
            trainer_profile = None
        s = MemberSession(
            member=member,
            trainer=trainer_profile,
            session_date=request.POST.get('session_date') or timezone.now().date(),
            exercise_name=request.POST.get('exercise_name', ''),
            sets=int(request.POST.get('sets', 3)),
            reps=int(request.POST.get('reps', 10)),
            weight_kg=float(request.POST.get('weight_kg', 0)),
            pain_response=float(request.POST.get('pain_response', 0)),
            rpe=float(request.POST.get('rpe', 5)),
            form_accuracy=float(request.POST.get('form_accuracy', 7)),
            jatc_score=float(request.POST.get('jatc_score', 70)),
            shoulder_tilt=float(request.POST.get('shoulder_tilt', 0)),
            pelvis_tilt=float(request.POST.get('pelvis_tilt', 0)),
            spine_alignment=float(request.POST.get('spine_alignment', 7)),
            knee_alignment=float(request.POST.get('knee_alignment', 7)),
            ankle_alignment=float(request.POST.get('ankle_alignment', 7)),
            lr_deviation=float(request.POST.get('lr_deviation', 0)),
            qc_status=request.POST.get('qc_status', 'PASS'),
            memo=request.POST.get('memo', ''),
        )
        s.save()
        s.calculate_qs_and_route()
        messages.success(request, f'{member.name} 세션이 기록되었습니다. QS: {s.qs_score} [{s.route}]')
        return redirect('session_detail', pk=s.pk)
    return render(request, 'sessions/session_form.html', {'members': members, 'action': '기록'})


@login_required
def dashboard_view(request):
    from django.db.models import Avg
    total_members = Member.objects.filter(is_active=True).count()
    total_sessions = MemberSession.objects.count()
    avg_qs = MemberSession.objects.aggregate(avg=Avg('qs_score'))['avg'] or 0
    route_counts = {
        'AUTO': MemberSession.objects.filter(route='AUTO').count(),
        'REVIEW': MemberSession.objects.filter(route='REVIEW').count(),
        'BLOCK': MemberSession.objects.filter(route='BLOCK').count(),
    }
    recent_sessions = MemberSession.objects.select_related('member').order_by('-created_at')[:8]
    block_sessions = MemberSession.objects.filter(route='BLOCK').select_related('member').order_by('-created_at')[:5]
    review_sessions = MemberSession.objects.filter(route='REVIEW').select_related('member').order_by('-created_at')[:5]
    return render(request, 'dashboard/dashboard.html', {
        'total_members': total_members,
        'total_sessions': total_sessions,
        'avg_qs': round(avg_qs, 1),
        'route_counts': route_counts,
        'recent_sessions': recent_sessions,
        'block_sessions': block_sessions,
        'review_sessions': review_sessions,
    })
