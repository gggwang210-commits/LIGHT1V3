# LIGHT ONE 최종 포트폴리오 요약

## 1. 프로젝트 한 줄 소개

LIGHT ONE은 PT 상담 리포트에 사용되는 촬영 데이터가 비교 가능한 조건인지 확인하기 위해 카메라, 조명, 촬영 구도, 바닥 기준 마커를 수치화하고 PASS/CHECK/FAIL로 분류하는 품질 검증 MVP입니다.

## 2. 문제 정의

PT 현장에서 회원의 체형 변화나 운동 상담 기록을 비교하려면 촬영 조건이 일정해야 합니다. 하지만 실제 현장에서는 카메라 위치, 조명 밝기, 배경, 피험자 위치, 바닥 기준점이 매번 달라질 수 있습니다.

촬영 조건이 흔들리면 같은 회원이라도 전후 비교 결과가 달라 보일 수 있습니다. LIGHT ONE은 이 문제를 줄이기 위해 분석 전에 촬영 품질을 먼저 확인하는 구조로 설계되었습니다.

## 3. 현재 구현한 것

| 구분         | 구현 내용                                |
| ---------- | ------------------------------------ |
| 카메라 캘리브레이션 | 체커보드 기반 카메라 보정과 재투영 오차 계산            |
| 조명 정규화     | 화이트밸런스, 평균 밝기 정규화, 조명 균일도 계산         |
| 촬영 부스 QC   | 피험자 구도, 배경, 바닥 기준 마커 확인              |
| 통합 데모      | demo_pipeline.py로 카메라·조명·QC 결과 통합 실행 |
| 테스트        | 합성 데이터 기반 테스트 20개 통과                 |
| 문서화        | 기술 구조, 사업계획 근거, 체크리스트, 데모 리포트 샘플 정리  |

## 4. 실행 방법

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python demo_pipeline.py
grep -nE '(/workspaces|C:\\Users|C:/Users)' demo_result.json || echo "OK: no local absolute paths"
```

## 5. 실행 결과 요약

최종 검증 기준은 다음과 같습니다.

```text
Ran 20 tests
OK
```

```text
[P1] 카메라 캘리브레이션 / 재투영 오차: PASS
[P2] 조명 정규화 / 균일도 검사: PASS
[P3] 촬영 부스 QC 게이트: PASS
결과 JSON 저장: demo_result.json
OK: no local absolute paths
```

위 결과는 합성 데이터 기반 데모 결과입니다. 실제 센터 성능 수치가 아니라, 코드가 품질 지표를 계산하고 PASS/CHECK/FAIL로 분류할 수 있음을 보여주는 실행 증거입니다.

## 6. GitHub에서 확인할 핵심 파일

| 파일                                | 역할                    |
| --------------------------------- | --------------------- |
| README.md                         | 프로젝트 소개, 실행 방법, 문서 링크 |
| demo_pipeline.py                  | 카메라·조명·QC 통합 데모       |
| demo_result.json                  | 통합 데모 결과 JSON         |
| docs/architecture.md              | 기술 구조 요약              |
| docs/business-plan-evidence.md    | 사업계획서용 기술 근거          |
| docs/portfolio-checklist.md       | 제출 전 점검표              |
| docs/demo-report-sample-basic.md  | Basic 상담 리포트 샘플       |
| docs/demo-report-sample-review.md | Review 상담 리포트 샘플      |
| docs/demo-report-sample-retake.md | Retake 상담 리포트 샘플      |
| docs/safety-policy.md             | 안전·개인정보·비의료 경계        |
| docs/roadmap.md                   | 향후 개발 계획              |

## 7. 안전 및 개인정보 경계

LIGHT ONE은 의료 진단, 치료 판단, 재활 처방, 질환 위험도 예측을 제공하지 않습니다.

현재 저장소에는 실제 회원 이미지, 얼굴 이미지, 민감 건강정보, API Key, .env 파일, DB 접속정보를 포함하지 않습니다.

사용 가능한 표현은 운동상담 참고용, 자세 체크, 체형 관찰 리포트, 촬영 품질 확인, 측정 신뢰도 보조, 트레이너 검토 필요 항목, 재촬영 권고입니다.

피해야 할 표현은 진단, 치료, 재활, 처방, 질환 위험도 예측, 통증 위험도 예측, 의료기기, 의료 AI입니다.

## 8. 발표용 30초 설명

LIGHT ONE은 PT 현장에서 상담 리포트에 사용되는 촬영 데이터가 비교 가능한 조건인지 먼저 확인하는 품질 검증 MVP입니다. 카메라 재투영 오차, 조명 균일도, 그림자 비율, 피험자 구도, 배경 통제, 바닥 기준 마커 검출 여부를 계산하고 PASS/CHECK/FAIL로 분류합니다. 현재는 합성 데이터 기반 통합 데모와 테스트 20개를 통해 실행 가능성을 확인했으며, 의료 진단이나 처방이 아니라 트레이너의 운동상담을 보조하는 비의료 참고 도구로 설계했습니다.

## 9. 다음 보완 과제

1. 실제 센터 촬영 SOP 문서화
2. 실제 센터 체커보드·그레이카드 촬영 데이터 수집
3. 운영자별 QC 통과율 기록
4. PT 인터뷰 질문지 작성
5. 파일럿 의향서 LOI 초안 작성
6. 규칙 기반 상담 리포트 생성기 설계
7. MediaPipe 또는 OpenPose 실험은 별도 브랜치에서 분리 진행
