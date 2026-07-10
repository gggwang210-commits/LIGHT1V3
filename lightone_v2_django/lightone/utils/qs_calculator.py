ROUTE_AUTO = 'AUTO'
ROUTE_REVIEW = 'REVIEW'
ROUTE_BLOCK = 'BLOCK'


def clamp(value, minimum=0, maximum=100):
    """Constrain a numeric score to the inclusive project score range."""
    return max(minimum, min(maximum, float(value)))


def normalize_score(value):
    """Normalize 0-10 or 0-100 inputs to a 0-100 score."""
    value = float(value)
    if 0 <= value <= 10:
        value *= 10
    return clamp(value)


def normalize_ten_scale(value):
    """Compatibility alias for score inputs that may use a 0-10 scale."""
    return normalize_score(value)


def map_pain_response_score(pain_level):
    """Convert a 0-10 discomfort response into a higher-is-better score."""
    return clamp(100 - (clamp(pain_level, 0, 10) * 10))


def calculate_qs(
    *args,
    form_accuracy=None,
    discomfort_response=None,
    rpe=None,
    qc_score=None,
    form=None,
    rep=None,
    rest=None,
    pain_level=None,
):
    """Calculate QS for legacy and current-MVP input shapes."""
    if args:
        if len(args) != 4:
            raise TypeError('calculate_qs() positional usage requires four values')
        form_accuracy, rep_score, rest_score, pain_response = args
    elif form is not None or rep is not None or rest is not None or pain_level is not None:
        form_accuracy = form if form is not None else form_accuracy
        rep_score = rep if rep is not None else 0
        rest_score = rest if rest is not None else 0
        pain_response = pain_level if pain_level is not None else 0
    else:
        discomfort_score = map_pain_response_score(discomfort_response or 0)
        rpe_score = 100 - (abs(clamp(rpe or 0, 0, 10) - 7) * 10)
        score = (
            normalize_score(form_accuracy or 0) * 0.4
            + discomfort_score * 0.3
            + rpe_score * 0.2
            + normalize_score(qc_score or 0) * 0.1
        )
        return round(clamp(score), 1)

    score = (
        normalize_score(form_accuracy or 0) * 0.4
        + normalize_score(rep_score) * 0.3
        + normalize_score(rest_score) * 0.2
        + map_pain_response_score(pain_response) * 0.1
    )
    return round(clamp(score), 1)


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
