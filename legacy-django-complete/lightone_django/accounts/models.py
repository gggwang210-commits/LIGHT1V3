from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('trainer', '트레이너'),
        ('admin', '관리자'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='trainer')
    display_name = models.CharField('표시 이름', max_length=50, blank=True)

    def __str__(self):
        return self.display_name or self.username


class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    center_name = models.CharField('센터명', max_length=100, blank=True)
    specialty = models.CharField('전문 분야', max_length=100, blank=True, default='체형교정·기능회복')
    bio = models.TextField('소개', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.display_name} 트레이너'
