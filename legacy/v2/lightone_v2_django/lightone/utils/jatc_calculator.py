from lightone.algorithms import SAFETY_NOTICE, clamp, normalize_ten_scale


def _has_trainer_memo_flag(session):
    memo = getattr(session, 'memo', '') or getattr(session, 'trainer_memo', '') or ''
    flags = ('검토', '통증', '중단', '주의', 'review', 'pain', 'stop', 'flag')
    return any(flag in memo.lower() for flag in flags)


def _rep_achievement(session):
    planned = getattr(session, 'planned_reps', 0) or 0
    completed = getattr(session, 'completed_reps', 0) or 0
    if not planned:
        return 100
    return clamp((completed / planned) * 100)


def _rest_compliance(session):
    planned = getattr(session, 'planned_rest_seconds', 0) or 0
    actual = getattr(session, 'actual_rest_seconds', 0) or 0
    if not planned:
        return 100
    return clamp(100 - min(abs(actual - planned) / planned * 100, 100))


def calculate_jatc(session):
    """Return MVP JATC components for non-medical exercise counseling reference.

    MVP 기준:
    - QS는 전체 JATC의 45%로 반영해 기존 세션 품질 평가를 중심 신호로 사용한다.
    - QC 상태는 PASS 100, CHECK 70, FAIL 0으로 환산해 20% 반영한다.
    - pain_response는 0~10 통증 반응을 역점수화해 20% 반영하고, 7 이상이면 BLOCK 후보가 된다.
    - trainer memo flag는 통증/중단/검토 등 키워드가 있으면 15점 감점해 트레이너 검토를 유도한다.
    - 결과와 안내 문구는 진단·치료·처방이 아닌 “비의료 운동상담 참고용”이다.
    """
    qs_score = clamp(getattr(session, 'qs_score', 0))
    if not qs_score:
        form = normalize_ten_scale(getattr(session, 'form_accuracy', 0) or getattr(session, 'posture_score', 0))
        pain = 100 - (clamp(getattr(session, 'pain_response', 0), 0, 10) * 10)
        rpe = 100 - (abs(clamp(getattr(session, 'rpe', 0), 0, 10) - 7) * 10)
        qs_score = clamp((form * 0.4) + (pain * 0.3) + (rpe * 0.2) + 10)

    qc_component = {'PASS': 100, 'CHECK': 70, 'FAIL': 0}.get(getattr(session, 'qc_status', 'PASS'), 70)
    pain_component = 100 - (clamp(getattr(session, 'pain_response', 0), 0, 10) * 10)
    function_component = clamp(
        (normalize_ten_scale(getattr(session, 'function_training_score', 0)) * 0.5)
        + (_rep_achievement(session) * 0.3)
        + (_rest_compliance(session) * 0.2)
    )
    memo_flag = _has_trainer_memo_flag(session)
    memo_penalty = 15 if memo_flag else 0
    score = (qs_score * 0.45) + (qc_component * 0.2) + (pain_component * 0.2) + (function_component * 0.15) - memo_penalty
    return {
        'score': round(clamp(score), 1),
        'qs_score': round(qs_score, 1),
        'qc_component': round(qc_component, 1),
        'pain_component': round(pain_component, 1),
        'function_component': round(function_component, 1),
        'trainer_memo_flag': memo_flag,
        'notice': SAFETY_NOTICE,
    }
