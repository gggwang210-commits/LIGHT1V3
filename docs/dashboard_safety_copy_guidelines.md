# 대시보드 안전 문구 가이드라인

LIGHTONE V2 대시보드는 **비의료 웰니스·운동 상담 지원 서비스**의 화면입니다. 모든 화면 문구는 운동 기록, 통증 반응, 촬영 품질, 트레이너 메모를 구조화하고 트레이너 검토를 돕는 범위 안에서 작성해야 합니다. 의료 진단, 치료, 재활 치료, 질병 예측, 통증 원인 확정, AI 단독 판단처럼 오해될 수 있는 표현은 사용하지 않습니다.

## 1. 금지 표현 목록

아래 표현은 버튼, 카드 제목, 배지, 토스트, 모달, 리포트, 관리자 콘솔, 도움말, 마케팅성 대시보드 문구에 사용하지 않습니다. 영어 UI를 병행하는 경우 영어 금지 표현도 동일하게 제한합니다.

| 구분 | 한국어 금지 표현 | English prohibited copy | 금지 사유 |
|---|---|---|---|
| 진단 | 진단, AI 진단, 자세 진단, 통증 진단 | diagnosis, AI diagnosis, posture diagnosis, pain diagnosis | 의료 진단 또는 임상 판단으로 오해될 수 있음 |
| 치료 | 치료, 치료 효과, 치료 계획, 치료 추천 | treatment, therapeutic effect, treatment plan, treatment recommendation | 의료적 치료 제공 또는 효과 주장으로 오해될 수 있음 |
| 처방 | 처방, 운동 처방, 자동 처방, AI 처방 | prescription, exercise prescription, automated prescription, AI prescription | 의학적 처방 또는 자동 의사결정으로 오해될 수 있음 |
| 재활 치료 | 재활 치료, 재활 처방, 재활 진단 | rehabilitation treatment, rehab prescription, rehab diagnosis | 의료·재활 치료 영역으로 오해될 수 있음 |
| 통증 원인 확정 | 통증 원인 분석, 통증 원인 판정, 원인을 찾았습니다 | pain cause analysis, cause detected, root cause identified | 의학적 인과관계 판단으로 오해될 수 있음 |
| 질병·손상 예측 | 질병 위험도, 부상 위험 예측, 손상 판정 | disease risk, injury risk prediction, injury detected | 질병·손상 예측 또는 판정으로 오해될 수 있음 |
| 효과 보장 | 완치, 개선 보장, 통증 제거, 부상 예방 보장 | cure, guaranteed improvement, pain elimination, guaranteed injury prevention | 결과 보장 또는 치료 효과 주장으로 오해될 수 있음 |
| AI 최종 판단 | AI가 판단했습니다, AI가 결정했습니다, 자동 승인 | AI decided, AI determined, automatically approved | Human-in-the-loop 원칙과 충돌할 수 있음 |
| 환자 지칭 | 환자, 증상자, 질환자 | patient, symptomatic patient, diseased user | 의료 서비스 맥락으로 오해될 수 있음 |
| 의료 수준 주장 | 의료 수준 분석, 임상급 분석, 병원급 리포트 | medical-grade analysis, clinical-grade analysis, hospital-grade report | 의료기기 또는 임상 서비스로 오해될 수 있음 |

> 주의: **“AI가 통증 원인을 분석했습니다.”**는 금지 예시로만 사용할 수 있습니다. 실제 제품 화면, 도움말, 리포트, 영업 자료에서는 제품 주장으로 사용하지 않습니다.

## 2. 안전 대체 표현

