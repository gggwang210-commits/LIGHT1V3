# LIGHT ONE Dashboard Strategy

LIGHT ONE의 대시보드는 비의료 PT 상담 리포트 SaaS와 프리미엄 컨디셔닝 운영 시스템을 상용화하기 위한 역할 기반 제품 구조입니다. 목표는 회원의 변화 기록을 이해하기 쉬운 상담 경험으로 전환하고, 트레이너의 세션 운영과 리포트 검토를 표준화하며, 센터 관리자가 운영·매출·리텐션 지표를 안전하게 관리하도록 돕는 것입니다.

## Product principles

1. **Human-in-the-Loop first**: AI-assisted consultation support는 초안과 요약을 돕지만 최종 커뮤니케이션은 트레이너 검토를 거칩니다.
2. **Non-medical boundary**: 진단, 치료, 처방, 통증 원인 확정, 질병 위험 예측을 하지 않습니다.
3. **Explainable wellness records**: QS/JATC, 통증 반응, 자세 참고 지표는 상담 참고용 변화 기록으로 설명합니다.
4. **Retention operating system**: 세션 기록, 피드백, 리포트, 예약, 결제를 재등록 상담 흐름으로 연결합니다.
5. **Synthetic-first portfolio**: 공개 저장소에는 합성 데이터와 정적 프로토타입만 포함합니다.

## Role-based architecture

| Role | Product surface | Core job | Success outcome |
|---|---|---|---|
| Member | Member App | 내 컨디션, 변화, 피드백, 예약/결제 이해 | 다음 행동이 명확하고 신뢰감 있는 상담 경험 |
| Trainer | Trainer Console | 변화 검토, 세션 기록, 리포트 초안 검토, 요청 응답 | 상담 준비 시간 절감과 일관된 커뮤니케이션 |
| Admin / Center Manager | Admin Console | 센터 운영, 트레이너, 회원, 리포트, 결제, 권한 관리 | 리텐션 기회와 운영 리스크를 조기에 파악 |

## Commercialization-ready MVP scope

- Documentation: screen blueprint, IA, component library, data model, safety copy rules.
- Static prototype: dependency-free HTML/CSS/JS screens using synthetic data.
- Sample data: enough JSON to render dashboard cards and test data shape.
- Tests: repository-level checks for docs, sample data, README links, prototype presence.

## Safety boundary

LIGHT ONE is **not** a medical diagnosis, treatment, prescription, rehabilitation prescription, pain cause determination, disease prediction, or clinical decision support product. Dashboard language must use safe alternatives such as pain response record, caution signal, conditioning program suggestion, trainer review, and non-medical wellness reference report.
