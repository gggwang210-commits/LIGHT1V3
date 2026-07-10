# LIGHT ONE 데이터 스키마 설계서

> MVP 단계: 가상 CSV·더미 데이터만 사용. 실제 회원 데이터 미포함.  
> [확인필요] 실제 데이터 수집 시 개인정보보호법·IRB 준수 필수.

---

## 1. 테이블 구조 (Django Models 설계 기준)

### 1.1 Member (회원)

```python
class Member(models.Model):
    member_id     = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # 비식별화: 실명 대신 난수 ID 사용
    gender        = models.CharField(max_length=10, choices=[('M','남성'),('F','여성'),('X','미기재')])
    age_group     = models.CharField(max_length=10)   # 20대·30대·40대 등
    goal          = models.CharField(max_length=100)  # 체형관리·통증완화·근성장 등
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 개인정보보호법 준수: 최소 수집 원칙
        # 실명·연락처·주민번호 저장 금지 (MVP 단계)
        pass
```

### 1.2 Session (세션)

```python
class Session(models.Model):
    session_id    = models.UUIDField(primary_key=True, default=uuid.uuid4)
    member        = models.ForeignKey(Member, on_delete=models.CASCADE)
    trainer_note  = models.TextField(blank=True)   # 트레이너 관찰 메모
    session_date  = models.DateField()
    session_no    = models.PositiveIntegerField()  # 누적 세션 번호
    created_at    = models.DateTimeField(auto_now_add=True)
```

### 1.3 ExerciseLog (운동 기록 — 세트 단위)

```python
class ExerciseLog(models.Model):
    session       = models.ForeignKey(Session, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    set_no        = models.PositiveIntegerField()
    reps_target   = models.PositiveIntegerField()
    reps_actual   = models.PositiveIntegerField()
    weight_kg     = models.FloatField()
    rest_sec      = models.PositiveIntegerField()
    rest_target   = models.PositiveIntegerField()
    rpe           = models.FloatField()
```

### 1.4 PainLog (통증 기록)

```python
class PainLog(models.Model):
    REGION_CHOICES = [
        ('L_SPINE', '요추'), ('T_SPINE', '흉추'), ('C_SPINE', '경추'),
        ('L_SHOULDER', '좌어깨'), ('R_SHOULDER', '우어깨'),
        ('L_KNEE', '좌무릎'), ('R_KNEE', '우무릎'),
        ('HIP', '고관절'), ('NONE', '없음'),
    ]
    session       = models.ForeignKey(Session, on_delete=models.CASCADE)
    timing        = models.CharField(max_length=10, choices=[('PRE','세션 전'),('MID','세션 중'),('POST','세션 후')])
    nrs_score     = models.FloatField()
    region        = models.CharField(max_length=20, choices=REGION_CHOICES)
    # 통증 기록은 의료 진단이 아닌 트레이너 참고용 메모
```

### 1.5 PostureLog (자세 관찰)

```python
class PostureLog(models.Model):
    session           = models.ForeignKey(Session, on_delete=models.CASCADE)
    shoulder_level    = models.CharField(max_length=20, choices=[('LEVEL','수평'),('L_HIGH','좌높음'),('R_HIGH','우높음')])
    pelvis_tilt       = models.CharField(max_length=20, choices=[('NEUTRAL','중립'),('ANTERIOR','전방경사'),('POSTERIOR','후방경사')])
    head_position     = models.CharField(max_length=20, choices=[('NEUTRAL','중립'),('FORWARD','전방이동')])
    trainer_note      = models.TextField(blank=True)
    asymmetry_index   = models.FloatField(null=True, blank=True)
    joint_angles_json = models.JSONField(null=True, blank=True)
```

### 1.6 QualityScore (QS — 세션 단위)

```python
class QualityScore(models.Model):
    session           = models.OneToOneField(Session, on_delete=models.CASCADE)
    form_score        = models.FloatField()
    rep_score         = models.FloatField()
    rest_score        = models.FloatField()
    pain_score        = models.FloatField()
    qs_total          = models.FloatField()
    routing           = models.CharField(max_length=10, choices=[('AUTO','자동진행'),('REVIEW','검토필요'),('BLOCK','안전신호')])

    def calculate_qs(self):
        base = (self.form_score + self.rep_score + self.rest_score + self.pain_score) / 4 * 100
        self.qs_total = round(base, 1)
        if self.qs_total >= 80:
            self.routing = 'AUTO'
        elif self.qs_total >= 60:
            self.routing = 'REVIEW'
        else:
            self.routing = 'BLOCK'
        return self.qs_total
```

