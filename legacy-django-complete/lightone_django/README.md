<!--
ARCHIVE NOTICE:
이 파일은 레거시 보관본입니다. 최신 기준은 루트 README.md와 docs/README.md를 우선합니다.
본 자료는 비의료 운동상담 참고용이며, 의료 진단·치료·처방 목적이 아닙니다. 모든 판단은 담당 트레이너가 검토합니다.
-->

# LIGHT ONE — AI 기반 체형분석 PT 솔루션 SaaS MVP

## 📋 프로젝트 개요

**LIGHT ONE**은 PT 현장의 운동 기록, 통증/RPE, 자세 관찰, 촬영 품질 데이터를 구조화해 QS(Quality Score), 변화 추세, 위험 라우팅, 트레이너 리포트를 제공하는 **데이터 기반 PT 의사결정지원 서비스**입니다.

- **핵심 가치**: AI가 트레이너를 대체하는 것이 아니라 트레이너의 판단을 보조합니다.
- **초기 MVP**: 더미 데이터 기반 프로토타입 (실제 개인정보·건강정보·영상 없음)
- **기술 스택**: Django 4.2 + SQLite + Bootstrap 5 + Chart.js
- **팀 프로젝트 수준**: COPD 선별 서비스 팀 프로젝트와 동등한 완성도

---

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 프로젝트 디렉토리 진입
cd lightone_django

# 가상 환경 활성화
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate  # Windows

# 필수 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터베이스 초기화 및 시딩

```bash
# 마이그레이션 생성 및 적용
python manage.py makemigrations
python manage.py migrate

# 더미 데이터 자동 생성 (8명 회원 + 79개 세션)
python manage.py seed_demo
```

### 3. 개발 서버 실행

```bash
python manage.py runserver
```

**접속 정보:**
- 🌐 URL: `http://127.0.0.1:8000/`
- 이 경로는 보관용이며 기존 고정 계정 시드는 비활성화되었습니다. 현재 실행 기준은 루트의 `lightone_v2_django`입니다.

---

## 📁 프로젝트 구조

```
lightone_django/
├── config/                    # Django 설정
│   ├── settings.py           # 프로젝트 설정
│   ├── urls.py               # URL 라우팅
│   └── wsgi.py               # WSGI 진입점
├── accounts/                 # 사용자 인증 & 프로필
│   ├── models.py             # User, TrainerProfile
│   ├── views.py              # 로그인/로그아웃
│   └── urls.py               # 인증 URL
├── members/                  # 회원 관리
│   ├── models.py             # Member 모델
│   ├── views.py              # 회원 CRUD
│   └── urls.py               # 회원 URL
├── pt_sessions/              # 세션 기록 & QS 점수화
│   ├── models.py             # MemberSession (QS 엔진 포함)
│   ├── views.py              # 세션 CRUD & 대시보드
│   ├── urls.py               # 세션 URL
│   └── management/
│       └── commands/
│           └── seed_demo.py  # 더미 데이터 생성 명령어
├── reports/                  # 상담 리포트
│   ├── models.py             # WeeklyReport 모델
│   ├── views.py              # 리포트 생성 & 조회
│   └── urls.py               # 리포트 URL
├── templates/                # HTML 템플릿
│   ├── base.html             # 기본 레이아웃 (사이드바 + 대시보드)
│   ├── accounts/             # 로그인 페이지
│   ├── dashboard/            # 대시보드
│   ├── members/              # 회원 관리 페이지
│   ├── pt_sessions/          # 세션 기록 페이지
│   └── reports/              # 리포트 페이지
├── static/                   # 정적 파일
│   ├── css/
│   │   └── lightone.css      # 프리미엄 UI 스타일 (민트/청록 계열)
│   └── js/
│       └── lightone.js       # 프론트엔드 유틸리티
├── db.sqlite3                # SQLite 데이터베이스
├── manage.py                 # Django 관리 명령어
└── README.md                 # 이 파일
```

---

## 🎯 핵심 기능

### 1. **대시보드**
- 활성 회원 수, 총 세션 수, 평균 QS 점수 통계
- 위험 라우팅 분포 (AUTO/REVIEW/BLOCK)
- 최근 세션 목록 + BLOCK/REVIEW 세션 주의 알림

### 2. **회원 관리**
- 회원 등록/수정/조회
- 회원별 최근 세션 기록 조회
- 운동 목표, 불편 부위, 특이사항 관리

### 3. **세션 기록 입력**
- 운동 기록 (운동명, 세트, 회수, 중량)
- 컨디션 지표 (통증, RPE, 자세 정확도, JATC 점수)
- 체형 관찰 6항목 (어깨, 골반, 척추, 무릎, 발목, 좌우 편차)
- **QS 점수 자동 계산** (규칙 기반 엔진)
- **위험 라우팅 자동 판정** (AUTO/REVIEW/BLOCK)

### 4. **QS 점수화 엔진** (MVP 규칙 기반)
```
QS = 100 - (통증반응 × 5) - (|RPE - 7| × 2) + (자세정확도 × 1.5)
범위: 0~100점

라우팅 규칙:
- AUTO:   QS ≥ 70 AND 통증 < 4
- REVIEW: QS 40~70 OR 통증 4~6
- BLOCK:  QS < 40 OR 통증 ≥ 7
```

