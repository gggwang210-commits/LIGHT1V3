from .models import Member, MemberSession, StrategyItem


STATUS_BADGES = {
    'AUTO': 'badge-auto badge-green',
    'REVIEW': 'badge-review badge-yellow',
    'BLOCK': 'badge-block badge-red',
}


def routing_label(route):
    return route or 'UNKNOWN'


def routing_badge_class(route):
    normalized = (route or '').upper()
    if normalized in {'AUTO', 'GREEN'}:
        return 'badge-green'
    if normalized in {'REVIEW', 'YELLOW'}:
        return 'badge-yellow'
    if normalized in {'BLOCK', 'RED'}:
        return 'badge-red'
    return 'badge-gray'


def _decorate_session(session):
    session.routing_label = routing_label(session.route)
    session.routing_badge_class = routing_badge_class(session.route)
    return session


def _empty_member_dashboard():
    return {
        'selected_member_id': None,
        'qs_labels': [],
        'qs_scores': [],
        'breakdown_values': [],
        'recent_sessions': [],
        'status_badges': STATUS_BADGES,
    }


def _member_dashboard_context(member_id=None):
    member_qs = Member.objects.all().order_by('synthetic_id')
    if member_id:
        member_qs = member_qs.filter(synthetic_id=member_id)

    member = member_qs.first()
    if not member:
        return _empty_member_dashboard()

    recent_sessions = list(
        MemberSession.objects.filter(member_name=member.display_label)
        .select_related('indicator')
        .order_by('-created_at', '-qs_score')[:5]
    )
    recent_sessions = [_decorate_session(session) for session in recent_sessions]
    chronological_sessions = list(reversed(recent_sessions))
    breakdown_values = []
    if recent_sessions:
        latest = recent_sessions[0]
        breakdown_values = [
            latest.qs_form_component,
            latest.rep_score,
            latest.rest_score,
            latest.qs_discomfort_component,
            latest.jatc_score,
            latest.posture_score,
            latest.function_training_score,
            latest.lifestyle_score,
        ]

    return {
        'selected_member_id': member.synthetic_id,
        'qs_labels': [session.created_at.strftime('%m/%d') for session in chronological_sessions],
        'qs_scores': [session.qs_score for session in chronological_sessions],
        'breakdown_values': breakdown_values,
        'recent_sessions': recent_sessions,
        'status_badges': STATUS_BADGES,
    }


def dashboard_context(member_id=None):
    sessions = list(MemberSession.objects.select_related('indicator').all())
    sessions = [_decorate_session(session) for session in sessions]
    total = len(sessions)
    if total:
        avg_qs = round(sum(s.qs_score for s in sessions) / total, 1)
        avg_jatc = round(sum(s.jatc_score for s in sessions) / total, 1)
    else:
        avg_qs = 0
        avg_jatc = 0

    counts = {key: sum(1 for s in sessions if s.route == key) for key in STATUS_BADGES}
    qc_counts = {key: sum(1 for s in sessions if s.qc_status == key) for key in ['PASS', 'CHECK', 'FAIL']}

    feature_importance = [
        {'name': 'Pain response', 'value': 0.28},
        {'name': 'Form quality', 'value': 0.25},
        {'name': 'RPE', 'value': 0.18},
        {'name': 'Capture QC', 'value': 0.13},
        {'name': 'JATC', 'value': 0.10},
        {'name': 'Lifestyle', 'value': 0.06},
    ]

    qs_labels = [session.created_at.strftime('%m/%d') for session in sessions]
    qs_scores = [session.qs_score for session in sessions]
    breakdown_labels = ['Pain response', 'Form quality', 'RPE', 'Capture QC', 'JATC', 'Lifestyle']
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
