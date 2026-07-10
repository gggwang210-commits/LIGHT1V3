# QS/JATC 엔진 명세

본 자료는 비의료 운동상담 참고용이며, 의료 진단·치료·처방 목적이 아닙니다. 모든 판단은 담당 트레이너가 검토합니다.

## 1. 파일 위치

엔진 파일은 다음 위치에 있습니다.

```text
lightone_v2_django/lightone/engines.py
```

기존 호환을 위해 `lightone/algorithms.py`는 `engines.py`를 다시 내보내는 wrapper로 유지합니다.

## 2. 핵심 함수

- `calculate_qs_score(data: QsInput)`
- `route_jatc(qs_score, pain_flag=False)`
- `build_report_summary(qs_score, route)`
- `calculate_qs(form_accuracy, discomfort_response, rpe, qc_score=100)`
- `calculate_jatc(qs_score, form_accuracy, discomfort_response, rpe)`
- `route_session(qs_score, jatc_score, discomfort_response, qc_status="PASS")`

## 3. 상태 정의

- `READY`: 참고값 기준 진행 가능
- `CAUTION`: 트레이너 확인 필요
- `BLOCK`: 트레이너 검토 전 진행 보류

Django 화면은 기존 데이터 모델 호환을 위해 `AUTO`, `REVIEW`, `BLOCK`을 사용합니다.

## 4. 검증 기준

- 모든 입력값은 범위 검증을 거칩니다.
- QS/JATC는 의료 판단값으로 설명하지 않습니다.
- 가중치와 임계값은 MVP 데모용 내부 초안입니다.
- 파일럿 데이터 확보 전 정확도나 효과를 단정하지 않습니다.

## 5. [확인필요]

[확인필요] QS/JATC 가중치와 라우팅 임계값은 실제 파일럿 데이터와 전문가 검토 후 조정해야 합니다.
