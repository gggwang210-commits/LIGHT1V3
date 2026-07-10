# LIGHT ONE Dashboard Strategy

LIGHT ONE의 대시보드는 비의료 PT 상담 리포트 SaaS와 프리미엄 컨디셔닝 운영 시스템을 상용화하기 위한 역할 기반 제품 구조입니다. 목표는 회원의 운동 기록, 컨디션 기록, 체형 변화, 인바디 수치, 생활패턴 기록을 이해하기 쉬운 상담 경험으로 전환하고, 트레이너의 세션 운영과 리포트 검토를 표준화하며, 센터 관리자가 운영·매출·리텐션 지표를 안전하게 관리하도록 돕는 것입니다.

사업 방향의 상위 기준은 [`business_direction.md`](business_direction.md)를 따른다. 즉, 첫 번째 제품은 트레이너와 회원 사이의 기록, 분석, 피드백, 리포트, 소통을 하나로 묶는 컨디셔닝 대시보드 SaaS다.

## Product principles

1. **Human-in-the-Loop first**: AI-assisted consultation support는 초안과 요약을 돕지만 최종 커뮤니케이션은 트레이너 검토를 거칩니다.
2. **Non-medical boundary**: 진단, 치료, 처방, 통증 원인 확정, 질병 위험 예측을 하지 않습니다.
3. **Explainable wellness records**: QS/JATC, 통증 반응, 자세 참고 지표는 상담 참고용 변화 기록으로 설명합니다.
4. **Trainer-member feedback loop**: 회원 입력, 트레이너 검토, 피드백 발송, 다음 세션 계획을 하나의 흐름으로 연결합니다.
5. **Condition-aware coaching**: 수면, 생활패턴, RPE, 통증 반응, 인바디, 체형 참고 기록은 운동 강도 조절과 컨디셔닝 제안의 참고 자료로 사용합니다.
6. **Retention operating system**: 세션 기록, 피드백, 리포트, 예약, 결제를 재등록 상담 흐름으로 연결합니다.
7. **Synthetic-first portfolio**: 공개 저장소에는 합성 데이터와 정적 프로토타입만 포함합니다.

## Role-based architecture

| Role | Product surface | Core job | Success outcome |
|---|---|---|---|
| Member | Member App | 내 운동 기록, 컨디션, 체형 변화, 인바디 변화, 피드백, 예약/결제 이해 | 다음 행동이 명확하고 신뢰감 있는 상담 경험 |
| Trainer | Trainer Console | 운동·컨디션·측정값 변화 검토, 세션 기록, 리포트 초안 검토, 요청 응답 | 상담 준비 시간 절감과 일관된 커뮤니케이션 |
| Admin / Center Manager | Admin Console | 센터 운영, 트레이너, 회원, 리포트, 결제, 권한 관리 | 리텐션 기회와 운영 리스크를 조기에 파악 |

## Dashboard data domains

| Domain | Member value | Trainer value |
|---|---|---|
| Exercise log | 내가 수행한 운동과 진행 상황 확인 | 세트, 반복, 중량, RPE, 수행 메모 기반 세션 조절 |
| Condition log | 오늘 컨디션과 불편감 기록 | 운동 강도, 휴식, 다음 세션 주의사항 판단 참고 |
| Lifestyle and sleep | 수면·생활패턴이 컨디션과 연결되는지 이해 | 피로 누적, 회복 상태, 운동 강도 조절 참고 |
| InBody metrics | 체성분 변화 확인 | 체중, 골격근량, 체지방률 변화 설명과 상담 자료 |
| Posture and body reference | 체형·자세 변화 리포트 확인 | 촬영 QC와 변화 비교 기반 피드백 작성 |
| Communication | 트레이너 피드백과 답변 확인 | 회원 질문, 피드백 이력, 다음 과제 관리 |

## Commercialization-ready MVP scope

- Documentation: screen blueprint, IA, component library, data model, safety copy rules.
- Static prototype: dependency-free HTML/CSS/JS screens using synthetic data.
- Sample data: enough JSON to render dashboard cards and test data shape.
- Tests: repository-level checks for docs, sample data, README links, prototype presence.

## Safety boundary

LIGHT ONE is **not** a medical diagnosis, treatment, prescription, rehabilitation prescription, pain cause determination, disease prediction, or clinical decision support product. Dashboard language must use safe alternatives such as pain response record, caution signal, conditioning program suggestion, trainer review, and non-medical wellness reference report.