### 1.7 JATC (통합 상태지수 — 세션 단위)

```python
class JATCScore(models.Model):
    session             = models.OneToOneField(Session, on_delete=models.CASCADE)
    pain_index          = models.FloatField()
    posture_index       = models.FloatField()
    function_index      = models.FloatField()
    lifestyle_index     = models.FloatField()
    jatc_total          = models.FloatField()
    bottleneck_flag     = models.CharField(max_length=50, blank=True)

    WEIGHTS = {
        'pain':      0.20,
        'posture':   0.30,
        'function':  0.30,
        'lifestyle': 0.20,
    }

    def calculate_jatc(self):
        self.jatc_total = round(
            self.pain_index * self.WEIGHTS['pain'] +
            self.posture_index * self.WEIGHTS['posture'] +
            self.function_index * self.WEIGHTS['function'] +
            self.lifestyle_index * self.WEIGHTS['lifestyle'], 1
        )
        indices = {'통증': self.pain_index, '자세': self.posture_index, '근기능': self.function_index, '생활습관': self.lifestyle_index}
        low = [k for k, v in indices.items() if v < 50]
        self.bottleneck_flag = ','.join(low) if low else ''
        return self.jatc_total
```

### 1.8 RoutingResult (라우팅 결과 — 트레이너 검토용)

```python
class RoutingResult(models.Model):
    STATUS_CHOICES = [
        ('AUTO', '자동 진행 가능'),
        ('REVIEW', '트레이너 검토 필요'),
        ('BLOCK', '안전 신호 — 전문가 상담 권고'),
    ]
    session         = models.OneToOneField(Session, on_delete=models.CASCADE)
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES)
    reason          = models.TextField()
    trainer_checked = models.BooleanField(default=False)
    trainer_note    = models.TextField(blank=True)
    checked_at      = models.DateTimeField(null=True, blank=True)
    # BLOCK은 의료 진단이 아닌 안전 신호
```

---

## 2. 더미 데이터 CSV 샘플 구조

### sessions_dummy.csv

```csv
session_id,member_id,session_no,session_date,goal
SESS-001,MEMB-A01,1,2026-03-01,체형관리
SESS-002,MEMB-A01,2,2026-03-08,체형관리
SESS-003,MEMB-B02,1,2026-03-02,통증완화
```

### exercise_log_dummy.csv

```csv
session_id,exercise,set_no,reps_target,reps_actual,weight_kg,rpe
SESS-001,스쿼트,1,12,10,40.0,6
SESS-001,스쿼트,2,12,12,40.0,7
SESS-001,런지,1,10,10,0.0,5
```

### pain_log_dummy.csv

```csv
session_id,timing,nrs_score,region
SESS-001,PRE,2,L_KNEE
SESS-001,POST,3,L_KNEE
SESS-003,PRE,5,L_SPINE
SESS-003,MID,7,L_SPINE
```

### qs_dummy.csv

```csv
session_id,form_score,rep_score,rest_score,pain_score,qs_total,routing
SESS-001,0.9,0.833,1.0,0.5,82.3,AUTO
SESS-002,0.7,0.667,0.5,0.5,60.4,REVIEW
SESS-003,0.5,0.5,0.5,0.0,37.5,BLOCK
```

---

## 3. 데이터 안전 정책

```text
커밋 금지:
- 실제 회원 이미지, 얼굴 이미지, 민감 건강정보
- API Key, 인증정보, .env 파일
- 고객 인터뷰 원본 (개인정보 포함 가능)

테스트·데모:
- 합성(synthetic) 데이터 또는 비식별 샘플만 사용
- 모든 ID는 UUID 또는 난수 기반

[확인필요] 실제 회원 데이터 수집·분석 시:
- 개인정보보호법 제23조 (민감정보 별도 동의)
- 건강정보 분리 저장 및 최소 수집 원칙
- IRB 승인 후 진행
```

---

*LIGHT ONE — 프로의 기준, 이제는 데이터입니다.*
