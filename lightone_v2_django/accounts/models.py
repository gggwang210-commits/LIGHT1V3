from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('member', '회원'),
        ('trainer', '트레이너'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
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
