from django.db import models

from accounts.models import MemberProfile, TrainerProfile
from .algorithms import (
    SAFETY_NOTICE,
    calculate_jatc,
    calculate_qs,
    map_pain_response_score,
    normalize_score,
    route_session,
)
from .utils.qs_calculator import determine_routing


class MemberSession(models.Model):
    ROUTE_CHOICES = [
        ('AUTO', 'AUTO'),
        ('REVIEW', 'REVIEW'),
        ('BLOCK', 'BLOCK'),
    ]
    QC_CHOICES = [
        ('PASS', 'PASS'),
        ('CHECK', 'CHECK'),
        ('FAIL', 'FAIL'),
    ]

    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='sessions')
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='conducted_sessions')

    member_name = models.CharField(max_length=80)
    trainer_name = models.CharField(max_length=80, default='LIGHTONE Trainer')
    goal = models.CharField(max_length=120)
    discomfort_area = models.CharField(max_length=120, blank=True)
    qs_score = models.FloatField(default=0)
    jatc_score = models.FloatField(default=0)
    form_accuracy = models.FloatField(default=0)
    pain_response = models.FloatField(default=0)
    rpe = models.FloatField(default=0)
    rep_score = models.FloatField(default=100)
    rest_score = models.FloatField(default=100)
    qc_score = models.FloatField(default=100)
    safety_notice = models.TextField(default=SAFETY_NOTICE)
    qs_form_component = models.FloatField(default=0)
    qs_discomfort_component = models.FloatField(default=0)
    qs_rpe_component = models.FloatField(default=0)
    qs_qc_component = models.FloatField(default=100)
    route = models.CharField(max_length=10, choices=ROUTE_CHOICES, default='AUTO')
    qc_status = models.CharField(max_length=10, choices=QC_CHOICES, default='PASS')
    memo = models.TextField(blank=True)
    posture_score = models.FloatField(default=0)
    lifestyle_score = models.FloatField(default=0)
    function_training_score = models.FloatField(default=0)
    review_note = models.TextField(blank=True)
    trainer_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-qs_score']

    def __str__(self):
        return f'{self.member_name} - {self.route}'

    QS_ROUTE_CALCULATED_FIELDS = {
        'qs_form_component',
        'qs_discomfort_component',
        'qs_rpe_component',
        'qs_qc_component',
        'qs_score',
        'jatc_score',
        'route',
        'safety_notice',
    }

    def calculate_qs_and_route(self):
        """Calculate MVP QS/JATC scores and non-medical trainer review routing."""
        self.qs_form_component = normalize_score(self.form_accuracy)
        self.qs_discomfort_component = map_pain_response_score(self.pain_response)
        self.qs_rpe_component = normalize_score(self.rep_score)
        self.qs_qc_component = normalize_score(self.rest_score)
        self.qs_score = calculate_qs(self.form_accuracy, self.rep_score, self.rest_score, self.pain_response)
        self.jatc_score = calculate_jatc(self.qs_score, self.form_accuracy, self.pain_response, self.rpe)
        safety_flags = {'qc_status_fail': self.qc_status == 'FAIL'}
        self.route = determine_routing(self.qs_score, self.pain_response, safety_flags=safety_flags)
        self.safety_notice = SAFETY_NOTICE

    def save(self, *args, **kwargs):
        # Keep manually entered aggregate QS values until raw input is present.
        if self.form_accuracy or self.rpe or not self.qs_score:
            self.calculate_qs_and_route()
        super().save(*args, **kwargs)
        Indicator.objects.update_or_create(
            member_session=self,
            defaults={
                'qs_score': self.qs_score,
                'jatc_score': self.jatc_score,
                'route': self.route,
                'qc_status': self.qc_status,
                'non_medical_notice': SAFETY_NOTICE,
                'trainer_review_required': self.route in {'REVIEW', 'BLOCK'} or self.qc_status != 'PASS',
            },
        )


