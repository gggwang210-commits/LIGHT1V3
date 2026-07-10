# Admin / Center Manager Dashboard Specification

## A. Purpose

The admin dashboard should help center owners/managers:
- monitor center operations
- manage trainers
- manage members
- track report usage
- monitor reservations and payments
- identify retention and re-registration opportunities
- monitor communication quality
- manage privacy and access permissions

## B. Core sections

| Section | Purpose | Main action |
|---|---|---|
| Center Overview | 운영 핵심 지표 요약 | 오늘 현황 확인 |
| Trainer Performance | 세션, 응답, 리포트 처리 현황 | 업무 균형 조정 |
| Member Status | 활성/휴면/만료 임박 회원 | 회원 상세 확인 |
| Report Generation Metrics | 리포트 초안, 검토, 발송률 | 누락 관리 |
| Reservation Calendar | 전체 예약과 취소/변경 현황 | 예약 조정 |
| Payment Overview | 결제 예정, 미납, 이용권 잔여 | 결제 이슈 처리 |
| Re-registration Pipeline | 재등록 후보와 상담 상태 | 상담 배정 |
| Risk / Review Queue | REVIEW/BLOCK 수와 처리 상태 | 안전 큐 점검 |
| Communication Monitoring | 응답 시간과 미응답 요청 | 커뮤니케이션 품질 확인 |
| Feedback & Complaints | 회원 만족도와 불만 접수 | 후속 조치 지정 |
| Permission Management | 역할 기반 권한 관리 | 접근 권한 변경 |
| SaaS Plan / Billing | 센터 구독 플랜과 사용량 | 플랜 확인 |
| Data Export / Audit Log | 비민감 요약 내보내기와 접근 로그 | 감사 로그 확인 |

## C. Admin KPIs

| KPI | Definition | Safe interpretation |
|---|---|---|
| active members | 최근 30일 세션 또는 리포트 기록이 있는 회원 수 | 운영 활성도 |
| upcoming sessions | 향후 7일 예약 세션 수 | 수요 예측 |
| completed sessions | 기간 내 완료 세션 수 | 트레이너 업무량 |
| report generation rate | 완료 세션 대비 리포트 생성 비율 | 상담 운영 품질 |
| REVIEW/BLOCK count | 검토 또는 중단 안내 신호 수 | 안전 검토 필요량 |
| re-registration candidates | 이용권 만료 임박 또는 상담 타이밍 회원 | 리텐션 기회 |
| trainer response time | 회원 요청 평균 응답 시간 | 커뮤니케이션 품질 |
| member satisfaction score | 세션 후 만족도 설문 평균 | 서비스 경험 참고 |
| unpaid payments | 결제 예정일 초과 건수 | 운영 이슈 |
| churn risk members | 방문 감소·피드백 미확인 등 운영 기반 이탈 가능 회원 | 재접점 후보 |

## D. Admin safety controls

- role-based access: Member, Trainer, AdminUser 권한 분리.
- sensitive data access log: 고/중 민감도 데이터 접근 기록 생성.
- media storage control: 촬영 파일은 공개 저장소에 저장하지 않으며 접근 만료 정책 적용.
- data deletion request workflow: 삭제 요청 접수, 검토, 처리, 감사 로그 기록.
- consent status monitoring: 동의 철회·만료 상태를 관리자 대시보드에 표시.
- no real personal data in public GitHub: 공개 저장소에는 합성 데이터만 포함.
