from .utils.qs_calculator import (
    clamp,
    calculate_qs,
    map_pain_response_score,
    normalize_score,
)

SAFETY_NOTICE = '비의료 운동상담 참고, 트레이너 검토 필요'

ROUTE_AUTO = 'AUTO'
ROUTE_REVIEW = 'REVIEW'
ROUTE_BLOCK = 'BLOCK'



def calculate_jatc(qs_score, form_accuracy, discomfort_response, rpe):
    """JATC combines QS, movement quality, discomfort stability and session load fit."""
    form_component = normalize_score(form_accuracy)
    discomfort_component = map_pain_response_score(discomfort_response)
    rpe_component = 100 - (abs(clamp(rpe, 0, 10) - 7) * 10)
    score = (clamp(qs_score) * 0.5) + (clamp(form_component) * 0.2) + (clamp(discomfort_component) * 0.2) + (clamp(rpe_component) * 0.1)
    return round(clamp(score), 1)


def determine_routing(qs_score, jatc_score=None, discomfort_response=0, qc_status='PASS'):
    if jatc_score is None:
        jatc_score = qs_score
    if qc_status == 'FAIL' or discomfort_response >= 7 or qs_score < 40 or jatc_score < 40:
        return ROUTE_BLOCK
    if qc_status == 'CHECK' or discomfort_response >= 4 or qs_score < 70 or jatc_score < 60:
        return ROUTE_REVIEW
    return ROUTE_AUTO


def route_session(qs_score, jatc_score, discomfort_response, qc_status='PASS'):
    return determine_routing(qs_score, jatc_score, discomfort_response, qc_status)
