# LIGHT ONE V2

> 비의료 PT 상담 리포트 SaaS MVP  
> 작성 기준일: 2026-07-09

본 자료는 비의료 운동상담 참고용이며, 의료 진단·치료·처방 목적이 아닙니다. 모든 판단은 담당 트레이너가 검토합니다.

LIGHT ONE V2는 PT샵·헬스장·필라테스 센터가 회원의 운동 수행 기록, 통증 반응 참고값, RPE, 촬영 QC, 트레이너 메모를 구조화해 상담 리포트 초안을 만드는 Django 기반 MVP입니다.

이 프로젝트는 의료 서비스가 아닙니다. AI 또는 점수 계산 로직은 트레이너의 판단을 대체하지 않으며, 회원에게 전달되는 모든 리포트는 담당 트레이너가 검토해야 합니다.

## 1. 프로젝트 개요

LIGHT ONE V2의 목적은 트레이너가 흩어진 운동상담 기록을 정리하고, 재등록 상담이나 컨디셔닝 안내에 활용할 수 있는 설명 가능한 리포트 초안을 만드는 것입니다.

핵심 사용자는 센터 대표와 트레이너입니다. 회원은 트레이너가 검토한 상담 자료를 통해 자신의 운동 반응과 수행 흐름을 이해합니다.

## 2. 비의료 서비스 경계

LIGHT ONE V2는 다음을 제공하지 않습니다.

- 의료 진단
- 치료 또는 재활 치료
- 의학적 처방
- 질환 위험도 판단
- 통증 원인 확정
- AI 단독 판단

LIGHT ONE V2가 제공하는 것은 비의료 운동상담 참고 자료입니다. 자세한 기준은 `docs/governance/non-medical-boundary.md`를 확인하세요.

## 3. 현재 구현 범위

현재 ZIP에는 다음 구현이 포함되어 있습니다.

- Django MVP 앱: `lightone_v2_django/`
- 회원 세션 입력 폼
- 트레이너 대시보드
- 상담 리포트 상세 화면
- QS/JATC 참고 엔진: `lightone_v2_django/lightone/engines.py`
- 합성 데이터 생성 명령
- 비의료 안전 문구 테스트
- 개인정보·배포 전 체크리스트
- 파일럿 검증 문서

현재 상태는 상용 배포 직전이 아니라, 파일럿 센터 1곳에서 검증 가능한 MVP 데모 버전입니다.

## 4. 빠른 실행 방법

```bash
cd lightone_v2_django
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_synthetic_data --reset
python manage.py runserver
```

브라우저에서 다음 주소를 엽니다.

```text
http://127.0.0.1:8000/
```

로그인이 필요한 경우 관리자 계정 또는 테스트 계정을 별도로 생성해야 합니다.

```bash
python manage.py createsuperuser
```

## 5. 테스트 방법

```bash
cd lightone_v2_django
python manage.py check
python manage.py test
pytest
```

현재 작업 환경에서는 Django 패키지가 설치되어 있지 않아 `python manage.py check`와 `python manage.py test`를 실제 통과로 확정하지 못했습니다. 명령 실행 결과와 미확인 항목은 `PROJECT_AUDIT.md`에 기록했습니다.

## 6. 대시보드 구조

대시보드는 다음 정보를 보여줍니다.

- 전체 세션 수
- QS 평균 참고값
- JATC 평균 참고값
- AUTO / REVIEW / BLOCK 분포
- 통증 반응 참고, 자세 품질, RPE, 촬영 QC 보조 지표
- 최근 상담 리포트 목록
- 파일럿 실행 우선순위

`BLOCK`은 의료 주의 필요 상태이 아닙니다. 트레이너 검토 전 진행 보류 상태를 의미합니다.

## 7. QS/JATC 엔진 개요

QS/JATC 엔진은 `lightone_v2_django/lightone/engines.py`에 있습니다.

핵심 함수는 다음과 같습니다.

- `calculate_qs_score`
- `route_jatc`
- `calculate_qs`
- `calculate_jatc`
- `route_session`
- `build_report_summary`

QS/JATC 기준은 MVP 데모용 내부 초안입니다. 파일럿 데이터와 전문가 검토 후 조정해야 합니다.

## 8. 합성 데이터 원칙

샘플 데이터는 실제 회원·고객·회원/고객·트레이너의 개인정보 또는 건강정보를 포함하지 않는 합성 데이터여야 합니다.

합성 데이터 생성 명령은 다음과 같습니다.

```bash
python manage.py seed_synthetic_data --reset
```

자세한 기준은 `sample_data/README.md`를 확인하세요.

## 9. 파일럿 검증 계획

추천 파일럿 순서는 다음과 같습니다.

1. 트레이너 1~2명에게 샘플 리포트 설명 가능성 검토를 받습니다.
2. 실제 센터 1곳에서 세션 기록 입력 시간을 측정합니다.
3. 회원 상담에서 리포트 이해도와 재방문 의사를 확인합니다.
4. 가격 지불의사와 월 구독 가능성을 검증합니다.

자세한 문서는 `docs/product/pilot-checklist.md`와 `docs/validation/wtp-test-plan.md`를 확인하세요.

## 10. 배포 전 체크리스트

배포 전 최소 확인 항목은 다음과 같습니다.

- `DEBUG=False`
- 운영 `SECRET_KEY` 환경변수 주입
- `ALLOWED_HOSTS` 운영 도메인 제한
- HTTPS 적용
- 세션·CSRF 보안 쿠키 설정
- 실제 개인정보 수집 전 동의서 확인
- 고객 데이터 삭제 요청 프로세스 수립
- 파일럿 데이터와 운영 데이터 분리
- 의료·법률 전문가 문구 검토

자세한 문서는 `docs/governance/deployment-security-checklist.md`와 `docs/governance/privacy-checklist.md`를 확인하세요.

## 11. [확인필요] 항목

[확인필요] 의료·법률 전문가가 비의료 표현과 BLOCK 라우팅 문구를 최종 검토해야 합니다.

[확인필요] 개인정보 처리방침, 동의서, 데이터 삭제 절차는 실제 파일럿 전 공식 검토가 필요합니다.

[확인필요] QS/JATC 가중치와 임계값은 파일럿 데이터 확보 후 조정해야 합니다.

[확인필요] 가격, 과금 단위, 고객 지불의사는 트레이너 인터뷰와 파일럿 계약으로 검증해야 합니다.