class Member(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAUSED', 'Paused'),
        ('ARCHIVED', 'Archived'),
    ]

    synthetic_id = models.CharField(max_length=40, unique=True)
    display_label = models.CharField(max_length=80)
    goal = models.CharField(max_length=120, blank=True)
    experience_level = models.CharField(max_length=40, blank=True)
    discomfort_area = models.CharField(max_length=80, blank=True)
    consent_status = models.CharField(max_length=30, default='synthetic_demo')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['synthetic_id']

    def __str__(self):
        return self.display_label


class Session(models.Model):
    ROUTE_CHOICES = MemberSession.ROUTE_CHOICES
    QC_CHOICES = MemberSession.QC_CHOICES

    session_id = models.CharField(max_length=40, unique=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='session_records')
    exercise_name = models.CharField(max_length=120)
    session_date = models.DateField()
    planned_reps = models.PositiveIntegerField(default=0)
    completed_reps = models.PositiveIntegerField(default=0)
    planned_rest_seconds = models.PositiveIntegerField(default=0)
    actual_rest_seconds = models.PositiveIntegerField(default=0)
    rpe = models.PositiveSmallIntegerField(default=0)
    pain_response = models.PositiveSmallIntegerField(default=0)
    trainer_memo = models.TextField(blank=True)
    capture_condition = models.CharField(max_length=120, blank=True)
    qc_status = models.CharField(max_length=10, choices=QC_CHOICES, default='PASS')
    route = models.CharField(max_length=10, choices=ROUTE_CHOICES, default='AUTO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-session_date', 'session_id']

    def __str__(self):
        return f'{self.session_id} - {self.member.display_label}'

    def update_indicator_scores(self):
        rep_score = (self.completed_reps / self.planned_reps * 100) if self.planned_reps else 0
        rest_score = 100
        if self.planned_rest_seconds and self.actual_rest_seconds:
            rest_delta = abs(self.actual_rest_seconds - self.planned_rest_seconds)
            rest_score = max(0, 100 - (rest_delta / self.planned_rest_seconds * 100))
        qs_score = calculate_qs(form=rep_score, rep=rep_score, rest=rest_score, pain_level=self.pain_response)
        jatc_score = calculate_jatc(qs_score, rep_score, self.pain_response, self.rpe)
        route = route_session(qs_score, jatc_score, self.pain_response, self.qc_status)
        legacy_key = f'legacy-session:{self.session_id}'
        member_session = MemberSession.objects.filter(memo__contains=legacy_key).first()
        if member_session is None:
            member_session = MemberSession(memo=legacy_key)
        member_session.member_name = self.member.display_label
        member_session.trainer_name = ''
        member_session.goal = self.member.goal or self.exercise_name
        member_session.discomfort_area = self.member.discomfort_area
        member_session.qs_score = qs_score
        member_session.jatc_score = jatc_score
        member_session.form_accuracy = rep_score
        member_session.pain_response = self.pain_response
        member_session.rpe = self.rpe
        member_session.rep_score = rep_score
        member_session.rest_score = rest_score
        member_session.route = route
        member_session.qc_status = self.qc_status
        member_session.memo = f'{legacy_key}\n{self.trainer_memo}'.strip()
        member_session.save()
        self.route = route
        self.save(update_fields=['route', 'updated_at'])
        return member_session.indicator


class Indicator(models.Model):
    ROUTE_CHOICES = MemberSession.ROUTE_CHOICES
    QC_CHOICES = MemberSession.QC_CHOICES

    member_session = models.OneToOneField(MemberSession, on_delete=models.CASCADE, related_name='indicator')
    qs_score = models.FloatField(default=0)
    jatc_score = models.FloatField(default=0)
    route = models.CharField(max_length=10, choices=ROUTE_CHOICES, default='AUTO')
    qc_status = models.CharField(max_length=10, choices=QC_CHOICES, default='PASS')
    non_medical_notice = models.TextField(default=SAFETY_NOTICE)
    trainer_review_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-qs_score']

    def __str__(self):
        return f'{self.member_session.member_name} indicator - {self.route}'


class StrategyItem(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=80)
    priority = models.CharField(max_length=30, default='high')
    status = models.CharField(max_length=40, default='needs_action')
    output = models.TextField(blank=True)
    risk = models.TextField(blank=True)

    def __str__(self):
        return self.title
