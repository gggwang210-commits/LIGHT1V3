from .models import Indicator, Member, MemberSession, StrategyItem


def _empty_member_dashboard():
    return {
        'selected_member_id': None,
        'qs_labels': [],
        'qs_scores': [],
        'breakdown_values': [],
        'recent_sessions': [],
        'status_badges': {
            'AUTO': 'badge-auto badge-green',
            'REVIEW': 'badge-review badge-yellow',
            'BLOCK': 'badge-block badge-red',
        },
    }


def _member_dashboard_context(member_id=None):
    member_qs = Member.objects.all().order_by('member_id')
    if member_id:
        member_qs = member_qs.filter(member_id=member_id)

    member = member_qs.first()
    if not member:
        return _empty_member_dashboard()

    recent_sessions = list(
        member.sessions.select_related('indicator').order_by('-date', 'exercise_name')[:5]
    )
    chronological_sessions = list(reversed(recent_sessions))
    indicators = [getattr(session, 'indicator', None) for session in chronological_sessions]
    indicators = [indicator for indicator in indicators if indicator is not None]

    latest_indicator = getattr(recent_sessions[0], 'indicator', None) if recent_sessions else None
    breakdown_values = []
    if latest_indicator:
        breakdown_values = [
            latest_indicator.form_accuracy,
            latest_indicator.rep_rate,
            latest_indicator.rest_compliance,
            latest_indicator.pain_score,
            latest_indicator.jatc_pain,
            latest_indicator.jatc_posture,
            latest_indicator.jatc_function,
            latest_indicator.jatc_lifestyle,
        ]

    return {
        'selected_member_id': str(member.member_id),
        'qs_labels': [session.date.strftime('%m/%d') for session in chronological_sessions],
        'qs_scores': [indicator.qs_score for indicator in indicators],
        'breakdown_values': breakdown_values,
        'recent_sessions': recent_sessions,
        'status_badges': {
            'AUTO': 'badge-auto badge-green',
            'REVIEW': 'badge-review badge-yellow',
            'BLOCK': 'badge-block badge-red',
        },
    }


def dashboard_context(member_id=None):
    sessions = list(MemberSession.objects.all())
    total = len(sessions)
    if total:
        avg_qs = round(sum(s.qs_score for s in sessions) / total, 1)
        avg_jatc = round(sum(s.jatc_score for s in sessions) / total, 1)
    else:
        avg_qs = 0
        avg_jatc = 0

    counts = {key: sum(1 for s in sessions if s.route == key) for key in ['AUTO', 'REVIEW', 'BLOCK']}
    qc_counts = {key: sum(1 for s in sessions if s.qc_status == key) for key in ['PASS', 'CHECK', 'FAIL']}

    indicator_counts = {
        key: Indicator.objects.filter(routing_status=key).count()
        for key in ['AUTO', 'REVIEW', 'BLOCK']
    }
    for key, value in indicator_counts.items():
        if value:
            counts[key] += value
    total += sum(indicator_counts.values())

    feature_importance = [
        {'name': '통증 반응', 'value': 0.28},
        {'name': '폼 정확도', 'value': 0.25},
        {'name': 'RPE', 'value': 0.18},
        {'name': '촬영 QC', 'value': 0.13},
        {'name': 'JATC', 'value': 0.10},
        {'name': '생활습관', 'value': 0.06},
    ]

    qs_labels = [session.date.strftime('%m/%d') for session in sessions]
    qs_scores = [session.qs_score for session in sessions]
    breakdown_labels = ['통증 반응', '폼 정확도', 'RPE', '촬영 QC', 'JATC', '생활습관']
    breakdown_values = [0.28, 0.25, 0.18, 0.13, 0.10, 0.06]

    context = {
        'sessions': sessions,
        'recent_sessions': sessions,
        'strategy_items': StrategyItem.objects.all()[:6],
        'total': total,
        'avg_qs': avg_qs,
        'avg_jatc': avg_jatc,
        'counts': counts,
        'qc_counts': qc_counts,
        'feature_importance': feature_importance,
        'qs_labels': qs_labels,
        'qs_scores': qs_scores,
        'breakdown_labels': breakdown_labels,
        'breakdown_values': breakdown_values,
    }
    context.update(_member_dashboard_context(member_id))
    return context
