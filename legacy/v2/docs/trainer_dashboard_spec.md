# Trainer Dashboard Specification

## A. Purpose

The trainer dashboard should help trainers:
- review member changes
- detect caution signals
- prepare the next session
- generate reports
- respond to member requests
- manage re-registration timing
- maintain communication history

## B. Core sections

| Section | Purpose | Main action |
|---|---|---|
| Trainer Home | 오늘 업무, 검토 대기, 주요 알림 요약 | 우선순위 확인 |
| Today Sessions | 오늘 예약 회원과 세션 상태 | 세션 시작 |
| Member Change Timeline | 회원별 컨디션·통증 반응·피드백 변화 | 상세 검토 |
| QS/JATC Summary | 운동 상담 참고 점수와 라우팅 상태 | REVIEW 사유 확인 |
| Pain Response & RPE | 세션별 통증 반응과 주관적 운동 강도 | 기록 보완 |
| Exercise Performance Log | 운동, 세트, 반복, 난이도, 메모 | 수행 기록 입력 |
| AUTO/REVIEW/BLOCK Queue | 자동/검토/중단 권고 큐 | 안전 검토 처리 |
| Report Drafts | AI-assisted 초안과 트레이너 리뷰 상태 | 리포트 확정 |
| Member Requests | 회원 질문과 요청 | 답변 작성 |
| Feedback Inbox | 세션 후 피드백 작성/발송 | 피드백 보내기 |
| Next Session Plan | 다음 세션 주의사항과 과제 | 계획 저장 |
| Re-registration Candidates | 만료 임박, 변화 요약, 상담 타이밍 | 상담 준비 |
| Communication History | 회원과의 안내·피드백 기록 | 이력 확인 |

## C. Trainer workflow

### Before session
1. Today Sessions에서 회원을 선택합니다.
2. 이전 피드백, 최근 통증 반응 기록, REVIEW/BLOCK 여부를 확인합니다.
3. 다음 세션 주의사항과 컨디셔닝 과제를 확인합니다.

### During session
1. Exercise Performance Log에 운동명, 세트, 반복, 난이도, RPE를 입력합니다.
2. 통증 반응은 원인 판단이 아니라 “반응 기록”으로 입력합니다.
3. 특이사항은 트레이너 노트에 남깁니다.

### After session
1. Report Drafts에서 비의료 상담 리포트 초안을 생성합니다.
2. 트레이너 피드백을 추가하고 위험한 표현을 제거합니다.
3. Next Conditioning Actions를 배정합니다.

### Weekly review
1. Member Change Timeline에서 주간 변화를 비교합니다.
2. 재등록 상담에 사용할 설명 포인트를 정리합니다.
3. 리포트 생성률과 피드백 누락을 확인합니다.

### Risk review
1. REVIEW/BLOCK Queue에서 사유를 확인합니다.
2. BLOCK은 진단이 아니라 운동 중단·전문가 상담 권고가 필요한 caution signal로 안내합니다.
3. 회원에게 불안감을 주는 표현 없이 다음 안전 행동을 안내합니다.

## D. Solution planning structure

The trainer should not “prescribe treatment.” Instead, the system should support:
- 운동 난이도 조정
- 동작 범위 조정
- 휴식·회복 안내
- 다음 세션 주의사항
- 컨디셔닝 과제
- 병원 상담 권고가 필요한 red flag 안내 only as a caution, not diagnosis

## E. Sample trainer UI copy

- 카드: “오늘 REVIEW 3건: 통증 반응 또는 촬영 품질 확인이 필요합니다.”
- 버튼: “리포트 초안 검토”
- 버튼: “트레이너 피드백 추가”
- 버튼: “다음 세션 주의사항 저장”
- 큐 안내: “BLOCK은 진단이 아닌 세션 운영 중단 및 전문가 상담 안내 신호입니다.”
- 요청 답변: “기록해 주신 불편감은 다음 세션 전 확인하겠습니다. 갑작스러운 심한 통증이나 일상생활 제한이 있으면 전문기관 상담을 권합니다.”
- 재등록 상담: “최근 4주 변화와 수행 기록을 바탕으로 다음 컨디셔닝 목표를 제안합니다.”
