from django.db import models
from members.models import Member
from accounts.models import TrainerProfile


class WeeklyReport(models.Model):
    """4주 단위 상담 리포트 — 트레이너 상담용"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='weekly_reports')
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    week_start = models.DateField('주차 시작일')
    week_end = models.DateField('주차 종료일')

    # 집계 지표
    avg_qs = models.FloatField('평균 QS 점수', default=0)
    avg_pain = models.FloatField('평균 통증 반응', default=0)
    avg_rpe = models.FloatField('평균 RPE', default=0)
    session_count = models.PositiveIntegerField('세션 횟수', default=0)
    posture_score = models.FloatField('체형 종합 점수', default=0)

    # 라우팅 요약
    auto_count = models.PositiveIntegerField('AUTO 횟수', default=0)
    review_count = models.PositiveIntegerField('REVIEW 횟수', default=0)
    block_count = models.PositiveIntegerField('BLOCK 횟수', default=0)

    # 트레이너 콘텐츠
    trainer_comment = models.TextField('트레이너 콘멘트', blank=True)
    next_goal = models.TextField('다음 주차 목표', blank=True)
    reregistration_signal = models.BooleanField('재등록 상담 신호', default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-week_start']

    def __str__(self):
        return f'{self.member.name} 리포트 ({self.week_start} ~ {self.week_end})'

    def route_summary(self):
        total = self.session_count or 1
        return {
            'auto_pct': round(self.auto_count / total * 100),
            'review_pct': round(self.review_count / total * 100),
            'block_pct': round(self.block_count / total * 100),
        }
