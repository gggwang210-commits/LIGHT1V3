# LIGHT ONE V2: Django 초기 세팅 및 핵심 코드 가이드

**작성일:** 2026-07-01  
**작성 목적:** 기존 COPD 프로젝트 구조를 기반으로 LIGHT ONE V2의 핵심 뼈대(회원/트레이너 계정 분리, 로그인 미들웨어, 세션 기록 모델)를 즉시 실행할 수 있는 코드 제공.

---

## 1. 프로젝트 초기화 및 구조 설정

로컬 환경의 터미널에서 다음 명령어를 실행하여 Django 프로젝트와 앱을 생성합니다.

```bash
# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

# 패키지 설치
pip install django djangorestframework python-decouple

# 프로젝트 및 앱 생성
django-admin startproject config .
python manage.py startapp accounts
python manage.py startapp sessions
python manage.py startapp reports
```

---

## 2. 전역 로그인 미들웨어 (common/middleware.py)

COPD 프로젝트의 가장 큰 장점이었던 **자동 접근 제어 미들웨어**입니다. 프로젝트 루트에 `common` 폴더를 만들고 `middleware.py`를 작성합니다.

```python
# common/middleware.py
from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve

def _resolve_url_name(path):
    try:
        match = resolve(path)
    except Exception:
        return None
    return f'{match.namespace}:{match.url_name}' if match.namespace else match.url_name

class LoginRequiredMiddleware:
    """
    프로젝트 전역 접근 제어 미들웨어.
    미로그인 사용자가 보호된 페이지에 접근하면 로그인 페이지로 보냄.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        # 정적 파일, Django admin은 항상 예외
        if path.startswith(settings.STATIC_URL) or path.startswith('/admin/'):
            return self.get_response(request)

        url_name = _resolve_url_name(path)

        if request.user.is_authenticated:
            # 로그인한 사용자가 가입/로그인 페이지 접근 시 대시보드로 이동
            guest_only_names = getattr(settings, 'GUEST_ONLY_URL_NAMES', [])
            if url_name in guest_only_names:
                if request.user.role == 'trainer':
                    return redirect('accounts:trainer_dashboard')
                return redirect('accounts:member_dashboard')
            return self.get_response(request)

        # 미로그인 사용자가 보호된 페이지 접근 시 로그인 페이지로 이동
        exempt_names = getattr(settings, 'LOGIN_EXEMPT_URL_NAMES', [])
        if url_name in exempt_names:
            return self.get_response(request)

        login_url = getattr(settings, 'LOGIN_URL', 'accounts:login')
        return redirect(login_url)
```

---

## 3. 핵심 설정 파일 (config/settings.py)

`config/settings.py`에 생성한 앱과 미들웨어를 등록하고, 커스텀 유저 모델을 지정합니다.

```python
# config/settings.py (추가 및 수정할 부분)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom Apps
    'accounts',
    'sessions',  # 세션 기록 관리
    'reports',   # 리포트 및 대시보드
]

# 커스텀 유저 모델 지정
AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 커스텀 로그인 미들웨어 (반드시 AuthenticationMiddleware 뒤에 위치)
    'common.middleware.LoginRequiredMiddleware',
]

# 로그인/비로그인 접근 제어 설정
LOGIN_URL = 'accounts:login'

LOGIN_EXEMPT_URL_NAMES = [
    'accounts:login',
    'accounts:signup',
    'accounts:signup_member',
    'accounts:signup_trainer',
]

GUEST_ONLY_URL_NAMES = [
    'accounts:login',
    'accounts:signup',
    'accounts:signup_member',
    'accounts:signup_trainer',
]
```

---

## 4. 데이터베이스 모델 설계 (models.py)

### 4.1 계정 모델 (accounts/models.py)
COPD의 환자/의사 모델을 회원/트레이너 모델로 전환합니다.

```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('member', '회원'),
        ('trainer', '트레이너'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    name = models.CharField('이름', max_length=50)

class MemberProfile(models.Model):
    SEX_CHOICES = [('M', '남성'), ('F', '여성')]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    goals = models.TextField('운동 목표', blank=True)
    
    def __str__(self):
        return f"{self.user.name} 회원"

class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    certification_no = models.CharField('자격번호', max_length=50, blank=True)
    center_name = models.CharField('소속 센터', max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.name} 트레이너"
```

