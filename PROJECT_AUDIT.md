# PROJECT_AUDIT

작성 기준일: 2026-07-09

본 자료는 비의료 운동상담 참고용이며, 의료 진단·치료·처방 목적이 아닙니다. 모든 판단은 담당 트레이너가 검토합니다.

## 1. 초기 상태

업로드 ZIP 파일은 `LightOne_V2-main/LightOne_V2-main/` 형태의 중첩 루트 구조를 가지고 있었습니다.

확인된 주요 구성은 다음과 같습니다.

- Django MVP: `lightone_v2_django/`
- 레거시 Django 프로젝트: `lightone_django_complete/`
- 중복 자산 폴더: `2/repo_lightoneV2/`
- 문서: `docs/`, `lightone_v2_django/docs/`, 루트 `README.md`
- 정적 자산: `assets/`, `lightone_v2_django/static/`
- 샘플 데이터: `sample_data/`
- 테스트: `tests/`, `lightone_v2_django/lightone/tests/`

초기 ZIP 크기는 약 74MB였습니다. 대용량 이미지와 영상 파일, 중복 대시보드 자산, 로컬 DB와 캐시 파일이 함께 포함되어 있었습니다.

## 2. 발견한 문제

- 루트 폴더가 한 번 더 중첩되어 있었습니다.
- `db.sqlite3`, `__pycache__`, `.pyc` 등 배포 ZIP에 부적절한 파일이 있었습니다.
- `yungsang.mp4` 등 대용량 원본 영상이 로그인 화면에 직접 연결되어 있었습니다.
- `2/repo_lightoneV2/`와 Django static 이미지 사이에 중복 대시보드 자산이 있었습니다.
- `lightone_django_complete/`는 현재 MVP와 중복되는 레거시 Django 구현이었습니다.
- 기존 `base.html`은 로그인 전용 구조라 Django 대시보드 템플릿의 block 구조와 맞지 않았습니다.
- `session_form.html`은 실제 `ModelForm`에 없는 필드를 렌더링하려 했습니다.
- QS/JATC 계산 로직은 있었지만 `engines.py`로 분리되어 있지 않았습니다.
- BLOCK 문구가 의료 판단처럼 오인될 수 있는 표현을 일부 포함했습니다.
- Chart.js CDN 실패 시 대체 안내가 없었습니다.
- GitHub workflow에 현재 MVP와 맞지 않는 publish workflow가 남아 있었습니다.

## 3. 수정한 항목

- 최종 루트 폴더를 `lightone-v2-mvp-nonmedical/`로 단일화했습니다.
- Django 앱은 `lightone_v2_django/`에 유지했습니다.
- `lightone/engines.py`를 추가하고 QS/JATC 순수 계산 로직을 정리했습니다.
- `lightone/algorithms.py`는 기존 import 호환 wrapper로 바꿨습니다.
- `calculate_qs_score`, `route_jatc`, `build_report_summary`를 추가했습니다.
- 기존 `calculate_qs`, `calculate_jatc`, `route_session` 호환 함수를 유지했습니다.
- `forms.py`의 중복 위젯과 미연결 필드 참조를 정리했습니다.
- `views.py`가 모든 주요 화면에 비의료 안전 문구를 전달하도록 수정했습니다.
- `base.html`을 일반 앱 레이아웃으로 재작성했습니다.
- dashboard, report, session, method 템플릿에 비의료 안전 문구와 안전한 BLOCK 설명을 반영했습니다.
- 로그인·회원가입 화면의 원본 영상 의존을 제거하고 정적 webp 배경으로 대체했습니다.
- Chart.js CDN 로드 실패 시 그래프 대신 안내 문구가 보이도록 fallback을 추가했습니다.
- `seed_synthetic_data.py` management command를 추가했습니다.
- `test_qs.py`, `test_jatc.py`, `test_non_medical_copy.py`를 보강했습니다.
- `README.md`, `docs/README.md`, governance, product, validation 문서를 새 구조로 정리했습니다.
- `.env.example`, `pytest.ini`, 배포 보안 체크리스트를 추가했습니다.
- PyPI publish workflow는 archive로 이동했습니다.
- 최종 ZIP에는 `.env`, `db.sqlite3`, 캐시, 원본 영상, 미참조 대용량 레거시 이미지를 포함하지 않도록 정리했습니다.

## 4. 삭제하지 않고 archive 처리한 항목

다음 항목은 최신 실행 기준에서 제외하고 archive 또는 manifest로 보관했습니다.

- 기존 루트 README: `docs/archive/legacy-docs/README.original.md`
- 기존 docs: `docs/archive/legacy-docs/`
- 기존 Django 내부 docs: `docs/archive/django-app-docs/`
- 기존 PyPI publish workflow: `docs/archive/github-workflows/python-publish.yml`
- 레거시 Django 구현: `docs/archive/legacy-django-complete/`
- 중복 V2 자산 폴더: `assets/archive/legacy_repo_lightoneV2/`
- 제외한 대용량 파일 목록: `assets/archive/large-files/`

