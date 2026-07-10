# Step 1 데이터 모델

LIGHT ONE Step 1은 PT 상담 흐름을 회원 단위로 기록하고, 세션별 운동 반응을 구조화하며, QS/JATC 같은 참고 지표를 분리해 관리하기 위한 최소 데이터 구조입니다.

## 모델 목적

| 모델 | 목적 |
|------|------|
| `MemberSession` | 회원별 운동 상담/운동 세션의 목표, 불편감 반응, RPE, QC 상태, 메모를 기록합니다. |
| `Indicator Snapshot` | `MemberSession`에 저장된 QS, JATC, Breakdown, route 값을 상담 참고 지표로 사용합니다. |
| `StrategyItem` | MVP 사업·운영 우선순위 항목을 대시보드에 표시하기 위한 내부 관리 데이터입니다. |

## 비의료 참고 원칙

- QS/JATC는 의료 진단, 치료, 처방을 위한 기준이 아니라 운동 상담 참고 지표입니다.
- `AUTO`, `REVIEW`, `BLOCK` 라우팅은 트레이너의 세션 운영 판단을 보조하는 안전 신호입니다.
- 최종 판단과 회원 안내는 트레이너가 검토합니다.

## 개인정보 최소화 원칙

- fixture와 데모 데이터는 실제 회원 정보가 아닌 synthetic 데이터를 사용합니다.
- 이름, 연락처, 이메일, 주소 등 직접 식별정보는 운영 전 제거하거나 비식별 코드로 대체해야 합니다.
- 새 기능은 `member_id` 또는 비식별 코드 기반으로 설계합니다.

## 검증 명령

```bash
cd lightone_v2_django
python manage.py check
python manage.py test lightone.tests.test_qs --verbosity 2
```
