# LIGHTONE V2

**비의료 웰니스 SaaS · 트레이너 검토 기반 상담 리포트 · 브랜드 운영 시스템**

> 측정이 아니라, 설명 가능한 컨디셔닝 상담 시스템.

---

## 한 줄 정의

LIGHT ONE은 PT샵·헬스장·필라테스 센터가 회원의 운동 수행, 통증 반응, 자세 변화, 생활습관 데이터를 구조화하고, 트레이너 검토 기반 상담 리포트를 생성하여 재등록 상담, 회원 유지, 프리미엄 컨디셔닝 프로그램 운영에 활용하도록 돕는 비의료 웰니스 SaaS이자 브랜드 운영 시스템이다.

```
프로젝트 상태: 전략 전환 / 사업 설계 단계
작성 기준일:   2026-06-30
핵심 키워드:   PT 상담 리포트, 기능적 컨디셔닝, QS, JATC,
              Human-in-the-Loop, 비의료 웰니스, 브랜드 운영 시스템
```

---

## 목차

1. [What LIGHT ONE is](#1-what-light-one-is)
2. [What LIGHT ONE is not](#2-what-light-one-is-not)
3. [왜 V2인가](#3-왜-v2인가)
4. [핵심 고객 문제](#4-핵심-고객-문제)
5. [제품 포지셔닝](#5-제품-포지셔닝)
6. [제품 모듈](#6-제품-모듈)
7. [기술 계층](#7-기술-계층)
8. [데이터 아키텍처](#8-데이터-아키텍처)
9. [안전 및 규제 경계](#9-안전-및-규제-경계)
10. [비즈니스 모델](#10-비즈니스-모델)
11. [시장 진출 전략](#11-시장-진출-전략)
12. [모두의창업 2기 대응 전략](#12-모두의창업-2기-대응-전략)
13. [현재 증거 현황](#13-현재-증거-현황)
14. [다음 조치](#14-다음-조치)
15. [저장소 운영 규칙](#15-저장소-운영-규칙)
16. [면책 조항](#16-면책-조항)
17. [문서 지도](#17-문서-지도)

---

## 1. What LIGHT ONE is

LIGHT ONE은 PT샵·헬스장·필라테스 센터가 회원의 운동 수행, 통증 반응, 자세 변화, 생활습관 데이터를 구조화하고, 트레이너 검토 기반 상담 리포트를 생성하여 재등록 상담, 회원 유지, 프리미엄 컨디셔닝 프로그램 운영에 활용하도록 돕는 비의료 웰니스 SaaS이자 브랜드 운영 시스템이다.

LIGHT ONE은 센터와 트레이너가 흩어진 상담·운동·촬영 품질 데이터를 한곳에 모아 회원에게 설명 가능한 상담 자료로 전환하도록 돕습니다. 핵심은 AI의 자동 판단이 아니라, **트레이너 검토(Human-in-the-Loop)**를 거친 기록 구조화, 상담 리포트, 회원 유지 운영 흐름입니다.

## 2. What LIGHT ONE is not

LIGHT ONE은 의료기기, 진단 도구, 자동 처방 시스템이 아닙니다. 특히 다음 기능과 표현을 제공하지 않습니다.

- AI 자동 의료 진단
- 질병 위험 예측
- 자동 처방
- 병원 진단 리포트
- 통증 원인 확정
- 치료 효과 판단

---

## Repository Map

| 경로 | 역할/상태 |
|------|-----------|
| `LIGHTONE_redesigned_v2/` | 정적 랜딩페이지 자산입니다. V2 메시지와 화면 흐름을 빠르게 확인하는 프론트엔드 시안 영역입니다. |
| `lightone_v2_django/` | Django 기반 MVP입니다. 회원/상담/리포트 등 실제 서비스 기능을 구현·검증하는 실행 코드 영역입니다. |
| `lightone_v2_django/docs/` | Django MVP 실행 방법, 사업화 전략, 기능 정의 등 구현과 운영에 필요한 문서를 모아둔 영역입니다. |
| `assets/` | 인포그래픽 등 README, 제안서, 발표 자료에서 함께 사용할 공용 자산 영역입니다. |
| `아이디어-구상/` | 초기 아이디어, 문제 정의, 사업 방향성 메모를 보관하는 기획 초안 영역입니다. |
| `2/repo_lightoneV2/` | V2 관련 자산 정리본으로 보이며, 현재는 중복/보관 자산 여부를 확인한 뒤 유지 또는 정리할 예정인 검토 대상 영역입니다. 파일 이동 없이 상태만 명시합니다. |

---


## QS Dashboard

LIGHT ONE Django MVP에는 QS/JATC 기반 상담 보조 흐름을 확인할 수 있는 QS Dashboard가 포함되어 있습니다. 이 화면과 데이터는 제품 검증용 synthetic/demo 데이터만 사용하며, 의료 진단·치료·처방 목적이 아닙니다.

### Dashboard URL

- 로컬 서버 실행 후 대시보드: `http://127.0.0.1:8000/`
- Django 앱 내부 대시보드 라우트: `lightone:dashboard` (`lightone_v2_django/lightone/urls.py`의 빈 경로)

### Synthetic 데이터 생성 방법

```bash
cd lightone_v2_django
python manage.py migrate
python manage.py seed_lightone
```

`seed_lightone` 명령은 QS Dashboard 확인용 synthetic 회원·운동 세션·지표 데이터와 기본 로그인 계정을 생성합니다. 실제 회원 개인정보, 실제 건강정보, 실제 촬영 이미지/영상은 퍼블릭 저장소와 데모 데이터에 포함하지 않습니다.

### 서버 실행 방법

```bash
cd lightone_v2_django
python manage.py runserver
```

서버 실행 후 브라우저에서 `http://127.0.0.1:8000/`로 접속해 QS Dashboard를 확인합니다.

### 테스트 실행 방법

```bash
cd lightone_v2_django
python manage.py test
```

필요 시 저장소 루트에서 정적 문서·프로토타입 변경 사항을 함께 검토합니다.

### 비의료 안내

- QS/JATC 점수와 AUTO/REVIEW/BLOCK 라우팅은 비의료 운동 상담 참고 자료입니다.
- LIGHT ONE은 의료기기, 진단 도구, 자동 처방 시스템이 아닙니다.
- 통증 악화, 신경학적 증상, 급성 손상 의심 등 의학적 판단이 필요한 상황에서는 의료 전문가의 판단이 우선합니다.
- AI/규칙 기반 산출물은 최종 판단자가 아니라 트레이너 검토(Human-in-the-Loop)를 돕는 보조 레이어입니다.

### 개인정보 표시 기준

- 데모와 README에는 synthetic 데이터만 표시합니다.
- 퍼블릭 저장소에는 실제 회원 이름, 연락처, 생년월일, 얼굴 이미지, 원본 영상, 민감 건강정보를 포함하지 않습니다.
- 분석 테이블과 화면 예시는 직접 식별정보 대신 회원 ID, 연령대, 성별 분류, 운동 목표, 세션 지표처럼 비의료 참고 목적의 최소 정보만 사용합니다.
- 실제 서비스 전환 전 개인정보보호법, 민감정보 처리 동의, 보관·파기 정책, 접근 권한, 감사 로그 기준은 별도 법률/보안 검토가 필요합니다. [확인필요]

### 사용 폰트 stack

QS Dashboard CSS는 폰트 파일을 레포지토리에 추가하지 않고 다음 fallback stack을 사용합니다.

```css
:root {
  --font-dashboard: "Pretendard", "SUIT", "Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", "Inter", Arial, sans-serif;
}

body {
  font-family: var(--font-dashboard);
}
```

[확인필요] 폰트 라이선스와 상업적 이용 가능 범위는 실제 배포 전 공식 배포처 기준으로 최종 확인이 필요합니다. 폰트 파일은 프로젝트에 포함하지 않고, CSS font-family fallback stack 또는 공식 CDN 방식만 사용합니다.

---

## 3. 왜 V2인가

초기 LIGHT ONE은 촬영 QC, 조명 정규화, 카메라 캘리브레이션을 활용한 자세 변화 기록과 AI 기반 상담 보조 중심으로 설계되었습니다. 시장 조사와 심사 피드백을 반영하여 V2로 전환합니다.

| 구분 | V1 방향 | 한계 | V2 전환 방향 |
|------|---------|------|-------------|
| 시장 | AI 기반 자세 기록 앱 | 키오스크·앱 경쟁 포화 | 상담 보고서 SaaS + 컨디셔닝 OS |
| 기술 | 포즈 추정·측정 | 오픈소스/SDK로 기술 평준화 | QC를 신뢰도 보조 레이어로 재배치 |
| 규제 | 통증 원인 확정·자세 이상 판정 | 의료기기 오인 가능성 | 비의료 운동 상담으로 한정 |
| 사업성 | D2C 앱 | 리텐션·마케팅 비용 부담 | B2B 센터·트레이너·기업 파일럿 |
| 심사 | AI 기반 촬영·기록 보조 서비스 | 방어 가능성 부족 | 방법론 IP + 실행 로드맵 |

**V2 핵심 전환:**
- "AI가 자세 이상을 판정한다" → "트레이너 검토 기반으로 상담·기록·재등록 문제를 해결한다"
- 송광일의 현장 방법론(근기능 파악 → 운동 선택 → 컨디셔닝 설계)을 무형 IP로 체계화
- 기술 자산(카메라·조명·QC)은 버리지 않고 신뢰도 보조 계층으로 재활용

---

## 4. 핵심 고객 문제

PT 현장에서 반복되는 문제:

1. 회원의 운동 기록, 통증 반응, 상담 내용이 카카오톡·사진첩·메모장·인바디 결과지에 **분산** 저장
2. 트레이너가 상담 전 자료 정리에 과도한 시간 소요
3. 재등록 상담 시 회원에게 설명할 **구조화된 자료** 부재
4. 트레이너별 상담 품질 편차 관리 불가
5. 촬영 조건(각도·조명·거리) 차이로 자세 변화 기록의 **신뢰도 저하**

---

## 5. 제품 포지셔닝

### 5.1 초기 — 비의료 PT 상담 보고서 SaaS

| 역할 | 대상 | 핵심 가치 |
|------|------|-----------|
| 구매자 | PT샵·헬스장·필라테스 센터 대표 | 상담 품질 표준화, 재등록률 개선 |
| 사용자 | 트레이너, 코치 | 상담 준비 시간 단축, 구조화된 설명 자료 |
| 수혜자 | PT 회원 | 자신의 변화가 이해되는 상담 경험 |

### 5.2 중기 — 기능적 컨디셔닝 OS

근기능 평가, 통증 반응 기록, 운동 수행 품질 추적, 생활습관 모니터링, 컨디셔닝 프로그램 설계를 통합하는 운영 체제. 트레이너 검토(Human-in-the-Loop) 기반 프로그램 조정.

### 5.3 장기 — 교육·인증 IP + B2B 확장

한국형 기능적 컨디셔닝 인증 과정, 센터/트레이너 레벨제 커리큘럼, 기업 복리후생 운동 프로그램, 병원·전문가 협력 비의료 운동 상담 모델.

---

## 6. 제품 모듈

### 6.1 데이터 입력

회원 기본정보, 운동 목표, 주요 불편감 부위, 세션별 운동 기록, RPE(주관적 운동 강도), 통증 반응, 생활습관 체크, 트레이너 메모

### 6.2 QS 엔진 (Quality Score, 운동 수행 품질 지수)

운동 실천 품질을 요약하는 지표입니다.

**구성 요소:** 폼 정확도(Form Accuracy), 반복수 달성률(Rep Completion), 휴식 준수(Rest Compliance), 통증 반응(Pain Response)

**라우팅 규칙:**

| 상태 | 조건 | 의미 |
|------|------|------|
| `AUTO` | QS 양호, 특이사항 없음 | 일반 상담 보고서 자동 생성 |
| `REVIEW` | QS 경계값 또는 통증 반응 존재 | 트레이너 확인 필요 |
| `BLOCK` | 통증 악화, 세션 중단, 위험 신호 | 세션 중단 + 전문가 상담 안내 |

> 현재 QS/JATC 및 AUTO/REVIEW/BLOCK 임계값은 MVP 데모용 내부 초안이며 의료 판단 기준이 아닙니다. 파일럿 데이터와 전문가 검토 후 조정이 필요하고, BLOCK은 진단이 아니라 운동 세션 중단 및 전문가 상담 권고 신호입니다.
>
> QS는 의료적 판단이 아닌 **운동 상담 참고 점수**입니다.

### 6.3 JATC 엔진 (Joint Achievement & Tracking Composite, 통합 상태 지수)

통증 반응, 자세 변화, 근기능, 생활습관을 하나의 상담용 지표로 통합합니다.

**구성:** Pain(통증 반응), Posture(자세 변화), Function(근기능·운동 수행), Lifestyle(생활습관)

> 현재 JATC 가중치 및 임계값은 MVP 데모용 내부 초안이며 의료 판단 기준이 아닙니다. 파일럿 데이터와 전문가 검토 후 조정이 필요하고, BLOCK은 진단이 아니라 운동 세션 중단 및 전문가 상담 권고 신호입니다.
>
> [확인필요] JATC 가중치 및 임계값은 파일럿 데이터 수집 후 전문가 검토 필요

### 6.4 상담 보고서 생성기

| 유형 | 설명 |
|------|------|
| 기본 보고서 | 정상 입력, QS AUTO → 자동 생성 |
| 검토 보고서 | QS REVIEW → 트레이너 확인 후 확정 |
| 재촬영 보고서 | 촬영 조건 미달 또는 입력 품질 부족 → 재촬영/재입력 필요 |

### 6.5 트레이너 검토 흐름 (Human-in-the-Loop)

```
데이터 입력
  → QS/JATC 규칙 기반 산출
  → AUTO / REVIEW / BLOCK 라우팅
  → 트레이너 검토 (AI는 최종 판단자가 아님)
  → 상담 리포트 확정
  → 회원 상담 및 재등록 관리 활용
```

---

## 7. 기술 계층

V1의 기술 자산은 V2에서 **메인 상품이 아닌 신뢰도 보조 레이어**로 재배치됩니다.

| 모듈 | 역할 | 핵심 기능 |
|------|------|-----------|
| 카메라 캘리브레이션 | 촬영 품질 판정 | 내부 파라미터 산출, RMSE 기반 PASS/CHECK/FAIL 판정, 왜곡 보정 |
| 조명 정규화 | 촬영 환경 표준화 | Gray-world 화이트밸런스, CLAHE 히스토그램 균등화, 균일도 ≥90% 기준 |
| 센터 QC | 촬영 환경 기준 확인 | 중심 정렬, 전신 포함, 배경·바닥 마커 검증 |
| 포즈 추정 | 자세 변화 기록 보조 | RTMPose(Apache 2.0) 우선, MediaPipe·MoveNet 호환 |

> 포즈 추정 기술 자체는 경쟁 해자가 아닙니다. LIGHTONE V2의 해자는 **현장 데이터 구조화, 컨디셔닝 방법론, 상담 보고서 UX, 트레이너 교육·인증 IP**에 있습니다.

---

## 8. 데이터 아키텍처

### 3계층 데이터 모델

```
Member Layer
  └─ Member_ID, 성별, 연령대, 운동 목표, 운동 경험, 주요 불편감 부위, 동의 상태

Session Layer
  └─ Session_ID, 운동명, 세트, 반복, 중량, 휴식, RPE
  └─ 통증 반응, 트레이너 메모, 촬영 조건, 촬영 품질 상태

Indicator Layer
  └─ QS, JATC, REVIEW/BLOCK 신호, 상담 우선순위, 리포트 생성 상태
```

### 데이터 분리 원칙

- 원본 이미지/영상은 별도 저장소에 보관
- 분석 테이블에는 Media_ID, Session_ID, 촬영 조건, 추출 지표, 품질 상태만 저장
- 회원 식별 정보와 민감 건강정보는 퍼블릭 저장소에 업로드하지 않음

---

## 9. 안전 및 규제 경계

LIGHTONE V2는 **비의료 웰니스·운동 상담 지원 서비스**로 설계합니다.

### 제공하지 않는 것

- AI 자동 의료 진단
- 질병 위험 예측
- 자동 처방
- 병원 진단 리포트
- 통증 원인 확정
- 치료 효과 판단
- 임상 의사결정 지원
- 환자 상태 평가
- 의학적 효능·효과 주장

### 표현 가이드

| 사용하지 않는 표현 | 대체 표현 |
|---------------------|-----------|
| 진단 | 측정, 기록, 확인 |
| 치료 | 관리, 컨디셔닝, 운동 상담 |
| 처방 | 운동 제안, 프로그램 조정 제안 |
| 재활 | 운동 상담, 컨디셔닝 플랜 |
| 통증 원인 분석 | 통증 반응 기록 |
| 위험도 판정 | 주의 신호, 트레이너 확인 필요 |
| AI가 판단 | 트레이너가 검토 |

### 개인정보 원칙

최소 수집, 명시적 동의, 목적 제한, 비식별화, 접근권한 분리, 암호화 저장, 감사 로그, 보관기간 설정, 삭제 요청 처리

---

## 10. 비즈니스 모델

### 초기 수익 모델

| 티어 | 대상 | 가격대 | 상태 |
|------|------|--------|------|
| 스타터 | 1인 트레이너 | 월 29,000~49,000원 | [확인필요] |
| 스튜디오 | 소형 PT샵·필라테스 센터 | 월 99,000~149,000원 | [확인필요] |
| 셋업+SaaS | 촬영 환경 구축이 필요한 센터 | 초기 30만 원 + 월 구독 | [확인필요] |
| 교육 | 트레이너 교육·인증 | 과정별 과금 | [확인필요] |
| B2B | 기업 복리후생 운동 프로그램 | 프로젝트 단가 | [확인필요] |

> 모든 가격은 센터 원장·트레이너 인터뷰 전 가설입니다. 실제 지불의사 검증(WTP) 인터뷰 후 확정 필요.

### 수익 우선순위

1. PT 상담 보고서 SaaS
2. 트레이너 교육·인증 프로그램
3. 기업 B2B 복리후생 파일럿
4. 병원·전문가 협력 비의료 운동 상담 모델
5. 소비자용 D2C 앱 (후순위)

---

## 11. 시장 진출 전략

### Phase 0→1: 최소 증거 확보

- 트레이너/센터 3~5곳 미니 인터뷰
- 샘플 보고서 3종 제작 및 피드백
- QS/JATC 입력폼 프로토타입
- QC 파이프라인 사전 점검
- 비의료 표현 검수 완료
- GitHub 저장소 정리, 문서화

### Phase 1→10: 사용성 검증

- 파일럿 센터 1~3곳 운영
- 회원 n=10~30명 동의 기반 테스트
- 보고서 생성 성공률 측정
- 트레이너 검토 플로우 실사용 테스트
- 재등록 상담 활용도 확인

### Phase 10→100: 반복 판매 구조

- 교육·인증 1기 운영
- 스타터 → 스튜디오 티어 전환 유도
- 기업 B2B 파일럿 제안서 제작
- 피트니스 CRM(바디코디 등) 보완재 제휴 검토
- 병원·전문가 협력 가능성 검토

---

## 12. 모두의창업 2기 대응 전략

### 핵심 메시지

> "AI 기반 상담 보조와 자세 변화 기록을 활용하되, 핵심은 PT 현장의 상담 기록과 재등록 문제를 해결하는 비의료 웰니스 SaaS이자 브랜드 운영 시스템입니다. 이를 한국형 기능적 컨디셔닝 방법론 교육·인증 IP로 확장합니다."

### 예상 심사 질문 대응

| 심사 질문 | 대응 논리 | 증거 |
|-----------|-----------|------|
| 실제 고객 문제가 있는가? | PT 상담·재등록 시 구조화된 정보 부족 | 인터뷰 결과 [확인필요] |
| 만들 수 있는가? | GitHub 기반 촬영 QC·조명 정규화·리포트 모듈 구현 완료 | lightone 저장소 기술 모듈 |
| AI가 핵심인가? | AI 자체보다 데이터 구조화 + 트레이너 검토(HITL)가 핵심 | QS/JATC 설계, HITL 흐름도 |
| 규제 리스크는? | 의료 표현 제거, 비의료 운동 상담으로 한정 | 안전 정책, 표현 가이드 |
| 수익 모델은? | 센터 SaaS → 교육·인증 → 기업 B2B | 티어별 가격 가설, 파일럿 계획 |
| 왜 이 대표인가? | PT 현장 20년 + AI 바이오메디컬 학습 + 사업화 의지 | 경력, 포트폴리오, 문서화 |

---

## 13. 현재 증거 현황

| 항목 | 상태 | 비고 |
|------|------|------|
| lightone 기술 모듈 (GitHub) | ✅ 확인됨 | QC·조명·캘리브레이션 모듈 활용 가능 |
| V2 전략서 | ✅ 작성됨 | 사업 설계 방향 문서화 완료 |
| QS/JATC 정의 | ⚠️ 초안 | 파일럿 데이터 기반 검증 필요 |
| 고객 인터뷰 | ❌ 미실시 | 3~5명 인터뷰 필요 |
| 지불의사(WTP) | ❌ 미검증 | [확인필요] |
| 규제 적합성 | ⚠️ 방향 설정 | 공식 법률 검토 필요 |
| B2B 기업 파일럿 | ❌ 미착수 | LOI 또는 미팅 필요 |

---

## 14. 다음 조치

### 이번 주

- [ ] README 기반 GitHub 저장소 정리
- [ ] 1페이지 사업소개서 제작
- [ ] 샘플 보고서 3종 정리
- [ ] 트레이너/센터 원장 인터뷰 질문지 작성
- [ ] 비의료 표현 검수표 적용

### 2주 내

- [ ] QS/JATC 입력 MVP 구현
- [ ] 상담 보고서 PDF 생성 프로토타입
- [ ] QC 결과 → 보고서 연결 파이프라인
- [ ] 파일럿 대상 센터 3곳 리스트업
- [ ] 모두의창업 2기 제출 문서 최종화

### 1개월 내

- [ ] 센터 1곳 파일럿 운영
- [ ] 트레이너 피드백 수집
- [ ] 보고서 생성 성공률 측정
- [ ] 재등록 상담 활용 사례 정리
- [ ] 교육·인증 커리큘럼 Level 1 초안 작성

---

## 15. 저장소 운영 규칙

| 도구 | 역할 | 운영 원칙 |
|------|------|-----------|
| Google Drive | 제안서, 보고서, 제출 서류 | 최종·심사용 서류 관리 |
| GitHub | 기술 구현, README, 코드, 로드맵 | 실행 가능성·기술 기반 증명 |
| Slack | 의사결정 기록, 리뷰 공유 | 설명 없이 링크만 투척 금지 |
| Airtable | 고객 DB, 액션 리스트, 인터뷰 관리 | 주장-근거-상태-[확인필요] 연결 |

### README 업데이트 기준

이 README는 고정 문서가 아닌 **V2 사업 설계의 살아있는 문서(Living Document)**입니다.

- 고객 인터뷰 결과 반영 시 → §2 핵심 고객 문제, §11 증거 현황 업데이트
- MVP 구현 진행 시 → §4 제품 모듈, §5 기술 계층 업데이트
- 가격 검증 완료 시 → §8 비즈니스 모델의 [확인필요] 제거
- 규제 검토 완료 시 → §7 안전 및 규제 경계 업데이트
- 모두의창업 2기 결과 확정 시 → §10 대응 전략 업데이트

---

## 16. 면책 조항

본 문서는 사업 기획, 기술 검증, 비의료 웰니스·운동 상담 서비스 설계를 위한 자료입니다. 의료 진단, 치료, 처방, 효능·효과 검증, 질병 위험 예측을 목적으로 하지 않습니다. 통증·자세·운동 관련 정보는 트레이너가 검토할 참고 자료이며, 의학적 판단이 필요한 경우 의료 전문가의 판단이 우선합니다.

---

## 17. 문서 지도

| 문서 | 용도 |
|------|------|
| [저장소 맵](docs/repository-map.md) | 루트 README, Django MVP, 실행 문서, 거버넌스 문서의 관계를 한눈에 확인 |
| [비의료 경계 정책](docs/governance/non-medical-boundary.md) | 의료 오인 방지를 위한 기능·표현·라우팅 기준 |
| [개인정보 보호 체크리스트](docs/governance/privacy-checklist.md) | 파일럿과 MVP 운영 시 개인정보·민감 기록 취급 기준 |
| [파일럿 검증 계획](docs/validation/pilot-validation-plan.md) | 센터 파일럿 목표, 지표, 절차, 중단 기준 |
| [트레이너·센터 고객 인터뷰 질문지](docs/validation/trainer-interview-script.md) | PT샵·헬스장·필라테스 센터·트레이너 대상 고객 문제 검증 질문지 |
| [고객 발견 인터뷰 로그 템플릿](docs/validation/customer-discovery-log-template.md) | 인터뷰 결과, 핵심 가설, 지불의사, 후속 액션 기록 양식 |
| [WTP 지불의사 테스트 계획](docs/validation/wtp-test-plan.md) | 월 구독·리포트당 과금 수용성 검증 계획 |
| [파일럿 센터 리스트 템플릿](docs/validation/pilot-center-list-template.md) | 동의 기반·비식별화·최소수집 원칙의 파일럿 후보 관리 양식 |
| [LIGHTONE V2 1페이지 사업 요약](docs/submission/one-page-business-summary.md) | 고객검증·파일럿 실행 전 단계의 외부 설명용 1페이지 요약 |
| [모두의창업 2기 제출 요약](docs/submission/modu-startup-summary.md) | 외부 제출용 1~2페이지 사업 요약 |
| [Windows 실행 가이드](docs/execution-guide/windows-run-guide.md) | 저장소 루트 기준 Windows 실행 절차 |
| [Django MVP README](lightone_v2_django/README.md) | MVP 기능, 계정, 빠른 시작, 라우팅 기준 |
| [기존 Windows 실행 문서](lightone_v2_django/RUN_WINDOWS.md) | Django 폴더 내부 기준의 간단 실행 명령 |

---

## 관련 저장소

| 저장소 | 용도 |
|--------|------|
| [lightone](https://github.com/gggwang210-commits/lightone) | V1 아카이브 — 기술 모듈 원본 |
| **LightOne_V2** (이 저장소) | V2 프로덕션 — 사업 전략 + 정리된 자산 |

---

*LIGHTONE V2 — 측정이 아니라, 설명 가능한 컨디셔닝 상담 시스템.*

---

## Dashboard Strategy: Role-based Product Architecture

LIGHT ONE의 상용화형 대시보드는 **회원(Member) · 트레이너(Trainer) · 관리자/센터 매니저(Admin)** 3개 역할을 기준으로 설계됩니다. 목적은 운동 수행, 통증 반응 기록, 자세·동작 참고 지표, 세션 피드백, 리포트, 예약, 결제를 하나의 비의료 웰니스 상담 운영 흐름으로 연결하는 것입니다.

### Non-medical safety boundary

LIGHT ONE은 의료 진단, 질병 예측, 치료, 처방, 재활 처방, 통증 원인 확정, 임상 의사결정 지원을 제공하지 않습니다. 대시보드의 모든 지표와 문구는 **AI-assisted consultation support**, **pain response record**, **caution signal**, **conditioning program suggestion**, **trainer review**, **non-medical wellness reference report** 범위로 제한합니다.

### Member / Trainer / Admin dashboard overview

| Role | Dashboard purpose | Key sections |
|---|---|---|
| Member Dashboard | 오늘 컨디션, 최근 변화, 트레이너 피드백, 다음 행동, 예약/결제를 쉽게 이해 | Today Summary, Condition Score Card, Pain Response Trend, Trainer Feedback, Reservation, Payment, Report History |
| Trainer Dashboard | 회원 변화 검토, 주의 신호 확인, 세션 기록, 리포트 초안 검토, 재등록 상담 준비 | Today Sessions, Member Change Timeline, QS/JATC Summary, AUTO/REVIEW/BLOCK Queue, Report Drafts, Re-registration Candidates |
| Admin / Center Manager Dashboard | 센터 운영, 트레이너 업무, 회원 상태, 리포트 사용, 예약/결제, 권한과 감사 로그 관리 | Center Overview, Trainer Performance, Member Status, Report Generation Metrics, Payment Overview, Permission Management |

### Dashboard documentation

- [Dashboard Strategy](docs/dashboard_strategy.md)
- [Member Dashboard Specification](docs/member_dashboard_spec.md)
- [Trainer Dashboard Specification](docs/trainer_dashboard_spec.md)
- [Admin Dashboard Specification](docs/admin_dashboard_spec.md)
- [Dashboard Information Architecture](docs/dashboard_information_architecture.md)
- [Dashboard Component Library](docs/dashboard_component_library.md)
- [Dashboard Data Model](docs/dashboard_data_model.md)
- [Dashboard Sample User Flows](docs/dashboard_sample_user_flows.md)
- [Dashboard Safety Copy Guidelines](docs/dashboard_safety_copy_guidelines.md)
- [Codex Implementation Plan](docs/dashboard_codex_implementation_plan.md)

### Static dashboard prototype

- [Member Dashboard Prototype](prototype/dashboards/member_dashboard.html)
- [Trainer Dashboard Prototype](prototype/dashboards/trainer_dashboard.html)
- [Admin Dashboard Prototype](prototype/dashboards/admin_dashboard.html)
- [Dashboard Theme CSS](prototype/dashboards/dashboard_theme.css)
- [Dashboard Mock Data](prototype/dashboards/dashboard_mock_data.js)

Prototype files are dependency-free and use synthetic data only.