대용량 바이너리는 최종 ZIP 용량과 배포 안전성을 위해 경로 manifest만 남기고 제외했습니다.

## 5. 테스트 결과

### 실행된 검증

- Python syntax compile: 통과
- 순수 QS/JATC 엔진 smoke test: 통과
- 금지 파일 스캔: 확인 필요
- 고위험 문구 스캔: 통과

### Django 명령 결과

현재 작업 환경에는 Django 패키지가 설치되어 있지 않아 Django 명령은 실행 불가였습니다.

`python manage.py check`

```text
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
Traceback (most recent call last):
  File "/mnt/data/lightone-v2-mvp-nonmedical/lightone_v2_django/manage.py", line 13, in <module>
    main()
    ~~~~^^
  File "/mnt/data/lightone-v2-mvp-nonmedical/lightone_v2_django/manage.py", line 8, in main
    from django.core.management import execute_from_command_line
ModuleNotFoundError: No module named 'django'
```

`python manage.py test`

```text
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
Traceback (most recent call last):
  File "/mnt/data/lightone-v2-mvp-nonmedical/lightone_v2_django/manage.py", line 13, in <module>
    main()
    ~~~~^^
  File "/mnt/data/lightone-v2-mvp-nonmedical/lightone_v2_django/manage.py", line 8, in main
    from django.core.management import execute_from_command_line
ModuleNotFoundError: No module named 'django'
```

`pytest`

```text
============================= test session starts ==============================
platform linux -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0
rootdir: /mnt/data/lightone-v2-mvp-nonmedical/lightone_v2_django
configfile: pytest.ini
testpaths: lightone/tests
plugins: cov-7.0.0, json-report-1.5.0, ddtrace-4.4.0, metadata-3.1.1, anyio-4.13.0, Faker-40.1.2, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 0 items / 3 errors

==================================== ERRORS ====================================
_________________ ERROR collecting lightone/tests/test_jatc.py _________________
ImportError while importing test module '/mnt/data/lightone-v2-mvp-nonmedical/lightone_v2_django/lightone/tests/test_jatc.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
lightone/tests/test_jatc.py:1: in <module>
    from django.test import TestCase
E   ModuleNotFoundError: No module named 'django'
___________ ERROR collecting lightone/tests/test_non_medical_copy.py ___________
ImportError while importing test module '/mnt/data/lightone-v2-mvp-nonmedical/lightone_v2_django/lightone/tests/test_non_medical_copy.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.13/importlib/__init__.py:88: in import_module
```

## 6. 비의료·개인정보 리스크 점검

- 모든 주요 화면에 비의료 안전 문구를 반영했습니다.
- BLOCK은 “의료 판단”이 아니라 “트레이너 검토 전 진행 보류”로 설명했습니다.
- `sample_data/README.md`에 합성 데이터 원칙을 명시했습니다.
- 최종 ZIP에서 `.env`, `db.sqlite3`, `.pyc`, `__pycache__`, 원본 동영상 파일을 제외했습니다.
- 실제 개인정보, API 키, 토큰, 비밀번호가 포함되지 않도록 스캔했습니다.

단, archive 문서는 레거시 보관본입니다. 최신 기준은 루트 README와 `docs/README.md`를 우선해야 합니다.

## 7. 남은 [확인필요]

[확인필요] 의료·법률 전문가가 비의료 표현, BLOCK 문구, 리포트 문구를 최종 검토해야 합니다.

[확인필요] 실제 파일럿 전 개인정보 처리방침, 동의서, 데이터 삭제 절차를 공식 검토해야 합니다.

[확인필요] Django 패키지가 설치된 로컬 또는 CI 환경에서 `python manage.py check`, `python manage.py test`, `pytest`를 재실행해야 합니다.

[확인필요] QS/JATC 가중치와 임계값은 파일럿 데이터와 전문가 검토 후 조정해야 합니다.

[확인필요] 가격, 과금 단위, 고객 지불의사는 파일럿 인터뷰로 검증해야 합니다.

## 8. 다음 추천 작업

1. 로컬 가상환경에서 `pip install -r lightone_v2_django/requirements.txt` 후 Django 테스트를 재실행합니다.
2. 트레이너 1~2명에게 샘플 리포트 설명 가능성과 입력 부담을 검증합니다.
3. 파일럿 센터 1곳을 선정해 개인정보 동의서와 비의료 안내 문구를 먼저 검토합니다.
4. QS/JATC 임계값은 실제 파일럿 데이터가 쌓인 뒤 조정합니다.

## 9. 최종 산출물 상태

- 최종 파일 수: 262개
- 최종 폴더 크기: 약 2.76MB
- 상용 배포 직전 상태: 아님
- 파일럿 검증 가능성: 있음
- 필수 공식 검토: 의료·법률·개인정보·배포 보안
