from django.db import models
from members.models import Member
from accounts.models import TrainerProfile


class MemberSession(models.Model):
    """PT 세션 기록 데이터 모델 — QS 점수화 및 위험 라우팅 포함"""

    ROUTE_CHOICES = [
        ('AUTO', 'AUTO — 일반 진행 가능'),
        ('REVIEW', 'REVIEW — 트레이너 검토 필요'),
        ('BLOCK', 'BLOCK — 안전 신호 발생'),
    ]
    QC_CHOICES = [
        ('PASS', 'PASS — 정상'),
        ('CHECK', 'CHECK — 재확인 필요'),
        ('FAIL', 'FAIL — 분석 불가'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_sessions')
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='conducted_sessions')
    session_date = models.DateField('세션일', null=True, blank=True)

    # 운동 기록
    exercise_name = models.CharField('주요 운동', max_length=120, blank=True)
    sets = models.PositiveIntegerField('세트', default=3)
    reps = models.PositiveIntegerField('회수', default=10)
    weight_kg = models.FloatField('중량(kg)', default=0)

    # 컨디션 지표 (0시작, 자동 계산)
    pain_response = models.FloatField('통증 반응 (0-10)', default=0)
    rpe = models.FloatField('RPE 운동 자각도 (0-10)', default=5)
    form_accuracy = models.FloatField('자세 정확도 (0-10)', default=7)
    jatc_score = models.FloatField('JATC 점수 (0-100)', default=70)

    # 자동 산출 필드
    qs_score = models.FloatField('QS 점수', default=0)
    route = models.CharField('위험 라우팅', max_length=10, choices=ROUTE_CHOICES, default='AUTO')
    qc_status = models.CharField('촬영 QC', max_length=10, choices=QC_CHOICES, default='PASS')

    # 자세 관찰 (6항목 체형 평가)
    shoulder_tilt = models.FloatField('어깨 기울기(도)', default=0)
    pelvis_tilt = models.FloatField('골반 기울기(도)', default=0)
    spine_alignment = models.FloatField('첥추 정렬도(0-10)', default=7)
    knee_alignment = models.FloatField('무릅 정렬도(0-10)', default=7)
    ankle_alignment = models.FloatField('발목 정렬도(0-10)', default=7)
    lr_deviation = models.FloatField('좌우 편차(도)', default=0)

    memo = models.TextField('트레이너 메모', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.member.name} — QS {self.qs_score} [{self.route}]'

    def calculate_qs_and_route(self):
        """
        규칙 기반 QS 점수화 엔진 (MVP용)
        — 통증 반응이 높을수록 감점, RPE 과도 시 감점, 자세 정확도 높을수록 가산
        — BLOCK: 통증 반응 7이상 또는 QS < 40
        — REVIEW: 통증 반응 4이상 또는 QS < 70
        — AUTO: QS >= 70
        """
        base = 100.0
        penalty = (self.pain_response * 5.0) + (abs(self.rpe - 7) * 2.0)
        bonus = self.form_accuracy * 1.5
        score = base - penalty + bonus
        self.qs_score = round(max(0.0, min(100.0, score)), 1)

        if self.pain_response >= 7 or self.qs_score < 40:
            self.route = 'BLOCK'
        elif self.pain_response >= 4 or self.qs_score < 70:
            self.route = 'REVIEW'
        else:
            self.route = 'AUTO'
        self.save()
        return self

    def posture_summary(self):
        """6항목 체형 평가 평균 점수"""
        items = [
            max(0, 10 - abs(self.shoulder_tilt)),
            max(0, 10 - abs(self.pelvis_tilt)),
            self.spine_alignment,
            self.knee_alignment,
            self.ankle_alignment,
            max(0, 10 - abs(self.lr_deviation)),
        ]
        return round(sum(items) / len(items) * 10, 1)  # 0-100·점수로 환산
