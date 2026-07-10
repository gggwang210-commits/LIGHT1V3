from lightone.algorithms import ROUTE_AUTO, ROUTE_BLOCK, ROUTE_REVIEW


def _has_safety_flags(safety_flags=None):
    if safety_flags is None:
        return False
    if isinstance(safety_flags, str):
        return bool(safety_flags.strip())
    if isinstance(safety_flags, dict):
        return any(bool(value) for value in safety_flags.values())
    if isinstance(safety_flags, (list, tuple, set)):
        return any(bool(value) for value in safety_flags)
    return bool(safety_flags)


def _is_low_or_none_pain(pain_level):
    if pain_level is None:
        return True

    try:
        numeric_pain = float(pain_level)
    except (TypeError, ValueError):
        normalized_pain = str(pain_level).strip().lower()
        return normalized_pain in {'none', 'no', 'low', '0', '없음', '낮음'}

    # Project pain scale convention for numeric inputs:
    # 0~3 = low/none (AUTO eligible), 4~6 = mild/review, 7~10 = high/block.
    return 0 <= numeric_pain <= 3


def _is_high_pain(pain_level):
    try:
        numeric_pain = float(pain_level)
    except (TypeError, ValueError):
        normalized_pain = str(pain_level).strip().lower()
        return normalized_pain in {'high', 'severe', 'block', '높음', '심함'}

    # Project pain scale convention for numeric inputs:
    # 0~3 = low/none (AUTO eligible), 4~6 = mild/review, 7~10 = high/block.
    return numeric_pain >= 7


def determine_routing(qs_score, pain_level, safety_flags=None):
    """Determine non-medical routing from QS, pain level, and safety flags."""
    if _has_safety_flags(safety_flags) or _is_high_pain(pain_level):
        return ROUTE_BLOCK
    if float(qs_score) >= 80 and _is_low_or_none_pain(pain_level):
        return ROUTE_AUTO
    return ROUTE_REVIEW
