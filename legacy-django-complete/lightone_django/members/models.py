from django.db import models
from accounts.models import TrainerProfile


class Member(models.Model):
    SEX_CHOICES = [('M', '남성'), ('F', '여성')]
    GOAL_CHOICES = [
        ('posture', '체형교정'),
        ('pain', '통증감소'),
        ('strength', '스트렉스 감소'),
        ('weight', '체중관리'),
        ('rehab', '기능회복'),
        ('performance', '운동능력 향상'),
    ]
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    name = models.CharField('이름', max_length=50)
    age = models.PositiveIntegerField('나이', null=True, blank=True)
    sex = models.CharField('성별', max_length=1, choices=SEX_CHOICES, blank=True)
    goal = models.CharField('운동 목표', max_length=20, choices=GOAL_CHOICES, default='posture')
    discomfort_area = models.CharField('불편 부위', max_length=120, blank=True)
    memo = models.TextField('특이사항', blank=True)
    is_active = models.BooleanField('활성 회원', default=True)
    registered_at = models.DateField('등록일', auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']

    def __str__(self):
        return f'{self.name} ({self.get_goal_display()})'

    def latest_qs(self):
        s = self.member_sessions.order_by('-created_at').first()
        return s.qs_score if s else None

    def latest_route(self):
        s = self.member_sessions.order_by('-created_at').first()
        return s.route if s else None