| 위험 표현 | 안전 대체 표현 | English safe alternative | 사용 맥락 |
|---|---|---|---|
| 진단 | 기록, 확인, 상담 참고 | record, check, coaching reference | 상태 카드, 요약 리포트 |
| AI 진단 결과 | AI 보조 요약, 시스템 참고 요약 | AI-assisted summary, system-generated reference summary | 대시보드 요약 영역 |
| 치료 | 관리, 컨디셔닝, 운동 상담 | care support, conditioning, exercise coaching | 회원 안내, 트레이너 메모 |
| 처방 | 운동 제안, 프로그램 조정 제안 | exercise suggestion, program adjustment suggestion | 루틴 조정, 다음 세션 제안 |
| 재활 | 컨디셔닝, 회복 지원 운동 상담 | conditioning, recovery-support coaching | 운동 상담 플랜 |
| 통증 원인 분석 | 통증 반응 기록, 불편감 응답 요약 | pain response record, discomfort response summary | 문진·세션 후 피드백 |
| 통증 원인 판정 | 트레이너 확인 필요 신호 | trainer review signal | REVIEW 배지, 알림 |
| 위험도 판정 | 주의 신호, 검토 우선순위 | caution signal, review priority | 관리자·트레이너 큐 |
| 부상 위험 예측 | 운동 중 주의가 필요한 패턴 | pattern requiring attention during exercise | 세션 준비 카드 |
| AI가 판단 | 트레이너 검토를 돕는 참고 정보 | reference information for trainer review | 모든 역할 공통 |
| 자동 승인 | 트레이너 확인 후 전달 가능 | ready for trainer confirmation | AUTO 상태 설명 |
| 환자 | 회원, 사용자, 고객 | member, user, client | 회원용·트레이너용 화면 |
| 병원급 리포트 | 비의료 웰니스 참고 리포트 | non-medical wellness reference report | 리포트 제목·footer |

## 3. 역할별 화면 문구 작성 규칙

### 3.1 회원용 화면

회원용 화면은 불안감을 높이거나 자가진단을 유도하지 않는 문구를 사용합니다.

- 회원에게 보이는 문구는 “현재 기록”, “운동 중 반응”, “트레이너와 확인할 내용” 중심으로 작성합니다.
- 통증, 불편감, 피로도는 원인·질환·손상으로 연결하지 않고 사용자가 입력한 반응 또는 세션 관찰 기록으로 표현합니다.
- AI 또는 시스템은 최종 판단자가 아니라 트레이너 상담 전 참고 요약을 제공하는 도구로 설명합니다.
- `REVIEW` 또는 `BLOCK`에 해당하는 경우 공포감을 주는 표현 대신 “트레이너 확인 필요”, “세션을 잠시 중단하고 확인”처럼 행동 안내 중심으로 작성합니다.
- 회원용 리포트에는 “필요 시 의료 전문가와 상담하세요”라는 안내를 포함할 수 있으나, 특정 질병·손상 가능성을 단정하지 않습니다.

### 3.2 트레이너용 화면

트레이너용 화면은 Human-in-the-Loop 검토를 전제로, 상담 우선순위와 확인 항목을 명확히 전달합니다.

- 카드와 알림은 “검토 필요”, “확인 항목”, “주의 신호”, “입력 품질 확인”처럼 운영 가능한 문구로 작성합니다.
- 트레이너가 회원에게 전달하기 전 최종 검토해야 한다는 문구를 리포트 생성·전송 플로우에 표시합니다.
- `AUTO`는 자동 확정이 아니라 “트레이너 확인 후 전달 가능” 상태로 설명합니다.
- `REVIEW`는 통증 반응, RPE, 촬영 품질, 메모 불일치 등 검토 이유를 비의료적으로 설명합니다.
- `BLOCK`은 세션 중단 권고 신호이며 의료 진단이 아님을 명시하고, 필요 시 의료 전문가 상담 안내를 제공합니다.

### 3.3 관리자용 화면

관리자용 화면은 서비스 안전성, 운영 품질, 권한 관리, 감사 가능성을 중심으로 작성합니다.

- 관리자 지표는 진단·치료 성과가 아니라 상담 처리 현황, 검토 큐, 데이터 품질, 라우팅 분포, 권한 변경 이력 중심으로 표시합니다.
- 센터·트레이너 성과 문구는 “치료 성공률”, “통증 개선률 보장”처럼 의료 효과로 해석될 수 있는 표현을 사용하지 않습니다.
- 관리자 설정에는 금지어 검수, 리포트 footer 면책 문구, 권한별 노출 범위, 데이터 보관·삭제 기준을 포함합니다.
- 운영 로그와 감사 화면은 실제 회원의 민감정보를 불필요하게 노출하지 않고, 가능한 경우 비식별 ID와 요약 상태를 사용합니다.
- 외부 제출·영업용 대시보드 캡처에는 비의료 서비스 경계와 검증 전 수치 표시 원칙을 유지합니다.