### 5. **상담 리포트**
- 4주 단위 회원 분석 리포트 자동 생성
- 평균 QS, 통증, RPE 집계
- 라우팅 분포 (AUTO/REVIEW/BLOCK 비율)
- 재등록 신호 판정 (일관된 성과 + 충분한 세션 횟수)
- 세션별 상세 데이터 + 차트 시각화

---

## 🔐 사용자 역할

| 역할 | 권한 | 접근 범위 |
|------|------|---------|
| **트레이너** | 회원 관리, 세션 기록, 리포트 생성 | 자신의 회원 데이터만 |
| **관리자** | 전체 시스템 관리 + Django Admin | 모든 데이터 |

---

## 📊 더미 데이터 구성

**seed_demo 명령어 실행 시 자동 생성:**
- **회원**: 8명 (다양한 나이, 성별, 운동 목표)
- **세션**: 회원당 8~12회 (총 79개)
- **특징**:
  - 실제 통증 반응, RPE, 자세 정확도 분포 반영
  - AUTO/REVIEW/BLOCK 라우팅 자동 계산
  - 트레이너 계정 + 관리자 계정 자동 생성

---

## 🛠 주요 기술 결정

### 1. **QS 점수화 엔진**
- **규칙 기반** (초기 MVP): 통증, RPE, 자세 정확도의 가중치 조합
- **향후 고도화**: XGBoost/LightGBM 예측 모델 연결 가능

### 2. **위험 라우팅 (AUTO/REVIEW/BLOCK)**
- **의료 진단 아님**: 안전 신호 기반 의사결정 보조
- **트레이너 판단 우선**: 시스템은 참고 자료, 최종 판단은 트레이너

### 3. **UI/UX 디자인**
- **프리미엄 Bootstrap 5**: 민트/청록 계열 브랜드 컬러
- **COPD 팀 프로젝트 수준**: 전문적이고 깔끔한 인터페이스
- **반응형 디자인**: 데스크톱/태블릿/모바일 지원

### 4. **데이터베이스**
- **SQLite**: 초기 MVP용 경량 데이터베이스
- **향후 확장**: PostgreSQL/MySQL로 마이그레이션 가능

---

## 📝 관리자 페이지

Django Admin에서 모든 데이터 관리 가능:
```
http://127.0.0.1:8000/admin/
```

**관리 가능 항목:**
- 사용자 및 트레이너 프로필
- 회원 정보
- 세션 기록 (QS 점수, 라우팅 읽기 전용)
- 주간 리포트

---

## 🚀 배포 가이드

### 프로덕션 배포 전 체크리스트

```bash
# 1. 보안 설정
DEBUG = False  # settings.py
SECRET_KEY = os.environ.get('SECRET_KEY')  # 환경 변수 사용

# 2. 정적 파일 수집
python manage.py collectstatic --noinput

# 3. 데이터베이스 마이그레이션
python manage.py migrate --noinput

# 4. Gunicorn으로 실행
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### 권장 배포 플랫폼
- **Heroku**: 간단한 배포
- **AWS EC2 + RDS**: 확장성
- **Railway/Render**: 모던 클라우드 플랫폼

---

## ⚠️ 주의사항

### 1. **의료 관련 면책**
- 이 시스템은 **의료 진단 도구가 아닙니다**.
- BLOCK 신호는 **안전 신호**이며, 의료 전문가 상담 필요 여부는 트레이너가 판단합니다.
- 모든 리포트에 "의료 진단이 아님" 명시되어 있습니다.

### 2. **개인정보보호**
- 초기 MVP는 더미 데이터만 사용합니다.
- 실제 개인정보 수집 시 **GDPR/개인정보보호법 준수** 필수
- 건강정보 수집 시 **식품의약품안전처 사전 검토** 필요

### 3. **규제 확인**
- 의료기기 분류 여부: 식약처 사전 상담 필요
- 의료법 준수: 의료인 감수 필요
- 개인정보 처리방침 수립 필수

---

## 📚 향후 개발 로드맵

| Phase | 목표 | 기술 |
|-------|------|------|
| **Phase 1 (현재)** | MVP 프로토타입 | Django + SQLite |
| **Phase 2** | 베타 테스트 (실제 PT샵) | 데이터 수집 + 피드백 |
| **Phase 3** | ML 모델 고도화 | XGBoost + OpenPose |
| **Phase 4** | 모바일 앱 | React Native/Flutter |
| **Phase 5** | SaaS 상용화 | 구독 모델 + 결제 연동 |

---

## 🤝 팀 정보

**LIGHT ONE 프로젝트**
- 기획/개발: 송광일 (AI 전문가 양성과정, 바이오메디컬 AI 학습자)
- 기술 스택: Django, Bootstrap, Chart.js, SQLite
- 참고 프로젝트: COPD 선별 서비스 (팀 프로젝트 수준)

---

## 📞 지원

**문제 해결:**
1. 마이그레이션 오류: `python manage.py migrate --fake-initial`
2. 정적 파일 오류: `python manage.py collectstatic`
3. 포트 충돌: `python manage.py runserver 8001`

**추가 문의:**
- 프로젝트 기획서: `LIGHTONE_신규창업지원_전략서.md` 참조
- 사업 계획: 모두의창업 2기 지원 자료 참조

---

**Last Updated**: 2026년 7월
**License**: MIT (팀 프로젝트 학습용)
