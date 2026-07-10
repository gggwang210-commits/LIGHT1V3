import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from accounts.models import User, MemberProfile, TrainerProfile
from lightone.models import MemberSession

# 1. 슈퍼유저/트레이너 생성
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin', name='김라이트(관리자)', role='trainer')
    TrainerProfile.objects.create(user=admin_user, certification_no='TR-2026-001', center_name='LIGHT ONE 랩스')
    print("Admin 트레이너 생성 완료")

admin_user = User.objects.get(username='admin')
trainer_prof = admin_user.trainer_profile

# 2. 회원 생성
if not User.objects.filter(username='member1').exists():
    m1 = User.objects.create_user('member1', 'm1@example.com', '1234', name='이슬비', role='member')
    mp1 = MemberProfile.objects.create(user=m1, sex='F', goals='라운드숄더 개선 및 체력 증진')
    
    m2 = User.objects.create_user('member2', 'm2@example.com', '1234', name='허병철', role='member')
    mp2 = MemberProfile.objects.create(user=m2, sex='M', goals='허리 통증 완화 및 근력 강화')
    print("더미 회원 생성 완료")

mp1 = User.objects.get(username='member1').member_profile
mp2 = User.objects.get(username='member2').member_profile

# 3. 기존 MemberSession 비우고 더미 생성
MemberSession.objects.all().delete()

sessions_data = [
    (mp1, '이슬비', '상체 후면 근력 강화', '오른쪽 어깨', 8, 3, 6, '견갑골 안정화 잘됨. 무게 2kg 증량'),
    (mp1, '이슬비', '코어 및 밸런스', '', 9, 1, 5, '코어 힘 많이 좋아짐. 다음 세션 하체 진행'),
    (mp2, '허병철', '하체 근력 (스쿼트)', '허리 하단', 5, 6, 8, '허리 말림 현상 발생하여 가동범위 제한함. 코어 먼저 잡아야 함'),
    (mp2, '허병철', '상체 프레스', '어깨 전면', 4, 8, 9, '통증 반응이 높아 운동 중단. 다음 세션 움직임 품질 개선 방향으로 조정'),
]

for mp, m_name, goal, disc, form, pain, rpe, memo in sessions_data:
    session = MemberSession(
        member=mp,
        trainer=trainer_prof,
        member_name=m_name,
        trainer_name=trainer_prof.user.name,
        goal=goal,
        discomfort_area=disc,
        form_accuracy=form,
        pain_response=pain,
        rpe=rpe,
        memo=memo
    )
    session.save()

print("더미 세션 데이터 생성 완료")