## 4. Unsafe/Safe 예시

| 화면 위치 | Unsafe copy | Safe copy | 비고 |
|---|---|---|---|
| 회원 요약 카드 | AI가 통증 원인을 분석했습니다. | 입력된 통증 반응을 요약했습니다. 트레이너와 함께 확인하세요. | 금지 예시는 제품 주장으로 사용 금지 |
| 회원 알림 | 부상 위험이 높습니다. | 운동 중 주의가 필요한 반응이 기록되었습니다. | 위험 예측 대신 주의 신호로 표현 |
| 트레이너 큐 | AI가 운동 처방을 완료했습니다. | 프로그램 조정 제안이 생성되었습니다. 전달 전 확인하세요. | 자동 처방 금지 |
| 트레이너 리포트 | 자세 진단 결과: 골반 이상 | 자세 관찰 메모: 좌우 움직임 차이가 기록되었습니다. | 진단·이상 단정 금지 |
| 관리자 통계 | 통증 치료 성공률 85% | 세션 후 불편감 응답 감소 사례 비율 85% [검증필요] | 효과 보장 금지, 검증 상태 표시 |
| 라우팅 배지 | BLOCK: 손상 의심 | BLOCK: 세션 중단 후 트레이너 확인 필요 | 손상 의심 단정 금지 |
| 리포트 제목 | 병원급 AI 분석 리포트 | 비의료 웰니스 상담 참고 리포트 | 의료 수준 주장 금지 |
| CTA 버튼 | AI 진단 받기 | 운동 기록 확인하기 | 진단 유도 금지 |

## 5. 대시보드 footer 비의료 면책 문구

모든 회원용, 트레이너용, 관리자용 대시보드 footer에는 아래 문구를 기본으로 표시합니다. 공간이 제한된 모바일 화면에서는 짧은 버전을 사용하고, “자세히” 링크 또는 도움말 모달에서 기본 문구 전문을 제공합니다.

### 기본 문구

> LIGHTONE V2는 비의료 웰니스·운동 상담 지원 서비스입니다. 본 화면의 기록, 요약, 라우팅 정보는 의료 진단, 치료, 재활 치료, 질병·손상 예측, 통증 원인 확정을 목적으로 하지 않으며, 트레이너 검토를 돕기 위한 참고 정보입니다. 통증이 지속되거나 건강상 우려가 있는 경우 의료 전문가와 상담하세요.

### 짧은 문구

> 비의료 웰니스 참고 정보입니다. 진단·치료·통증 원인 확정이 아니며, 필요 시 의료 전문가와 상담하세요.

### English reference copy

> LIGHTONE V2 is a non-medical wellness and exercise coaching support service. Records, summaries, and routing information shown here are for trainer review only and are not intended for medical diagnosis, treatment, rehabilitation treatment, disease or injury prediction, or confirmation of pain causes. If pain persists or you have health concerns, consult a qualified medical professional.

## 6. 배포 전 검수 체크리스트

- [ ] 금지 표현이 카드, 버튼, 배지, 토스트, 모달, 리포트, footer에 포함되지 않았는가?
- [ ] 통증 관련 문구가 원인 확정이 아니라 반응 기록 또는 트레이너 확인 항목으로 표현되었는가?
- [ ] `AUTO`, `REVIEW`, `BLOCK` 라우팅이 의료 판단이 아니라 검토 우선순위로 설명되었는가?
- [ ] 회원용 화면이 불안·자가진단을 유도하지 않는가?
- [ ] 트레이너용 화면이 전달 전 최종 검토 책임을 명확히 표시하는가?
- [ ] 관리자용 화면이 치료 성과나 임상 효과를 주장하지 않는가?
- [ ] 모든 대시보드 footer에 비의료 면책 문구가 포함되었는가?