### 4.2 세션 기록 모델 (sessions/models.py)
COPD의 `daily_care`와 `screening`을 결합하여, 의료적 표현을 배제한 PT 세션 기록 모델을 만듭니다.

```python
# sessions/models.py
from django.db import models
from accounts.models import MemberProfile, TrainerProfile

class SessionRecord(models.Model):
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='sessions')
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, null=True, related_name='conducted_sessions')
    session_date = models.DateField('세션 진행일', auto_now_add=True)
    
    # 주관적/객관적 상태 지표 (0~10 등 척도화)
    rpe = models.IntegerField('운동자각도(RPE)', default=0, help_text="0~10 사이의 주관적 힘듦 정도")
    pain_level = models.IntegerField('통증 반응(NRS)', default=0, help_text="0~10 사이의 통증 정도 (의료 진단 아님)")
    
    # 자세 및 품질 관찰 (트레이너 관찰)
    posture_quality = models.IntegerField('자세 품질', default=5, help_text="1~10 사이의 자세 안정성")
    
    trainer_memo = models.TextField('트레이너 메모', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-session_date', '-created_at']

    def __str__(self):
        return f"{self.member.user.name} - {self.session_date}"

class EvaluationResult(models.Model):
    ROUTING_CHOICES = [
        ('AUTO', '일반 진행 (특이사항 없음)'),
        ('REVIEW', '트레이너 검토 필요 (주의)'),
        ('BLOCK', '안전상 중단 권고 (통증 등)'),
    ]
    
    session = models.OneToOneField(SessionRecord, on_delete=models.CASCADE, related_name='evaluation')
    qs_score = models.FloatField('품질 점수(QS)', default=0.0)
    routing_status = models.CharField('위험 라우팅', max_length=10, choices=ROUTING_CHOICES, default='AUTO')
    generated_at = models.DateTimeField(auto_now_add=True)

    def calculate_qs(self):
        """
        간단한 규칙 기반 QS 산출 로직 (MVP용)
        - 자세가 좋고(높음), 통증이 낮고(낮음), RPE가 적절하면 높은 점수
        """
        base_score = 100
        penalty = (self.session.pain_level * 5) + (abs(self.session.rpe - 7) * 2)
        bonus = (self.session.posture_quality * 2)
        
        final_score = base_score - penalty + bonus
        self.qs_score = max(0, min(100, final_score)) # 0~100 사이 보정
        
        # 라우팅 로직
        if self.session.pain_level >= 7 or self.qs_score < 40:
            self.routing_status = 'BLOCK'
        elif self.session.pain_level >= 4 or self.qs_score < 70:
            self.routing_status = 'REVIEW'
        else:
            self.routing_status = 'AUTO'
            
        self.save()
```

---

## 5. 초기 마이그레이션 및 실행

위 코드를 모두 작성한 후, 데이터베이스를 생성하고 관리자 계정을 만듭니다.

```bash
# DB 마이그레이션
python manage.py makemigrations accounts sessions
python manage.py migrate

# 슈퍼유저 생성 (관리자)
python manage.py createsuperuser

# 서버 실행
python manage.py runserver
```

---

## 👨‍🏫 멘토의 조언 (Next Step)

광일 님, 이 코드는 COPD 프로젝트의 핵심 장점인 **"안전한 접근 제어"**와 **"역할 분리"**를 그대로 가져오면서, 의료적 리스크를 완전히 덜어낸 LIGHT ONE V2의 뼈대입니다. 

특히 `EvaluationResult` 모델의 `calculate_qs()` 함수를 보시면, 복잡한 머신러닝 없이 **규칙 기반(Rule-based)**으로 점수와 라우팅(AUTO/REVIEW/BLOCK)을 계산하도록 만들어 두었습니다. 초기 MVP 단계에서는 이 정도로도 충분히 사업계획서와 데모 시연을 설득력 있게 진행할 수 있습니다.

**다음으로 추천하는 작업:**
1. 위 코드를 로컬 환경에 복사하여 에러 없이 서버가 뜨는지 확인하세요.
2. `admin.py`에 모델들을 등록하고 더미 데이터를 10개 정도 넣어보세요.
3. 그 데이터가 들어간 것을 확인하면, 광일 님의 주특기인 **정규화된 시각화 대시보드(views.py 및 Chart.js)**를 붙이는 작업을 진행하겠습니다.

코드를 적용하시다가 막히는 부분이나 에러가 발생하면 언제든 터미널 로그를 복사해서 알려주세요!
